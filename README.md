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

#### Admin Stories
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

![alt text](https://github.com/RhysPollardDevelopment/Fullstack-milestone/blob/master/readmedocs/featurestable.png "Viability/importance Table")

![alt text](https://github.com/RhysPollardDevelopment/Fullstack-milestone/blob/master/readmedocs/feasiblitychart.png "feature importance graph")

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

Other features are considered future goals should the website continue to be developed and can be found in the [features](#Features) section.

### Structure Plane
The structure for this site was chosen around each ap containing as much likewise information and views as was necessary, therefore each app often contains multiple models and instances of data.

Django was required as the framework language, PostgresSQL was used for the deployed database on Heroku.

The main app was split into the following models, with invoice and recipes only loosely being connected by their dates:
![alt text](https://github.com/RhysPollardDevelopment/Fullstack-milestone/blob/master/readmedocs/drawSQL-export-2021-06-16_15_51.png "Entity relationship Diagram")

* **CustomerService**:  
Used to control manage views for pages regarding information about the company to customers or communication from customers.

* **Products app**:  
Displays example products from pseudo-companies and manages all CRUD operations in relation to product instances in model.  
Products Model
    
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


*  **Profiles app**:  
Stores User information and stripe customer id. Also has a property to decide if user has an active subscription or not.  
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

* **Recipes app**:  
Displays recipes to the user and manages all CRUD operations in relation to recipe instances in model.  
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

* **Subscriptions app**:  
Stores key information from stripe to prevent need for frequent API calls. Invoices are also stored to reduce calls to stripe API and allow local assignment and comparison against products earnt for monthly subscriptions.  
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

### Wireframes
All wireframes have been constructed using the Balsamiq tool at the beginning of the project. Any key or major changes to design and purpose were redesigned before being made in html and are includes within the documents below.

Designs were focussed on large, pleasant images to engage users and form a positive, emotional response from the website.

* Wireframe
* Wireframe
* Wireframe
* Wireframe
* Wireframe
* Wireframe
* Wireframe
* Wireframe
* Wireframe

### Surface Design
* Colour scheme
* Typography
* Images:
* Forms:


## Features
#### Common Features:
* Navigation header:  
Navigation bar for all view breakpoints, has stylized content and design to follow common expectations of using to navigate the main branches of the website.
* Dynamic visibility/access:  
Some features are only visible (or accessible) when a user is authenticated and logged in, such as the login/register navigation being removed and profile displayed in its place. Similarly some navigation links (e.g. Subscription button and pages) are hidden and some content made available is user is subscribed.
* Toasts/Messages:  
All pages have access to the messages function pop up to display anu success or error messages from the system.
* Footer:  
Footer containing an extra set of navigation links and some site legal information across every page.

#### Other Features:
* Login authentication system:  
Users can register, login and store their security information in django-all-auth using back end validation.
* Subscriptions:  
Stripe api used to create a payment method and intent which can call for monthly payments to maintain subscription.
* Subscription form:  
Use of stripe card element for dynamic error and updating features. Form also supports delivery and billing address with hidden forms selectable through use of a checkbox.
* Password Reset:  
Django-all-auth provided password reset system to allow users to change or be sent a reset link for their Freebees password.
* Recipe Collection:  
List of recipes with associated Freebees honey to accompany the recipe's theme. Restricted to subscribed users if posted within the last 3 months.
* Profile Page:  
Page for users to see their subscription status, subscription history and updated certain details.
* Partners page:  
Html page for displaying partner companies which are known to practice the form of beekeeping advocated by Freebees website.
* Honey product examples:  
Examples of the most common/best rated products offered by fake partner companies which customer can receive as part of their subscription.
* Subscription cancellation/reactivation:  
Subscribed users can cancel their subscription and reactivate until the end of their alloted time.
*  Subscription history:  
Page in profile which highlights invoices from current and previous subscriptions along with any recipes or products that were received as part of subscription.
* Automated emails:  
Webhooks from stripe are used to not only create and update subscription models, but send emails to customers on any major changes or updates to their subscription.

#### Future goals:
* Filter for recipes on main recipe list.
* Pagination for recipes, subscription history and maybe products as site grows.
* Promotional offers.
* 12 month/6 month subscriptions.
* Individual product purchases and shopping cart.
* Monthly email notifications.
* Subscription tiers: have option of extra additional honey per month.

## Technologies

### Required:
HTML, CSS, JavaScript, Python, Django, Postgres, Stripe payments.

#### Languages
* [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
* [CSS3](https://developer.mozilla.org/en-US/docs/Archive/CSS3)
* [Javascript 6](https://developer.mozilla.org/en-US/docs/Web/JavaScript) Specifically ECMAScript 6/2015
* [Python 3.9.5](https://www.python.org/)

#### Libraries, Frameworks and Tools
* [Bootstrap v4.7.0](https://getbootstrap.com/): Front end framework for development of websites, offers pre-designed components and classes which can be further customised.
* [jQuery](https://jquery.com/): Library of base JavaScript, allowing the use of interactivity and features on components and simplifying DOM.
* Git: Version control system used to catalogue project development.
* [Django](https://www.djangoproject.com/): Framework used for this project.
* [Stripe](https://stripe.com/gb): Payment/subscription authentication system which handles payment for this app.
* [Heroku](https://www.heroku.com/): Website for deployment and hosting of Freebees.
* [Psycopg2](https://pypi.org/project/psycopg2/): Adapter to allow PostresSQL to interact with python.
* [Gunicorn](https://gunicorn.org/): Green unicorn, WSGI deployment tool.
* [Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/): Package for displaying forms.
* [AWS S3 Bucket](https://aws.amazon.com/): Cloud storage system for static and media files.
* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html): Package to aid with file transfer to S3 bucket.
* [Pillow](https://python-pillow.org/): Package for processing and saving images.
* [Black](https://black.readthedocs.io/en/stable/): Python formatter, aids in committing to PEP8.
* [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools): Online resource in Chrome browser, used to make edit pages quickly to diagnose problems or test changes.
* [Google Fonts](https://fonts.google.com/): Library used to embed and link expanded font choices into the project.
* [Gmail](https://www.google.com/gmail/): Email service used to deliver emails from python.
* [favicon-generator](https://www.favicon-generator.org/): Favicon generator which converts images into favicons for use in the browser tab.
* [Adobe Color](https://color.adobe.com/explore): Online tool used for identifying colour palettes and themes. Used to extrapolate colours from images and find suitable colour rnges.
* [Balsamiq](https://balsamiq.com/): Wireframing tool for concept creation and design for website.
* [Font-Awesome](https://fontawesome.com/): Library offering a wide icon set for use in projects.
* [Autoprefixer CSS Online](https://autoprefixer.github.io/): parsed CSS and produced webkit vendor prefixes for CSS stylings to work correctly on other browsers.
* [Visual Studio Code](https://code.visualstudio.com/): A programming environment for developing which allows for extensions and testing.
* [Prettier](https://prettier.io/): A tool used in combination with VS Code to format and style code.
* [Jasmine](https://jasmine.github.io/): A tool used in combination with VS code to perform unit testing.
* [ESLint](https://eslint.org/): Linting tool installed in visual studio code.
* [Pep8 Online](http://pep8online.com/): Linting tool online used to correct python code and ensure was pep8 compliant. 
* [Am i responsive](http://ami.responsivedesign.is/): Tool used to see if a webpage is responsive across multiple screens.
* [Responsinator](http://www.responsinator.com/): Website which mocks multiple phones and devices of different sizes and orientations.
* [Clip Paint Studio](https://www.clipstudio.net/en/): Used to adjust some images and create landing page header.
* [Compressjpeg.com](https://compressjpeg.com/): To make larger images smaller and easy to load.

#### Databases:
* [PostgresSQL](https://www.postgresql.org/): The relational database used for the deployed project.
* [SQlite3]

## Testing
All testing can be found in [Testing.md]()

## Deployment