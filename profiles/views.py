from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from checkout.models import Order

from .forms import UserProfileForm
from .models import UserProfile


# Create your views here.
@login_required
def profile_page(request, pk):
    ''' Displays the user profile '''

    profile = get_object_or_404(UserProfile, id=pk)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'profiles/profile.html', context)


def my_wishlist(request, pk):
    ''' Renders wishlist page '''
    context = {

    }
    return render(request, 'profiles/wishlist.html', context)


def my_orders(request, pk):
    ''' Renders my orders page '''
    profile = get_object_or_404(UserProfile, id=pk)
    orders = profile.orders.all()
    context = {
        'orders': orders,
    }
    return render(request, 'profiles/my_orders.html', context)


def order_history(request, pk):
    ''' Renders order history page '''
    order = get_object_or_404(Order, id=pk)

    context = {
        'order': order,
        'order_history': True,
    }
    return render(request, 'checkout/checkout-success.html', context)
