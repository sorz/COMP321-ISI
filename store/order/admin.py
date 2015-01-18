from django.contrib import admin

from .models import OrderItem, PendingOrder, HoldingOrder, \
    OnDeliveryOrder, ConfirmedOrder, CancelledOrder


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    can_delete = False
    exclude = ('product', )
    editable_fields = []
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        return 'id', 'quantity', 'price', 'total_price', 'state'

    def has_add_permission(self, request):
        return False


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('owner', 'purchase_date', 'recipient_name', 'state',
                       'shipment_date', 'recipient_address', 'recipient_address_2',
                       'recipient_postcode', 'total_price')
    fieldsets = (
        (None, {
            'fields': ('owner', 'state', 'total_price', 'purchase_date', 'shipment_date')
        }),
        ('Recipient Information', {
            'fields': ('recipient_name', 'recipient_postcode',
                       'recipient_address', 'recipient_address_2')
        })
    )
    list_display = ('owner', 'recipient_name', 'purchase_date', 'state', 'total_price')
    list_filter = ('state', )
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        return False

    @staticmethod
    def make_ship(self, request, queryset):
        for order in queryset.all():
            order.ship()
    make_ship.short_description = 'Ship selected order'

    @staticmethod
    def make_hold(self, request, queryset):
        for order in queryset.all():
            order.hold()
    make_hold.short_description = 'Hold selected order'

    @staticmethod
    def make_cancel(self, request, queryset):
        for order in queryset.all():
            order.cancel()
    make_cancel.short_description = 'Cancel selected order.'


@admin.register(PendingOrder)
class PendingOrderAdmin(OrderAdmin):
    actions = ['make_ship', 'make_hold', 'make_cancel']
    list_filter = []

    def queryset(self, request):
        return self.model.objects.filter(state='P')

@admin.register(HoldingOrder)
class HoldingOrderAdmin(OrderAdmin):
    actions = ['make_ship', 'make_cancel']
    list_filter = []

    def queryset(self, request):
        return self.model.objects.filter(state='H')


@admin.register(OnDeliveryOrder)
class OnDeliveryOrderAdmin(OrderAdmin):
    list_filter = []

    def queryset(self, request):
        return self.model.objects.filter(state='S')

    def get_actions(self, request):
        return ['make_ship']

@admin.register(ConfirmedOrder)
class ConfirmedOrderAdmin(OrderAdmin):
    actions = []
    list_filter = []

    def queryset(self, request):
        return self.model.objects.filter(state='R')


@admin.register(CancelledOrder)
class CancelledOrderAdmin(OrderAdmin):
    actions = []
    list_filter = []

    def queryset(self, request):
        return self.model.objects.filter(state='C')