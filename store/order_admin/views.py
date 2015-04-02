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

    def is_valid_duration(self, date_start="", date_end=""):
        """Determine if two given strings are valid date or duration"""
        if len(date_start) != 0 and len(date_end) != 0:
            try:
                sdate = strptime(date_start, "%Y-%m-%d")
                edate = strptime(date_end, "%Y-%m-%d")
            except:
                return 'ERRFMT'
            if edate >= sdate:
                return 'APTDATE'
            else:
                return 'ERRDUR'
        elif len(date_start) == 0 and len(date_end) == 0:
            return 'EMPDATE'
        else:
            return 'APTDATE'

    def get_queryset(self):
        orders = super().get_queryset()
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        try:
            if start:
                orders = orders.filter(purchase_date__gt=start)
            if end:
                orders = orders.filter(purchase_date__lt="%s 23:59:59.99" % end)
        except ValidationError:
            messages.add_message(self.request, messages.ERROR,
                             "Date validation errs. "
                             "Please select appropriate dates.")
        return orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start'] = self.request.GET.get('start', '')
        context['end'] = self.request.GET.get('end', '')
        #validate date format
        if self.is_valid_duration(context['start'], context['end']) == 'EMPDATE':
            messages.add_message(self.request, messages.WARNING,
                             "Date field is empty. "
                             "Please select appropriate dates.")
        elif self.is_valid_duration(context['start'], context['end']) == 'ERRFMT':
            messages.add_message(self.request, messages.ERROR,
                             "Incorrect date format. "
                             "Please select appropriate dates.")
        elif self.is_valid_duration(context['start'], context['end']) == 'ERRDUR':
            messages.add_message(self.request, messages.ERROR,
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
