from django.db.models import Sum
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
    total_grand_total = Order.objects.aggregate(
        total_grand_total=Sum('grand_total'))
    grand_total_sum = total_grand_total['total_grand_total']
    context = {'orders': orders,
               'orders_count': orders_count,
               'books_count': books_count,
               'total': grand_total_sum, }
    return render(request, 'admin_panel/admin_dashboard.html', context)
