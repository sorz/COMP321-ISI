from django.db import models
from django.contrib.auth.models import User

from product.models import Product


class Cart(models.Model):
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

    def add_item(self, product, quantity=1):
        """Add (or increase the quantity if existed) a product into shopping cart."""
        assert quantity > 0
        item, created = self.cartitem_set.get_or_create(product=product, defaults={'quantity': 0})
        item.quantity += quantity
        item.save()


class CartItem(models.Model):
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

    def __str__(self):
        return "%s x %s" % (self.product, self.quantity)