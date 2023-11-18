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


def faq_page(request):
    ''' Renders FAQ page  '''
    return render(request, 'home/faq.html')


def about_page(request):
    ''' Renders About us page '''
    return render(request, 'home/about.html')
