import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from django_pandas.io import read_frame
from .models import Experiment, Sample, Dna, Vector, Measurement, Inducer


##################
### TIMESERIES ###
##################

# Get dataframe of measurement values for a set of samples in a query
# -----------------------------------------------------------------------------------
def get_measurements(sample):
    # Get measurements for a given sample, with
    meas = Measurement.objects.filter(sample__id__exact=sample.id)
    df = read_frame(meas)
    # Not sure if useful
    df = df.sort_values(by='time')
    return df

# Model functions for fitting to data
# -----------------------------------------------------------------------------------
def gompertz(t, A, um, l):
    return ((A*np.exp(-np.exp((((um*np.exp(1))/A)*(l-t))+1))))

# Analysis functions that compute timeseries from a dataframe with given keyword args
# -----------------------------------------------------------------------------------
def compute_diff(**kwargs):
    # Get timeseries from dataframe and compute smoothed diffs, choosing measurement by name
    df = kwargs['df']
    mname = kwargs['mname']
    m = df[df['name']==mname]
    ts = pd.Series(m['value'].values, index=m['time'])

    # Compute the diff and add to the data values array
    sts = ts.rolling(window=10, min_periods=3, center=True).median()
    diffs = sts.diff()

    # Time series with diff values
    return diffs

def get_values(**kwargs):
    # Get timeseries from dataframe, choosing measurement by name
    df = kwargs['df']
    mname = kwargs['mname']
    m = df[df['name']==mname]
    ts = pd.Series(m['value'].values, index=m['time'])

    # Time series with diff values
    return ts

def expression_rate(**kwargs):
    # Parameters:
    #   df = data frame to analyse
    #   mname = measurement name
    #   skip = number of time points to skip to avoid low OD
    #   bgval = background OD value to remove, if not supplied defaults to miniumum value
    df = kwargs['df']
    mname = kwargs['mname']
    skip = kwargs['skip']

    diff = compute_diff(**kwargs).values
    oddf = df[df['name']=='OD']
    odts = pd.Series(oddf['value'].values, index=oddf['time'])
    odts.sort_index()
    t = odts.index

    # Background OD
    if 'bgval' in kwargs:
        bgval = kwargs['bgval']
    else:
        bgval = odts.values.min()

    od = odts.values - bgval
    ts = pd.Series(diff[skip:]/od[skip:], index=odts.index[skip:])

    return ts

# Analysis functions that compute value from a dataframe with given keyword args
# ----------------------------------------------------------------------------------
def ratiometric_alpha(**kwargs):
    # Parameters:
    #   bounds = tuple of list of min and max values for  Gompertz model parameters
    #   df = dataframe of measurements including OD
    #   mname = name of measurement for which to compute alpha
    #   ndt = number of doubling times to extend exponential phase
    bounds = kwargs['bounds']
    df = kwargs['df']
    mname = kwargs['mname']
    ndt = kwargs['ndt']

    # input values for Gompertz model fit
    oddf = df[df['name']=='OD']
    odts = pd.Series(oddf['value'].values, index=oddf['time'])
    odts.sort_index()
    t = odts.index
    od = odts.values
    y = np.log(od) - np.log(od.min())

    # Fit Gompertz model
    z,_=curve_fit(gompertz, t, y, bounds=bounds)
    A = z[0]
    um = z[1]
    l = z[2]

    # Compute time of peak growth
    tm = ((A/(np.exp(1)*um))+l)
    # Compute doubling time at peak growth
    dt = np.log(2)/um
    # Time range to consider exponential growth phase
    t1 = tm
    t2 = tm + ndt*dt

    # Compute alpha as slope of fluo vs od
    # Dataframe of fluorescence measurements
    mdf = df[df['name']==mname][(df['time']>=t1) & (df['time']<=t2)]
    mts = pd.Series(mdf['value'].values, index=mdf['time'])
    mts.sort_index()
    # Dataframe of od measurements
    oddf = df[df['name']=='OD'][(df['time']>=t1)&(df['time']<=t2)]
    odts = pd.Series(oddf['value'].values, index=oddf['time'])
    odts.sort_index()

    odvals = odts.values
    mvals = mts.values
    length = min(len(odvals),len(mvals))
    z = np.polyfit(odvals[:length], mvals[:length], 1)
    p = np.poly1d(z)

    # Return slope as alpha
    alpha = z[0]
    return alpha

def ratiometric_rho(**kwargs):
    # Parameters:
    #   bounds = tuple of list of min and max values for  Gompertz model parameters
    #   df = dataframe of measurements including OD
    #   mname = name of measurement for which to compute alpha
    #   ndt = number of doubling times to extend exponential phase
    bounds = kwargs['bounds']
    df = kwargs['df']
    mname1 = kwargs['mname1']
    mname2 = kwargs['mname2']
    ndt = kwargs['ndt']

    alpha1 = ratiometric_alpha(bounds=bounds, df=df, mname=mname1, ndt=ndt)
    alpha2 = ratiometric_alpha(bounds=bounds, df=df, mname=mname2, ndt=ndt)
    return alpha1/alpha2

def mean_expression(**kwargs):
    mname = kwargs['mname']
    df = kwargs['df']
    return df[df['name']==mname]['value'].mean()

def mean_diff(**kwargs):
    mname = kwargs['mname']
    df = kwargs['df']
    diffs = compute_diff(df[df['name']==mname])
    return diffs.values.mean()

# Functions to analyse sample queries, performing some transformation per sample
#
#   Pass a function which takes kwargs including the dataframe = df
#
# -----------------------------------------------------------------------------------
def statistics(qsamples, func, **kwargs):
    # Return descriptive statistics for the function func applied to some samples
    # For now, mean and std
    values = []
    for s in qsamples:
        df = get_measurements(s)
        kwargs['df'] = df
        value = func(**kwargs)
        values.append(value)
    mean = np.mean(np.array(values))
    std = np.std(np.array(values))
    return mean,std

def kymograph(qsamples, func, **kwargs):
    # func() takes a dataframe as argument and returns another timeseries, eg. expression rate
    concs = []
    times = []
    values = []

    for s in qsamples:
        df = get_measurements(s)
        kwargs['df'] = df
        ts = func(**kwargs)

        ind_qs = Inducer.objects.filter(sample__id__exact=s.id)
        inds_concs = [i.concentration for i in ind_qs]

        # Just for one inducer??
        # FIX THIS!! [0] in FlapWeb is [1] in flapjack
        concs.append([inds_concs[0]]*(len(ts)))
        values.append(ts.values)
        times.append(ts.index)

    x = np.array(times).T.ravel()
    y = np.array(concs).T.ravel()
    z = np.array(values).T.ravel()

    idx = np.where(y>0)

    df = pd.DataFrame({'value':z[idx], 't':x[idx], 'conc':np.log(y[idx])})
    c1,bins1 = pd.cut(df.t, 80, retbins=True)
    c2,bins2 = pd.cut(df.conc, 12, retbins=True)
    hm = df.groupby([c1, c2]).value.mean().unstack()
    print(bins1.shape)
    print(bins2.shape)
    print(c1.shape)
    return hm,bins1,bins2

def induction_curve(qsamples, func, **kwargs):
    # Get inducer concentrations
    #concs = [s.inducers[0].concentration for s in qsamples]
    # FIX THIS!! [0] in FlapWeb is [1] in flapjack
    concs = [Inducer.objects.filter(sample__id__exact=s.id)[0].concentration for s in qsamples]
    values = []
    for s in qsamples:
        df = get_measurements(s)
        # Apply function to measurements dataframe
        kwargs['df'] = df
        value = func(**kwargs)
        values.append(value)
    return np.array(concs), np.array(values)

"""
# EXAMPLE
# I get 64 samples
qsamples = Sample.objects.filter(experiment__name__exact='Tim210813').filter(inducer__pubchemid__exact='C6').filter(inducer__pubchemid__exact='Arabinose').filter(vector__dna__name__exact='DBD2')
# Now for each sample in qsamples I want to get the inducer[0]
concs = [Inducer.objects.filter(sample__id__exact=s.id)[0].concentration for s in qsamples]
"""
def induction_heatmap(qsamples, func, nbins, **kwargs):
    # Get inducer concentrations
    #concs1 = [s.inducers[0].concentration for s in qsamples]
    #concs2 = [s.inducers[1].concentration for s in qsamples]

    #FIX THIS [0] in FlapWeb is [1] in flapjack
    concs1 = [Inducer.objects.filter(sample__id__exact=s.id)[1].concentration for s in qsamples]
    concs2 = [Inducer.objects.filter(sample__id__exact=s.id)[0].concentration for s in qsamples]
    concs1 = np.array(concs1)
    concs2 = np.array(concs2)

    # Compute values
    values = []
    for s in qsamples:
        df = get_measurements(s)
        kwargs['df'] = df
        # Apply function to measurements dataframe
        value = func(**kwargs)
        values.append(value)
    values = np.array(values)

    # Group data as heatmap array
    idx = np.where((concs1>0)*(concs2>0))[0]
    x = np.log10(concs1[idx])
    y = np.log10(concs2[idx])
    z = values[idx]
    df = pd.DataFrame({'value':z, 'conc1':x, 'conc2':y})
    c1,bins1 = pd.cut(df.conc1, nbins, retbins=True)
    c2,bins2 = pd.cut(df.conc2, nbins, retbins=True)
    hm = df.groupby([c1, c2]).value.mean().unstack()

    return hm,bins1,bins2

# Analysis functions that take a list of DNA names, and compute some measure, returning a list
# --------------------------------------------------------------------------------------------

def bar_graph(session, engine, dnas, func, **kwargs):
    # Compute mean and standard deviation of gene expression per plasmid
    means = []
    stds = []
    for d in dnas:
        #samps = session.query(tables.Sample).filter(tables.Sample.dnas.any(name=d)).all()
        samps = Sample.objects.filter(vector__dna__name__exact=d)
        # Compute means and std dev of gene expression
        m,s = statistics(samps, func, **kwargs)

        means.append(m)
        stds.append(s)
        print(m,s)

    return means,stds

def hill(x, a, b, k, n):
    return (a*(x/k)**n + b) / (1 + (x/k)**n)
