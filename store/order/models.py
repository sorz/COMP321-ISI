from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Order(models.Model):
    """Stores recipient information and delivery state."""
    STATE_CHOICES = (
        ('P', 'Pending'),
        ('S', 'Shipping'),
        ('R', 'Received'),
        ('H', 'Hold'),
        ('C', 'Cancelled')
    )
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='P')
    purchase_date = models.DateTimeField(auto_now_add=True)
    shipment_date = models.DateTimeField(null=True)
    recipient_name = models.CharField(max_length=255)
    recipient_address = models.CharField(max_length=255)
    recipient_address_2 = models.CharField(max_length=255, null=True)
    recipient_postcode = models.CharField(max_length=63, null=True)

    def _get_owner(self):
        return self.cart.owner
    owner = property(_get_owner)

    def ship(self):
        """Ship a pending/hold order. Used by vendor."""
        assert self.state == 'P' or self.state == 'H'
        assert self.shipment_date is None
        self.state = 'S'
        self.shipment_date = timezone.now()
        self.save()

    def hold(self):
        """Hold a pending order. Used by vendor."""
        assert self.state == 'P'
        self.state = 'H'
        self.save()

    def cancel(self, operator):
        """Cancel a pending/hold order. Used by vendor/customer."""
        assert self.state == 'P' or self.state == 'H'

        if operator.is_superuser:  # is vendor
            message = 'Cancelled by vendor.'
        else:
            message = 'Cancelled by customer.'
            # Only vendor or owner can cancel the order.
            assert self.owner == operator

        self.state = 'C'
        self.message_set.create(writer=operator, content=message)
        self.save()

    def confirm(self):
        """Confirm a shipped order. Used by customer."""
        assert self.state == 'S'
        self.state = 'R'
        self.save()

    def __str__(self):
        return "%s: %s" % (self.owner, self.get_state_display())


class Message(models.Model):
    """Order message, wrote by customer and vendor."""
    order = models.ForeignKey(Order)
    writer = models.ForeignKey(User)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def _get_wrote_by_vendor(self):
        return self.writer.is_superuser
    wrote_by_vendor = property(_get_wrote_by_vendor)
