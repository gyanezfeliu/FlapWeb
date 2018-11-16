from django.db import models

# Create your models here.
class Experiment(models.Model):
    name = models.TextField()
    machine = models.TextField()

class Sample(models.Model):
    experiment_id = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    row = models.TextField()
    col = models.IntegerField()
    media = models.TextField()
    strain = models.TextField()

class Dna(models.Model):
    name = models.TextField()
    sboluri = models.TextField()

class Vector(models.Model):
    dna_id = models.ForeignKey(Dna, on_delete=models.CASCADE)
    sample_id = models.ForeignKey(Sample, on_delete=models.CASCADE)

class Measurement(models.Model):
    sample_id = models.ForeignKey(Sample, on_delete=models.CASCADE)
    name = models.TextField()
    value = models.FloatField()
    time = models.FloatField()

class Inducer(models.Model):
    sample_id = models.ForeignKey(Sample, on_delete=models.CASCADE)
    concentration = models.FloatField()
    puchemid = models.TextField()

class LoadProcess(models.Model):
    content = models.TextField()
    file = models.TextField()
