from django import forms
from django.forms.models import inlineformset_factory
from django.forms import ModelForm

from product.models import Product, Photo


class ProductForm(ModelForm):
    class Meta:
        model = Product


class PhotoForm(ModelForm):
    class Meta:
        model = Photo


PhotoFormSet = inlineformset_factory(Product, Photo, form=PhotoForm)