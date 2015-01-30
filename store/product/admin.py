from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from .models import Product, Photo


class PhotoInline(AdminImageMixin, admin.StackedInline):
    model = Photo
    extra = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    inlines = [PhotoInline]
    list_filter = ('category', )
    search_fields = ('id', 'name')