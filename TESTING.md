# Testing.md

## Table of contents
* [Automated testing](#automated-testing)
* [Validation](#validation)
* [Functionality](#functionality)
* [Compatability and responsiveness](#browser-compatibility-and-responsiveness)
* [User stories](#user-story-testing)
* [Bugs](#bugs)
* [Future testing]

Testing was performed through this project when any new feature was implemented or altered. This was performed as much as possible to Test Driven development (TDD) standards as best as possible, while trying to cover both integration and unit testing.

To best imitate Git-flow, branches were employed to isolate code from the master branch and ensure stability while achieving required user stories, before incorporating into the main code branch. Once ensured for stability, each branch's changes were pushed to the deployed website. This meant that any errors which occurred could only exist within one area of the code and could be identified much faster.

To ensure that this project works and maintains as expected, backend validation is performed by Django, model restrictions and form validation in views. On the front end this is self inserted validation alongside HTML validation which is most often asserted through model forms. Defensive programming also assists in maintaining site integrity by warning users of actions with permanent effects, such as confirmation models on instance deletion, along with formatting requirements for insertion of data.

## Automated Testing
Django code was testing primarily using in framework testing tools, spanning across every app for any views, models or forms created to ensure that any changes did not break or alter the viability of code. The coverage package was used to determine the amount of code covered and generate reports, showing code coverage of **91%**.

* Unit testing was performed using TDD where possible by creating the tests with the desired responses and crafting the views and models to meet those assertions as best possible. To view tests, enter `python manage.py test <appname>` in the terminal. The appname is optional but allows for targetted testing.

* The use of unittest.mock and unittest.patch was essential to prevent the necessity of Stripe API calls, reducing the dependencies ensured this was unittesting and not integration testing.   

To run this report using coverage in the terminal:
```coverage run --source=recipes,products,profiles,subscriptions,customerservice```

To see the results, either the `coverage report` or `coverage html` command can be run, though the latter requires a http server to view.

[Django code coverage report](https://github.com/RhysPollardDevelopment/Fullstack-milestone/blob/master/readmedocs/coverage-report.png)

## Validation

### HTML   
All HTML files were tested with the [W3 Markup Validation Service](https://validator.w3.org/) through either URI validation, or through direct input from page sources where login and other restrictions were imposes. There were some minor errors which occurred, primarily with stray end tags but also having two forms with autofocus on the same page. There were a number of warnings which comprised of anchor tags not needing role="link" and scripts not needed type="text/javascript".   

### CSS
All CSS files tested with the [W3 CSS Validation service](https://jigsaw.w3.org/css-validator/) by direct input.   
There was only one error: the property `text-underline-offset` did not accept pixel values, this was removed as it did not serve its purpose in that case. All other warnings were about the use of variables for colours and fonts. As these were not used much as anticipated they were removed.

### PEP8
All python files were tested using online [PEP8 validator](http://pep8online.com/) for assessment.   
Only one warning arose; a line which was too long was split and formatted by black so a operator (+) was left with a blank space infront of it. This was fixed so the line did not need to break. Migration files and other django generated files were not assessed as they often generate code which is not PEP8 valid.

### JavaScript
All javascript files have been tested using [JShint online validator](https://jshint.com/).   
All Javascript was found to be syntactically correct, however warnings were common for $ as an undefined variable and that the code used EcmaScript 6 features such as `let` and `const`. Other warnings arose for undefined or unused variables `Stripe`, `google` and `marker`. As these variables were referenced directly from the Stripe and Google documentation, the code has been tested thoroughly by its creators and seems unwise to remove.


## Functionality    
The table below details the current functionality of the entire Freebees site, following any corrections and updates which can be in the [bugs](#bugs) section.  
This testing does not extend to Django All-auth pages (beyond links added to other pages) as this functionality should have been tested by Django prior to its inclusion.


|Number|Test Action | Expected Outcome | Test Outcome |
|:---:|---------|---------------|:--------:|
|1|Click subscribe now on index page Header|Be sent to the subscriptions explanation page.|PASS|
|2|Click subscribe now on index first section|Be sent to the subscriptions explanation page.|PASS|
|3|Click about us on index page|Move to about us page|PASS|
|4|Click on our partners button on Index page|Be moved to recipes page|PASS|
|5|Click on our honey button on Index page|Be moved to products page|PASS|
|6|Click company logo on navabar and footer|Be sent to index page.|PASS|
|7|Click navbar links to see if directed correctly.|All navbar links direct to respective pages.|PASS|
|8|Navbar links should become active on respective page|All links should highlight when on their page.|PASS|
|9|Click social icons on footer.|New page opens at the corresponding website.|PASS|
|10|Clicking subscribe now on Subscription page without logging in.|Login page appears.|pass|
|11|Navbar change for mobile and tablet|navbar reduced to a drop down with burger icon.|PASS|
|12|Product page loads|Multiple products with descriptions and loaded images.|PASS|
|13|Mobile and tablet version of product pages.|Products should resize and reposition to take up better space.|PASS|
|14|Select product image or more info button.|Load individual product page with added details.|PASS|
|15|Click multiple products in rapid succession.|Should load the first selected.|PASS|
|16|Product details page loads|Header with background, image and details.|PASS|
|17|Click visit button for honey company.|New browser tab should open, page should not exist as fake address.|PASS|
|18|Subscribe now button on product page clicked|Redirected to subscription details page.|PASS|
|19|Click on the related recipes|User should be moved to the respective recipe details page|pass|
|20|Click on other products at bottom of product page|User should be moved to the other recipe's details page.|PASS|
|21|Our recipes button clicked|Redirected to recipes list.|PASS|
|22|Product page in mobile and tablet version.|Page responds to match new dimensions, background changes for mobile header.|PASS|
|23|Recipes list url is chosen.|Header, title and list of recipes with details and images are loaded|PASS|
|24|Recipe list change during mobile and tablet.|List of recipes and header change dimensions to match new screen size.|PASS|
|25|Click recipe icon or button with "restricted" page|Recipe header and ingredients load but rest is blurred with a subscription button.|PASS *|
|26|Click restricted access subscription button.|Redirected to subscription page.|PASS|
|27|Click recipe image or button without a restricted badge|All recipe items should load along with featured product and other recipes.|PASS|
|28|Click featured recipe image or button|Redirected to specific product page|PASS|
|29|Click other recipe link image|Be redirected to other recipe page, loading depends on restriction.|PASS|
|30|User disables restricted blur|Fake instructions and products will be displayed.|PASS|
|31|User clicks fake image or button for product in restricted section.|User is sent to the subscriptions page.|PASS|
|32|Authenticated user access restricted recipe page.|Recipe header and ingredients load but rest is blurred with a subscription button.|PASS|
|33|Subscribed user access restricted recipe page.|Recipe header and instructions are all shown, along with featured product and other recipes|PASS|
|34|Our story page loads|Header, images and test relating to company purpose are loaded.|PASS|
|35|Our partners page is loaded.|Partners images and description are loaded along with test asking for more partners.|PASS|
|36|Click partners icons or visit buttons|New browser tab should open, page should not exist as fake address.|PASS|
|37|No partners are created on loading.|Message stating that partners will be added soon is displayed in icons' spot.|PASS|
|38|Give us a buzz button is clicked|User is moved to contact page.|PASS|
|39|Contact page is loaded.|Contact form, social media links and company contact details are loaded with google map.|PASS|
|40|Click social icons on footer.|New page opens at the corresponding website.|PASS|
|41|Form is completed correctly and submitted|User is redirected to a success page and given a button to move location.|PASS|
|42|Form is not completely filled|Front end validation prevents submission and warns user.|PASS|
|43|Google maps is dragged|Map view moves with the users drag|PASS|
|44|Google map is double clicked|Map zooms in further.|PASS|
|45|Contact page views on mobile or tablet|Contact form becomes full width and page re-aligns to fit screen sizes.|PASS|
|46|login page loaded.|Login form is loaded with option to sign up or retrieve password.|PASS|
|47|Sign up link is clicked from login-page|Sign up form is loaded|PASS|
|48|Forgot password link is clicked from login-page|Password reset page is loaded.|PASS|
|49|Log in with empty fields|Validation requests user to complete field.|PASS|
|50|Login with incorrect information|Form informs user that information is incorrect.|PASS|
|51|Login correctly|User is redirected to the index page.|PASS|
|52|Logout button is visible when logged in|Logout should have replaced the login button.|PASS|
|53|Click logout button|User is moved to the log out form.|PASS|
|54|Signout button is clicked|user is redirected to index and login button is visible|PASS|
|55|Logged in user tries to enter /account/login/|user is redirected to index page|PASS|
|56|Signup page is loaded|Sign up form is loaded with two email inputs, a username and 2 password inputs.|PASS|
|57|Login link from signup page is clicked.|user is moved to the login page.|PASS|
|58|Sign up form is incomplete|Sign up form front end validation warns user that information is required.|PASS|
|59|Email address do not match|Page reloads with red error messahe stating "must type same email each time".|PASS|
|60|Passwords do not match|Page reloads with error message stating "Passwords must match"|PASS|
|61|Enter invalid email address|Page reloads with error asking for valid email address|PASS|
|62|Password is too short|Page reloads with error explaining too short|PASS|
|63|password is numerical only|Page reloads eith error saying password cannot be numerical|PASS|
|64|Successful sign up|Directed to page asking for email verification and email is sent.|PASS|
|65|Email confirmation page is opened through email link|Confirmation page is opened with button to confirm|PASS|
|66|Email confirmation button is clicked.|User is redirected to login page.|PASS|
|67|Email confirmation page is opened without email link|Message presented explaining this link is invalid and suggests resending verfication email.|PASS|
|68|Subscription page loaded|header loaded with how it works section and images below.|PASS|
|69|Either subscribe now button clicked on subscriptions page as anon user|Both direct to login page as checkout required authentication|pass|
|70|Subscribe now buttons on subscription page as logged in user.|Redirected to checkout page.|PASS|
|71|New logged in user at checkout.|No delivery or billing details should be completed in form|PASS|
|72|Unchecking "Billing address same as delivery"|Second half of form should drop down for billing information.|PASS|
|73|Same billing, submit without all required information.|Validation requests user to complete field.|PASS|
|74|Different billing, submit without all required information.|Validation requests user to complete field.|PASS|
|75|Delivery/billing complete, no card details|Stripe card should present error of lacking card detail.|PASS|
|76|Delivery/billing complete, card details incomplete|Stripe card should present error of lacking card detail.|PASS|
|77|Expiry date has beenr eached|Stripe card element provides error of "Your card's expiration year is in the past".|PASS|
|78|CVC number is incorrectly completed|Stripe card element provides error of "Your card's security code is incomplete".|PASS|
|79|postcode/zip is incomplete|Stripe card element provides error of "Your postal code is incomplete"|PASS|
|80|Card used which required authorisation.|Authorisation panel will load asking for user acceptance or denial.|PASS|
|81|Card authorisation is declined|Submission halts and stripe element presents error.|PASS*|
|82|card authorisation is accepted|Submission continues and database creates new subscription and invoice and moves to success page.|PASS*|
|83|Card payment is accepted without authorisation|Loading overlay ocurrs and then user is moved to success page.|PASS|
|84|Update delivery address is not checked.|Submission occurs successfully, user profile shows no address added for delivery.|PASS|
|85|Update delivery address is checked.|Submission occurs successfully, user profile shows the new address in update address page.|PASS|
|86|Click profile button on success page.|User is directed to their profile page.|PASS|
|87|User tries to use subscription navbar link|Navbar link is no longer visible as user has subscription.|PASS|
|88|User tries to access /subscription with an active subscription|User is redirected to index|PASS|
|89|User tries to access /subscription/checkout with subscription|User is redirected to index|PASS|
|90|User tries to access /subscription/checkout/complete with subscription|User is redirected to index|PASS|
|91|Load profile page without subscription|Profile page displays image, username, email, joined date and no active subscription plus 2 buttons|PASS|
|92|Load prfile page with subscription|Page displays image, username, email, joined date, subscribed since date, billing date ad cancel sub button|PASS|
|93|Click update password|User is directed to django all auth update password page.|PASS|
|94|Click change email|User is directed to django all auth email form.|PASS|
|95|Cancel subscription button is clicked|Confirmation modal appears explaining results of cancellation.|PASS|
|96|Click cancel button on modal.|Modal is removed and user returns to page.|PASS|
|97|Confirm button is clicked on modal|user is directed to image page with text and button to go to profile.|PASS|
|98|Click profile button on cancel confirmation page.|User is returned to profile and cancel button is now reactivate button.|PASS|
|99|Reactivate subscription button is clicked|User is directed to an update page stating that their subscription is active|pass|
|100|Click profile button on reactivation confirmation page.|User is returned to profile and cancel button is now cancel button.|PASS|
|101|Address header in profile is selected|Page reloads with update detail forms for billing and delivery.|PASS|
|102|Address header in profile is selected if addresses already saved.|Page loads with forms already filled with information.|PASS|
|103|Update address form and click Update|Redirected to profile page and messages says delivery updated. Return to page shows change.|PASS|
|104|Updated billing and click update|Redirected to profile page and messages says billing updated. Return to page shows change.|PASS|
|105|Incomplete address for billing update|Validation requests user to complete field.|PASS|
|106|Try to enter data longer than field maximum|Form input will not let you enter more than the maximum amount of characters.|PASS|
|107|Subscription History loaded without subscription|Active icon on subscription header: message stating no invoices to show.|PASS|
|108|Subscription History loaded with subscription|Active icon on subscription header: Message showing recipe and honey for this month.|PASS|
|109|Click image for recipe or honey|Directed to page asking for email verification and email is sent.|PASS|
|110|Admin level user clicks profile navbar link|Drop down includes Add recipe, add product and add company.|PASS|
|111|Clicking the add object link in profile for recipe, product and company|Directs user to form for adding that object.|PASS|
|112|Add item form is incomplete when submitted|Validation requests user to complete field. All fields required.|PASS|
|113|Add item form is submitted successfully.|Redirected to page for that product.|PASS|
|114|Admin user views products/recipes/partners pages|Edit and delete buttons are visible under each product, recipe or company|PASS|
|115|Admin user clicks edit button on product/recipe/company|Opens form prefilled with product information.|PASS|
|116|Edit form is incorrectly filled/empty|validation requests user to completed required fields.|PASS|
|117|Delete button is pressed on products page.|Modal appears explaining outcome and has cancel and confirm button.|PASS|
|118|Recipe form given non date time in datetime field.|Page is reloaded with error stating that valid date time is required.|PASS|
|119|Recipe form given invalid date time|Page is reloaded with error stating that valid date time is required.|PASS|
|120|Company form given invalid url|Validation prevents submission and reloads page with error asking for valid url.|PASS|
|121|Profile button for change password success clicked|Returns user to profile page.|PASS|

## Browser Compatibility and Responsiveness
Freebees has been tested across the following browsers: Chrome, Edge, Safari, Opera, Firefox, Internet Explorer and Yandex.   
This has been done locally and using simulated environments from [BrowserStack](https://www.browserstack.com/), the website has been tested across multiple versions of windows, mac and multple different versions of each browser.
No issues were found across any of these browsers.

The responsive layout of Freebees has been assessed using [Am I Responsive?](http://ami.responsivedesign.is/), [Responsive Design Checker](https://responsivedesignchecker.com/) and [Responsinator](http://www.responsinator.com/). These tools helped to highlight key issues such as product image height issues for mobile phones turned to a landscape view.

This website has been tested across a range of emulated devices using [BrowserStack](https://www.browserstack.com/), Chrome Developer Tools and other browsers. Designs were started on the smallest mobile screens and developed to grow onto larger screens, ensuring content never struggles for space. Larger screens of 1200px and above have also been accounted for when special conditions are required.

## user stories:
Any user stories not started, say deprioritized in own seection.

## Bugs

#### Fixed Functionality:   
* **No 25:** Originally failed as discovered edge case: As products had been deleted during testing, the recipe loaded with a 500 error as no product object was available for the HTML template. This should not happen as product should be updated and recipes not left without a product; to account for this low risk the html checks if the product is None or exists and displays HTML accordingly.
* **No 25:** Also failed as restricted message overlay had an unreachable button. The z-index was too low and the button was not clickable, this was fixed by increasing the z-index so it was the highest object in its' div.
* **No 81:** While this passed its critera, in the back end this was a failure as the webhooks associated did not correctly respond to card authorization requests. When declined, the webhook for `customer.subscription.created` was called prior to failure, resulting in a new subscription and invoice instance which did not match the Stripe instance. This was solved by instead checking for the `invoice.paid` event which was created with the specific billing reason of `subscription-created`. As this webhook is called following the authorization decision, it better reflects the active state of the subscription.
* **No 82:** This also failed for the same reasons as No.81, however it also failed in the back end database as the `customer.subscription.update` webhook is called following a successful subscription. This webhook sent invalid emails and risked an internal error if the webhook was received prior to the subscription being created as it was dependent on an existing subscription object. As webhooks are not received in order, the `customer.subscription.update` was updated to check us user had an active subscription before attempting to update.

## Future testing
* test webhooks in django, Due to high % across site and relative ease of most data, did not seem necessary to perform large volumes of testing.