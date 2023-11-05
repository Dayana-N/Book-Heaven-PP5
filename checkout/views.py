from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import OrderForm


# Create your views here.
def checkout(request):
    ''' Renders the checkout page '''
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your shopping cart is empty')
        return redirect('all-products')

    order_form = OrderForm()

    context = {'order_form': order_form}
    return render(request, 'checkout/checkout.html', context)
