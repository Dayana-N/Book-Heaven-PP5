# Create your models here.
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django_countries.fields import CountryField

from products.models import Book
from profiles.models import UserProfile

# Create your models here.
STATUS = (
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
)


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    discount = models.DecimalField(
        blank=True, null=True, max_digits=6, decimal_places=2)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        '''
        Generate a random, unique order number using UUID
        '''
        return uuid.uuid4().hex.upper()

    def update_total(self):
        ''' Update the total every time an item is added'''
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))[
            'lineitem_total__sum'] or 0

        if self.order_total < settings.DELIVERY_THRESHOLD:
            self.delivery_cost = settings.DELIVERY_FEE
        else:
            self.delivery_cost = 0

        if self.discount and self.discount > 0:
            self.order_total -= self.discount

        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        '''
        Override the original save method to set the order number
        if it hasn't been set already.
        '''
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderStatus(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=200, null=True, blank=True, choices=STATUS, default=STATUS[0][0])

    def __str__(self):
        return f'{self.order.order_number} - {self.status}'


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(
        Book, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=False, blank=False)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        ''' Set the line item total '''
        self.lineitem_total = self.product.product_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'ISBN{self.product.isbn} on order {self.order.order_number}'
