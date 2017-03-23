import os, os.path, tempfile, zipfile
import shutil
from osgeo import ogr
from osgeo import osr
from django.http import FileResponse


from shapeshare.shapeShare import utils


def export_data(shapefile):
    dst_dir = tempfile.mkdtemp()
    dst_file = str(os.path.join(dst_dir, shapefile.filename))
    dst_spatial_ref = osr.SpatialReference()
    dst_spatial_ref.ImportFromWkt(shapefile.srs_wkt)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    datasource = driver.CreateDataSource(dst_file)
    layer = datasource.CreateLayer(str(shapefile.filename),
                                   dst_spatial_ref)
    for attr in shapefile.attribute_set.all():
        field = ogr.FieldDefn(str(attr.name), attr.type)
        field.SetWidth(attr.width)
        field.SetPrecision(attr.precision)
        layer.CreateField(field)
    # Create our coordinate transformation.

    src_spatial_ref = osr.SpatialReference()
    src_spatial_ref.ImportFromEPSG(4326)

    coord_transform = osr.CoordinateTransformation(
                        src_spatial_ref, dst_spatial_ref)
    
    # Calculate which geometry field holds the shapefile's geometry.

    geom_field = utils.calc_geometry_field(shapefile.geom_type)
    
    # Export the shapefile's features.

    for feature in shapefile.feature_set.all():
        geometry = getattr(feature, geom_field)
        geometry = utils.unwrap_geos_geometry(geometry)

        dst_geometry = ogr.CreateGeometryFromWkt(geometry.wkt)
        dst_geometry.Transform(coord_transform)

        dst_feature = ogr.Feature(layer.GetLayerDefn())
        dst_feature.SetGeometry(dst_geometry)

        layer.CreateFeature(dst_feature)
        dst_feature.Destroy()
        
    datasource.Destroy()

    # Compress the shapefile as a ZIP archive.

    temp = tempfile.TemporaryFile()
    zip = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)

    shapefile_name = os.path.splitext(shapefile.filename)[0]

    for fName in os.listdir(dst_dir):
        zip.write(os.path.join(dst_dir, fName), fName)

    zip.close()
    shutil.rmtree(dst_dir)

    # Return the ZIP archive back to the caller.

    temp.flush()
    temp.seek(0)

    response = FileResponse(temp)
    response['Content-type'] = "application/zip"
    response['Content-Disposition'] = "attachment; filename=" + shapefile_name + ".zip"
    return response