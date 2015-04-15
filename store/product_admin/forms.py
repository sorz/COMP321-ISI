from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from sorl.thumbnail.admin.current import AdminImageWidget

from product.models import Product, Photo


PRODUCT_STATUS = (
    ('NORMAL', 'In stock'),
    ('OUT-OFF-STOCK', 'Out of stock'),
    ('OFF-SHELF', 'Off shelf')
)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['sale_quantity', 'sale_amount', 'in_stock', 'off_shelf']


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'description']
        widgets = {'image': AdminImageWidget}


PhotoFormSet = inlineformset_factory(Product, Photo, form=PhotoForm)
