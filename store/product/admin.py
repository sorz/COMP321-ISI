from django.contrib import admin

from .models import Product, Property, Photo


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 2


class PropertyInLine(admin.TabularInline):
    model = Property


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    inlines = [PhotoInline, PropertyInLine]
    list_filter = ('category', )
    search_fields = ('id', 'name')