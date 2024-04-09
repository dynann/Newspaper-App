from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your tests here.

class SignupPageTests(TestCase):
    def test_url_exist_at_correct_location_signup_view(self):
        response = self.client.get("/account/signup/")
        self.assertEqual(response.status_code, 200)
        
    def test_signup_view_name(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")
        
    def test_signup_form(self):
        response = self.client.post(
            reverse("signup"),{
                "username": "test2",
                "email": "testuser16@gmail.com",
                "password1": "nannrann16",
                "password2": "nannrann16",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].get_username, "test2")
        self.assertEqual(get_user_model().objects.all()[0].get_email_field_name, "testuser16@gmail.com")