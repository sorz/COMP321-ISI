from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField("address", max_length=255)
    address_2 = models.CharField("address (2th line)", max_length=255, blank=True)
    postcode = models.CharField("zip", max_length=63, blank=True)
