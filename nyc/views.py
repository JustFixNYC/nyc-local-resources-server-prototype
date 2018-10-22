import json
from django.shortcuts import render
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

from .models import Zipcode, TenantResource
from . import geocoding


def index(request):
    address = request.GET.get('address', '')
    georesults = geocoding.search(address)
    georesult = None
    js_params = None
    best_resource = None
    if georesults:
        georesult = georesults[0]
        longitude, latitude = georesult.geometry.coordinates
        origin = Point(longitude, latitude, srid=4326)
        resources = TenantResource.objects.filter(
            catchment_area__contains=Point(longitude, latitude),
        ).annotate(distance=Distance('geocoded_point', origin)).order_by('distance')
        if resources:
            best_resource = resources.first()
            js_params = {
                'mapboxAccessToken': settings.MAPBOX_ACCESS_TOKEN,
                'origin': [latitude, longitude],
                'originName': georesult.properties.name,
                'target': [best_resource.geocoded_latitude, best_resource.geocoded_longitude],
                'targetName': best_resource.name,
                'area': json.loads(best_resource.catchment_area.geojson)
            }

    return render(request, 'index.html', {
        'address': address,
        'js_params': js_params,
        'georesult': georesult,
        'best_resource': best_resource
    })
