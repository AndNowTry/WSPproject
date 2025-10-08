from django.test import TestCase
from django.urls import reverse

class PostViewTest(TestCase):
    def test_login_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_code(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_logout_code(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
