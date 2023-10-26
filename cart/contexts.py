from decimal import Decimal


def cart_contents(request):
    '''
    Handles the shopping cart contents
    '''
    delivery_threshold = 50
    delivery_fee = 12

    bag_items = []
    total = 0
    product_count = 0

    if total < delivery_threshold:
        free_delivery_delta = delivery_threshold - total
    else:
        delivery_fee = 0
        free_delivery_delta = 0

    grand_total = total + delivery_fee
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery_fee': delivery_fee,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': delivery_threshold,
        'grand_total': grand_total,
    }
    return context
