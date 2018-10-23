from .models import Experiment
from .models import Sample
from .models import Dna
from .models import Construct
from .models import Vector
from .models import Measurement
import csv

#Leo el archivo y saco la información del archivo
# Asumiré que ya lo hice
class MonkeyReader():

    def cargarBase():
        name = 'pepito'
        last = 'los palotes'
        age = 32
        a1 = Alumno(nombre = name, apellido = last, edad = age)
        a1.save()
