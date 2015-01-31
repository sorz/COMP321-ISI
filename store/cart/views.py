from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.core.urlresolvers import reverse
from rest_framework.views import APIView

from .utils import Cart
from .models import Product
from .forms import CartItemFormSet


@login_required
def index(request):
    cart = Cart(request.user)

    if request.method == 'POST':
        formset = CartItemFormSet(request.POST, instance=cart.user)
        if formset.is_valid():
            formset.save()

            # If cart isn't empty, redirect user to order page.
            if cart.item_set.all():

                # Before redirecting, we save the hash of cart i.
                # So when user confirm order in few minutes,
                # we can check and ensure it's not been changed.
                request.session['cart-hash'] = hash(cart)

                return HttpResponseRedirect(reverse('order:create'))

            else:
                # Cart is empty, just reload this page where "empty" should be shown.
                return HttpResponseRedirect('.')
    else:
        formset = CartItemFormSet(instance=cart.user)

    dictionary = {'cart': cart, 'item_formset': formset}
    return render(request, 'cart/index.html', dictionary)


# TODO: Refactor it by using REST framework, or delete it.
@login_required
def rest_cart(request):
    cart = Cart(request.user)

    # Return all items.
    if request.method == 'GET':
        response = {'items': []}
        for item in cart.item_set.all():
            response['items'].append({
                'name': item.name,
                'price': item.price,
                'quantity': item.quantity
            })
        return JsonResponse(response)

    # Delete all items on cart.
    elif request.method == 'DELETE':
        cart.item_set.all.delete()
        return HttpResponse(status=204)

    else:
        return HttpResponseNotAllowed(['GET', 'DELETE'])


class ItemView(APIView):
    @method_decorator(login_required)
    def put(self, request, product_id):
        """Set the quantity of item."""
        cart = Cart(request.user)
        product = get_object_or_404(Product, pk=product_id)

        quantity = int(request.data.get('quantity', 1))
        created = cart.set_item(product, quantity)

        if created:
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=204)

    @method_decorator(login_required)
    def post(self, request, product_id):
        """Add some items."""
        cart = Cart(request.user)
        product = get_object_or_404(Product, pk=product_id)

        quantity = int(request.data.get('quantity', 1))
        cart.add_item(product, quantity)
        return HttpResponse(status=204)

    @method_decorator(login_required)
    def delete(self, request, product_id):
        """Delete a item."""
        cart = Cart(request.user)
        product = get_object_or_404(Product, pk=product_id)

        cart.remove(product)
        return HttpResponse(status=204)
