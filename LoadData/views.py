from django.http import HttpResponse
from django.shortcuts import render
import json

from .models import Experiment, Sample, Dna, Construct, Vector, Measurement
from . import file_reader as fr
from . import search as sch

from .forms import UploadFileForm

def leer(request):

    form = UploadFileForm(request.POST, request.FILES)
    upload = handle_uploaded_file(request.FILES['dataFile'])

    data = json.dumps({
    'status': 'ok',
    'upload_error': upload,
    'posts': request.POST
    })

    fr.MonkeyReader.loadSynergy(request.POST['dataFull'], request.FILES['dataFile'].name)
    return HttpResponse(data, content_type='application/json')

def plot(request):
    # Definir el método de búsqueda: tomar los valores entregados en el request
    # Luego hacer la query y
    pass
    """
    # Para probar que responde"
    data = json.dumps({
    'status': 'Ok',
    'posts': request.POST
    })
    return HttpResponse(data, content_type='application/json')
    """
    json_to_plot = sch.make_search(['', '', '', ''])

def handle_uploaded_file(f):
    with open('../uploads/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
def index(request):
    return render(request, 'index.html', {})

def search(request):
    return render(request, 'search.html', {})
