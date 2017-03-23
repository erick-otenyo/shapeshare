from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from models import Category, Shapefile, Feature, Attribute, AttributeValue


admin.site.register(Category)
admin.site.register(Shapefile)
admin.site.register(Feature, LeafletGeoAdmin)
admin.site.register(Attribute)
admin.site.register(AttributeValue)

