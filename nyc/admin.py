from django.contrib.gis import admin
from .models import Zipcode, TenantResource


@admin.register(Zipcode)
class ZipcodeAdmin(admin.GeoModelAdmin):
    list_display = ['postalcode', 'po_name', 'borough']
    search_fields = ['postalcode']


@admin.register(TenantResource)
class TenantResourceAdmin(admin.GeoModelAdmin):
    autocomplete_fields = ['zipcodes']
    readonly_fields = ['geocoded_address', 'geocoded_latitude', 'geocoded_longitude']

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        obj.update_catchment_area()
        obj.save()
