from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import transaction

from .forms import OrderForm
from cart.utils import Cart


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

    # TODO: Check out-of-stack & off-shelf status, non-item.

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():

            # To improve database performance and keep integrity.
            with transaction.atomic():
                order = order_form.save(commit=False)
                order.owner = request.user
                order.save()
                cart.checkout(order)
                cart.item_set.all().delete()

            # Remove the hash since its mission is completed.
            request.session.delete('cart-hash')

            return HttpResponse("done.")  # TODO: redirection
    else:
        order_form = OrderForm()

    dictionary = {'cart': cart, 'order_form': order_form}
    return render(request, 'order/create.html', dictionary)
