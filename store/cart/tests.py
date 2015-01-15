from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Cart
from product.models import Product


class CartTestCast(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="RMS", email="god@koujiao.org",
                                        password=r"ppnn13%dkstFeb.1st")
        self.cart = Cart.objects.create(owner=user)
        self.coke = Product.objects.create(name="Coke", price="3.50", in_stock=False)
        self.god_ship = Product.objects.create(name="Laptop Computer", price="8000")

        self.cart.add_item(self.coke, 10)
        self.cart.add_item(self.god_ship)

    def test_shopping_cart(self):
        coke = self.cart.cartitem_set.get(product=self.coke)
        ship = self.cart.cartitem_set.get(product=self.god_ship)

        self.assertEqual(coke.name, "Coke")
        self.assertEqual(coke.in_stock, False)
        self.assertEqual(ship.in_stock, True)

        # Check (total) price
        self.assertEqual(ship.price, Decimal('8000'))
        self.assertEqual(coke.total_price, Decimal('35.00'))
        self.assertEqual(self.cart.total_price, Decimal('8035.00'))

    def test_purchase(self):
        self.assertEqual(self.cart.purchased, False)
        self.cart.purchase()
        self.assertEqual(self.cart.purchased, True)

        self.coke.price = '2.50'
        self.coke.save()
        coke = self.cart.cartitem_set.get(product=self.coke)
        self.assertEqual(coke.price, Decimal('3.50'))
