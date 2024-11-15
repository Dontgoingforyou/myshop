from django import forms
from config import settings


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=settings.PRODUCT_QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


