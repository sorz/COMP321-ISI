from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseForbidden, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.db import transaction
from django.views.generic import TemplateView, FormView
from rest_framework.views import APIView

from .forms import OrderForm, MessageForm
from .models import Order, InvalidOrderStatusChangeException
from account.models import Profile
from cart.utils import Cart, CannotCheckoutItemException
from store.utils import make_page


@login_required
def create(request):
    cart = Cart(request.user)

    # Check hash to ensure the cart (order) is consistent between
    # database and user's expected.
    # If it's modified in other page, redirect user to cart view to checkout again.
    cart_hash = request.GET.get('hash')
    if cart_hash is None or cart_hash != str(hash(cart)):
        messages.add_message(request, messages.WARNING,
                             "Some items have been changed, "
                             "please be prudential and checkout again.")
        return redirect('cart:index')

    # Empty cart, return.
    if not cart.item_set.all().exists():
        return redirect('cart:index')

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():

            order = order_form.save(commit=False)
            order.owner = request.user
            try:

                # We use transaction to improve database performance and keep integrity.
                # Checkout action will rollback if any product cannot be checked out.
                with transaction.atomic():
                    order.save()
                    cart.checkout(order)
                    cart.item_set.all().delete()

            except CannotCheckoutItemException:
                # Some items are off-shelf,
                # cart.checkout() will throw this exception in the case.
                # Redirect user back to cart view.
                messages.add_message(request, messages.WARNING,
                                     "Some products are off-shelf, "
                                     "please delete them and checkout again.")
                return HttpResponseRedirect(reverse('cart:index'))

            # Remove the hash since its mission is completed.
            request.session.delete('cart-hash')
            messages.add_message(request, messages.SUCCESS,
                                 "Congratulation. Your order will be handled sooner if possible.")
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


class BaseOrderListView(TemplateView):
    """Show a list of certain orders.

    Used by order list for both customer and vendor, report for vendor.
    """
    template_name = 'order/list.html'
    title = 'All Purchase Orders'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['current_app'] = self.request.resolver_match.namespace
        return super().render_to_response(context, **response_kwargs)

    def get_queryset(self):
        """Return the queryset of orders. Need to be override."""
        return Order.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = make_page(self.get_queryset(),
                                      self.request.GET.get('page'))
        context['title'] = self.title
        return context


class _LoginRequiredOrderListView(BaseOrderListView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CurrentView(_LoginRequiredOrderListView):
    title = 'Current Purchase'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user,
                                             status__in=['P', 'S', 'H'])


class PastView(_LoginRequiredOrderListView):
    title = 'Past Purchase'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user,
                                             status__in=['R', 'C'])


class BaseOrderDetailView(FormView):
    form_class = MessageForm
    template_name = 'order/detail.html'
    title = 'Purchase detail'
    success_url = '.'
    vendor = False
    order = None

    def dispatch(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, pk=kwargs['order_id'])

        # Only vendor or owner of this order can view or add message.
        if not self.vendor and self.order.owner != request.user:
            return HttpResponseForbidden('This order can only be viewed by the vendor or owner.')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        message = form.save(commit=False)
        message.order = self.order
        message.by_vendor = self.vendor
        message.save()

        messages.add_message(self.request, messages.SUCCESS,
                             "Message has been added.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        context['order_messages'] = self.order.message_set.all()
        context['vendor'] = self.vendor
        context['title'] = self.title
        return context


class DetailView(BaseOrderDetailView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@login_required
def done(request, order_id):
    """Shown after order is confirmed by customer."""
    order = get_object_or_404(Order, pk=order_id)

    if order.status != 'R':
        return HttpResponseRedirect(reverse('order:detail', args=[order_id]))

    dictionary = {'order': order}
    return render(request, 'order/done.html', dictionary)


class OrderView(APIView):
    def put(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        if not request.user.is_authenticated():
            return HttpResponseForbidden('No login.')

        vendor = request.user.is_staff
        if request.user != order.owner and not vendor:
            return HttpResponseForbidden('Permission denied to access this order.')

        new_status = request.data.get('status')
        if new_status is None:
            return HttpResponseBadRequest('Lack argument "status".')

        # If it has already been this status, just return ok.
        if order.status == new_status:
            return HttpResponse(status=204)

        try:
            # Cancel this order.
            if new_status == 'C':
                order.cancel(operator=request.user)

            # Confirm Received, only customer.
            elif new_status == 'R':
                if vendor and request.user != order.owner:
                    return HttpResponseForbidden('Only customer can do it.')
                order.confirm()

            # Hold this order, only vendor.
            elif new_status == 'H':
                if not vendor:
                    return HttpResponseForbidden('Only vendor can do it.')
                order.hold()

            # Ship this order, only vendor.
            elif new_status == 'S':
                if not vendor:
                    return HttpResponseForbidden('Only vendor can do it.')
                order.ship()

        except InvalidOrderStatusChangeException:
            return HttpResponseForbidden('Wrong status.')

        return HttpResponse(status=204)
