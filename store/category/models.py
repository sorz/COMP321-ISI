from django.db import models


class Category(models.Model):
    """Product category with optional description."""
    name = models.CharField('Category Name', max_length=255)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class PropertyName(models.Model):
    """Stores names of properties of each category.

    Different categories have different (independent) properties,
    A certain product has zero or more properties (with value) selected from
    which category it belong to.
    """
    category = models.ForeignKey(Category)
    name = models.CharField("Property Name", max_length=255)
    description = models.TextField(null=True)

    def __str__(self):
        return "%s: %s" % (self.category.name, self.name)
