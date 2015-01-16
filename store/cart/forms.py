from django import forms
from django.forms.models import inlineformset_factory

from .models import Cart, CartItem


_quantity_input = forms.NumberInput(attrs={'min': 1, 'step': 1, 'autocomplete': 'off'})
CartItemFormSet = inlineformset_factory(Cart, CartItem, extra=0,
                                        fields=('quantity',),
                                        widgets=({'quantity': _quantity_input}))