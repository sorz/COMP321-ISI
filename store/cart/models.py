from django.db import models
from django.contrib.auth.models import User

from product.models import Product


class CartItem(models.Model):
    """Stores quantity of a product for Cart."""
    owner = models.ForeignKey(User)
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
