# FreeBees
## Code Institute - Full Stack Development Milestone
This is my final Milestone project, the goal of which is a full-stack e-commerce site capable of handling some form of transaction from a customer.
I have chosen to build a subscription based service for sale and support of ethically produced honey.

[Live Website](https://freebees-fullstack-milestone.herokuapp.com/)

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

## Live Site
[Live Website](https://freebees-fullstack-milestone.herokuapp.com/)S

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
    * Date time picker for recipe publish date gracefully regressed to a text input with a format applied as django crispy forms does not have a date time picker widget. I have decided to keep this as date pickers can vary heavily between browsers and this is more than effective for the website's purpose.


## Features
#### Common Features:
* **Navigation header**:  
Navigation bar for all view breakpoints, has stylized content and design to follow common expectations of using to navigate the main branches of the website.
* **Dynamic visibility/access**:  
Some features are only visible (or accessible) when a user is authenticated and logged in, such as the login/register navigation being removed and profile displayed in its place. Similarly some navigation links (e.g. Subscription button and pages) are hidden and some content made available is user is subscribed.
* **Toasts/Messages**:  
All pages have access to the messages function pop up to display anu success or error messages from the system.
* **Footer**:  
Footer containing an extra set of navigation links and some site legal information across every page.

#### Other Features:
* **Login authentication system**:  
Users can register, login and store their security information in django-all-auth using back end validation.
* **Subscriptions**:  
Stripe api used to create a payment method and intent which can call for monthly payments to maintain subscription.
* **Subscription form**:  
Use of stripe card element for dynamic error and updating features. Form also supports delivery and billing address with hidden forms selectable through use of a checkbox.
* **Password Reset**:  
Django-all-auth provided password reset system to allow users to change or be sent a reset link for their Freebees password.
* **Recipe Collection**:  
List of recipes with associated Freebees honey to accompany the recipe's theme. Restricted to subscribed users if posted within the last 3 months.
* **Profile Page**:  
Page for users to see their subscription status, subscription history and updated certain details.
* **Partners page**:  
Html page for displaying partner companies which are known to practice the form of beekeeping advocated by Freebees website.
* **Honey product examples**:  
Examples of the most common/best rated products offered by fake partner companies which customer can receive as part of their subscription.
* **Subscription cancellation/reactivation**:  
Subscribed users can cancel their subscription and reactivate until the end of their alloted time.
*  **Subscription history**:  
Page in profile which highlights invoices from current and previous subscriptions along with any recipes or products that were received as part of subscription.
* **Automated emails**:  
Webhooks from stripe are used to not only create and update subscription models, but send emails to customers on any major changes or updates to their subscription.

#### Future goals:
Goals to be implemented should the project be continued at a future point in further releases.
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
* [SQlite3](https://sqlite.org/index.html): Local database storage in python.

## Testing
All testing can be found in [Testing.md](https://github.com/RhysPollardDevelopment/Fullstack-milestone/blob/master/TESTING.md)

## Deployment

#### Environmental Setup:
1. It is worth setting up a virtual environment and any settings within Python before starting any project to ensure a clean stable working environment. This will contain any packages, linters and installations and prevents cross project errors and version issues.
    * Python 3 has a built in virtual environment called [venv](https://docs.python.org/3/tutorial/venv.html) which can be created using the below code:  
    ```python3 -m venv .virtual-environment-name```  
    This will create your virtual environment directory with the name/path given.

    * To activate your virtual environment on Windows, run:  
    `.virtual-environment-name\Scripts\activate.bat` or `.virtual-environment-name\Scripts\activate`
    On Unix or MacOS, use:
    ```source .virtual-environment-name/bin/activate```

### How to run locally:
These instructions will allow you to run this project on your local machine/environment.

1. Follow this link to the [full repository](https://github.com/RhysPollardDevelopment/Fullstack-milestone).

2. On the upper right of repository page, select the green _"Code"_ button.

3. The easiest solution for most instances is to look for the repository address under the _"Clone"_ heading and select the clipboard icon.

4. In your local IDE, open the terminal and enter the following:  
    ```git clone https:\\the-copied-url-in-your-clipboard-from-respository```

5. Upon pressing enter your local clone will be ready.

6. In your IDE, navigate to your cloned project if required.  
``` cd/path/to/cloned/folder```

7. Now to activate your virtual environment (see above if need help with this step), remembering the capital S in Scripts.
    ```.virtual-environment-name\Scripts\activate```

8. To ensure all required packages/dependencies are installed:
    ```pip install -r requirements.txt```

9. Next, you need to create an environmental variables file. This can be a `.env` or `env.py` file. 

10. **Ensure your environmental variables file is added to .gitignore**. These are private keys and must not be shared publically.

11. Assuming you are using a `env.py` file, add the following variables to your variables list:
    ```python
    os.environ.setdefault('SECRET_KEY', '<generated using a secret key generator>)
    os.environ.setdefault('STRIPE_PRICE_ID', '<From the Stripe website>)
    os.environ.setdefault('STRIPE_PUBLIC_KEY', '<From the Stripe website>)
    os.environ.setdefault('STRIPE_SECRET_KEY', '<From the Stripe website>)
    os.environ.setdefault('STRIPE_WEBHOOK_SECRET', '<From the Stripe website>)
    os.environ.setdefault('DEVELOPMENT', True)
    ```  

    Assuming you are using a `.env``` file, the same keys should be used as above but in the format:  
    ```VARIABLE_NAME=variable```  

    The majority of these keys are created from [stripe](https://stripe.com/gb) as a registered user.

12. Go to `settings.py` in your the main fullstack app and import these environmental variables.

13. Now you're ready to run the website locally with:
    ```python manage.py runserver```

14. The website should be available on localhost:8000, usually defined as `http:\\127.0.0.1:8000` in your browser of choice.

15. In the terminal, run the following lines `python manage.py makemigrations` and `python manage.py migrate` to migrate models to the local database.

16. To add products locally, a super user account will be needed. This can be achieved by typing `python manage.py createsuperuser` in the terminal and following the prompts given.  
The administration portal to add new instances of products, recipes or companies can be found by adding `\admin` to the home page address.

##### Notes:
You may need to add `127.0.0.1` to allowed hosts list in your `settings.py` file.

Also, the use of `python`, `pip`, `python3` and `pip3` can vary between versions of python/IDE/your own machine so check to be sure.

The local version will be running off of the local SQlite3 database unless you provide a database url which we cover in the Heroku section below.

### Heroku

#### Amazon Web Services S3
For this website, you will require an AWS account and S3 bucket to store and load media and static files. The required settings and instructions are as follows:

1. Travel to the [AWS website](https://aws.amazon.com/) and create and AWS account using whatever details are required, when you login in you will be a **Root User**.
    * You will need add your billing details, there is a free usage limit so this depends on how much use your site receives.

2. Once you have an account, locate the **S3** services by selecting the _"Services"_ dropdown in the top left and either searching for _"S3"_ or selecting it from the menu.

3. Create a bucket with the _"Create Bucket"_ button.
    * Your name should ideally match your project name/heroku app name.
    * Select the region closest to you.
    * Uncheck _"Block all public access"_.
    * Tick the acknowledgement below.

4. To set up the new bucket, select the bucket name and choose the _"Properties"_ Tab.

5. Scroll down to _"Static Website Hosting"_ and select _"Edit_".
    * In this new screen, make sure static website hosting is set to **Enable**.
    * Enter `index.html` and `error.html` default values for the two document inputs as you will not be needing these.
    * Then click the _"Save"_ button.

6. Move to the _"Permissions"_ tab and scroll to the bottom for the CORS configuration. Click _"Edit"_, copy in this code and click _"Save"_:
    ```
    [
        {
            "AllowedHeaders": [
                "Authorization"
            ],
            "AllowedMethods": [
                "GET"
            ],
            "AllowedOrigins": [
                "*"
            ],
            "ExposeHeaders": []
        }
    ]
    ```
7. On the same tab, scroll to the _"Bucket Policy"_ section and select _"Policy generator"_.
    * In the new tab, the bucket type of policy will be **S3 Bucket Policy**.
    * Enter an asterisk (*) in _"Principle"_ to allow all.
    * Select the get object choice from the _"Actions"_ selector.
    * The ARN value can be gotten from the browser tab already open (**Do not close this current tab**), above the empty _"Policy_" field and can be copied by clicking the left icon.

8. Once copied into the input, click _"Add Statement"_ followed by _"Generate Policy"_. The output can then be copied in its entirety into the _"Policy"_ editor on the same tab you found the ARN value.
    * Before saving, find the line of code you have pasted started with `Resource` and include `/*` at the end to allow all access to all resources and click save.
    ```"Resource": "arn:aws:s3:::Your-bucket-name/*"```

9. Staying in the permissions tab, find the _"Access control list(ACL)"_ section and select _"Edit"_.
    * Find _"Everyone (public access)"_ and under the _"Objects"_ header, tick **List**.
    * Tick _"I understand the effects of these changes on my objects and buckets"_ followed by _"Save Changes"_.

10. In the services at top of the page, search or find the _"IAM"_ service to create user access to our bucket.
    * In the side panel, make a new group with a recogniseable name to go with your project.
    * Click _"Next step"_ until you can finally click _"Create group"_.

11. Next, click _"Policies"_ on the left side pnael and then _"Create Policy"_.
    * Select the _"JSON"_ tab and click **import managed policy** in top right to retrieve a pre-made policy.
    * Filter by typing **S3** in the input and choose _"AmazonS3FullAccess"_, then click _"Import"_.
    * As we do not want full access to everything, we will copy the ARN number from our bucket policy and paste it in `"Resource":"*"` as the following.
    ```
    "Resource": [
        "arn:aws:s3:::your-bucket-name",
        "arn:aws:s3:::your-bucket-name/*",
    ]
    ```
    * Click _"Review Policy"_, give it a name and description, then click _"Create Policy"_.

12. Return to the groups list, select your newly made group object.
    * Click _"Attach Policy"_ and search for your new policy name.
    * Select the new policy and hit _"Attach policy"_.

13. Finally, create a user for this group. Select the user option on the side panel.
    * Create a user with a recogniseable name and give them **Programmatic access**.
    * Tick the box on the new group you have made and then click next until you reach _"Create User"_.
    * Use _"Download.csv"_ to collect your users access key and secret access key.

**Do not lose or delete the _"download.csv"_ file, you can only access it once and is required to access your S3 bucket.**

#### Deployment to Heroku
This process will allow you to publish and host a live version of this project on the heroku app.

1. Travel to the heroku website and create a user account as required.

2. Once registered, click  _"New"_ in the top right and _"Create App"_ from the dropdown.

3. Choose a name and region best suited for you before pressing the create app button.

4. Once in Heroku's app page, got to _"Resources"_ and search for _"Heroku Postgres"_ wihin the Add-ons section.
    * Choose the _"Hobby Dev"_ free version and click _"Provision"_ button.

5. Once provisioned, move to the _"Settings"_ header in your heroku and scroll to Config Var. Here you can click _"reveal Config Vars"_ to see and add configuration details.

6. To set up out Heroku Postgres, copy the `DATABASE_URL` variable from the configuration variables and add it to your `.env` or `env.py` file in the required format.

7. Now that the correct database has been configured, migrate your models to the Postgres SQL database  
    `python manage.py makemigrations` then `python manage.py migrate`

8. Much like before, creating a super user is a good idea to allow admin access.
    ```python manage.py createsuperuser```

9. It is advisable to now remove the `DATABASE_URL` from your environment to prevent multiple sources editing the database. Also, in `settings.py`, add the url of your heroku app to the `ALLOWED_HOSTS` list.

10. If you have added any other packages or software, ensure you freeze the dependencies into your `requirements.txt`
    ```pip freeze --local > requirements.txt```

11. Create a Procfile that tells Heroku what sort of app to make by typing the following (with the < > section being replaced entirely with your project name).
    ```web:gunicorn <project_name>.wsgi:application```

12. To prepare for our heroku deployment, `git add`, `git commit` with comment and then `git push` your changes to Github.

13. Go to Heroku and in the _"Settings"_ header, select _"Reveal Config Vars"_ and add the following
    |Key                    | Value                        |
    |-----------------------|------------------------------|
    |AWS_ACCESS_KEY_ID      |AWS_access_key                |
    |AWS_SECRET_ACCESS_KEY  |AWS_secret_access_key         |
    |DATABASE_URL           |generated_by_herokupostgres   |
    |EMAIL_HOST_PASSWORD    |your_email_host_key           |
    |EMAIL_HOST_USER        |your_email_host_user          |
    |SECRET_KEY             |secret_key                    |
    |STRIPE_PRICE_ID        |stripe_subscription_product_id|
    |STRIPE_PUBLIC_KEY      |stripe_public_key             |
    |STRIPE_SECRET_KEY      |stripe_secret_key             |
    |STRIPE_WEBHOOK_SECRET  |stripe_secret_webhook_key     |
    |USE_AWS                |True                          |

14. Select the _"Deploy"_ and in the _"Deployment Method"_ section, choose the Github option and in the input below, search for the correct repository you wish to connect to Heroku.

15. Once connected, scroll downwards to _"Automatic Deploys"_ 
    * Click _"Enable Automatic Deploys"_, followed by _"Deploy Branch"_.
    * Now any time this repository receives a push request, heroku will update and re-launch the app.
    * You can check on the status by going to the _"Activity"_ header.

16. Open your app with _"Open App"_ to view the completed website.

17. Your S3 buckest should now contain a `static/` folder, you can now add the `media/` folder for images and documents.

18. Your app is now deployed, as a super user you may add products, recipes and companies using the `heroku_url/admin/` panel or using any CRUD forms available on the site.

## Credits
### Content
* All partner companies and apiaists are fictional and created by myself purely for this project.
* 

#### Media

### Code reference
* Django testing was aided significantly with help from [Pluralsight](https://app.pluralsight.com/), specifically their course on [Django testing, security and performance](https://app.pluralsight.com/library/courses/django-testing-security-and-performance), alongside the code institute introduction module for django.
* [Django documents](https://docs.djangoproject.com/en/3.2/topics/testing/tools/) was also referenced throughout testing.
* The majority of coding examples and insights were taken from [python docs](https://docs.python.org/3/) and [Django Docs](https://www.djangoproject.com/) as they are the primary sources of information.
* `Stripe_elements.js` and much of the code for the `create_subscription` view was copied and edited from [a stripe subscription tutorial](https://stripe.com/docs/billing/subscriptions/fixed-price) or inspired heavily by their official subscription documents. Their API references were also used extensively in the collection of data from webhooks and API calls.
* Where these sources of information were not suitable or specific enough I have endeavoured to place comments in the code detailing the origin of the code snippet, or at least inspiration for the written code result.

### Acknowledgements
Special thanks to my mentor Brian Macharia for his help and advice in development this project. Extra thanks go to the testers composed of family and friends.

### Disclaimer
This project has been made for purely academic purposes.