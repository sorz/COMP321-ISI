from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

from category.models import Category


RATING_DISPLAY = ('Horrible', 'Bad', 'Fair', 'Good', 'Fantastic')


class Product(models.Model):

    STATUS_CHOICES = (
        ('N', 'In stock'),
        ('O', 'Out of stock'),
        ('F', 'Off shelf')
    )

    name = models.CharField('Product name', max_length=255)
    price = models.DecimalField('Price ($)', max_digits=9, decimal_places=2,
                                validators=[MinValueValidator(0)])
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')
    category = models.ForeignKey(Category)
    description = models.TextField(blank=True)

    # Cache the total sale quantity and amount, re-calculate
    # once any order include this product is confirmed.
    sale_quantity = models.IntegerField(default=0)
    sale_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    # Cache the average rating, re-calculate once any user change the rating.
    average_rating = models.FloatField("Average rating", default=0, editable=False)

    # Router specified properties:

    eth_chip = models.CharField('Ethernet chip', max_length=127, blank=True)
    # e.g. Atheros AR9344. Blank value stands for unknown.

    cpu_model = models.CharField('CPU model', max_length=127, blank=True)
    # e.g. AR9344. Blank value stands for unknown.

    lan_speed = models.IntegerField("Max LAN speed",
                                    validators=[MinValueValidator(1)])
    lan_ports = models.IntegerField('No. of LAN ports',
                                    validators=[MinValueValidator(0)])
    wan_ports = models.IntegerField('No. of WAN ports',
                                    validators=[MinValueValidator(0)])
    wireless_type = models.CharField(max_length=127, blank=True)
    # e.g. 802.11b/g/n/ac. Blank value stands for not supported.

    power = models.CharField(max_length=127, blank=True)
    # e.g. 12 VDC, 2 A. Blank value stands for unknown.

    has_usb = models.BooleanField('Has USB ports', default=False)

    @property
    def in_stock(self):
        return self.status == 'N'

    @property
    def off_shelf(self):
        return self.status == 'F'

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

    Each product may have one or more photos.
    Each photo has an image file and an optional description.
    """
    product = models.ForeignKey(Product, null=True)
    image = ImageField(upload_to='photos/%Y/%m')
    description = models.CharField(max_length=255, null=True)
    # TODO: Maintain the display order of photos (#E7)

    # Delete image file when photo is removed. Not useful, having been implemented by inlineformset
    # Can be better implemented by pre_delete signal
    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(Photo, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)


class Rating(models.Model):
    """User's rating for a product.

    Point is between (both include) 1 to 5.
    """
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    point = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
