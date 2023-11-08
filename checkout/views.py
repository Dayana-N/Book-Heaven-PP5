import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from cart.contexts import cart_contents
from products.models import Book

from .forms import OrderForm
from .models import Order, OrderLineItem


# Create your views here.
def checkout(request):
    ''' Renders the checkout page '''
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()

            for item_id, item_quantity in cart.items():
                try:
                    book = Book.objects.get(id=item_id)
                    if book.stock_amount > 0:
                        book.stock_amount -= item_quantity
                        book.save()
                    else:
                        messages.error(
                            request, f'{book.title} is out of stock. Please remove this item and try again.')
                        return redirect('view-cart')

                    order_line_item = OrderLineItem(
                        order=order,
                        product=book,
                        quantity=item_quantity,
                    )
                    order_line_item.save()

                except Book.DoesNotExist:
                    messages.error(
                        request, 'Unknown item in shopping cart. Please try again later.')
                    order.delete()
                    return redirect('view-cart')
            return redirect('checkout-success', order.order_number)
        else:
            messages.error(
                request, 'There was an error with this form. Please enter valid information.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, 'Your shopping cart is empty')
            return redirect('all-products')

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing.')

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    ''' Renders checkout success page '''
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, 'Your order has been placed.')

    if 'cart' in request.session:
        del request.session['cart']

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout-success.html', context)
