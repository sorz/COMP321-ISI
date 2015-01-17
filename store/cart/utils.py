from order.models import OrderItem


class Cart():
    def __init__(self, owner):
        self.user = owner
        self.item_set = self.user.cartitem_set

    def get(self, *args, **kwargs):
        return self.user.cartitem_set.get(*args, **kwargs)

    def add_item(self, product, quantity=1):
        """Add (or increase the quantity if existed) a product into shopping cart."""
        assert quantity > 0
        item, created = self.user.cartitem_set.get_or_create(product=product,
                                                             defaults={'quantity': 0})
        item.quantity += quantity
        item.save()

    def checkout(self, order):
        """Copy all items on cart into order.

        Should be called in transaction to improve performance and keep integrity."""
        for item in self.user.cartitem_set.all():
            assert item.quantity >= 0
            assert item.in_stock
            assert not item.off_shelf
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            ).save()

    @property
    def total_price(self):
        price = 0
        for item in self.user.cartitem_set.all():
            price += item.total_price
        return price