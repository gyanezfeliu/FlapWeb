# File reader reads and loads the data into the DB
# Method loadSynerty is called from views.leer and 

# Models
from .models import Experiment
from .models import Sample
from .models import Dna
from .models import Construct
from .models import Vector
from .models import Measurement

# Data handling
import pandas as pd
import numpy as np
import json
import os
import openpyxl as opxl
from itertools import islice
import csv

#Leo el archivo y saco la información del archivo
# Asumiré que ya lo hice
class MonkeyReader():

    def loadSynergy(metadata, file_name):

        # Cargo Metadata
        file_route = '../uploads/' + file_name
        #data_str = open(metadata).read()
        data = json.loads(metadata)
        df_json = pd.DataFrame(data)
        columns = [x+str(y) for x in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] for y in range(1,13)]
        df_json.columns = columns
        df_json.index = ['Strain', 'Media', 'DNA']

        experiment_name = os.path.basename(file_route).split('/')[-1].split('.')[0]
        medidas = ['OD600:600', 'RFP-YFP:585/10,620/15', 'RFP-YFP:500/27,540/25', 'CFP:420/50,485/20', 'Results']

        wb = opxl.load_workbook(filename = file_route, data_only=True)
        ws = wb['Data']
        machine_name = ws['B'][8].value + str(ws['B'][9].value)

        name_map = {'OD600:600':'OD', 'RFP-YFP:500/27,540/25':'YFP', 'CFP:420/50,485/20':'CFP',
        'RFP-YFP:585/10,620/15':'RFP'}

        # Cargo data
        lista_rows = [(celda.value, celda.row, opxl.utils.column_index_from_string(celda.column))
                    for celda in ws['A']
                    if celda.value in medidas]

        ws.delete_rows(0, 48)

        lista_rows2 = [(celda.value, celda.row, opxl.utils.column_index_from_string(celda.column))
                    for celda in ws['A']
                    if celda.value in medidas]

        data = ws.values
        cols = next(data)[1:]
        data = list(data)
        idx = [r[0] for r in data]
        data = (islice(r, 1, None) for r in data)
        df = pd.DataFrame(data, columns=cols)

        df.columns = df.columns.map(lambda x: x.replace('T° OD600:600', 'T°'))

        df_OD = pd.DataFrame(df.iloc[0:lista_rows2[0][1] - 3])
        df_OD['name'] = 'OD'

        df_RFP = pd.DataFrame(df.iloc[lista_rows2[0][1] + 1:lista_rows2[1][1] - 3])
        df_RFP['name'] = 'RFP'
        df_RFP.index = range(97)

        df_YFP = pd.DataFrame(df.iloc[lista_rows2[1][1] + 1:lista_rows2[2][1] - 3])
        df_YFP['name'] = 'YFP'
        df_YFP.index = range(97)

        df_CFP = pd.DataFrame(df.iloc[lista_rows2[2][1] + 1:lista_rows2[3][1] - 3])
        df_CFP['name'] = 'CFP'
        df_CFP.index = range(97)

        df_OD = df_OD.drop([96])

        # 1) Experiment
        e = Experiment(name=experiment_name, machine=machine_name)
        e.save()

        # 2) Sample
        # get experiment_id
        # row, col, media, strain

        # 3) DNA
        # name

        # Empiezo a recorrer los platillos que están en df_json: indexes: strain, media, dna:
        for col_name, col_serie in df_json.iteritems():
            # experiment_id
            plate_row = col_name[0]
            plate_col = col_name[1:]
            st = col_serie['Strain']['value']
            med = col_serie['Media']['value']

            s = Sample(experiment_id=e, row=plate_row, col=plate_col, media=med, strain=st, IPTG=0, aTc=0)
            s.save()

            DNA_name = col_serie['DNA']['value']
            d = Dna(name=DNA_name, sequence='AATG')
            d.save()

            # 4) Measurement
            # name, value, time
            for i, value in enumerate(df_OD[col_name]):
                nam = df_OD['name'].iloc[i]
                val = value
                t = df_OD['Time'].iloc[i]

                m = Measurement(name=nam, value=val, time=t, sample_id=s)
                m.save()
