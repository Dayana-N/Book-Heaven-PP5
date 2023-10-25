from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render, reverse

from .models import Book, Category, Genre


# Create your views here.
def all_products(request):
    '''
    Render all products on products page
    '''
    books = Book.objects.all().order_by('-created')
    query = None
    genre = None
    category = None

    if request.GET:
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

    context = {
        'books': books,
        'search_query': query,
        'genre': genre,
        'category': category
    }
    return render(request, 'products/products.html', context)


def product(request, pk):
    '''
    Renders single produc page
    '''
    book = get_object_or_404(Book, pk=pk)
    context = {'book': book, }
    return render(request, 'products/single-product.html', context)
