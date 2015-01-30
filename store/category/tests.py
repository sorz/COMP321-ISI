from django.test import TestCase

from product.models import Product
from .models import Category


class CategoryTestCast(TestCase):
    def setUp(self):
        self.book = Category.objects.create(name="Book")
        self.food = Category.objects.create(name="Food", description="Something edible.")

    def test_fetch_category(self):
        food = Category.objects.get(name="Food")
        self.assertEqual(food.description, "Something edible.")

    def test_find_product_by_category(self):
        Product.objects.create(name="Coke", category=self.food, price=3.50)

        coke = Product.objects.get(category=self.food)
        self.assertEqual(coke.name, "Coke")
