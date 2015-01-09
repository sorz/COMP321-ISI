from django.db import models


class Category(models.Model):
    name = models.CharField('Category Name', max_length=244)
    description = models.TextField()

    def __str__(self):
        return self.name