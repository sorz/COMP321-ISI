from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from admin.decorators import vendor_required

from order.views import BaseOrderListView, BaseOrderDetailView

from time import strptime
from django.contrib import messages


class _VendorOrderListView(BaseOrderListView):
    """Common view used by pending and on-delivery order list."""
    template_name = 'order_admin/list.html'

    @method_decorator(vendor_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class _ReportListView(_VendorOrderListView):
    """Common view used by fulfilled, cancelled and best-selling report."""

    def get_queryset(self):
        orders = super().get_queryset()
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')

        if start:
            try:
                orders = orders.filter(purchase_date__gt=start)
            except ValidationError:
                pass  # Error handling is in get_context_data().
        if end:
            try:
                orders = orders.filter(purchase_date__lt="%s 23:59:59.99" % end)
            except ValidationError:
                pass
        return orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start'] = self.request.GET.get('start', '')
        context['end'] = self.request.GET.get('end', '')

        # Validate date format
        start_date = end_date = None
        if context['start']:
            try:
                start_date = strptime(context['start'], "%Y-%m-%d")
            except ValueError:
                context['start_has_error'] = 'has-error'
        if context['end']:
            try:
                end_date = strptime(context['end'], "%Y-%m-%d")
            except ValueError:
                context['end_has_error'] = 'has-error'

        if 'start_has_error' in context or 'end_has_error' in context:
            messages.add_message(self.request, messages.WARNING,
                                 "Incorrect date format. "
                                 "Please select appropriate dates.")
        if start_date and end_date and end_date < start_date:
            context['start_has_error'] = context['end_has_error'] = 'has-error'
            messages.add_message(self.request, messages.WARNING,
                                 "End date should be later than start date. "
                                 "Please select appropriate dates.")
        return context


class PendingView(_VendorOrderListView):
    title = 'Pending Orders'

    def get_queryset(self):
        return super().get_queryset().filter(status__in=['P', 'H'])


class OnDeliveryView(_VendorOrderListView):
    title = 'On-delivery Orders'

    def get_queryset(self):
        return super().get_queryset().filter(status='S')


class FulfilledView(_ReportListView):
    template_name = 'order_admin/report_fulfilled.html'
    title = "Fulfilled Order Report"

    def get_queryset(self):
        return super().get_queryset().filter(status='R')


class CancelledView(_ReportListView):
    template_name = 'order_admin/report_cancelled.html'
    title = "Cancelled Order Report"

    def get_queryset(self):
        return super().get_queryset().filter(status='C')


class DetailView(BaseOrderDetailView):
    template_name = 'order_admin/detail.html'
    vendor = True

    @method_decorator(vendor_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
