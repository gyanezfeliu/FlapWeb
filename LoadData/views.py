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
    to_show = fr.MonkeyReader.test(request)
    return render(request, 'to_plot.html', {'graph': to_show})

def searchRes(request):
    data = json.dumps({
    'status': 'Ok',
    'posts': request.POST
    })
    return HttpResponse(data, content_type='application/json')

def plots(request, id=0):
    return render(request, 'plots.html', {})

def home(request):
    return render(request, 'home.html', {})
def test(request):
    to_show = fr.MonkeyReader.test()

    # return render(request, 'test.html', {'graph': to_show})
    return render(request, 'search.html', {'graph': to_show})
