from django.contrib import admin

from .models import OrderItem, Order


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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('owner', 'purchase_date', 'recipient_name', 'state',
                       'shipment_date', 'recipient_address', 'recipient_address_2',
                       'recipient_postcode', 'total_price')
    fieldsets = (
        (None, {
            'fields': ('owner', 'state', 'total_price',
                       'purchase_date', 'shipment_date')
        }),
        ('Recipient Information', {
            'fields': ('recipient_name', 'recipient_postcode',
                       'recipient_address', 'recipient_address_2')
        })
    )
    list_display = ('id', 'owner', 'recipient_name', 'purchase_date',
                    'state', 'total_price')
    list_filter = ('state', )
    search_fields = ('id', 'owner__username', 'recipient_name',
                     'recipient_address', 'recipient_address_2')
    date_hierarchy = 'purchase_date'
    inlines = [OrderItemInline]
    actions = ['make_ship', 'make_hold', 'make_cancel']

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

