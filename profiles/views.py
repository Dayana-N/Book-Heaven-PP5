from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from checkout.models import Order
from products.models import Book

from .forms import UserProfileForm
from .models import UserProfile, Wishlist


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


@login_required
def my_wishlist(request, pk):
    ''' Renders wishlist page '''
    profile = get_object_or_404(UserProfile, id=pk)
    wishlist = Wishlist.objects.filter(user=profile).order_by('-created')
    context = {
        'wishlist': wishlist,
    }
    return render(request, 'profiles/wishlist.html', context)


@login_required
def wishlist_add(request, pk):
    ''' Adds products to favourites, Takes request and product id as pk '''
    profile = request.user.userprofile
    product = get_object_or_404(Book, pk=pk)
    redirect_url = request.POST.get('redirect_url')

    wishlist, created = Wishlist.objects.get_or_create(
        user=profile, product=product)
    if created:
        messages.success(request, f'{product.title} added to your wishlist')
    else:
        wishlist.delete()
        messages.success(
            request, f'{product.title} removed from your wishlist')

    return redirect(redirect_url)


@login_required
def my_orders(request, pk):
    ''' Renders my orders page '''
    profile = get_object_or_404(UserProfile, id=pk)
    orders = profile.orders.all().order_by('-date')
    context = {
        'orders': orders,
    }
    return render(request, 'profiles/my_orders.html', context)


@login_required
def order_history(request, pk):
    ''' Renders order history page '''
    order = get_object_or_404(Order, id=pk)

    context = {
        'order': order,
        'order_history': True,
    }
    return render(request, 'checkout/checkout-success.html', context)
