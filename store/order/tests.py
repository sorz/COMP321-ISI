from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Order
from cart.models import Cart
from product.models import Product


class OrderTestCast(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username="RMS", email="god@koujiao.org",
                                                 password=r"ppnn13%dkstFeb.1st")
        self.vendor = User.objects.create_superuser(username="Loongson",
                                                    email="weiwu@ict.ac.cn",
                                                    password="123456")

        self.cart = Cart.objects.create(owner=self.customer)
        self.product = Product.objects.create(name="Notebook", price="2000")
        self.cart.add_item(self.product)

        self.order = Order.objects.create(recipient_name="RMS",
                                          recipient_address="Koujiao Temple")
        self.cart.purchase(self.order)

    def test_values(self):
        self.assertEqual(self.order.state, 'P')
        self.assertEqual(self.cart.total_price, Decimal('2000'))
        self.assertTrue(self.cart.purchased)
        self.assertIsNone(self.order.shipment_date)
        self.assertIsNotNone(self.order.purchase_date)

    def test_normal_ship(self):
        self.order.ship()
        self.assertIsNotNone(self.order.shipment_date)
        self.assertEqual(self.order.state, 'S')

        self.order.confirm()
        self.assertEqual(self.order.state, 'R')

    def test_hold_ship(self):
        self.order.hold()
        self.assertEqual(self.order.state, 'H')

        self.order.ship()
        self.assertEqual(self.order.state, 'S')

    def test_hold_cancel_by_vendor(self):
        self.order.hold()
        self.order.cancel(self.vendor)
        self.assertEqual(self.order.state, 'C')

        message = self.order.message_set.last()
        self.assertEqual(message.writer, self.vendor)
        self.assertTrue(message.is_wrote_by_vendor)
        self.assertTrue("by vendor" in message.content)

    def test_pending_cancel_by_customer(self):
        self.order.cancel(self.customer)

        message = self.order.message_set.last()
        self.assertEqual(message.writer, self.customer)
        self.assertFalse(message.is_wrote_by_vendor)
        self.assertTrue("by customer" in message.content)
