from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Contact

class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')

    def test_home_page_renders(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')

    def test_registration_successful(self):
        response = self.client.post(self.home_url, {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='john_doe').exists())

    def test_password_mismatch(self):
        response = self.client.post(self.home_url, {
            'username': 'jane_doe',
            'email': 'jane@example.com',
            'password': 'password1',
            'confirm_password': 'password2',
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='jane_doe').exists())

    def test_duplicate_username(self):
        User.objects.create_user(username='existing_user', email='existing@example.com', password='password123')
        response = self.client.post(self.home_url, {
            'username': 'existing_user',
            'email': 'other@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.filter(username='existing_user').count(), 1)


class ContactTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact_url = reverse('contact')

    def test_contact_page_renders(self):
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Us')

    def test_contact_submission_successful(self):
        response = self.client.post(self.contact_url, {
            'full_name': 'Alice Smith',
            'email': 'alice@example.com',
            'subject': 'Inquiry about service',
            'message': 'Hello, I would like to learn more.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contact.objects.filter(email='alice@example.com').exists())

    def test_contact_submission_missing_fields(self):
        response = self.client.post(self.contact_url, {
            'full_name': 'Alice Smith',
            'email': '',
            'subject': 'Inquiry',
            'message': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Contact.objects.filter(full_name='Alice Smith').exists())
