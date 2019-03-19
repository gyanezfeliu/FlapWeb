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

class MonkeyReader():

    def loadSynergy(metadata, file_name):

        file_route= '../uploads/'+file_name
        lp = LoadProcess(content=metadata, file=file_route)
        lp.save()
        subprocess.Popen(['python', 'manage.py', 'runscript', 'load_DB', '--script-args', str(lp.id)], stdout=subprocess.PIPE)

    def massUpload():
        subprocess.Popen(['python', 'manage.py', 'runscript', 'massiveUpload'], stdout=subprocess.PIPE)

    def get_samps(d_query):

        if d_query['exp_name'] != '':
            d_query['exp_name'] = Experiment.objects.get(id=int(d_query['exp_name'])).name
        if d_query['dna_name'] != '':
            d_query['dna_name'] = Dna.objects.get(id=int(d_query['dna_name'])).name
        if d_query['med_name'] != '':
            d_query['med_name'] = Sample.objects.get(id=int(d_query['med_name'])).media
        if d_query['str_name'] != '':
            d_query['str_name'] = Sample.objects.get(id=int(d_query['str_name'])).strain
        if d_query['ind_name'] != '':
            d_query['ind_name'] = Inducer.objects.get(id=int(d_query['ind_name'])).pubchemid
        if d_query['mea_name'] != '':
            d_query['mea_name'] = Measurement.objects.get(id=int(d_query['mea_name'])).name


        if d_query['exp_name'] != '' and d_query['dna_name'] != '' and d_query['med_name'] != '' and d_query['str_name'] != '':
            samps = Sample.objects.filter(experiment__name__iexact=d_query['exp_name'],
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

        elif d_query['exp_name'] != '' and d_query['dna_name'] != '' and d_query['med_name'] != '' and d_query['str_name'] == '':
            samps = Sample.objects.filter(experiment__name__iexact=d_query['exp_name'],
                                          vector__dna__name__exact=d_query['dna_name'],
                                          media__exact=d_query['med_name'])

        elif d_query['exp_name'] != '' and d_query['dna_name'] != '' and d_query['med_name'] == '' and d_query['str_name'] != '':
            samps = Sample.objects.filter(experiment__name__iexact=d_query['exp_name'],
                                          vector__dna__name__exact=d_query['dna_name'],
                                          strain__exact=d_query['str_name'])

        elif d_query['exp_name'] != '' and d_query['dna_name'] != '' and d_query['med_name'] == '' and d_query['str_name'] == '':
            samps = Sample.objects.filter(experiment__name__iexact=d_query['exp_name'],
                                          vector__dna__name__exact=d_query['dna_name'])

        elif d_query['exp_name'] != '' and d_query['dna_name'] == '' and d_query['med_name'] != '' and d_query['str_name'] != '':
            samps = Sample.objects.filter(experiment__name__iexact=d_query['exp_name'],
                                          media__exact=d_query['med_name'],
                                          strain__exact=d_query['str_name'])

        elif d_query['exp_name'] != '' and d_query['dna_name'] == '' and d_query['med_name'] != '' and d_query['str_name'] == '':
            samps = Sample.objects.filter(experiment__name__iexact=d_query['exp_name'],
                                          media__exact=d_query['med_name'])

        elif d_query['exp_name'] != '' and d_query['dna_name'] == '' and d_query['med_name'] == '' and d_query['str_name'] != '':
            samps = Sample.objects.filter(experiment__name__iexact=d_query['exp_name'],
                                          strain__exact=d_query['str_name'])

        elif d_query['exp_name'] != '' and d_query['dna_name'] == '' and d_query['med_name'] == '' and d_query['str_name'] == '':
            samps = Sample.objects.filter(experiment__name__iexact=d_query['exp_name'])

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

    def plot(request):
        # Makes no sense to filter by measure name since this method gets all measurement names
        d_query = {}
        d_query['exp_name'] = request.POST['param1[0][1][value]']
        d_query['dna_name'] = request.POST['param1[0][2][value]']
        d_query['med_name'] = request.POST['param1[0][3][value]']
        d_query['str_name'] = request.POST['param1[0][4][value]']
        d_query['ind_name'] = request.POST['param1[0][5][value]']
        d_query['mea_name'] = request.POST['param1[0][6][value]']

        samps = MonkeyReader.get_samps(d_query)

        fig1 = plt.figure()
        for s in samps:
            df = an.get_measurements(s)
            y = df[df['name']=='YFP']['value']
            c = df[df['name']=='CFP']['value']
            r = df[df['name']=='RFP']['value']

            # By default it plots YFP vs RFP, should be able to change it interactively
            plt.plot(y, r, '.')
        plt.xlabel('RFP Expression (AU)')
        plt.ylabel('YFP Expression (AU)')

        fig2 = plt.figure()
        for s in samps:
            df = an.get_measurements(s)
            er = an.expression_rate(df=df, mname=d_query['mea_name'], skip=20)
            # er = an.expression_rate(df=df, mname='CFP', skip=20)
            plt.plot(er)
        plt.ylabel("{} Expression rate".format(d_query['mea_name']))
        plt.xlabel('Time (hours)')

        return [fig_to_html(fig2), fig_to_html(fig1)];

    def analysis_induction(request):
        analysis_type = request.POST['param1[]']

        dict_query = json.loads(request.POST['param1[0][1][value]'])
        d_query = {}
        # d_query['exp_name'] = dict_query['posts']['exp_name']
        # d_query['dna_name'] = dict_query['posts']['dna_name']
        # d_query['med_name'] = dict_query['posts']['med_name']
        # d_query['str_name'] = dict_query['posts']['str_name']
        # d_query['ind_name'] = dict_query['posts']['ind_name']
        # d_query['mea_name'] = dict_query['posts']['mea_name']
        d_query['exp_name'] = dict_query['posts']['experiment']
        d_query['dna_name'] = dict_query['posts']['dna']
        d_query['med_name'] = dict_query['posts']['media']
        d_query['str_name'] = dict_query['posts']['strain']
        d_query['ind_name'] = dict_query['posts']['inducer']
        d_query['mea_name'] = dict_query['posts']['measurement_name']

        if analysis_type == "INDUCTIONRHO" or analysis_type == "INDUCTIONALPHA":
            bounds_min = [int(request.POST['param1[1][1][value]']),
                          int(request.POST['param1[1][2][value]']),
                          int(request.POST['param1[1][3][value]'])]
            bounds_max = [int(request.POST['param1[1][4][value]']),
                          int(request.POST['param1[1][5][value]']),
                          int(request.POST['param1[1][6][value]'])]
            ndt = int(request.POST['param1[1][7][value]'])
            mname1 = request.POST['param1[1][8][value]']
            if analysis_type == "INDUCTIONRHO":
                mname2 = request.POST['param1[1][9][value]']
        else:
            mname1 = request.POST['param1[1][1][value]']

        samps = MonkeyReader.get_samps(d_query)

        if analysis_type == 'INDUCTIONRHO':
            concs,my = an.induction_curve(samps, an.ratiometric_rho, bounds=(bounds_min, bounds_max), mname1=mname1, mname2=mname2, ndt=ndt)

        elif analysis_type == 'INDUCTIONALPHA':
            concs,my = an.induction_curve(samps, an.ratiometric_alpha, bounds=(bounds_min, bounds_max), mname=mname1, ndt=ndt)

        elif analysis_type == 'INDUCTIONMEAN':
            concs,my = an.induction_curve(samps, an.mean_expression, mname=mname1)

        fig1 = plt.figure()
        plt.plot(np.log10(concs), my, '.')
        plt.xlabel("log({} conc.) (M)".format(d_query['ind_name']))
        plt.ylabel('Mean fluorescence (AU)')

        #### CURVE FIT
        z,_= curve_fit(an.hill, concs, my, bounds=([0,0,0,1],[1,1,1e-2,2]))
        a = z[0]
        b = z[1]
        k = z[2]
        n = z[3]

        x = np.linspace(-6,-2,200)
        fig2 = plt.figure()
        plt.plot(x, an.hill(10**x,a,b,k,n), '-.')
        plt.plot(np.log10(concs),my,'r.')
        plt.xlabel("log({} conc.) (M)".format(d_query['ind_name']))
        plt.ylabel('Mean fluorescence (AU)')

        return [fig_to_html(fig1), fig_to_html(fig2)];

    def analysis_heatmap(request):
        analysis_type = request.POST['param1[]']

        dict_query = json.loads(request.POST['param1[0][1][value]'])
        d_query = {}
        # d_query['exp_name'] = dict_query['posts']['exp_name']
        # d_query['dna_name'] = dict_query['posts']['dna_name']
        # d_query['med_name'] = dict_query['posts']['med_name']
        # d_query['str_name'] = dict_query['posts']['str_name']
        # d_query['ind_name'] = dict_query['posts']['ind_name']
        # d_query['mea_name'] = dict_query['posts']['mea_name']
        d_query['exp_name'] = dict_query['posts']['experiment']
        d_query['dna_name'] = dict_query['posts']['dna']
        d_query['med_name'] = dict_query['posts']['media']
        d_query['str_name'] = dict_query['posts']['strain']
        d_query['ind_name'] = dict_query['posts']['inducer']
        d_query['mea_name'] = dict_query['posts']['measurement_name']

        if analysis_type == "HEATMAPRHO" or analysis_type == "HEATMAPALPHA":
            bounds_min = [int(request.POST['param1[1][1][value]']),
                          int(request.POST['param1[1][2][value]']),
                          int(request.POST['param1[1][3][value]'])]
            bounds_max = [int(request.POST['param1[1][4][value]']),
                          int(request.POST['param1[1][5][value]']),
                          int(request.POST['param1[1][6][value]'])]
            ndt = int(request.POST['param1[1][7][value]'])
            nbins = int(request.POST['param1[1][8][value]'])
            mname1 = request.POST['param1[1][9][value]']
            if analysis_type == "HEATMAPRHO":
                mname2 = request.POST['param1[1][10][value]']
        else:
            nbins = int(request.POST['param1[1][1][value]'])
            mname1 = request.POST['param1[1][2][value]']

        samps = MonkeyReader.get_samps(d_query)

        if analysis_type == 'HEATMAPRHO':
            hm,x,y = an.induction_heatmap(samps, an.ratiometric_rho, nbins=nbins, bounds=(bounds_min, bounds_max), mname1=mname1, mname2=mname2, ndt=ndt)

        elif analysis_type == 'HEATMAPALPHA':
            hm,x,y = an.induction_heatmap(samps, an.ratiometric_alpha, nbins=nbins, bounds=(bounds_min, bounds_max), mname=mname1, ndt=ndt)

        elif analysis_type == 'HEATMAPMEAN':
            hm,x,y = an.induction_heatmap(samps, an.mean_expression, nbins=nbins, mname=mname1)

        fig = plt.figure()
        plt.pcolormesh(x[1:],y[1:],hm)
        plt.colorbar()
        plt.xlabel('log(C6 conc.) (M)')
        plt.ylabel('log(Arabinose conc.) (M)')
        return fig_to_html(fig);

    def analysis_kymograph(request):

        analysis_type = request.POST['param1[]']

        dict_query = json.loads(request.POST['param1[0][1][value]'])
        d_query = {}
        # d_query['exp_name'] = dict_query['posts']['exp_name']
        # d_query['dna_name'] = dict_query['posts']['dna_name']
        # d_query['med_name'] = dict_query['posts']['med_name']
        # d_query['str_name'] = dict_query['posts']['str_name']
        # d_query['ind_name'] = dict_query['posts']['ind_name']
        # d_query['mea_name'] = dict_query['posts']['mea_name']

        d_query['exp_name'] = dict_query['posts']['experiment']
        d_query['dna_name'] = dict_query['posts']['dna']
        d_query['med_name'] = dict_query['posts']['media']
        d_query['str_name'] = dict_query['posts']['strain']
        d_query['ind_name'] = dict_query['posts']['inducer']
        d_query['mea_name'] = dict_query['posts']['measurement_name']

        skip = int(request.POST['param1[1][1][value]'])
        mname = request.POST['param1[1][2][value]']
        samps = MonkeyReader.get_samps(d_query)

        hm,x,y = an.kymograph(samps, an.expression_rate, mname=mname, skip=skip)

        fig = plt.figure()
        plt.pcolor(hm)
        plt.colorbar()
        return fig_to_html(fig);
