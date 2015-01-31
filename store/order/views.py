from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseForbidden, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from rest_framework.views import APIView

from .forms import OrderForm, MessageForm
from .models import Order, InvalidOrderStatusChangeException
from account.models import Profile
from cart.utils import Cart, CannotCheckoutItemException


@login_required
def create(request):
    cart = Cart(request.user)

    # Check hash to ensure the cart (order) is consistent between
    # database and user's expected.
    # If it's modified in other page, redirect user to cart view to checkout again.
    cart_hash = request.GET.get('hash')
    if cart_hash is None or cart_hash != str(hash(cart)):
        # TODO: Show a message to tell user what happen.
        return redirect('cart:index')

    # Empty cart, return.
    if not cart.item_set.all().exists():
        return redirect('cart:index')

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():

            # We use transaction to improve database performance and keep integrity.
            # Checkout action will rollback if any product cannot be checked out.
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
            # TODO: Show success message to user.
            return redirect('order:detail', order.pk)
    else:
        initial = {'recipient_name': request.user.get_full_name()}
        try:
            initial['recipient_address'] = request.user.profile.address
            initial['recipient_address_2'] = request.user.profile.address_2
            initial['recipient_postcode'] = request.user.profile.postcode
        except Profile.DoesNotExist:
            pass

        order_form = OrderForm(initial=initial)

    dictionary = {'cart': cart, 'order_form': order_form,
                  'cart_hash': cart_hash}
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
    """Order detail page. Also handle message posting."""
    order = get_object_or_404(Order, pk=order_id)

    # Only owner of this order can view or add message.
    if order.owner != request.user:
        return HttpResponseForbidden('You cannot view this order.')

    # TODO: Reverse chronological order (D4)
    messages = order.message_set.all()

    if request.method == 'POST':
        message_form = MessageForm(request.POST)

        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.order = order
            message.by_vendor = False
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
def done(request, order_id):
    """Shown after order is confirmed by customer."""
    order = get_object_or_404(Order, pk=order_id)

    if order.status != 'R':
        return HttpResponseRedirect(reverse('order:detail', args=[order_id]))

    dictionary = {'order': order}
    return render(request, 'order/done.html', dictionary)


class OrderView(APIView):
    @method_decorator(login_required)
    def put(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        if order.owner != request.user:
            return HttpResponseForbidden('You cannot access this order.')

        new_status = request.data.get('status')
        if new_status is None:
            return HttpResponseBadRequest('Lack argument "status".')

        # If it has already been this status, just return ok.
        if order.status == new_status:
            return HttpResponse(status=204)

        # Cancel this order.
        if new_status == 'C':
            try:
                print('cancel')
                order.cancel(operator=request.user)
            except InvalidOrderStatusChangeException:
                return HttpResponseForbidden('Cannot cancel this order.')

        # Confirm Received.
        elif new_status == 'R':
            try:
                order.confirm()
            except InvalidOrderStatusChangeException:
                return HttpResponseForbidden('Cannot confirm this order.')

        return HttpResponse(status=204)
