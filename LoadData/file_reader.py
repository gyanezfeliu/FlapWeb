# File reader reads and loads the data into the DB
# Method loadSynerty is called from views.leer and

# Models
from .models import LoadProcess

# Data handling
import pandas as pd
import numpy as np
import json
import os
import openpyxl as opxl
from itertools import islice
import csv
import subprocess

#Leo el archivo y saco la información del archivo
# Asumiré que ya lo hice
class MonkeyReader():

    def loadSynergy(metadata, file_name):

        file_route= '../uploads/'+file_name
        lp = LoadProcess(content=metadata, file=file_route)
        lp.save()
        subprocess.Popen(['python', 'manage.py', 'runscript', 'load_DB', '--script-args', str(lp.id)], stdout=subprocess.PIPE)

    def massUpload():
        subprocess.Popen(['python', 'manage.py', 'runscript', 'massiveUpload'], stdout=subprocess.PIPE)
