from django.test import TestCase
from django.urls import reverse

class PostViewTest(TestCase):
    def test_home_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_ajax_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)





