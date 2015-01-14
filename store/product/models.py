from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

from category.models import Category, PropertyName


class Product(models.Model):
    name = models.CharField('Product Name', max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Photo(models.Model):
    product = models.ForeignKey(Product, null=True)
    image = models.ImageField(upload_to='photos/%Y/%m')
    description = models.CharField(max_length=255, null=True)


class Property(models.Model):
    product = models.ForeignKey(Product)
    name = models.ForeignKey(PropertyName)
    value = models.CharField(max_length=255)


class Rating(models.Model):
    user = models.ForeignKey(User, unique=True)
    point = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
