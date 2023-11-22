from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from products.models import Book

from .forms import ProductReviewForm
from .models import ProductReview


# Create your views here.
@login_required
def create_review(request, pk):
    ''' A view that handles creating reviews '''

    product = get_object_or_404(Book, pk=pk)
    user = request.user.userprofile
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = user
            review.save()
            messages.success(request, 'Review added successfully.')
        else:
            messages.error(
                request, 'Something went wrong. Please fill in the form again.')
    return redirect('product', pk)


@login_required
def delete_review(request, pk):
    '''A view to handle deleting reviews,
    takes request and book.id
    '''
    if request.method == 'POST':
        user = request.user.userprofile
        review_id = request.POST.get('review_id')
        review = get_object_or_404(ProductReview, id=review_id)
        if request.user.is_superuser or user == review.user:
            review.delete()
            messages.success(request, 'Review deleted successfully')
        else:
            messages.error(
                request, 'You are not allowed to delete this review')

    return redirect('product', pk=pk)
