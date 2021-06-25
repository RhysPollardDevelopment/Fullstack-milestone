// Creates card element using stripe code and examples.
// Most of the code in this is taken and altered from
// https://stripe.com/docs/billing/subscriptions/fixed-price
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
let stripe = Stripe(stripePublicKey);
let elements = stripe.elements();
var style = {
    base: {
        color: '#fff',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
let card = elements.create('card', {
    style: style
});
card.mount('#card-element');

// Handle realtime validation for card element
card.on('change', function (event) {
    displayError(event);
});

// Displays any error passed to it from the functions below.
// Main code altered from stripe fixed price-tutorial.
/// https://stripe.com/docs/billing/subscriptions/fixed-price
function displayError(event) {
    let displayError = document.getElementById('card-element-errors');
    if (event.error) {
        // Added in second check to also allow errors lacking same structure.
        if (event.error.message) {
            displayError.textContent = event.error.message;
            return;
        } else {
            displayError.textContent = event.error;
            return;
        }
    } else {
        displayError.textContent = '';
    }
}

// Defines subscription form and puts card into disabled state.
let subscriptionForm = document.getElementById('payment-form');
subscriptionForm.addEventListener('submit', function (ev) {
    ev.preventDefault();
    // Disables card input, button and then toggles loading overlay.
    card.update({
        'disabled': true
    });
    document.getElementById("submit-button").disabled = true;
    $("#loading-overlay").fadeToggle(100);
    createPayment(card);
});

// Collects information before calling stripe.createPaymentMethod for payment.
function createPayment(card) {
    // Loads form data so is accurate when form submitted.
    // Handle form submit and data post preparation.
    // https: //developer.mozilla.org/en-US/docs/Web/API/FormData/FormData
    let rawForm = new FormData(subscriptionForm);
    // Find ref for this!
    var data = {};
    rawForm.forEach(function (value, key) {
        data[key] = value;
    });
    // Extracts required values from page such as the checkbox values.
    var priceId = $('#id_stripe_price').text().slice(1, -1);
    const customerId = document.getElementById('customerId').value;
    var saveShipping = document.getElementById('save-shipping').checked;
    var sameBilling = document.getElementById('same-billing').checked;

    // If sameBilling is true, name for billing is equal to the 
    // subscriptionForm details. Otherwise they use billing name.
    let details;
    if (sameBilling) {
        details = {
            name: $.trim(subscriptionForm.full_name.value),
        };
    } else {
        details = {
            name: $.trim(subscriptionForm.billing_full_name.value),
        };
    }
    stripe
        .createPaymentMethod({
            type: 'card',
            card: card,
            billing_details: details,
        })
        .then((result) => {
            if (result.error) {
                $("#loading-overlay").fadeToggle(100);
                card.update({
                    'disabled': false
                });
                document.getElementById("submit-button").disabled = false;
                displayError(result);
            } else {
                createSubscription({
                    data: data,
                    customerId: customerId,
                    paymentMethodId: result.paymentMethod.id,
                    priceId: priceId,
                    saveShipping: saveShipping,
                    sameBilling: sameBilling,
                });
            }
        });
}

function createSubscription({
    customerId,
    data,
    paymentMethodId,
    priceId,
    saveShipping,
    sameBilling
}) {
    //https://stackoverflow.com/questions/10489332/append-json-strings/10489510
    // Used as reference for passing variable to object in JS.
    // Key data is added to data variable so it can be passed together.
    data.priceId = priceId;
    data.customerId = customerId;
    data.paymentMethodId = paymentMethodId;
    data.saveShipping = saveShipping;
    data.sameBilling = sameBilling;
    let formData = JSON.stringify(data);
    // Fetch request to ceate-subscription method, returns a HTTPresponse.
    return (
        fetch('create-subscription', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': data.csrfmiddlewaretoken,
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true',
            },
            body: formData,
        })
        .then((response) => {
            return response.json();
        })
        // If the card is declined, display an error to the user.
        .then((result) => {
            if (result.error) {
                // The card had an error when trying to attach to a customer.
                throw result;
            }
            return result;
        })
        // Normalize the result to contain the object returned by Stripe.
        // Add the additional details we need.
        .then((result) => {
            return {
                paymentMethodId: paymentMethodId,
                priceId: priceId,
                subscription: result,
            };
        })
        // Some payment methods require a customer to be on session
        // to complete the payment process. Check the status of the
        // payment intent to handle these actions.
        .then(handlePaymentThatRequiresCustomerAction)
        // If attaching this card to a Customer object succeeds,
        // but attempts to charge the customer fail, you
        // get a requires_payment_method error.
        .then(handleRequiresPaymentMethod)
        // No more actions required. Provision your service for the user.
        .then(onSubscriptionComplete)
        .catch((error) => {
            // An error has happened. Display the failure to the user here.
            // Catches any errors thrown during this progression and stops
            // process. Displayed in card error element suggested by Stripe.
            document.getElementById("submit-button").disabled = false;
            $("#loading-overlay").fadeToggle(100);
            card.update({
                "disabled": false
            });
            displayError(error);
        }));
}

// First in sequence after fetch response. Deals with customer authentication
// and situations requiring customer interaction.
function handlePaymentThatRequiresCustomerAction({
    subscription,
    invoice,
    priceId,
    paymentMethodId,
    isRetry,
}) {
    if (subscription && subscription.status === 'active') {
        // Subscription is active, no customer actions required.
        return {
            subscription,
            priceId,
            paymentMethodId
        };
    }

    // If it's a first payment attempt, the payment intent is on the subscription latest invoice.
    // If it's a retry, the payment intent will be on the invoice itself.
    let paymentIntent = invoice ? invoice.payment_intent : subscription.latest_invoice.payment_intent;
    // If authentication is required then payment status is "requires action".
    // Process is diverted here so a payment intent is retrieved from Stripe.
    if (
        paymentIntent.status === 'requires_action' ||
        (isRetry === true && paymentIntent.status === 'requires_payment_method')
    ) {
        return stripe
            .confirmCardPayment(paymentIntent.client_secret, {
                payment_method: paymentMethodId,
            })
            .then((result) => {
                if (result.error) {
                    // Starts process of error reporting by throwing error.
                    throw result;
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        // Change status to active as no other accessible
                        // way offered to check for success after this point.
                        subscription.status = 'active';
                        // Show a success message to your customer.
                        return {
                            priceId: priceId,
                            subscription: subscription,
                            invoice: invoice,
                            paymentMethodId: paymentMethodId,
                        };
                    }
                }
            });
    } else {
        // No customer action needed.
        return {
            subscription,
            priceId,
            paymentMethodId
        };
    }
}

// Second in sequence, attempts retries on payment methods if required.
// Not much use as only set up for 4 scenarios and none use this feature yet.
function handleRequiresPaymentMethod({
    subscription,
    paymentMethodId,
    priceId,
}) {
    if (subscription.status === 'active') {
        // subscription is active, no customer actions required.
        return {
            subscription,
            priceId,
            paymentMethodId
        };
    } else if (
        subscription.latest_invoice.payment_intent.status ===
        'requires_payment_method'
    ) {
        // Using localStorage to manage the state of the retry here,
        // feel free to replace with what you prefer.
        // Store the latest invoice ID and status.
        localStorage.setItem('latestInvoiceId', subscription.latest_invoice.id);
        localStorage.setItem(
            'latestInvoicePaymentIntentStatus',
            subscription.latest_invoice.payment_intent.status
        );
        throw {
            error: {
                message: 'Your card was declined.'
            }
        };
    } else {
        return {
            subscription,
            priceId,
            paymentMethodId
        };
    }
}

// Final part of sequence if not errors. Completes the user experience.
function onSubscriptionComplete(result) {
    // Payment was successful.
    if (result.subscription.status === 'active') {
        // Change your UI to show a success message to your customer.
        // Call your backend to grant access to your service based on
        // `result.subscription.items.data[0].price.product` the customer subscribed to.

        // Uses location.href to call complete view and move user.
        window.location.href = '/subscription/checkout/complete';
    }
}