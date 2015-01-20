from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction

from .forms import OrderForm, MessageForm
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


def _orders(request, statuses, title):
    """Return a list page including orders with specified statuses.

    Used for current purchase page and past purchase page.
    """
    orders = Order.objects.filter(owner=request.user,
                                  status__in=statuses)

    paginator = Paginator(orders, 3)  # 3 orders per page for testing.
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page.
        orders = paginator.page(paginator.num_pages)

    dictionary = {'orders': orders, 'title': title}
    return render(request, 'order/list.html', dictionary)


@login_required
def current(request):
    return _orders(request, ['P', 'S', 'H'], 'Current Purchase')


@login_required
def past(request):
    return _orders(request, ['R', 'C'], 'Past Purchase')


@login_required
def detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if order.owner != request.user:
        return HttpResponseForbidden('You cannot view this order.')

    # TODO: Reverse chronological order (D4)
    messages = order.message_set.all()

    if request.method == 'POST':
        message_form = MessageForm(request.POST)

        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.order = order
            message.writer = request.user
            message.save()

            # TODO: Show a "success" message to user.
            # Refresh page to prevent duplicate submission
            return HttpResponseRedirect('.')

    else:
        message_form = MessageForm()

    dictionary = {'order': order, 'messages': messages,
                  'message_form': message_form}
    return render(request, 'order/detail.html', dictionary)


@login_required
def rest_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if order.owner != request.user:
        return HttpResponseForbidden('You cannot access this order.')

    # Cancel the order by user.
    if request.method == 'DELETE':

        # Only allowed in pending or holding state.
        if order.status not in ['P', 'H']:
            return HttpResponseForbidden('Cannot cancel this order.')

        order.cancel(operator=request.user)
        return HttpResponse(status=204)
