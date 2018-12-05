# File reader reads and loads the data into the DB
# Method loadSynerty is called from views.leer and

# Models
from .models import Experiment, Sample, Dna, Vector, Measurement, Inducer, LoadProcess
# Data handling
import pandas as pd
import numpy as np
import json
import os
import openpyxl as opxl
from itertools import islice
import csv
import subprocess
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from mpld3 import fig_to_html, plugins
from mpld3.plugins import PointLabelTooltip

from . import analysis as an

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

    def test():

        #### INDUCTION CURVE

        samps = Sample.objects.filter(vector__dna__name__exact='T6')
        concs,my = an.induction_curve(samps, an.ratiometric_rho, bounds=([0,0,0],[3,1,5]), mname1='YFP', mname2='CFP', ndt=2)

        # fig = plt.figure()
        # plt.plot(np.log10(concs), my, '.')
        # plt.xlabel('log(Arabinose conc.) (M)')
        # plt.ylabel('Mean fluorescence (AU)')
        # return fig_to_html(fig);

        z,_= curve_fit(an.hill, concs, my, bounds=([0,0,0,1],[1,1,1e-2,2]))
        a = z[0]
        b = z[1]
        k = z[2]
        n = z[3]

        x = np.linspace(-6,-2,200)
        fig = plt.figure()
        plt.plot(x, an.hill(10**x,a,b,k,n), '-.')
        plt.plot(np.log10(concs),my,'r.')
        return fig_to_html(fig);

        #### HEATMAP

        # samps = Sample.objects.filter(vector__dna__name__exact='DBD2', experiment__name__exact='Tim210813')
        # hm_rho,x,y = an.induction_heatmap(samps, an.ratiometric_rho, nbins=8, bounds=([0,0,0],[3,1,5]), mname1='YFP', mname2='CFP', ndt=2)
        #
        # fig = plt.figure()
        # plt.pcolormesh(x[1:],y[1:],hm_rho)
        # plt.colorbar()
        # plt.xlabel('log(C6 conc.) (M)')
        # plt.ylabel('log(Arabinose conc.) (M)')
        # return fig_to_html(fig);


        #### KYMOGRAPH

        # samps = Sample.objects.filter(vector__dna__name__exact='T6')
        #
        # hm,x,y = an.kymograph(samps, an.expression_rate, mname='CFP', skip=10)
        #
        # fig = plt.figure()
        # plt.pcolor(hm)
        # plt.colorbar()
        # return fig_to_html(fig);
