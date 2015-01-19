from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from category.models import Category, PropertyName


class Product(models.Model):
    name = models.CharField('Product Name', max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category)
    in_stock = models.BooleanField(default=True)
    off_shelf = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    # Cache the average rating, re-calculate once any user change the rating.
    average_rating = models.FloatField("Average rating", default=0, editable=False)

    def update_rating(self):
        """Re-calculate the average rating and update the rating field."""
        total = 0
        count = 0
        for rating in self.rating_set.all():
            total += rating.point
            count += 1
        self.average_rating = total / count
        self.save()

    def __str__(self):
        return self.name


class Photo(models.Model):
    """Photos of product.

    Each product may has or not one or more photos.
    Each photo has a image file and optional description.
    """
    product = models.ForeignKey(Product, null=True)
    image = models.ImageField(upload_to='photos/%Y/%m')
    description = models.CharField(max_length=255, null=True)
    # TODO: Maintain the display order of photos (#E7)
    # TODO: Delete image file when photo is removed.


class Property(models.Model):
    """Stores properties of products.

    Property name is stored in PropertyName, which is associated with Category,
    so that available properties of a specific product is depending on product's category.
    """
    product = models.ForeignKey(Product)
    name = models.ForeignKey(PropertyName)
    value = models.CharField(max_length=255)

    def clean(self):
        """Ensure this property is belong to product's category."""
        super().clean()
        if self.name.category != self.product.category:
            raise ValidationError("Property (%s) is belong to <%s> but not product's category (%s)."
                                  % (self.name.name, self.name.category, self.product.category))


class Rating(models.Model):
    """User's rating for a product.

    Point is between (both include) 1 to 5.
    """
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    point = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
