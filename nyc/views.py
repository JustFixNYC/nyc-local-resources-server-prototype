import json
from django.shortcuts import render
from django.conf import settings

from .models import Zipcode


def index(request):
    origin = Zipcode.objects.get(postalcode="11201")
    js_params = {
        'mapboxAccessToken': settings.MAPBOX_ACCESS_TOKEN,
        'origin': [origin.latitude, origin.longitude],
        'area': json.loads(origin.geom.geojson)
    }
    return render(request, 'index.html', {
        'js_params': js_params
    })
