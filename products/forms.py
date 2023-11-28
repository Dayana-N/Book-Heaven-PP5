from django import forms

from .models import Author, Book


class ProductForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = ('discount', 'in_stock',)


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = '__all__'
