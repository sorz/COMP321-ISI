from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Product


@ensure_csrf_cookie
def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    dictionary = {'product': product, 'user': request.user}
    if product.off_shelf:
        return render(request, 'product/off-shelf.html', dictionary, status=404)
    else:
        return render(request, 'product/detail.html', dictionary)
