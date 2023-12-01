from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class CartPageTests(TestCase):
    def test_cart_page(self):
        '''
        Test if shopping cart page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(reverse('view-cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')
        self.assertContains(
            response, '<h3>Shopping Cart</h3>')
        self.assertNotContains(response, 'Not on the page')
