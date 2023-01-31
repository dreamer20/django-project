from django.test import TestCase
from django.urls import reverse
# Create your tests here.


class RegisterViewTest(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse('blog:register'))
        self.assertEqual(response.status_code, 200)
