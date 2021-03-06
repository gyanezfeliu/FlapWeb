from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Experiment(models.Model):
    name = models.TextField()
    machine = models.TextField()

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

    def __str__(self):
        return self.pubchemid

class LoadProcess(models.Model):
    content = models.TextField()
    file = models.TextField()

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username
