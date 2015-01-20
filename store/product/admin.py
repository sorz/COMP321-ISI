from django.contrib import admin

from .models import Product, Photo


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    inlines = [PhotoInline]
    list_filter = ('category', )
    search_fields = ('id', 'name')