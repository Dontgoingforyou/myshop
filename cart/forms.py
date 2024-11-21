from django import forms
from config import settings
from django.utils.translation import gettext_lazy as _

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=settings.PRODUCT_QUANTITY_CHOICES, coerce=int, label=_('Количество'))
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


