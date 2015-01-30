from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Product, Rating, Category


class ProductTestCast(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='All')
        self.book = Product.objects.create(name="1984", price=22.51,
                                           category=self.category, description="Dystopian")

    def test_get_product(self):
        book = Product.objects.get(name="1984")
        self.assertEqual(book.price, Decimal('22.51'))
        self.assertEqual(book.description, "Dystopian")

    def test_add_photo(self):
        self.book.photo_set.create(image='test.jpg', description='Test image')
        photo = self.book.photo_set.first()

        self.assertEqual(photo.image, 'test.jpg')
        self.assertEqual(photo.description, 'Test image')

    def test_rating(self):
        self.assertEqual(self.book.average_rating, 0)

        user = User.objects.create_user(username="RMS", email="god@koujiao.org",
                                        password=r"ppnn13%dkstFeb.1st")
        Rating.objects.create(user=user, product=self.book, point=3)
        Rating.objects.create(user=user, product=self.book, point=0)
        Rating.objects.create(user=user, product=self.book, point=5)
        Rating.objects.create(user=user, product=self.book, point=1)

        self.book.update_rating()
        self.assertEqual(self.book.average_rating, (3+0+1+5) / 4)

    # Property is tested on category.
