from django.contrib import messages
from django.shortcuts import get_object_or_404

from products.models import Book


def cart_contents(request):
    '''
    Handles the shopping cart contents
    '''
    delivery_threshold = 50
    delivery_fee = 12
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})
    items_to_remove = []

    for item_id, quantity in cart.items():
        book = get_object_or_404(Book, pk=item_id)
        # remove items that are out of stock
        if book.in_stock is False:
            items_to_remove.append(item_id)

        total += book.product_price * int(quantity)
        product_count += int(quantity)
        cart_items.append({
            'item_id': item_id,
            'quantity': int(quantity),
            'book': book,
        })

    for item_id in items_to_remove:
        cart.pop(item_id)
        messages.error(
            request, f'{book.title} is out of stock and has been removed from your cart.')

    request.session['cart'] = cart

    if total > delivery_threshold or total == 0:
        delivery_fee = 0
        free_delivery_delta = 0
    else:
        free_delivery_delta = delivery_threshold - total

    grand_total = total + delivery_fee
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery_fee': delivery_fee,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': delivery_threshold,
        'grand_total': grand_total,
    }
    return context
