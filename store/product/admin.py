from django.contrib import admin

from product.models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)