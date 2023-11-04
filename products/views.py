from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render, reverse

from .models import Author, Book, Category, Genre


# Create your views here.
def all_products(request):
    '''
    Render all products on products page
    '''
    books = Book.objects.all()
    query = None
    genre = None
    category = None
    sort = None
    direction = None

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

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'Please enter search criteria')
                return redirect(reverse('all-products'))

            queries = Q(title__icontains=query) | Q(
                description__icontains=query) | Q(author__name__icontains=query)
            books = books.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'books': books,
        'search_query': query,
        'genre': genre,
        'category': category,
        'current_sorting': current_sorting,
    }
    return render(request, 'products/products.html', context)


def product(request, pk):
    '''
    Renders single produc page
    '''
    book = get_object_or_404(Book, pk=pk)
    context = {'book': book, }
    return render(request, 'products/single-product.html', context)


def all_authors(request):
    ''' Renders a list of all authors '''
    authors = Author.objects.all().order_by('name')
    context = {'authors': authors}
    return render(request, 'products/authors.html', context)


def author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = author.books.all()
    context = {'author': author,
               'books': books, }
    return render(request, 'products/author.html', context)
