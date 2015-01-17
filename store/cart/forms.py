from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from .models import CartItem


_quantity_input = forms.NumberInput(attrs={'min': 1, 'step': 1, 'autocomplete': 'off'})
CartItemFormSet = inlineformset_factory(User, CartItem, extra=0,
                                        fields=('id', 'quantity',),
                                        widgets=({'quantity': _quantity_input}))