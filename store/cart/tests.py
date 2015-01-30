from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User

from .utils import Cart
from product.models import Product, Category
from order.models import Order


class CartTestCast(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="RMS", email="god@koujiao.org",
                                             password=r"ppnn13%dkstFeb.1st")
        self.cart = Cart(owner=self.user)
        category = Category.objects.create(name="All")
        category.save()
        self.coke = Product.objects.create(name="Coke", price="3.50", in_stock=False,
                                           category=category)
        self.god_ship = Product.objects.create(name="Laptop Computer", price="8000",
                                               category=category)

        self.cart.add_item(self.coke, 10)
        self.cart.add_item(self.god_ship)

    def test_shopping_cart(self):
        coke = self.cart.get(product=self.coke)
        ship = self.cart.get(product=self.god_ship)

        self.assertEqual(coke.name, "Coke")
        self.assertEqual(coke.in_stock, False)
        self.assertEqual(ship.in_stock, True)

        # Check (total) price
        self.assertEqual(ship.price, Decimal('8000'))
        self.assertEqual(coke.total_price, Decimal('35.00'))
        self.assertEqual(self.cart.total_price, Decimal('8035.00'))

    def test_checkout(self):
        self.coke.in_stock = True
        self.coke.save()

        order = Order.objects.create(owner=self.user, recipient_name="Ge Pao",
                                     recipient_address="ACFun")
        self.cart.checkout(order)
        self.assertEqual(len(order.orderitem_set.all()), 2)

        coke = order.orderitem_set.get(product=self.coke)
        self.assertEqual(coke.name, "Coke")
        self.assertEqual(coke.price, Decimal('3.50'))

        self.coke.price = 100
        self.assertEqual(coke.price, Decimal('3.50'))
