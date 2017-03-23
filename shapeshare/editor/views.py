from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from shapeshare.shapeShare.models import  Category, Shapefile
from django.http import HttpResponseRedirect
from shapeshare.editor.forms import ImportShapefileForm
from shapeshare.shapefileIO import importer
from django.http import HttpResponseNotFound
from shapeshare.shapefileIO import exporter
from django.db.models import Q


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        categorys = Category.objects.filter(user=request.user)
        shapefile_results = Shapefile.objects.all()
        query = request.GET.get("q")
        if query:
            categorys = category.filter(
                Q(category_name__icontains=query)).distinct()
            shapefile_results = shapefile_results.filter(
                Q(filename__icontains=query)
            ).distinct()
            return render(request, 'index.html', {
                'query':query,
                'categorys': categorys,
                'shapefiles': shapefile_results,
            })
        else:
            return render(request, 'index.html', {'categorys': categorys})
def list_shapefiles(request):
    shapefiles = Shapefile.objects.all().order_by("filename")
    return render(request, "list_shapefiles.html",
                  {'shapefiles': shapefiles})

def category_detail(request,category_id):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        user = request.user
        category= get_object_or_404(Category, pk=category_id)
        return render(request, 'category_detail.html', {'category': category, 'user': user})
    

def import_shapefile(request):
    if request.method == "GET":
        form = ImportShapefileForm()
        return render(request, "import_shapefile.html",
                      {'form'    : form,
                       'err_msg' : None})
    elif request.method == "POST":
        form = ImportShapefileForm(request.POST,
                                   request.FILES)
        if form.is_valid():
            shapefile = request.FILES['import_file']
            encoding  = request.POST['character_encoding']

            err_msg = importer.import_data(shapefile, encoding)

            if err_msg == None:
                return HttpResponseRedirect("/editor")
        else:
            err_msg = None

        return render(request, "import_shapefile.html",
                      {'form'    : form,
                       'err_msg' : err_msg})
    
def export_shapefile(request, shapefile_id):
    try:
        shapefile = Shapefile.objects.get(id=shapefile_id)
    except Shapefile.DoesNotExist:
        return HttpResponseNotFound()
    return exporter.export_data(shapefile)















