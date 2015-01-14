from django.contrib import admin

from .models import Category, PropertyName


class PropertyNameInline(admin.StackedInline):
    model = PropertyName


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PropertyNameInline]