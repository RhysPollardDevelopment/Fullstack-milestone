from django.test import TestCase


class TestCustomerServiceViews(TestCase):
    def test_get_index(self):
        """
        Test to get the main products page.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customerservice/index.html")

    def test_get_contact(self):
        """
        Test to get the main products page.
        """
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customerservice/contact.html")

    def test_get_about(self):
        """
        Test to get the main products page.
        """
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customerservice/about.html")
