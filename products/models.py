import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return str(self.name)


class Genre(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    friendly_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.friendly_name)


class Author(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(
        null=True, blank=True, upload_to='authors/', default='authors/default-author.png')
    bio = models.TextField()
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class Book(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    author = models.ManyToManyField(Author, related_name='books')
    description = models.TextField()
    image = models.ImageField(
        null=True, blank=True, upload_to='books/', default='books/product-not-found.png')
    publisher = models.CharField(max_length=200)
    date_published = models.DateField()
    language = models.CharField(max_length=200)
    pages = models.IntegerField(null=True, blank=True)
    isbn = models.CharField(max_length=13)
    stock_amount = models.IntegerField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    in_stock = models.BooleanField(default=True)
    on_sale = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField(null=True, blank=True)
    sale_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.title)

    @property
    def product_reviews(self):
        '''
        Returns boolean value based on
        if book has reviews
        '''
        reviews = self.reviews.all()
        if reviews:
            return True
        else:
            return False

    @property
    def get_average_rating(self):
        '''return the average rating for book'''
        reviews = self.reviews.all()

        if reviews:
            average_rating = reviews.aggregate(Avg('rating'))
            return range(int(average_rating['rating__avg']))
        else:
            return range(0)

    @property
    def price_discount(self):
        ''' 
        Calculate discount based on new price 
        '''
        if self.sale_price:
            discount = ((self.price - self.sale_price) / self.price) * 100
            return round(discount)
        else:
            return None

    @property
    def product_in_stock(self):
        ''' 
        Determines if the product is in stock
        based on the stock amount.
        '''
        if self.stock_amount >= 1:
            return True
        else:
            return False

    @property
    def product_price(self):
        ''' 
        Returns the price of item based on
        if item is on sale
        '''
        if self.on_sale and self.sale_price < self.price:
            return self.sale_price
        return self.price

    def save(self, *args, **kwargs):
        self.discount = self.price_discount
        self.in_stock = self.product_in_stock
        if not self.on_sale:
            self.sale_price = 0
        super().save(*args, **kwargs)
