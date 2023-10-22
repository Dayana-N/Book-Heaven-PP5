from django.shortcuts import render

from products.models import Book


# Create your views here.
def home(request):
    '''
    A view to render the home page
    '''
    books = Book.objects.all().order_by('-created')

    context = {
        'books': books,
    }
    return render(request, 'home/index.html', context)
