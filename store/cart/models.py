from django.db import models
from django.contrib.auth.models import User

from product.models import Product


class ProductItemInfo(models.Model):
    """Abstract model of commons of CartItem and OrderItem."""
    class Meta:
        abstract = True

    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)

    @property
    def total_price(self):
        if self.price is not None:
            return self.price * self.quantity

    @property
    def name(self):
        """Return product's name."""
        return self.product.name

    @property
    def in_stock(self):
        """Return product's in-stock status."""
        return self.product.in_stock

    @property
    def off_shelf(self):
        """Return product's off_shelf status."""
        return self.product.off_shelf

    @property
    def status(self):
        """Return a human friendly status description."""
        if self.product is None:
            return
        if self.off_shelf:
            return "Off Shelf"
        elif self.in_stock:
            return "In Stock"
        else:
            return "Out of Stock"

    @property
    def description(self):
        """Return product's description."""
        return self.product.description

    def __str__(self):
        return self.name


class CartItem(ProductItemInfo):
    """Stores quantity of a product for Cart."""
    owner = models.ForeignKey(User)

    @property
    def price(self):
        """Return product's price."""
        return self.product.price
