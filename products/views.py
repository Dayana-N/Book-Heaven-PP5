from django.shortcuts import render

from .models import Book


# Create your views here.
def all_products(request):
    '''
    Render all products on products page
    '''
    books = Book.objects.all().order_by('-created')

    context = {
        'books': books,
    }
    return render(request, 'products/products.html', context)
