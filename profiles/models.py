import uuid

from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField

from products.models import Book


# Create your models here.
class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          editable=False, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(
        max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(max_length=40, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Wishlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)
