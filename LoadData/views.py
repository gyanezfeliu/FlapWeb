from django.http import HttpResponse
from django.shortcuts import render
import json

from .models import Experiment, Sample, Dna, Vector, Measurement, Inducer
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

def massUpload(request):
    fr.MonkeyReader.massUpload()
    data = json.dumps({'Status': "Your data is being loaded"})
    return HttpResponse(data, content_type='application/json')

def handle_uploaded_file(f):
    with open('../uploads/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def index(request):
    return render(request, 'index.html', {})

def search(request):
    return render(request, 'search.html', {})

def plot(request):
    to_show = fr.MonkeyReader.plot(request)
    return render(request, 'to_plot.html', {'graph': to_show})

def to_analysis(request):
    # Recibo los datos desde Search como request
    data = json.dumps({
    'posts': request.POST
    })
    return render(request, 'analysis.html', {'from_search': data})

    # Esto tengo que hacerlo desde otro método, desde el $.post que haré desde
    # analysis.html, en donde enviaré formulario con la información de la query
    # y con la información del análisis. Debo por lo tanto cambiar el nombre a
    # ESTE método (arriba) y desde el otro método llamar a MonkeyReader.analysis
    # desde analysis.html para renderizar en el mismo analysis.html el gráfico
    # resultante, igual que como hice en search.

def make_analysis(request):
    to_analyse = fr.MonkeyReader.analysis(request)

    ## PARA INDUCTION CURVE
    #return render(request, 'analysis_made.html', {'graph': to_analyse})
    return HttpResponse(to_analyse, content_type='application/json')

def plots(request, id=0):
    return render(request, 'plots.html', {})

def home(request):
    return render(request, 'home.html', {})
def test(request):
    to_show = fr.MonkeyReader.test()

    # return render(request, 'test.html', {'graph': to_show})
    return render(request, 'search.html', {'graph': to_show})
