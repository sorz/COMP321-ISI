from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

from product.models import Product, Photo
from cart.models import ProductItemInfo


class InvalidOrderStatusChangeException(Exception):
    """Cannot change the status of order by this way."""

    def __init__(self, order, status_from, status_to):
        self.order = order
        self.status_from = status_from
        self.status_to = status_to

    def __str__(self):
        return "Cannot change order status from %s to %s." % \
               (self.status_from, self.status_to)


class Order(models.Model):
    """Stores recipient information and delivery status."""
    class Meta:
        ordering = ['-purchase_date']

    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('S', 'Shipping'),
        ('R', 'Received'),
        ('H', 'Hold'),
        ('C', 'Cancelled')
    )
    owner = models.ForeignKey(User)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    purchase_date = models.DateTimeField(auto_now_add=True)
    shipment_date = models.DateTimeField(null=True)

    # Stand for receipt date if status is received
    # or cancel date is status is cancelled.
    close_date = models.DateTimeField(null=True)

    recipient_name = models.CharField(max_length=255)
    recipient_address = models.CharField("address", max_length=255)
    recipient_address_2 = models.CharField("address (2th line)", max_length=255, blank=True)
    recipient_postcode = models.CharField("zip", max_length=63, blank=True)

    @property
    def total_price(self):
        price = 0
        for item in self.orderitem_set.all():
            price += item.total_price
        return price

    @property
    def elapsed_days(self):
        """Return the number of days elapsed between purchase date and close date.

        None if it's not received either canceled.
        """
        if not self.close_date:
            return
        elapsed = self.close_date - self.purchase_date
        return elapsed.days

    def ship(self):
        """Ship a pending/hold order. Used by vendor."""
        assert self.shipment_date is None
        self._change_status_atomically('PH', 'S')

        self.shipment_date = timezone.now()
        self.save()

    def hold(self):
        """Hold a pending order. Used by vendor."""
        self._change_status_atomically('P', 'H')
        self.save()

    def cancel(self, operator):
        """Cancel a pending/hold order. Used by vendor/customer."""
        if operator.is_superuser:  # is vendor
            message = 'Cancelled by vendor.'
        else:
            message = 'Cancelled by customer.'
            # Only owner (and vendor) can cancel the order.
            assert self.owner == operator

        self._change_status_atomically('PH', 'C')

        self.close_date = timezone.now()
        self.save()

        self.message_set.create(content=message, by_vendor=operator.is_superuser)

    def confirm(self):
        """Confirm a shipped order. Used by customer."""
        self._change_status_atomically('S', 'R')
        self.close_date = timezone.now()
        self.save()

        # Update sale quantity and amount of products.
        for orderitem in self.orderitem_set.all():
            orderitem.product.sale_quantity += orderitem.quantity
            orderitem.product.sale_amount += orderitem.total_price
            orderitem.product.save()

    def _change_status_atomically(self, from_status, to_status):
        """Change status and commit it atomically.

        Before making change, it check whether current status is "from_status",
        if not, raise InvalidOrderStatusChangeException.
        """
        # select_for_update() must execute in non-autocommit mode.
        with transaction.atomic():

            # Using select_for_update() to lock this record.
            # It prevent other transactions acquiring locks on it (they will wait for it).

            # All status change must use _change_status_atomically() eventually,
            # so they [require a lock] -> [check status] -> [make change] -> [commit & unlock].

            # It prevent invalid status change, and satisfy requirement (H5).

            # References
            # https://docs.djangoproject.com/en/dev/ref/models/querysets/#select-for-update
            # http://stackoverflow.com/questions/1645269/concurrency-control-in-django-model

            order = Order.objects.filter(pk=self.pk).select_for_update()[0]

            if order.status != to_status:
                # Ignore redundant operation.
                # Ensure status of self is updated.
                self.status = to_status
                return
            if order.status not in from_status:
                raise InvalidOrderStatusChangeException(order, order.status, to_status)

            order.status = to_status
            order.save()

        # Update status of self.
        self.status = to_status

    def get_image(self):
        """Find the first product which has a photo in this order.
        And return it's first photo.
        """
        for item in self.orderitem_set.all():
            photos = Photo.objects.filter(product__id=item.product_id)
            if photos.exists():
                return photos[0].image

    def __str__(self):
        return "%s: %s" % (self.owner, self.get_status_display())


class OrderItem(ProductItemInfo):
    """Stores quantity and purchase price of a product for a order."""
    order = models.ForeignKey(Order)
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                validators=[MinValueValidator(0)])


class Message(models.Model):
    """Order message, written by customer and vendor."""
    class Meta:
        ordering = ['-create_date']

    order = models.ForeignKey(Order)

    # True if it was wrote by vendor.
    # Otherwise, by customer (self.order.own).
    by_vendor = models.BooleanField(default=False)

    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)


    @property
    def writer_role(self):
        """Return 'Vendor' or 'Customer'."""
        if self.by_vendor:
            return 'Vendor'
        else:
            return 'Customer'

    @property
    def create_datetime_zone_aware(self):
        tz = timezone.get_current_timezone()
        date = self.create_date.astimezone(tz).strftime("%B %d, %Y, %H:%M:%S %Z")
        return date
