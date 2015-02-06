from django.db import models


class Category(models.Model):
    """Product category with optional description."""
    name = models.CharField('Category Name', max_length=255)
    description = models.TextField(null=True)

    def get_cover_image(self):
        """
        Return the front cover image, which is selected from
        one of product photo in this category.

        May return None if no front cover.
        """
        from product.models import Photo

        photos = Photo.objects.filter(product__category__id=self.pk)
        if photos.exists():
            return photos[0].image

    def __str__(self):
        return self.name
