from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render, reverse

from discount_codes.models import DiscountCode
from products.models import Book


# Create your views here.
def view_cart(request):
    '''
    A view to display the shopping cart page
    '''
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    '''
    A view that handles adding items to cart
    '''
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})
    book = get_object_or_404(Book, pk=item_id)

    if book.in_stock and quantity <= book.stock_amount:
        if item_id in list(cart.keys()):
            total_quantity = int(cart[item_id]) + quantity
            if total_quantity <= book.stock_amount:
                cart[item_id] = int(cart[item_id]) + quantity
                messages.success(
                    request, f'{book.title} was successfully added to cart')
            else:
                messages.error(
                    request, 'Not enough stock to fulfil this order.')
        else:
            cart[item_id] = quantity
            messages.success(
                request, f'{book.title} was successfully added to your cart')
    else:
        messages.error(request, 'Not enough stock to fulfil this order.')
    request.session['cart'] = cart
    return redirect(redirect_url)


def update_cart(request, item_id):
    '''
    Update cart
    '''

    cart = request.session.get('cart', {})
    book = get_object_or_404(Book, pk=item_id)
    quantity = request.POST.get('quantity')

    if item_id in list(cart.keys()):
        if int(quantity) > 0 and int(book.stock_amount) >= int(quantity):
            cart[item_id] = quantity
            messages.success(
                request, f'{book.title} quantity updated successfully.')
        else:
            messages.error(request, 'Not enough stock to fulfil this order')
    else:
        messages.error(request, 'Something went wrong. Please try again.')

    request.session['cart'] = cart

    return redirect(reverse('view-cart'))


def remove_from_cart(request, item_id):
    ''' Remove item from cart'''

    cart = request.session.get('cart', {})
    book = get_object_or_404(Book, pk=item_id)
    if item_id in cart.keys():
        try:
            cart.pop(item_id)
            messages.success(request, f'{book.title} removed from cart.')
            request.session['cart'] = cart
            return redirect(reverse('view-cart'))
        except Exception as e:
            messages.error(request, f'An error occured {e}')
            return redirect(reverse('view-cart'))


def add_discount(request):
    '''
    A view that handles applying
    discount codes
    '''
    if request.method == 'POST':
        code = request.POST.get('discount-code')
        try:
            code = DiscountCode.objects.get(code__exact=code)
            if code.active:
                discount = code.discount
                request.session['discount'] = discount
                messages.success(request, 'Discount code applied successfully')
            else:
                messages.error(request, 'The code is not active')
        except ObjectDoesNotExist:
            messages.error(request, 'Invalid discount code.')
    return redirect('view-cart')


def remove_discount(request):
    '''
    A view that handles removing
    discount codes
    '''
    if 'discount' in request.session:
        try:
            del request.session['discount']
            messages.success(request, 'Discount code removed.')
        except KeyError:
            messages.error(request, 'Failed to remove discount code')
    else:
        messages.info(request, 'No discount code found')
    return redirect('view-cart')
