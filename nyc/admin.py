from django.contrib.gis import admin
from .models import Zipcode


@admin.register(Zipcode)
class ZipcodeAdmin(admin.GeoModelAdmin):
    list_display = ['postalcode', 'po_name', 'borough']
