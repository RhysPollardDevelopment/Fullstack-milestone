from django.test import TestCase


class TestCustomerServiceViews(TestCase):
    def test_get_index(self):
        """
        Test to get index page.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customerservice/index.html")

    def test_get_contact(self):
        """
        Test to get contacts page.
        """
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customerservice/contact.html")

    def test_post_contact(self):
        """
        Test for posting a message using contact form.
        """
        data = {
            "name": "Test user",
            "subject": "Testing your contact form",
            "body": "This is a test message.",
            "email_address": "testuser@test.com",
        }

        response = self.client.post("/contact/", data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "customerservice/contact.html")

    def test_post_contact_fail(self):
        """
        Test for posting a message using contact form.
        """
        data = {
            "subject": "Testing your contact form",
            "body": "This is a test message.",
            "email_address": "testuser@test.com",
        }

        response = self.client.post("/contact/", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customerservice/contact.html")

    def test_get_contact_success(self):
        """
        Test to see if contact_success page is reachable.
        """
        # Line was too long to insert templated directly into assertion.
        template = "customerservice/contact_thanks.html"
        response = self.client.get("/contact/success")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)

    def test_get_about(self):
        """
        Test to get the main products page.
        """
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customerservice/about.html")
