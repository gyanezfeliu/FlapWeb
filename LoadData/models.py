from django.db import models

# Create your models here.
class Alumno(models.Model):
    nombre = models.CharField(max_length=35)
    apellido = models.CharField(max_length=35)
    #FechaNac = models.DateField()
    edad = models.PositiveSmallIntegerField()

    def NombreCompleto(self):
        nom = "{0}, {1}"
        return nom.format(self.apellido, self.nombre)

    def __str__(self):
        return self.NombreCompleto()
