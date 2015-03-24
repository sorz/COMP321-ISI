import zlib
from django.shortcuts import get_object_or_404

from order.models import OrderItem


class CannotCheckoutItemException(Exception):
    """Cannot checkout item due to invalid quantity, out-of-stock or off-shelf."""
    def __init__(self, item):
        self.item = item


class Cart():
    def __init__(self, owner):
        self.user = owner
        self.item_set = self.user.cartitem_set

    def get(self, *args, **kwargs):
        return self.item_set.get(*args, **kwargs)

    def remove(self, product):
        """Remove a item from shopping cart."""
        item = get_object_or_404(self.item_set, product=product)
        item.delete()

    def set_item(self, product, quantity=1):
        """Add or set the quantity of a product on shopping cart.

        Return True if new item is created.
        """
        assert quantity > 0
        item, created = self.item_set.get_or_create(product=product)
        item.quantity = quantity
        item.save()
        return created

    def add_item(self, product, quantity=1):
        """Add (or increase the quantity if existed) a product into shopping cart."""
        assert quantity > 0
        item, created = self.item_set.get_or_create(product=product,
                                                    defaults={'quantity': 0})
        item.quantity += quantity
        item.save()

    def checkout(self, order):
        """Copy all items on cart into order.

        Should be called in transaction to improve performance and keep integrity."""
        for item in self.item_set.all():
            if item.quantity <= 0 or item.off_shelf:
                raise CannotCheckoutItemException(item)
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            ).save()

    @property
    def total_price(self):
        price = 0
        for item in self.item_set.all():
            price += item.total_price
        return price

    def __hash__(self):
        """Hash user-id and all items information (name, price,
        quantity and state) in this cart.
        """
        crc = zlib.crc32(('%s:' % hash(self.user)).encode())
        for item in self.item_set.all():
            s = '%s,%s,%s,%s,%s.' % (item.name,
                                     item.price,
                                     item.quantity,
                                     item.in_stock,
                                     item.off_shelf)
            crc = zlib.crc32(s.encode(), crc)
        return crc
