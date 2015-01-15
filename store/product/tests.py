from decimal import Decimal
from django.test import TestCase

from .models import Product, Rating


class ProductTestCast(TestCase):
    def setUp(self):
        Product.objects.create(name="1984", price=22.51, description="Dystopian")

    def test_get_product(self):
        book = Product.objects.get(name="1984")
        self.assertEqual(book.price, Decimal('22.51'))
        self.assertEqual(book.description, "Dystopian")

    def test_add_photo(self):
        product = Product.objects.get(name="1984")
        product.photo_set.create(product=product, image='test.jpg', description='Test image')
        photo = product.photo_set.first()

        self.assertEqual(photo.image, 'test.jpg')
        self.assertEqual(photo.description, 'Test image')

    def test_rating(self):
        pass  # TODO

    # Property is tested on category.
