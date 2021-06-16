# FreeBees
## Code Institute - Full Stack Development Milestone
This is my final Milestone project, the goal of which is a full-stack e-commerce site capable of handling some form of transaction from a customer.
I have chosen to build a subscription based service for sale and support of ethically produced honey.

## Table of Contents
1. 
2. [UX](#User-experience-(UX))
3. [Design]
4. [Wireframes]
5. [Features]
6. [Technology Used]
7. [Testing]
8. [Deployment]
9. [Credits]
10. [Acknowledgement]

## User Experience (UX):
The purpose of Freebees was a website designed to support apiasts and smaller scale farms who use biodynamic/natural beekeeping practices and offer an alternative to the more commonly available forms of honey which are often made using unnecessary and unpleasant practices. The site's purpose was also designed with the intent of supporting other charities in the care and conservation of the UK's wildlife.

The website was conceived as there are other sites which work between local or smaller scale producers and offer them a means to sell with less mark up on products, such as [naked wines](https://www.nakedwines.com/). There are not any viable equivalents for honey or encouraging better practices, as someone interested in the environment and with a science background this was something which was of great importance to me, plus I really enjoy honey.

### Strategy Plane
The main business goals of this website are to encourage ethical honey purchases, preserve bees and their habitat, educate users and primarily encourage user subscriptions.

After doing research the main target audiences for Freebees are:
* Younger users (typically 18 to 40 years old).
* People who particularly enjoy honey.
* Users who feel comfortable giving to charitable causes.
* Those who feel comfortable committing to monthly subscription services.
While studies don't show a massive difference in age groups, classically those in a younger age group [reported themselves](https://www.statista.com/statistics/952863/climate-change-concerns-by-age-great-britain/) as more environmentally concerned. Therefore these are more likely to make purchases towards more sustainable, environmentally friendly purchases. Equally the rise of subscription models with products such as netflix has shown their viability at encouraging return customers.

Research:
* This is a B2C model, aimed at general consumers and environmentally conscious individuals.
* These mean this is a more emotional transaction which often leads to low visit rates.
* Use of emotional triggers, large images and small amounts of text are key to encourage subscribing.
* No similar services currently which are not specifically their own honey farm.
For this reason, Freebees also offers recipes to use with its honey products. These not only encourage return viewership to all users, but by restricting newer recipes to subscribed members it also offers an extra incentive to subscribe beyond free honey and supporting the company's goals.

### User stories
To decide on what requirements would be necessary for the site, user stories were created to highlight scenarios and needs for different types of user/customer.

1.	As an unauthenticated user, I want to find the websites purpose immediately upon entering the website.
2.	As a user, I want to be able to use the website on tablet, laptop and phone in a readable, sensible fashion.
3.	As an unauthenticated user, I want to contact the company with questions relating to the website or subscription services.
4.	As an unauthenticated user, I want to look at recipes on the website.
5.	As a general user, I want to be able have an easy option to search for recipes on the site.
6.	As a user, I want to have product pages describing the types of honey available.
8.	As a user, I want to see the current/next month’s subscription product so I can know if I’m interested in subscribing.
9.	As an unauthenticated user, I want to have a clear summary page of benefits for subscribing to the product.
10.	 As an unauthenticated user, I want to see the associated businesses and the reasoning for partnership.
11.	As a general user, I want to have information on why this company exists and is preferable to normal honey farms.
12.	As a user, I want the site to be easily navigable and simple to use.
13.	As an unauthenticated user, I want to easily be able to register and receive monthly orders and on-site benefits immediately.
14.	As a user, I want checkout to be simple and efficient with the minimum required number of steps.
15.	As a user, I want a secure payment system which encourages me that my details are safe.
16.	As a user, I would like a confirmation page and email re-assuring me of my purchases and subscription is complete. 
17.	As an authenticated/subscribed user, I want to contact the company regarding my subscription or details quickly.
18.	As an authenticated/previously subscribed user, I want to see my previous months’ deliveries and recipes.
19.	As an authenticated user, I want to look at recipes on the website.
20.	As a subscribed user, I want to look at the recipes on this website.
22.	As an authenticated user, I want login in and logout to be quick and easy for when I visit.
23.	As an authenticated user, I want to be able to ask for a password reset
24.	As an authenticated user, I want a link to my personal details/account to always be available.
25.	As an authenticated user, I want to easily update my address.
26.	As an authenticated user, I want to easily store my card details.
27.	As an authenticated user, I want resubscription to be easy and require less steps than originally subscribing.
28.	As a subscribed user, I want to be able to cancel my subscription easily.

Admin Stories
1.	As an admin, I want to add a new product to the application.
2.	As an admin, I want to update existing products on the store.
3.	As an admin, I want to delete existing products from the store.
4.	As an admin, I want to add new recipes to the website.
5.	As an admin, I want to edit current recipes on the website.
6.	As an admin, I want to delete recipes on the website.
7.	As an admin, I want to update membership details on the website.
8.	As an admin, I want to update the monthly gifts received on main page.
9.	As the business owner, I want customers to validate their emails so that promotional material or updates can be given easily.

#### Features implementation
In the decision of which features to create and their priority, a list was constructed to compare viability vs importance. Each object was scored from 1-5 in importance (how necessary to the site) and viability (how easily it could be achieved) and then plotted on a chat to decide which features were essential for minimum viable product (MVP) and which were set for future goals/stretch goals.
[alt text](readmedocs\featurestable.png "Viability/importance Table")

[alt text](readmedocs\feasiblitychart.png "Viability/importance Table")

### Scope Plane
To prevent scope creep and to maintain a robust service for users, a minimum viable product (MVP) was created with each task considered part of an epic goal. These goals were broken down into sprints which could be achieved and altered as required to maintain focus on important features.

Minimum Viable Product:
* Login/Authentication system.
* Subscription model, purchasing and verification.
* Product collection for monthly delivery.
* Partnership Company collection.
* Recipe collection.
* Profile page for updating details.
* Email verification/confirmation.

Other features are considered stretch goals or future goals should the website continue to be developed and can be found in the [features](#Features) section.

### Structure Plane
The structure for this site was chosen around each ap containing as much likewise information and views as was necessary, therefore each app often contains multiple models and instances of data.

Django was required as the framework language, PostgresSQL was used for the deployed database on Heroku.

The main app was split into the following apps:
[alt text](readmedocs\drawSQL-export-2021-06-16_15_51.png)

* CustomerService:  
Used to control manage views for pages regarding information about the company to customers or communication from customers.

* Products app:  
Displays example products from pseudo-companies and manages all CRUD operations in relation to product instances in model.
..* Products Model
    
        product_code = models.CharField(
            max_length=36, default=uuid.uuid4, editable=False
        )
        name = models.CharField(max_length=100)
        description = models.TextField(max_length=600)
        image = models.ImageField(null=True)
        texture = models.CharField(max_length=254, blank=True, null=True)
        flavour = models.CharField(max_length=254, blank=True, null=True)
        company = models.ForeignKey(
            "Company", null=True, blank=True, on_delete=models.SET_NULL
        )

        def __str__(self):
            return self.name
    }

    Companies Model

        name = models.CharField(max_length=100)
        description = models.TextField(max_length=600)
        logo = models.ImageField(null=True, blank=True)
        county = models.CharField(max_length=40, null=True, blank=True)
        company_url = models.URLField(max_length=250)
    
"""

*  Profiles app:  
Stores User information and stripe customer id. Also has a property to decide if user has an active subscription or not.
"""
    Profiles Model

        user = models.OneToOneField(User, on_delete=models.CASCADE)
        stripe_customer_id = models.CharField(max_length=255, null=True)
        default_phone_number = models.CharField(
            max_length=13, null=True, blank=True
        )
        default_street_address1 = models.CharField(
            max_length=80, null=True, blank=True
        )
        default_street_address2 = models.CharField(
            max_length=80, null=True, blank=True
        )
        default_town_or_city = models.CharField(
            max_length=40, null=True, blank=True
        )
        default_county = models.CharField(max_length=80, null=True, blank=True)
        default_postcode = models.CharField(max_length=20, null=True, blank=True)

        # Checks if there is an active subscription with an expiry date
        # after or equal to today.
        @property
        def has_active_subscription(self):
            today = timezone.now()
            active_subscriptions = self.stripesubscription_set.filter(
                end_date__gte=today
            )
            return active_subscriptions.count() > 0
"""

* Recipes app:  
Displays recipes to the user and manages all CRUD operations in relation to recipe instances in model.
"""
    Recipes Model
    
        title = models.CharField(max_length=255)
        description = models.CharField(max_length=400)
        ingredients = models.TextField(null=True)
        instructions = models.TextField(null=True)
        image = models.ImageField(null=True)
        publish_date = models.DateTimeField(
            null=True,
            help_text="Date used to determine loading date and user access.",
        )
        featured_product = models.ForeignKey(
            Product, null=True, on_delete=models.SET_NULL
        )
"""
* Subscriptions app:  
Stores key information from stripe to prevent need for frequent API calls. Invoices are also stored to reduce calls to stripe API and allow local assignment and comparison against products earnt for monthly subscriptions.
"""
    StripeSubscription Model

        subscription_id = models.CharField(
            max_length=255,
            help_text="Stripe subscription Id for communicating with stripe.",
        )
        start_date = models.DateTimeField(
            help_text="The start date of the subscription."
        )
        end_date = models.DateTimeField(
            help_text="The end date of the subscription."
        )
        stripe_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
        cancel_at_end = models.BooleanField(default=False)

        def __str__(self):
            return self.subscription_id
    }

    Invoice Model

        stripe_subscription = models.ForeignKey(
            StripeSubscription, null=True, on_delete=models.CASCADE
        )
        invoice_number = models.CharField(
            max_length=255, null=True, help_text="Stripe invoice code."
        )

        current_start = models.DateTimeField(
            null=True, help_text="The start date of current invoice period."
        )
        current_end = models.DateTimeField(
            null=True, help_text="The end date of current invoice period."
        )
        delivery_name = models.CharField(
            null=True,
            max_length=255,
            help_text="Name of person whom delivery is for.",
        )
        address_1 = models.CharField(max_length=255)
        address_2 = models.CharField(max_length=255)
        town_or_city = models.CharField(max_length=255)
        county = models.CharField(max_length=255)
        postcode = models.CharField(max_length=255)

        def __str__(self):
            return self.invoice_number
    
"""
