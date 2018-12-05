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

    def test(request):

        #### PLOTTING

        """
        param1[0][1][name]	exp_name
        param1[0][2][name]	dna_name
        param1[0][3][name]	med_name
        param1[0][4][name]	str_name
        param1[0][5][name]	ind_name
        param1[0][6][name]	mea_name
        param1[0][6][value]	OD
        """
        exp_name = request.POST['param1[0][1][value]']
        dna_name = request.POST['param1[0][2][value]']
        med_name = request.POST['param1[0][3][value]']
        str_name = request.POST['param1[0][4][value]']
        ind_name = request.POST['param1[0][5][value]']
        mea_name = request.POST['param1[0][6][value]']

        samps = Sample.objects.filter(vector__dna__name__exact=dna_name, strain__exact=str_name)
        #samps = Sample.objects.filter(vector__dna__name__exact='std:RFP/std:YFP/std:CFP', strain__exact='Top10')

        fig1 = plt.figure()
        for s in samps:
            df = an.get_measurements(s)
            y = df[df['name']=='YFP']['value']
            c = df[df['name']=='CFP']['value']
            r = df[df['name']=='RFP']['value']

            plt.plot(y, r, '.')
        plt.xlabel('Time (hours)')
        plt.ylabel('Expression (AU)')
        #return fig_to_html(fig1)


        fig2 = plt.figure()
        for s in samps:
            df = an.get_measurements(s)
            er = an.expression_rate(df=df, mname='CFP', skip=20)
            plt.plot(er)
        plt.ylabel('Expression rate')
        plt.xlabel('Time (hours)')

        return [fig_to_html(fig1), fig_to_html(fig2)];

        #### INDUCTION CURVE
        #
        # samps = Sample.objects.filter(vector__dna__name__exact='T6')
        # concs,my = an.induction_curve(samps, an.ratiometric_rho, bounds=([0,0,0],[3,1,5]), mname1='YFP', mname2='CFP', ndt=2)
        #
        # fig = plt.figure()
        # plt.plot(np.log10(concs), my, '.')
        # plt.xlabel('log(Arabinose conc.) (M)')
        # plt.ylabel('Mean fluorescence (AU)')
        # return fig_to_html(fig);



        #### CURVE FIT
        # z,_= curve_fit(an.hill, concs, my, bounds=([0,0,0,1],[1,1,1e-2,2]))
        # a = z[0]
        # b = z[1]
        # k = z[2]
        # n = z[3]
        #
        # x = np.linspace(-6,-2,200)
        # fig = plt.figure()
        # plt.plot(x, an.hill(10**x,a,b,k,n), '-.')
        # plt.plot(np.log10(concs),my,'r.')
        # return fig_to_html(fig);

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
