from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import transaction

from .forms import OrderForm
from .models import Order
from cart.utils import Cart, CannotCheckoutItemException


@login_required
def create(request):
    cart = Cart(request.user)

    # Check hash to ensure the cart (order) has not been modified
    # since user click checkout button on shopping cart view.
    # If it has been modified, redirect user to cart view to checkout again.
    cart_hash = request.session.get('cart-hash')
    if cart_hash is None or cart_hash != hash(cart):
        # TODO: Show a message to tell user what happen.
        request.session.delete('cart-hash')
        return HttpResponseRedirect(reverse('cart:index'))

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():

            # To improve database performance and keep integrity.
            with transaction.atomic():
                order = order_form.save(commit=False)
                order.owner = request.user
                order.save()

                try:
                    cart.checkout(order)
                except CannotCheckoutItemException:

                    # Some items are out-of-stock or off-shelf,
                    # abort operation and redirect user back to cart view.
                    # TODO: Show a message to tell user what happen.
                    transaction.abort()
                    return HttpResponseRedirect(reverse('cart:index'))

                cart.item_set.all().delete()

            # Remove the hash since its mission is completed.
            request.session.delete('cart-hash')
            return HttpResponse("done.")  # TODO: redirection
    else:
        order_form = OrderForm()

    dictionary = {'cart': cart, 'order_form': order_form}
    return render(request, 'order/create.html', dictionary)


@login_required
def index(request):
    dictionary = {'user': request.user}
    return render(request, 'order/index.html', dictionary)


@login_required
def current(request):
    orders = Order.objects.filter(owner=request.user,
                                  status__in=['P', 'S', 'H'])

    dictionary = {'orders': orders, 'title': 'Current Purchase'}
    return render(request, 'order/list.html', dictionary)


@login_required
def past(request):
    orders = Order.objects.filter(owner=request.user,
                                  status__in=['R', 'C'])

    dictionary = {'orders': orders, 'title': 'Past Purchase'}
    return render(request, 'order/list.html', dictionary)

@login_required
def detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    dictionary = {'order': order}
    return render(request, 'order/detail.html', dictionary)
