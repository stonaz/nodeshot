from django.contrib import admin
from django.contrib.gis.geos import Point
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

GEODJANGO_IMPROVED_WIDGETS = 'olwidget' in settings.INSTALLED_APPS


if GEODJANGO_IMPROVED_WIDGETS:
    from olwidget.admin import GeoModelAdmin
else:
    from django.contrib.gis.admin import ModelAdmin as GeoModelAdmin


def _get_geodjango_map_coords():
    """ point to be used by geodjango """
    try:
        lat, lng = settings.NODESHOT['SETTINGS']['ADMIN_MAP_COORDS']
    except KeyError:
        raise ImproperlyConfigured("missing NODESHOT['SETTINGS']['ADMIN_MAP_COORDS'] in settings")
    
    point = Point(lng, lat, srid=4326)
    
    if GEODJANGO_IMPROVED_WIDGETS:
        return (lat, lng)
    else:
        point.transform(900913)
        return point
    
def _get_geodjango_map_zoom():
    """ zoom level to be used by geodjango """
    try:
        return settings.NODESHOT['SETTINGS']['ADMIN_MAP_ZOOM']
    except KeyError:
        raise ImproperlyConfigured("missing NODESHOT['SETTINGS']['ADMIN_MAP_ZOOM'] in settings")


class BaseAdmin(admin.ModelAdmin):
    """
    Abstract administration model for BaseDate models.
        * 'added' and 'updated' fields readonly
        * save-on-top button enabled by default
    """
    save_on_top = True
    readonly_fields = ['added', 'updated']


class BaseGeoAdmin(BaseAdmin, GeoModelAdmin):
    """
    BaseAdmin + Geodjango support
    """
    if GEODJANGO_IMPROVED_WIDGETS:
        lat, lng = _get_geodjango_map_coords()
        options = {
            'layers': [
                'osm.mapnik',
                'google.streets',
                'google.physical',
                'google.satellite',
                'google.hybrid',
            ],
            'default_lat': lat,
            'default_lon': lng,
            'default_zoom': _get_geodjango_map_zoom(),
            #'hide_textarea': False,  # TODO: this might be configured in the future
        }
    else:
        default_lon, default_lat = _get_geodjango_map_coords()
        default_zoom = _get_geodjango_map_zoom()


class BaseStackedInline(admin.StackedInline):
    readonly_fields = ['added', 'updated']
    extra = 0


class BaseTabularInline(admin.TabularInline):
    readonly_fields = ['added', 'updated']
    extra = 0
