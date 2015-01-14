from django.shortcuts import render, get_object_or_404

from .models import Product, Property


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    dictionary = {'product': product}
    return render(request, 'product/detail.html', dictionary)
