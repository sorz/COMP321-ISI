from django.forms.models import inlineformset_factory
from django.forms import ModelForm

from product.models import Product, Photo


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['sale_quantity', 'sale_amount', 'in_stock', 'off_shelf']


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'description']


PhotoFormSet = inlineformset_factory(Product, Photo, form=PhotoForm)