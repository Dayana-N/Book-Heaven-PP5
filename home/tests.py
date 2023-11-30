from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class HomepageTests(TestCase):

    def test_homepage(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, '<h6 class="title">Fast Delivery</h6>')
        self.assertNotContains(response, 'Not on the page')


class AboutpageTests(TestCase):

    def test_url_available_by_name(self):
        response = self.client.get(reverse('about-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/about.html')
        self.assertContains(response, '<h3>About us</h3>')
        self.assertNotContains(response, 'Not on the page')


class FaqpageTests(TestCase):

    def test_url_available_by_name(self):
        response = self.client.get(reverse('faq-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/faq.html')
        self.assertContains(
            response, '<strong>Why did I receive only part of my order?</strong>')
        self.assertNotContains(response, 'Not on the page')


class PrivacypageTests(TestCase):

    def test_url_available_by_name(self):
        response = self.client.get(reverse('privacy-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/privacy_policy.html')
        self.assertContains(
            response, '<h1>Privacy Policy for Book Heaven</h1>')
        self.assertNotContains(response, 'Not on the page')
