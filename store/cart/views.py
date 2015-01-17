from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.core.urlresolvers import reverse

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
            return HttpResponseRedirect(reverse('order:create'))
    else:
        formset = CartItemFormSet(instance=cart.user)

    dictionary = {'cart': cart, 'item_formset': formset}
    return render(request, 'cart/index.html', dictionary)


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


@login_required
def rest_item(request, product_id):
    cart = Cart(request.user)
    product = get_object_or_404(Product, pk=product_id)

    # Set the quantity of items.
    if request.method == 'PUT':
        quantity = request.POST.get('quantity', 1)
        _, created = cart.item_set.get_or_create(product=product,
                                                 defaults={'quantity': quantity})
        if created:
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=204)

    # Add some items.
    elif request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        cart.add_item(product, quantity)
        return HttpResponse(status=204)

    # Delete a item.
    elif request.method == 'DELETE':
        item = get_object_or_404(cart.item_set, product=product)
        item.delete()
        return HttpResponse(status=204)

    else:
        return HttpResponseNotAllowed(['PUT', 'POST', 'DELETE'])
