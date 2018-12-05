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

    def plot(request):

        #### PLOTTING
        """
        # Parameter names:

        param1[0][1][name]	exp_name
        param1[0][2][name]	dna_name
        param1[0][3][name]	med_name
        param1[0][4][name]	str_name
        param1[0][5][name]	ind_name
        param1[0][6][name]	mea_name
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

        fig2 = plt.figure()
        for s in samps:
            df = an.get_measurements(s)
            er = an.expression_rate(df=df, mname='CFP', skip=20)
            plt.plot(er)
        plt.ylabel('Expression rate')
        plt.xlabel('Time (hours)')

        return [fig_to_html(fig1), fig_to_html(fig2)];

    def analysis(request):
        analysis_type = request.POST['param1[]']

        #Datos Query
        dict_query = json.loads(request.POST['param1[0][1][value]'])
        d_query = {}
        d_query['exp_name'] = dict_query['posts']['exp_name']
        d_query['dna_name'] = dict_query['posts']['dna_name']
        d_query['med_name'] = dict_query['posts']['med_name']
        d_query['str_name'] = dict_query['posts']['str_name']
        d_query['ind_name'] = dict_query['posts']['ind_name']
        d_query['mea_name'] = dict_query['posts']['mea_name']

        if analysis_type == "INDUCTIONRHO" or analysis_type == "INDUCTIONALPHA":
            bounds_min = [request.POST['param1[1][1][value]'],
                          request.POST['param1[1][2][value]'],
                          request.POST['param1[1][3][value]']]
            bounds_max = [request.POST['param1[1][4][value]'],
                          request.POST['param1[1][5][value]'],
                          request.POST['param1[1][6][value]']]
            ndt = request.POST['param1[1][7][value]']
            mname1 = request.POST['param1[1][8][value]']

        else:
            mname1 = request.POST['param1[1][1][value]']
        if analysis_type == "INDUCTIONRHO":
            mname2 = request.POST['param1[1][9][value]']

        samps = gen_samps(d_query)

        if analysis_type == 'INDUCTIONRHO':
            concs,my = an.induction_curve(samps, an.ratiometric_rho, bounds=([0,0,0],[3,1,5]), mname1='YFP', mname2='CFP', ndt=2)

        elif analysis_type == 'INDUCTIONALPHA':
            concs,my = an.induction_curve(samps, an.ratiometric_alpha, bounds=([0,0,0],[3,1,5]), mname1='YFP', ndt=2)

        elif analysis_type == 'INDUCTIONMEAN':
            concs,my = an.induction_curve(samps, an.mean_expression, mname1='YFP')


        # fig1 = plt.figure()
        # plt.plot(np.log10(concs), my, '.')
        # plt.xlabel('log(Arabinose conc.) (M)')
        # plt.ylabel('Mean fluorescence (AU)')
        #
        # #### CURVE FIT
        # z,_= curve_fit(an.hill, concs, my, bounds=([0,0,0,1],[1,1,1e-2,2]))
        # a = z[0]
        # b = z[1]
        # k = z[2]
        # n = z[3]
        #
        # x = np.linspace(-6,-2,200)
        # fig2 = plt.figure()
        # plt.plot(x, an.hill(10**x,a,b,k,n), '-.')
        # plt.plot(np.log10(concs),my,'r.')
        #
        # return [fig_to_html(fig1), fig_to_html(fig2)];


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

    def gen_samps(d_query):
        if d_query['exp_name'] != '' and d_query['dna_name'] != '' and d_query['med_name'] != '' and d_query['str_name'] != '':
            samps = Sample.objects.filter(experiment__name__exact=d_query['exp_name'],
                                          vector__dna__name__exact=d_query['dna_name'],
                                          media__exact=d_query['med_name'],
                                          strain__exact=d_query['str_name'])

        elif d_query['exp_name'] == '' and d_query['dna_name'] != '' and d_query['med_name'] != '' and d_query['str_name'] != '':
            samps = Sample.objects.filter(vector__dna__name__exact=d_query['dna_name'],
                                          media__exact=d_query['med_name'],
                                          strain__exact=d_query['str_name'])

        elif d_query['exp_name'] == '' and d_query['dna_name'] != '' and d_query['med_name'] != '' and d_query['str_name'] == '':
            samps = Sample.objects.filter(vector__dna__name__exact=d_query['dna_name'],
                                          media__exact=d_query['med_name'])

        elif d_query['exp_name'] == '' and d_query['dna_name'] != '' and d_query['med_name'] == '' and d_query['str_name'] != '':
            samps = Sample.objects.filter(vector__dna__name__exact=d_query['dna_name'],
                                          strain__exact=d_query['str_name'])

        elif d_query['exp_name'] == '' and d_query['dna_name'] != '' and d_query['med_name'] == '' and d_query['str_name'] == '':
            samps = Sample.objects.filter(vector__dna__name__exact=d_query['dna_name'])

        elif d_query['exp_name'] == '' and d_query['dna_name'] == '' and d_query['med_name'] != '' and d_query['str_name'] != '':
            samps = Sample.objects.filter(media__exact=d_query['med_name'],
                                          strain__exact=d_query['str_name'])

        elif d_query['exp_name'] == '' and d_query['dna_name'] == '' and d_query['med_name'] != '' and d_query['str_name'] == '':
            samps = Sample.objects.filter(media__exact=d_query['med_name'])

        elif d_query['exp_name'] == '' and d_query['dna_name'] == '' and d_query['med_name'] == '' and d_query['str_name'] != '':
            samps = Sample.objects.filter(strain__exact=d_query['str_name'])

        # If no experiment, dna, media or strain selected
        #if d_query['exp_name'] == '' and d_query['dna_name'] == '' and d_query['med_name'] == '' and d_query['str_name'] == '':
        else:
            if d_query['ind_name'] != '':
                samps = set([i.sample for i in Inducer.objects.filter(pubchemid__exact=d_query['ind_name'])])
                if d_query['mea_name'] != '':
                    samps_ids = [s.id for s in samps]
                    samps = set([m.sample for m in Measurement.objects.filter(name__exact=d_query['mea_name'], sample__id__in=samps_ids)])
            else:
                if d_query['mea_name'] != '':
                    samps = set([m.sample for m in Measurement.objects.filter(name__exact=d_query['mea_name'])])

            return samps

        samps_ids = [s.id for s in samps]

        if d_query['ind_name'] != '':
            samps = set([i.sample for i in Inducer.objects.filter(pubchemid__exact=d_query['ind_name'], sample__id__in=samps_ids)])
            samps_ids = [s.id for s in samps]
            if d_query['mea_name'] != '':
                samps = set([m.sample for m in Measurement.objects.filter(name__exact=d_query['mea_name'], sample__id__in=samps_ids)])
        else:
            if d_query['mea_name'] != '':
                samps = set([m.sample for m in Measurement.objects.filter(name__exact=d_query['mea_name'], sample__id__in=samps_ids)])
        return samps
