from django.forms import ModelForm

from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['recipient_name', 'recipient_address',
                  'recipient_address_2', 'recipient_postcode']
