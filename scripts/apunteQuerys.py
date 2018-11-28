from LoadData.models import Experiment, Sample, Dna, Vector, Measurement, Inducer, LoadProcess

# Retorna un queryset
Experiment.objects.all()
# Retorna el nombre del primero
Experiment.objects.all()[0].name
# Retorna el nombre de la máquina del primero
Experiment.objects.all()[0].machine

# Me da una lista con todos los objetos del queryset
[i.name for i in Dna.objects.all()]

# EJEMPLO QUERY
# Guardar EL OBJETO en una variable a través de obtenerla por ID
e = Experiment.objects.get(pk=8)
s = Sample.objects.get(pk=109)

# Me da el objeto experimento al que corresponde el sample
s.experiment

# Me da los samples que tiene el experimento
e.sample_set.all()

# Filter
# Case sensitive
Sample.objects.filter(media__exact='M9-glicerol')
# Case insensitive
Sample.objects.filter(media__iexact='m9-glicerol')

Inducer.objects.filter(concentration__gt=0.5)
Inducer.objects.filter(concentration__gte=0.5)

Measurement.objects.filter(value__gt=1130000)[0].sample_id.experiment_id.name

# Me entrega el object id
Dna.objects.filter(name__exact='std:RFP/std:YFP/std:CFP')[0]
# Me entrega el id
Dna.objects.filter(name__exact='std:RFP/std:YFP/std:CFP')[0].id
# Me entrega el objeto. SOLO FUNCIONA CUANDO HAY UN SOLO RESULTADO
Dna.objects.filter(name__exact='std:RFP/std:YFP/std:CFP').get()
#Me entrega el queryset
Dna.objects.filter(name__exact='std:RFP/std:YFP/std:CFP')
