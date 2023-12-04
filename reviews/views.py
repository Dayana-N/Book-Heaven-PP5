from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

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
                request, 'Something went wrong. Please fill in the form again.'
            )
    return redirect('product', pk)


@login_required
def delete_review(request, pk):
    '''A view to handle deleting reviews,
    takes request and review id
    '''
    review = get_object_or_404(ProductReview, pk=pk)
    book = review.product

    if request.method == 'POST':
        user = request.user.userprofile
        if request.user.is_superuser or user == review.user:
            try:
                review.delete()
                messages.success(request, 'Review deleted successfully.')
            except ObjectDoesNotExist:
                messages.error(
                    request, 'This review cannot be found in the database.')
            return redirect('product', book.id)

    context = {
        'review': review,
        'book': book,
    }

    return render(request, 'reviews/delete_review.html', context)


@login_required
def edit_review(request, pk):
    ''' A view to handle edit review,
    it takes request and review id '''
    review = get_object_or_404(ProductReview, pk=pk)
    book = review.product
    form = ProductReviewForm(instance=review)

    if request.method == 'POST':
        user = request.user.userprofile
        if request.user.is_superuser or user == review.user:
            form = ProductReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save()
                messages.success(request, 'Review updated successfully')
                return redirect('product', book.id)
            messages.error(
                request, 'Something went wrong. Please try again.')
        else:
            messages.error(
                request, 'You are not allowed to edit this review')

    context = {'review_form': form,
               'review': review,
               'book': book}
    return render(request, 'reviews/edit_review.html', context)
