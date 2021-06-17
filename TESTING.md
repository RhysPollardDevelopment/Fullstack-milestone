# Testing.md

## Table of contents
* [Unit testing Django]
* [Jasmine testing]
* [Integration testing]
* [Validators]
* [User story acceptance]
* [Bugs]
* [Future testing]

Testing was performed through this project when any new feature was implemented or altered. This was performed as much as possible to Test Driven development (TDD) standards as best as possible, while trying to cover both integration and unit testing.

For the back end code, branches were employed heavily to isolate code from the master branch and ensure stability before incorporating into the main code branch. Once ensured for stability, each branch's changes were pushed to the deployed website. This meant that any errors which occurred could only exist within one area of the code and could be identified much faster.

To ensure that this project works and maintains as expected, backend validation is performed by Django, model restrictions and form validation in views. On the front end this is self inserted validation alongside HTML validation which is most often asserted through model forms. Defensive programming also assists in maintaining site integrity by warning users of actions with permanent effects, such as confirmation models on instance deletion, along with formatting requirements for insertion of data.

## Unit testing
Django code was testing primarily using in framework testing tools, spanning across every app for any views, models or forms created to ensure that any changes did not break or alter the viability of code. The coverage package was used to determine the amount of code covered and generate reports, showing code coverage of **95%**.

* Unit testing was performed using TDD where possible by creating the tests with the desired responses and crafting the views and models to meet those assertions as best possible.

* The use of unittest.mock and unittest.patch was essential to prevent the necessity of Stripe API calls, reducing the dependencies ensured this was unittesting and not integration testing.
Below you can find one example of the django back end code coverage performed before front end tasks were undertaken:

![alt text](https://github.com/RhysPollardDevelopment/Fullstack-milestone/blob/master/readmedocs/coverage-report.png "Coverage report")

## Future testing
* test webhooks in django, Due to high % across site and relative ease of most data, did not seem necessary to perform large volumes of testing.