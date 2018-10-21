import json
from django.shortcuts import render
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry

from .models import Zipcode


def index(request):
    total_area = GEOSGeometry('POINT EMPTY', srid=4326)
    zipcodes = ['11201', '11231']
    areas = Zipcode.objects.filter(postalcode__in=zipcodes).all()
    for area in areas:
        total_area = total_area.union(area.geom)
    origin = list(reversed(total_area.centroid))

    js_params = {
        'mapboxAccessToken': settings.MAPBOX_ACCESS_TOKEN,
        'origin': origin,
        'area': json.loads(total_area.geojson)
    }
    return render(request, 'index.html', {
        'js_params': js_params
    })
