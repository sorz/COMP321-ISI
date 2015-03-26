from django.utils.decorators import method_decorator
from admin.decorators import vendor_required

from order.views import BaseOrderListView


class _VendorOrderListView(BaseOrderListView):
    template_name = 'order_admin/list.html'

    @method_decorator(vendor_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PendingView(_VendorOrderListView):
    title = 'Pending Orders'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user,
                                             status__in=['P', 'H'])


class OnDeliveryView(_VendorOrderListView):
    title = 'On-delivery Orders'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user,
                                             status='S')
