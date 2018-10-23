from django.db import models

# Create your models here.
class Experiment(models.Model):
    name = models.TextField()
    machine = models.TextField()

class Sample(models.Model):
    #experiment_id = models.IntegerField()
    experiment_id = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    row = models.IntegerField()
    col = models.IntegerField()
    media = models.TextField()
    strain = models.TextField()
    IPTG = models.FloatField()
    aTc = models.FloatField()

class Dna(models.Model):
    name = models.TextField()
    sequence = models.TextField()

class Construct(models.Model):
    dna_id = models.ForeignKey(Dna, on_delete=models.CASCADE)

class Vector(models.Model):
    dna_id = models.ForeignKey(Dna, on_delete=models.CASCADE)
    sample_id = models.ForeignKey(Sample, on_delete=models.CASCADE)

class Measurement(models.Model):
    name = models.TextField()
    value = models.FloatField()
    time = models.FloatField()
    sample_id = models.ForeignKey(Sample, on_delete=models.CASCADE)
