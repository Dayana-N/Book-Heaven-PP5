from django import forms

from .models import DiscountCode


class DiscountCodeForm(forms.ModelForm):
    class Meta:
        model = DiscountCode
        fields = '__all__'
