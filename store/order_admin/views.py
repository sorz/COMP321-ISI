from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from admin.decorators import vendor_required

from order.views import BaseOrderListView, BaseOrderDetailView


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
        try:
            if start:
                orders = orders.filter(purchase_date__gt=start)
            if end:
                orders = orders.filter(purchase_date__lt=end)
        except ValidationError:
            pass  # TODO: show a error message to user.
        return orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start'] = self.request.GET.get('start')
        context['end'] = self.request.GET.get('end')
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

    def get_queryset(self):
        return super().get_queryset().filter(status='C')


class CancelledView(_ReportListView):
    template_name = 'order_admin/list.html'

    def get_queryset(self):
        return super().get_queryset().filter(status='R')


class DetailView(BaseOrderDetailView):
    template_name = 'order_admin/detail.html'
    vendor = True

    @method_decorator(vendor_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
