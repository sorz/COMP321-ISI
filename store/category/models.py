from django.db import models


class Category(models.Model):
    name = models.CharField('Category Name', max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class PropertyName(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField("Property Name", max_length=255)
    description = models.TextField(null=True)

    def __str__(self):
        return "%s: %s" % (self.category.name, self.name)
