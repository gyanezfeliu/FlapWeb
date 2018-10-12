from django.shortcuts import render
from . import file_reader as fr
# Create your views here.
def leer(request):
    fr.MonkeyReader.cargarBase()
    return render(request, 'listo.html', {'data': "CTM"})
