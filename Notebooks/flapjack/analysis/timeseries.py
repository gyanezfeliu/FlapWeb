import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

def get_timeseries(df, mnames):
    '''
    Returns a timeseries for measurement of each sample in dataframe
    
    dict{(sample_id,measurement_name

    '''
    ts = {}
    samples = df[df.measurements_name==mname].groupby('samples_id')
    for id,s in samples:
        ts[id] = pd.Series(s['measurements_value'].values, index=s['measurements_time'])
    return(ts)

def phase_angles(df, m1, m2, window=5, min_periods=3):
    '''
    Calculate dm1/dm2 = phase angle for samples in ataframe
    '''
    pa = {}
    samples = df.groupby('samples_id')
    for id,s in samples:
        s1 = s[s.measurments_name==m1]
        s2 = s[s.measurments_name==m2]
        # Common time index from series 1
        timeindex = s1['measurements_time']
        ts1 = pd.Series(s1['measurements_value'].values, index=timeindex)
        ts2 = pd.Series(s2['measurements_value'].values, index=timeindex)
        sts1 = ts1.rolling(window=window, min_periods=min_periods, center=True).mean()
        sts2 = ts2.rolling(window=window, min_periods=min_periods, center=True).mean()
        pa[id] = sts1.diff()/sts2.diff()

    return(pa)

def compute_measurement_diff(df, name):
    # Compute the diff of measurements with measurement.name==name
    # Need to group by sample, sort by time, and then put all
    # the sample diffs together

    # First group each sample so that we can take their diffs
    samples = df[df.measurements_name==name].groupby('samples_id')
    # Construct an array of values to analyse
    values = np.array(())
    diffs = np.array(())
    t = np.array(())
    for id,s in samples:
        # First sort by time
        s = s.sort_values('measurements_time')
        # Compute the diff and add to the data values array
        # NOTE: Ignore the first 5 values because the times go past 24:00 to 00:00
        # FIX THIS in workbook reader code
        vals = s['measurements_value'].values[5:]
        dmeas = np.diff(vals)
        t = np.append(t, s['measurements_time'].values[6:])
        diffs = np.append(diffs, dmeas)
        values = np.append(values, vals[1:])

    # Numpy array with all diff values
    #plt.plot(values)
    return diffs,values,t

