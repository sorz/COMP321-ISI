from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator


from product.models import Product
from cart.models import ProductItemInfo


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

    def ship(self):
        """Ship a pending/hold order. Used by vendor."""
        assert self.status == 'P' or self.status == 'H'
        assert self.shipment_date is None
        self.status = 'S'
        self.shipment_date = timezone.now()
        self.save()

    def hold(self):
        """Hold a pending order. Used by vendor."""
        assert self.status == 'P'
        self.status = 'H'
        self.save()

    def cancel(self, operator):
        """Cancel a pending/hold order. Used by vendor/customer."""
        assert self.status == 'P' or self.status == 'H'

        if operator.is_superuser:  # is vendor
            message = 'Cancelled by vendor.'
        else:
            message = 'Cancelled by customer.'
            # Only owner (and vendor) can cancel the order.
            assert self.owner == operator

        self.status = 'C'
        self.message_set.create(content=message, by_vendor=operator.is_superuser)
        self.save()

    def confirm(self):
        """Confirm a shipped order. Used by customer."""
        assert self.status == 'S'
        self.status = 'R'
        self.save()

    def __str__(self):
        return "%s: %s" % (self.owner, self.get_status_display())


class OrderItem(ProductItemInfo):
    """Stores quantity and purchase price of a product for a order."""
    order = models.ForeignKey(Order)
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                validators=[MinValueValidator(0)])


class Message(models.Model):
    """Order message, wrote by customer and vendor."""
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
