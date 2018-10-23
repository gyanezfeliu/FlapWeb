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
# Create your views here.
def leer(request):
    fr.MonkeyReader.cargarBase()
    data = json.dumps({'status': 'ok'})

    return HttpResponse(data, content_type='application/json')

def index(request):
    return render(request, 'index.html', {})
