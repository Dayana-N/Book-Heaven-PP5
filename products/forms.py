from django import forms

from .models import Book


class ProductForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = ('discount', 'in_stock',)
