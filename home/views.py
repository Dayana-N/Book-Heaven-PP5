from django.shortcuts import render

from products.models import Book


# Create your views here.
def home(request):
    '''
    A view to render the home page
    '''
    books = Book.objects.all().order_by('-created')[:6]

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


def privacy_page(request):
    ''' Renders Privacy Policy page '''
    return render(request, 'home/privacy_policy.html')
