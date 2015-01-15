from django.db import models
from django.contrib.auth.models import User

from product.models import Product


class Cart(models.Model):
    """A set of products. As a shopping cart when purchase is false (default).
    Or just a collection of products for a order after purchased (order made).

    The number of un-purchase cart (shopping cart) for each user must be 0 or 1 at any time.
    """
    owner = models.ForeignKey(User)
    purchased = models.BooleanField(default=False)

    def purchase(self):
        """Save prices of items and set purchased to true."""
        assert not self.purchased
        self.purchased = True

        # Save current prices (purchase prices) permanently.
        for item in self.cartitem_set.all():
            assert item.quantity >= 0
            item.purchase_price = item.product.price
            item.save()

        # TODO: create and return a order

    def _get_total_price(self):
        price = 0
        for item in self.cartitem_set.all():
            price += item.total_price
        return price
    total_price = property(_get_total_price)

    def add_item(self, product, quantity=1):
        """Add (or increase the quantity if existed) a product into shopping cart."""
        assert quantity > 0
        item, created = self.cartitem_set.get_or_create(product=product, defaults={'quantity': 0})
        item.quantity += quantity
        item.save()


class CartItem(models.Model):
    """Stores quantity and price of a product for Cart.

    Price is only stored when purchasing.
    It's used to keep trading price is immutable from changing product price.
    """
    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(Product)
    purchase_price = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    quantity = models.IntegerField(default=1)

    def _get_price(self):
        """Return purchase price after purchased or return current price."""
        if self.purchase_price is None:
            return self.product.price
        else:
            return self.purchase_price
    price = property(_get_price)

    def _get_total_price(self):
        return self.price * self.quantity
    total_price = property(_get_total_price)

    def _get_name(self):
        """Return product's name"""
        return self.product.name
    name = property(_get_name)

    def _get_in_stock(self):
        """Return product's in-stock status"""
        return self.product.in_stock
    in_stock = property(_get_in_stock)

    def _get_description(self):
        """Return product's description"""
        return self.product.description
    description = property(_get_description)

    def __str__(self):
        return "%s x%s" % (self.name, self.quantity)