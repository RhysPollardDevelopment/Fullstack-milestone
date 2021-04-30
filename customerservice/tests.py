from django.test import TestCase


class homeTestViews(TestCase):
    def test_get_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customerservice/index.html")
