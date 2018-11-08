# Models
from LoadData.models import Experiment, Sample, Dna, Construct, Vector, Measurement, LoadProcess
# Data handling
import pandas as pd
import numpy as np
import json
import os
import openpyxl as opxl
from itertools import islice
import csv
import subprocess

#print(sys.argv)
def run(*args):
    print(int(args[0]))
