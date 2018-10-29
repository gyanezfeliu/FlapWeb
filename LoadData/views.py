from django.http import HttpResponse
from django.shortcuts import render
import json

from .models import Experiment
from .models import Sample
from .models import Dna
from .models import Construct
from .models import Vector
from .models import Measurement
from . import file_reader as fr

from .forms import UploadFileForm


# Create your views here.
def leer(request):
    fr.MonkeyReader.loadSynergy()
    form = UploadFileForm(request.POST, request.FILES)
    upload = handle_uploaded_file(request.FILES['dataFile'])

    data = json.dumps({
    'status': 'ok',
    'upload_error': upload,
    'posts': request.POST
    })

    return HttpResponse(data, content_type='application/json')

def index(request):
    return render(request, 'index.html', {})


def handle_uploaded_file(f):
    with open('../uploads/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
