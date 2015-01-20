from django.db import models


class Category(models.Model):
    """Product category with optional description."""
    name = models.CharField('Category Name', max_length=255)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name
