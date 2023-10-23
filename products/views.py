from django.shortcuts import get_object_or_404, render

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


def product(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {'book': book, }
    return render(request, 'products/single-product.html', context)
