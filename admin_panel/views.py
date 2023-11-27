from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from checkout.forms import OrderStatusForm
from checkout.models import Order, OrderStatus
from discount_codes.forms import DiscountCodeForm
from discount_codes.models import DiscountCode
from products.forms import ProductForm
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
    codes_total = discount_codes.count
    active_codes = DiscountCode.objects.filter(active=True)
    not_active_codes = DiscountCode.objects.filter(active=False)
    form = DiscountCodeForm()

    if request.GET:
        if 'refine' in request.GET:
            refine_value = request.GET['refine']
            orders = Order.objects.filter(orderstatus__status=refine_value)
            if refine_value == 'active':
                discount_codes = DiscountCode.objects.filter(active=True)
            elif refine_value == 'not_active':
                discount_codes = DiscountCode.objects.filter(active=False)
            else:
                discount_codes = DiscountCode.objects.all().order_by('-active')

    if request.method == 'POST':
        form = DiscountCodeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Code created successfully.')
        else:
            messages.error(request, 'Invalid form. Please try again.')

        return redirect('admin-discounts')
    context = {'discount_codes': discount_codes,
               'active_codes': active_codes,
               'not_active_codes': not_active_codes,
               'codes_total': codes_total,
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


def admin_add_product(request):
    '''A view to create products '''
    if not request.user.is_superuser:
        messages.error(request, 'You need admin rights to access this page.')
        return redirect('home')

    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('product', product.id)
        else:
            messages.error(request, 'Invalid form. Try again')
    context = {
        'form': form,
    }

    return render(request, 'admin_panel/product_form.html', context)


def admin_edit_product(request, pk):
    '''A view to edit products '''
    if not request.user.is_superuser:
        messages.error(request, 'You need admin rights to access this page.')
        return redirect('home')

    product = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('admin-panel')
        else:
            messages.error(request, 'Invalid form! Please try again.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.title}')

    context = {
        'edit': True,
        'form': form,
        'product': product,
    }
    return render(request, 'admin_panel/product_form.html', context)


def admin_delete_product(request, pk):
    '''A view to delete products '''
    if not request.user.is_superuser:
        messages.error(request, 'You need admin rights to access this page.')
        return redirect('home')

    product = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        try:
            product.delete()
            messages.success(request, f'{product.title} deleted successfully.')
        except ObjectDoesNotExist:
            messages.error(
                request, 'The product cannot be found in the database.')
        return redirect('admin-panel')

    context = {
        'product': product,
    }

    return render(request, 'admin_panel/delete_confirmation.html', context)
