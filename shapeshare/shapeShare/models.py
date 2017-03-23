from __future__ import unicode_literals

from django.contrib.auth.models import Permission, User
from django.contrib.gis.db import models



class Category(models.Model):
    user = models.ForeignKey(User, default=1)
    category_name=models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.category_name


class Shapefile(models.Model):
    category=models.ForeignKey(Category,null=True)
    filename = models.CharField(max_length=255)
    srs_wkt = models.CharField(max_length=255)
    geom_type = models.CharField(max_length=50)
    encoding = models.CharField(max_length=20)

    def __unicode__(self):
        return self.filename
    
        
class Attribute(models.Model):
    shapefile = models.ForeignKey(Shapefile,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.IntegerField()
    width = models.IntegerField()
    precision = models.IntegerField()

    def __unicode__(self):
        return self.name


class Feature(models.Model):
    shapefile = models.ForeignKey(Shapefile,on_delete=models.CASCADE)
    geom_point = models.PointField(srid=4326, blank=True, null=True)
    geom_multipoint = models.MultiPointField(srid=4326, blank=True, null=True)
    geom_multilinestring = models.MultiLineStringField(srid=4326, blank=True, null=True)
    geom_multipolygon = models.MultiPolygonField(srid=4326, blank=True, null=True)
    geom_geometrycollection = models.GeometryCollectionField(srid=4326, blank=True, null=True)

    def __unicode__(self):
        return str(self.id)
    
    
class AttributeValue(models.Model):
    feature = models.ForeignKey(Feature,on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute)
    value = models.CharField(max_length=255, blank=True,  null=True)

    def __unicode__(self):
        return self.value