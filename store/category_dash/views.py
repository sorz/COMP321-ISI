from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator

from category.models import Category
from category.views import IndexView, DetailView
from dashboard.decorators import vendor_required


class VendorIndexView(IndexView):
    @method_decorator(vendor_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class VendorDetailView(DetailView):
    @method_decorator(vendor_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# TODO: add/delete/modify categories.
