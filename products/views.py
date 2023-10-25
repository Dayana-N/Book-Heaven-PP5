from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render, reverse

from .models import Book


# Create your views here.
def all_products(request):
    '''
    Render all products on products page
    '''
    books = Book.objects.all().order_by('-created')

    if request.GET:
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
    }
    return render(request, 'products/products.html', context)


def product(request, pk):
    '''
    Renders single produc page
    '''
    book = get_object_or_404(Book, pk=pk)
    context = {'book': book, }
    return render(request, 'products/single-product.html', context)
