from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed

from .utils import get_or_create_cart
from .models import Product
from .forms import CartItemFormSet


@login_required
def index(request):
    cart = get_or_create_cart(request)

    formset_data = []
    for item in cart.cartitem_set.all():
        formset_data.append({
            "item": item.pk,
            "quantity": item.quantity,
        })
    item_formset = CartItemFormSet(initial=formset_data)

    dictionary = {'cart': cart, 'item_formset': item_formset}
    return render(request, 'cart/index.html', dictionary)


@login_required
def rest_cart(request):
    cart = get_or_create_cart(request)

    # Return all items.
    if request.method == 'GET':
        response = {'items': []}
        for item in cart.cartitem_set.all():
            response['items'].append({
                'name': item.name,
                'price': item.price,
                'quantity': item.quantity
            })
        return JsonResponse(response)

    # Delete all items on cart.
    elif request.method == 'DELETE':
        cart.cartitem_set.all.delete()
        return HttpResponse(status=204)

    else:
        return HttpResponseNotAllowed(['GET', 'DELETE'])


@login_required
def rest_item(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=product_id)

    # Set the quantity of items.
    if request.method == 'PUT':
        quantity = request.POST.get('quantity', 1)
        _, created = cart.cartitem_set.get_or_create(product=product,
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
        item = get_object_or_404(cart.cartitem_set, product=product)
        item.delete()
        return HttpResponse(status=204)

    else:
        return HttpResponseNotAllowed(['PUT', 'POST', 'DELETE'])
