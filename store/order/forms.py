from django import forms
from django.forms import ModelForm

from .models import Order, Message


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['recipient_name', 'recipient_address',
                  'recipient_address_2', 'recipient_postcode']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea()
        }
