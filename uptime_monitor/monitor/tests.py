from rest_framework.test import APITestCase

class SiteTests(APITestCase):

    def test_add_site(self):
        response = self.client.post(
            '/sites/',
            {"name": "Test", "url": "https://example.com"},
            format='json'
        )
        self.assertEqual(response.status_code, 201)