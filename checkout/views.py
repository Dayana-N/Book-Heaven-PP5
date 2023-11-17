import json

import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cart.contexts import cart_contents
from products.models import Book
from profiles.forms import UserProfileForm
from profiles.models import UserProfile

from .forms import OrderForm
from .models import Order, OrderLineItem


# Create your views here.
@require_POST
def cache_checkout_data(request):
    '''
    Handles the modification of Stripe PaymentIntent
    with cart data and user information.
    '''
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


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
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()

            for item_id, item_quantity in cart.items():
                try:
                    book = Book.objects.get(id=item_id)
                    if book.stock_amount > 0:
                        book.stock_amount -= int(item_quantity)
                        book.save()
                    else:
                        messages.error(
                            request, f'{book.title} is out of stock. Please remove this item and try again.')
                        return redirect('view-cart')

                    order_line_item = OrderLineItem(
                        order=order,
                        product=book,
                        quantity=int(item_quantity),
                    )
                    order_line_item.save()

                except Book.DoesNotExist:
                    messages.error(
                        request, 'Unknown item in shopping cart. Please try again later.')
                    order.delete()
                    return redirect('view-cart')

            request.session['save_info'] = 'save-info' in request.POST
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

        # Attempt to prefill the form with any info the user maintains in their profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
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
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()
    messages.success(request, 'Your order has been placed.')

    if 'cart' in request.session:
        del request.session['cart']

    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout-success.html', context)
