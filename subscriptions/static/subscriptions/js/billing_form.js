$(document).ready(function () {
    bindBilling();
    formSetup();

})

function formSetup() {
    let billingForm = document.getElementById("billing-form");
    let inputs = billingForm.getElementsByTagName("input");
    for (i = 0; i < inputs.length; i++) {
        inputs[i].required = false;
    }
}

function bindBilling() {
    let billingCheck = document.getElementById("same-billing");
    let billingForm = document.getElementById("billing-form");
    let inputs = billingForm.getElementsByTagName("input");

    if (billingCheck) {
        billingCheck.addEventListener("click", function () {
            if (billingCheck.checked) {
                billingForm.classList.add("d-none");
                for (i = 0; i < inputs.length; i++) {
                    inputs[i].required = false;
                }
            } else {
                billingForm.classList.remove("d-none");
                for (i = 0; i < inputs.length; i++) {
                    inputs[i].required = true;
                }
            };
        })
    }
};