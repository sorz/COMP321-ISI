from django import forms
from django.forms.formsets import formset_factory


from .models import CartItem


class CartItemForm(forms.Form):
    # Stores (the pk of) model instance.
    # http://stackoverflow.com/questions/4686858/django-forms-hidden-model-field
    item = forms.CharField(widget=forms.HiddenInput())

    quantity = forms.DecimalField(min_value=1, decimal_places=0)

    @property
    def item_instance(self):
        print(self.item)
        item = CartItem.objects.get(pk=self.item)
        print(item.name)
        return item

    def clean_item(self):
        """Return the CartItem instance."""
        data = self.cleaned_data['item']
        if not data:
            raise forms.ValidationError('Lack argument "item".')
        try:
            item = CartItem.objects.get(pk=data)
        except CartItem.DoesNotExist:
            raise forms.ValidationError('CharItem (id=%s) not existed.' % data)
        return item

CartItemFormSet = formset_factory(CartItemForm, extra=0, can_delete=True)