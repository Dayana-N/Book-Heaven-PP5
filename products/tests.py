from django.test import TestCase
from django.urls import reverse

from .models import Author, Book, Category, Genre


class ProductsPageTests(TestCase):
    def test_all_products_page(self):
        '''
        Test if all products page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(reverse('all-products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(
            response,
            '<li class="breadcrumb-item active" aria-current="page">Books</li>'
        )
        self.assertNotContains(response, 'Not on the page')


class ProductPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ''' Create test product'''
        cls.category = Category.objects.create(name='Fiction')
        cls.genre = Genre.objects.create(
            category=cls.category,
            name="horror",
            friendly_name='Horror')
        cls.author = Author.objects.create(name='Test author', bio='test bio')
        cls.product = Book.objects.create(
            genre=cls.genre,
            title="Test Title",
            id='f5604c36-bcf4-41fd-9acd-c67caf25ba24',
            description='Test description',
            publisher='test publisher',
            date_published='2023-12-08',
            language='english',
            isbn='9781399608893',
            stock_amount=3,
            price=20.00
        )
        cls.product.author.add(cls.author)

    def test_single_product_page(self):
        '''
        Test if the single product page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(
            reverse('product',
                    kwargs={'pk': 'f5604c36-bcf4-41fd-9acd-c67caf25ba24'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/single-product.html')
        self.assertContains(
            response, '<h5 class="my-2">Description:</h5>')
        self.assertNotContains(response, 'Not on the page')


class AuthorsPageTests(TestCase):
    def test_authors_page(self):
        '''
        Test if authors page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/authors.html')
        self.assertContains(
            response, '<h4 class="text-center">Authors:</h4>')
        self.assertNotContains(response, 'Not on the page')


class AuthorPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ''' Create test author'''
        cls.author = Author.objects.create(
            name='Test author',
            bio='test bio',
            id='ec742707-3c56-49a4-ac8f-4c2f3cc52022')

    def test_single_author_page(self):
        '''
        Test if authors page can be accessed
        and it returns the correct template
        '''
        response = self.client.get(
            reverse('author',
                    kwargs={'pk': 'ec742707-3c56-49a4-ac8f-4c2f3cc52022'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/author.html')
        self.assertNotContains(response, 'Not on the page')
