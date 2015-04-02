from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from rest_framework.views import APIView

from .utils import Cart
from .models import Product


@login_required
def index(request):
    cart = Cart(request.user)
    items = cart.item_set.all()

    dictionary = {'cart': cart, 'items': items, 'cart_hash': hash(cart)}
    return render(request, 'cart/index.html', dictionary)


class ItemView(APIView):
    @method_decorator(login_required)
    def put(self, request, product_id):
        """Set the quantity of item."""
        cart = Cart(request.user)
        product = get_object_or_404(Product, pk=product_id)

        quantity = int(request.data.get('quantity', 1))
        cart.set_item(product, quantity)
        return JsonResponse({'cartHash': hash(cart)})

    @method_decorator(login_required)
    def post(self, request, product_id):
        """Add some items."""
        cart = Cart(request.user)
        product = get_object_or_404(Product, pk=product_id)

        quantity = int(request.data.get('quantity', 1))
        cart.add_item(product, quantity)
        return JsonResponse({'cartHash': hash(cart)})

    @method_decorator(login_required)
    def delete(self, request, product_id):
        """Delete a item."""
        cart = Cart(request.user)
        product = get_object_or_404(Product, pk=product_id)

        cart.remove(product)
        return JsonResponse({'cartHash': hash(cart)})
