from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

from category.models import Category


RATING_DISPLAY = ('Horrible', 'Bad', 'Fair', 'Good', 'Fantastic')


class Product(models.Model):
    name = models.CharField('Product Name', max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category)
    in_stock = models.BooleanField(default=True)
    off_shelf = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    # Router specified properties:

    eth_chip = models.CharField('Ethernet Chip', max_length=127, blank=True)
    # e.g. Atheros AR9344. Blank value stands for unknown.

    cpu_model = models.CharField(max_length=127, blank=True)
    # e.g. AR9344. Blank value stands for unknown.

    lan_speed = models.IntegerField("Max LAN Speed",
                                    validators=[MinValueValidator(1)])
    lan_ports = models.IntegerField('No. of LAN ports',
                                    validators=[MinValueValidator(0)])
    wan_ports = models.IntegerField('No. of WAN ports',
                                    validators=[MinValueValidator(0)])
    wireless_type = models.CharField(max_length=127, null=True)
    # e.g. 802.11b/g/n/ac. Null value stands for not supported.

    power = models.CharField(max_length=127, blank=True)
    # e.g. 12 VDC, 2 A. Blank value stands for unknown.

    has_usb = models.BooleanField('Has USB ports', default=False)

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

    def get_average_rating_display(self):
        if 1 <= self.average_rating <= 5:
            return RATING_DISPLAY[round(self.average_rating) - 1]

    def has_bought_by_user(self, user):
        """Return True if this user has purchased it and confirmed the order."""
        orders = user.order_set.filter(status='R')
        for order in orders:
            if order.orderitem_set.filter(product=self).exists():
                return True
        return False

    def get_image(self):
        try:
            print(self.photo_set.all()[0].image)
            return self.photo_set.all()[0].image
        except Photo.DoesNotExist:
            pass

    def __str__(self):
        return self.name


class Photo(models.Model):
    """Photos of product.

    Each product may has or not one or more photos.
    Each photo has a image file and optional description.
    """
    product = models.ForeignKey(Product, null=True)
    image = ImageField(upload_to='photos/%Y/%m')
    description = models.CharField(max_length=255, null=True)
    # TODO: Maintain the display order of photos (#E7)
    # TODO: Delete image file when photo is removed.


class Rating(models.Model):
    """User's rating for a product.

    Point is between (both include) 1 to 5.
    """
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    point = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
