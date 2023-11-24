from django.shortcuts import render

from checkout.models import Order
from products.models import Book
from profiles.models import UserProfile


# Create your views here.
def admin_dashboard(request):
    '''A view to render the admin dashboard '''
    orders = Order.objects.all().order_by('-date')
    orders_count = orders.count()
    books_count = Book.objects.all().count()
    users_count = UserProfile.objects.all().count()
    context = {'orders': orders,
               'orders_count': orders_count,
               'books_count': books_count,
               'users_count': users_count, }
    return render(request, 'admin_panel/admin_dashboard.html', context)
