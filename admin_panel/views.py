from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render

from checkout.models import Order
from discount_codes.forms import DiscountCodeForm
from discount_codes.models import DiscountCode
from products.models import Book


# Create your views here.
@login_required
def admin_dashboard(request):
    '''A view to render the admin dashboard '''
    if not request.user.is_superuser:
        messages.error(request, 'You need admin rights to access this page.')
        return redirect('home')

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


@login_required
def admin_discounts(request):
    '''A view to handle admin discount codes page '''
    if not request.user.is_superuser:
        messages.error(request, 'You need admin rights to access this page.')
        return redirect('home')

    discount_codes = DiscountCode.objects.all()
    form = DiscountCodeForm()

    if request.method == 'POST':
        form = DiscountCodeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Code created successfully.')
        else:
            messages.error(request, 'Invalid form. Please try again.')

        return redirect('admin-discounts')
    context = {'discount_codes': discount_codes,
               'form': form, }
    return render(request, 'admin_panel/admin_discount.html', context)