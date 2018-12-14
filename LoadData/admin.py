from django.contrib import admin
from LoadData.models import Experiment, Sample, Dna, Vector, Measurement, Inducer
# Register your models here.
admin.site.register(Experiment)
admin.site.register(Sample)
admin.site.register(Dna)
admin.site.register(Vector)
admin.site.register(Measurement)
admin.site.register(Inducer)
