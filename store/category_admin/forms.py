from django.forms import ModelForm

from category.models import Category


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
