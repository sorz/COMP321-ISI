from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction

from .forms import OrderForm
from cart.utils import Cart


@login_required
def create(request):
    cart = Cart(request.user)

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

            return HttpResponse("done.")  # TODO: redirection
    else:
        order_form = OrderForm()

    dictionary = {'cart': cart, 'order_form': order_form}
    return render(request, 'order/create.html', dictionary)
