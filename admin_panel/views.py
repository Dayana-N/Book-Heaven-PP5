from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from checkout.forms import OrderStatusForm
from checkout.models import Order, OrderStatus
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

    orders = Order.objects.all()
    products = Book.objects.all()
    total_product_count = products.count()
    total_grand_total = Order.objects.aggregate(
        total_grand_total=Sum('grand_total'))
    grand_total_sum = total_grand_total['total_grand_total']

    if request.GET:
        if 'refine' in request.GET:
            refine_value = request.GET['refine']
            if refine_value == 'low_stock':
                products = Book.objects.filter(
                    stock_amount__gt=0, stock_amount__lte=5)
            elif refine_value == 'out_of_stock':
                products = Book.objects.filter(stock_amount=0)
            elif refine_value == 'in_stock':
                products = Book.objects.filter(stock_amount__gt=5)
            else:
                products = Book.objects.all().order_by('-created')

    context = {
        'orders': orders,
        'products': products,
        'total': grand_total_sum,
        'total_product_count': total_product_count, }
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
    '''A view to render and refine orders '''
    if not request.user.is_superuser:
        messages.error(request, 'You need admin rights to access this page.')
        return redirect('home')

    refine_value = None
    orders = Order.objects.all().order_by('-date')

    if request.GET:
        if 'refine' in request.GET:
            refine_value = request.GET['refine']
            orders = Order.objects.filter(orderstatus__status=refine_value)
            if refine_value == 'recent':
                orders = Order.objects.all().order_by('-date')

    orders_in_progress = Order.objects.filter(
        orderstatus__status='in_progress')
    orders_completed = Order.objects.filter(orderstatus__status='completed')
    orders_cancelled = Order.objects.filter(orderstatus__status='cancelled')

    context = {
        'orders': orders,
        'orders_in_progress': orders_in_progress,
        'orders_completed': orders_completed,
        'orders_cancelled': orders_cancelled,
        'current_sorting': refine_value,

    }
    return render(request, 'admin_panel/admin_orders.html', context)


@login_required
def admin_orders_edit(request, pk):
    '''A view to edit orders address and status '''
    if not request.user.is_superuser:
        messages.error(request, 'You need admin rights to access this page.')
        return redirect('home')

    order = get_object_or_404(Order, pk=pk)
    order_status = get_object_or_404(OrderStatus, order=order)
    form = OrderStatusForm(instance=order_status)

    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order_status)
        if form.is_valid():
            form.save()
            messages.success(request, 'Status updated successfully')
        else:
            messages.error(request, 'Invalid form. Try again')
        return redirect('admin-orders')

    context = {
        'order': order,
        'order_form': form,
    }

    return render(request, 'admin_panel/edit_order.html', context)
