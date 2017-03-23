# URLConf for the shapeEditor.editor application.
from django.conf.urls import url
from . import views

app_name='editor'

urlpatterns = [
    
    url(r'^$', views.index, name='index'),
    url(r'^shp_list/$', views.list_shapefiles, name='list_shapefiles'),
    url(r'^import$', views.import_shapefile, name='import_shapefile'),
    url(r'^(?P<category_id>[0-9]+)/$', views.category_detail, name='category_detail'),
    url(r'^export/(?P<shapefile_id>\d+)$', views.export_shapefile, name='export_shapefile'),

]


