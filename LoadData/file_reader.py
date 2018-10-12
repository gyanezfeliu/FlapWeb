from .models import Alumno
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
