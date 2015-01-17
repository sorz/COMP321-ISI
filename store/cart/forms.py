from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from .models import CartItem


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1, 'step': 1,
                                                 'autocomplete': 'off'})
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError('Quantity must be larger than 0.',
                                        code="invalid-quantity")
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        item = cleaned_data.get('id')

        # When it's off-shelf, the out-of-stock state dose not matter.
        # So we check off-shelf state first, and only raise it.
        if item.off_shelf:
            raise forms.ValidationError('This product is off shelf, '
                                        'please remove it and try again.',
                                        code='off-shelf')
        elif not item.in_stock:
            raise forms.ValidationError('This product is sold out, '
                                        'please remove it and try again.',
                                        code='out-of-stock')
        return cleaned_data

CartItemFormSet = inlineformset_factory(User, CartItem,
                                        form=CartItemForm, extra=0)