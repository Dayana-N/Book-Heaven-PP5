from django import forms

from .models import Author, Book
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = ('discount', 'in_stock',)

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput)


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = '__all__'
