from django.utils.decorators import method_decorator
from admin.decorators import vendor_required

from order.views import OrderListView


class _VendorRequiredOrderListView(OrderListView):
    @method_decorator(vendor_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PendingView(_VendorRequiredOrderListView):
    title = 'Pending Orders'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user,
                                             status='P')


class OnDeliveryView(_VendorRequiredOrderListView):
    title = 'On-delivery Orders'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user,
                                             status='S')
