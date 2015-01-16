from django.db import models
from django.contrib.auth.models import User

from product.models import Product
from order.models import OrderItem


class Cart(models.Model):
    """Shopping cart, which collect s set of products, with quantity.

    For each user, only one cart.
    """
    owner = models.OneToOneField(User)

    @property
    def total_price(self):
        price = 0
        for item in self.cartitem_set.all():
            price += item.total_price
        return price

    def add_item(self, product, quantity=1):
        """Add (or increase the quantity if existed) a product into shopping cart."""
        assert quantity > 0
        item, created = self.cartitem_set.get_or_create(product=product, defaults={'quantity': 0})
        item.quantity += quantity
        item.save()

    def checkout(self, order):
        """Copy all items on cart into order.

        Should be called in transaction to improve performance and keep integrity."""
        for item in self.cartitem_set.all():
            assert item.quantity >= 0
            assert item.in_stock
            assert not item.off_shelf
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            ).save()


class CartItem(models.Model):
    """Stores quantity of a product for Cart."""
    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)

    @property
    def price(self):
        """Return product's price"""
        return self.product.price

    @property
    def total_price(self):
        return self.price * self.quantity

    @property
    def name(self):
        """Return product's name"""
        return self.product.name

    @property
    def in_stock(self):
        """Return product's in-stock status"""
        return self.product.in_stock

    @property
    def off_shelf(self):
        """Return product's off_shelf status"""
        return self.product.off_shelf

    @property
    def description(self):
        """Return product's description"""
        return self.product.description

    def __str__(self):
        return "%s x%s" % (self.name, self.quantity)
