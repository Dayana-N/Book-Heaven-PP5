from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_page(self):
        '''
        Test if authors page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, '<h6 class="title">Fast Delivery</h6>')
        self.assertNotContains(response, 'Not on the page')


class AboutPageTests(TestCase):
    def test_about_page(self):
        '''
        Test if about page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(reverse('about-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/about.html')
        self.assertContains(response, '<h3>About us</h3>')
        self.assertNotContains(response, 'Not on the page')


class FaqPageTests(TestCase):
    def test_faq_page(self):
        '''
        Test if faq page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(reverse('faq-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/faq.html')
        self.assertContains(
            response, '<strong>Why did I receive only part of my order?</strong>')
        self.assertNotContains(response, 'Not on the page')


class PrivacyPageTests(TestCase):
    def test_privacy_page(self):
        '''
        Test if privacy page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(reverse('privacy-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/privacy_policy.html')
        self.assertContains(
            response, '<h1>Privacy Policy for Book Heaven</h1>')
        self.assertNotContains(response, 'Not on the page')
