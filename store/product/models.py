from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField('Category Name', max_length=244)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Product Name', max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.ForeignKey(User, unique=True)
    point = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
