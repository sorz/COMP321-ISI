from django.test import TestCase

from product.models import Product
from .models import Category, PropertyName


class CategoryTestCast(TestCase):
    def setUp(self):
        book = Category.objects.create(name="Book")
        food = Category.objects.create(name="Food", description="Something edible.")

        PropertyName.objects.create(category=book, name="ISBN",
                                    description="International Standard Book Number")
        PropertyName.objects.create(category=book, name="Publisher")
        PropertyName.objects.create(category=food, name="Shelf Life")

    def test_getting_category_property(self):
        """Fetch category and property."""
        food = Category.objects.get(name="Food")
        self.assertEqual(food.description, "Something edible.")

        p = food.propertyname_set.first()
        self.assertEqual(p.name, "Shelf Life")

    def test_product_with_property(self):
        """Add Coke in Food category with 1 year shelf life."""
        food = Category.objects.get(name="Food")
        coke = Product.objects.create(name="Coke", category=food, price=3.50)
        life = PropertyName.objects.get(name="Shelf Life")
        coke.property_set.create(name=life, value="1 Year")

        # Test property value
        self.assertEqual(coke.property_set.get(name=life).value, "1 Year")

        # Find product via specified category.
        coke = Product.objects.get(category=food)
        self.assertEqual(coke.name, "Coke")
