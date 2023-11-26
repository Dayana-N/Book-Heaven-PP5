from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

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

    discount_codes = DiscountCode.objects.all().order_by('-active')
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


@login_required
def admin_discounts_delete(request, pk):
    '''A view to delete discount codes '''
    if not request.user.is_superuser:
        messages.error(request, 'You need admin rights to access this page.')
        return redirect('home')

    code = get_object_or_404(DiscountCode, pk=pk)
    if request.method == 'POST':
        try:
            code.delete()
            messages.success(request, 'Code deleted successfully.')
        except ObjectDoesNotExist:
            messages.error(
                request, 'The code cannot be found in the database.')
        return redirect('admin-discounts')

    context = {
        'code': code,
    }
    return render(request, 'admin_panel/delete_confirmation.html', context)


@login_required
def admin_discounts_edit(request, pk):
    '''A view to edit discount codes '''
    if not request.user.is_superuser:
        messages.error(request, 'You need admin rights to access this page.')
        return redirect('home')

    code = get_object_or_404(DiscountCode, pk=pk)
    form = DiscountCodeForm(instance=code)

    if request.method == 'POST':
        form = DiscountCodeForm(request.POST, instance=code)

        if form.is_valid():
            form.save()
            messages.success(request, 'Code editted successfully.')
        else:
            messages.error(request, 'Invalid form. Please try again.')
        return redirect('admin-discounts')
    context = {
        'form': form,
        'code': code,
    }

    return render(request, 'admin_panel/edit_code.html', context)


@login_required
def admin_orders(request):
    '''A view to manage orders '''
    if not request.user.is_superuser:
        messages.error(request, 'You need admin rights to access this page.')
        return redirect('home')

    orders = Order.objects.all().order_by('-date')
    orders_count = orders.count()
    orders_in_progress = orders.filter(status='in_progress')
    orders_completed = orders.filter(status='completed')
    orders_cancelled = orders.filter(status='cancelled')
    context = {
        'orders': orders,
        'orders_count': orders_count,
        'orders_in_progress': orders_in_progress,
        'orders_completed': orders_completed,
        'orders_cancelled': orders_cancelled,
    }
    return render(request, 'admin_panel/admin_orders.html', context)
