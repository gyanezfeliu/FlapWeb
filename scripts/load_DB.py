# Models
from LoadData.models import Experiment, Sample, Dna, Vector, Measurement, Inducer, LoadProcess
# Data handling
import pandas as pd
import numpy as np
import json
import os
import openpyxl as opxl
from itertools import islice
import csv
import subprocess


def fix_synergy_time(t_old):
    t_new = np.array([])
    for i, value in enumerate(t_old):
        if i > 0:
            if t_old[i].hour < t_old[i - 1].hour:
                t_new = np.append(t_new, [24 + value.hour + value.minute/60 + value.second/3600])
            else:
                t_new = np.append(t_new, [value.hour + value.minute/60 + value.second/3600])
        else:
            t_new = np.append(t_new, [value.hour + value.minute/60 + value.second/3600])
    return t_new

def find_index(col, measures):
    return [(celda.value, celda.row, opxl.utils.column_index_from_string(celda.column))
        for celda in col
        if celda.value in measures]

def run(*args):

    id_data = int(args[0])
    metadata = LoadProcess.objects.get(id=id_data).content
    file_route = LoadProcess.objects.get(id=id_data).file

    # Cargo Metadata
    data = json.loads(metadata)
    df_json = pd.DataFrame(data)
    columns = [x+str(y) for x in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] for y in range(1,13)]
    df_json.columns = columns
    df_json.index = ['Strain', 'Media', 'DNA']

    #If el usuario no me da el nombre del experimento, le pongo el nombre del archivo de datos
    experiment_name = os.path.basename('ExpTest.xlsx').split('/')[-1].split('.')[0]

    # Estas medidas deben venir dadas por el usuario y yo debo sumar "Results"
    medidas = ['OD600:600', 'RFP-YFP:585/10,620/15', 'RFP-YFP:500/27,540/25', 'CFP:420/50,485/20', 'Results']

    wb = opxl.load_workbook(filename = file_route, data_only=True)
    ws = wb['Data']
    machine_name = ws['B'][8].value + str(ws['B'][9].value)

    # Completar esta lista para todos los posibles valores de longitudes de onda
    name_map = {'OD600:600':'OD', 'RFP-YFP:500/27,540/25':'YFP', 'CFP:420/50,485/20':'CFP',
    'RFP-YFP:585/10,620/15':'RFP'}

    lista_rows = find_index(ws['A'], medidas)
    ws.delete_rows(0, lista_rows[0][1] - 1)
    lista_rows2 = find_index(ws['A'], medidas)


    # Aquí empiezo el ciclo de armar el array con las series de tiempo

    # array consolidado que tiene los nombres para cada measurement
    #names = np.array([]).astype('object')
    names = np.array([], dtype='str')
    # array consolidado que tiene los measurement
    data = np.array([])
    # array consolidado que tiene los tiempos de los measurements
    times = np.array([])

    # datos que fueron extraído del excel del lector de placas
    raw_data = np.array(list(ws.values))
    #raw_data = np.delete(raw_data, 2, 1)

    # cantidad de los datos que se tomaron
    dim = lista_rows2[1][1] - lista_rows2[0][1] - 4

    # Paso los datos a un array
    for i in range(len(lista_rows2)-1):
        # names for the measurements
        name = np.zeros(dim)
        name = name.astype('str')
        name[:] = name_map[lista_rows2[i][0]]
        names = np.concatenate((names, name), axis=0)
        
        # AHORA ASUME QUE ES PARA TODOS LOS POCILLOS (A1 hasta H12), LUEGO DEBE CONSIDERAR SOLO LOS INDICADOS 
        # POR EL USUARIO
        # measurements
        data_array = raw_data[lista_rows2[0][1]+2:lista_rows2[1][1]-2, 3:].astype('float64')
        if i == 0:
            data = data_array
        else:
            data = np.concatenate((data, data_array), axis=0)
        
        # times for the measurements
        time = raw_data[lista_rows2[0][1]+2:lista_rows2[1][1]-2, 1]
        time = fix_synergy_time(time)
        times = np.concatenate((times, time), axis=0)

    # índice para recorrer las columnas del array de los datos
    max_cols = len(df_json.columns)
    col_ind = 0
    max_dind = len(data[:, 0])
    dind = 0

    # HACER UN IF DE VERIFICACION DE QUE LAS DIMENSIONES CALZAN
        # max_cols con el numero de cols de data
        # len(data[:, 0]) == dim * len(np.unique(names))


    # GUARDO LOS MEASUREMENT EN LA BD

    # 1) Experiment
    e = Experiment(name=experiment_name, machine=machine_name)
    e.save()

    # Empiezo a recorrer los platillos que están en df_json: indexes: strain, media, dna:
    #col_name corresponde a A1, A2, ..., H12
    #col_serie corresponde a la metadata para esa celda, por ej:
    '''
    Strain          {'name': 'data', 'value': 'None'}
    Media     {'name': 'data', 'value': 'M9-glucosa'}
    DNA             {'name': 'data', 'value': 'None'}
    '''
    for col_name, col_serie in df_json.iteritems():
        dind = 0
        
        # 2) Sample
        plate_row = col_name[0]
        plate_col = col_name[1:]
        st = col_serie['Strain']['value']
        med = col_serie['Media']['value']
        s = Sample(experiment=e, row=plate_row, col=plate_col, media=med, strain=st)
        s.save()

        # 3) DNA
        existing_dna = [i.name for i in Dna.objects.all()]
        DNA_name = col_serie['DNA']['value']

        if DNA_name != 'None':
            if DNA_name not in existing_dna:
                d = Dna(name=DNA_name, sboluri='')
                d.save()
                # 4) Vector
                v = Vector(dna=d, sample=s)
                v.save()
            else:
                d = Dna.objects.filter(name__exact=DNA_name)[0]
                v = Vector(dna=d, sample=s)
                v.save()

        # 5) Measurements
        while(dind < max_dind):
        #One measure, of a given measurement name(OD, CFP, etc), at a given time from a given well (A1,.., H12)
            t = times[dind]
            n = names[dind]
            v = data[:, col_ind][dind]
            m = Measurement(sample=s, name=n, value=v, time=t)
            m.save()
            dind += 1
        col_ind += 1