from django.contrib import admin
from django.contrib.auth.models import Group


# We don't use group function.
admin.site.unregister(Group)
