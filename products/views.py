from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render, reverse

from profiles.models import Wishlist
from reviews.forms import ProductReviewForm
from reviews.models import ProductReview

from .models import Author, Book, Category, Genre
from .utils import products_pagination


# Create your views here.
def all_products(request):
    '''
    Render all products on products page
    '''
    books = Book.objects.all().order_by('-created')
    query = None
    genre = None
    category = None
    sort = None
    direction = None
    deals = None
    new_arrivals = None

    if request.GET:
        if 'sort' in request.GET:
            sort_value = request.GET['sort']
            sort = sort_value
            if sort_value == 'title':
                sort_value = 'lower_name'
                books = books.annotate(lower_name=Lower('title'))
            if sort_value == 'genre':
                sort_value = 'genre__name'
            if sort_value == 'category':
                sort_value = 'genre__category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sort_value = f'-{sort_value}'
            books = books.order_by(sort_value)

        if 'genre' in request.GET:
            search_genre = request.GET['genre'].split(',')
            books = books.filter(genre__name__in=search_genre)
            genre = Genre.objects.filter(name__in=search_genre)

        if 'category' in request.GET:
            search_category = request.GET['category'].split(',')
            books = books.filter(
                genre__category__name__in=search_category)
            category = Category.objects.filter(name__in=search_category)

        if 'deals' in request.GET:
            books = books.filter(on_sale=True)
            deals = True

        if 'new_arrivals' in request.GET:
            books = books[:8]
            new_arrivals = True

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'Please enter search criteria')
                return redirect(reverse('all-products'))

            queries = Q(title__icontains=query) | Q(
                description__icontains=query) | Q(author__name__icontains=query) | Q(isbn__icontains=query)
            books = books.filter(queries)

    books_count = books.count()
    books = products_pagination(request, books, 8)

    current_sorting = f'{sort}_{direction}'

    context = {
        'books': books,
        'books_count': books_count,
        'search_query': query,
        'genre': genre,
        'category': category,
        'current_sorting': current_sorting,
        'values': request.GET,
        'new_arrivals': new_arrivals,
        'deals': deals,
    }
    return render(request, 'products/products.html', context)


def product(request, pk):
    '''
    Renders single product page
    '''
    wishlist = False
    user_review = None
    book = get_object_or_404(Book, pk=pk)
    if request.user.is_authenticated:
        profile = request.user.userprofile
        user_review = ProductReview.objects.all().filter(product=pk, user=profile)
        if Wishlist.objects.filter(user=profile, product=book).exists():
            wishlist = True

    # reviews
    review_form = ProductReviewForm()
    reviews = ProductReview.objects.all().filter(product=pk).order_by('-created')

    context = {
        'book': book,
        'wishlist': wishlist,
        'review_form': review_form,
        'reviews': reviews,
        'user_review': user_review,
    }
    return render(request, 'products/single-product.html', context)


def all_authors(request):
    ''' Renders a list of all authors '''
    authors = Author.objects.all().order_by('name')
    context = {'authors': authors}
    return render(request, 'products/authors.html', context)


def author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = author.books.all()
    books = products_pagination(request, books, 6)
    context = {'author': author,
               'books': books, }
    return render(request, 'products/author.html', context)
