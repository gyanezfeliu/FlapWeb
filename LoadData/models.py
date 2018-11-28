from django.db import models

# Create your models here.
class Experiment(models.Model):
    name = models.TextField()
    machine = models.TextField()
    #  This is used to add Experiments through the shell
    def __str__(self):
        return self.name

class Sample(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    row = models.TextField()
    col = models.IntegerField()
    media = models.TextField()
    strain = models.TextField()

    def __str__(self):
        return ("Row: {}, Col: {}".format(self.row, self.col))

class Dna(models.Model):
    name = models.TextField()
    sboluri = models.TextField()

    def __str__(self):
        return self.name

class Vector(models.Model):
    dna = models.ForeignKey(Dna, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)

class Measurement(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    name = models.TextField()
    value = models.FloatField()
    time = models.FloatField()

    def __str__(self):
        return self.name

class Inducer(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    concentration = models.FloatField()
    pubchemid = models.TextField()

    def __self__(self):
        return self.pubchemib

class LoadProcess(models.Model):
    content = models.TextField()
    file = models.TextField()
