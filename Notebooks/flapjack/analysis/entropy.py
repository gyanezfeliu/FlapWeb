import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


def entropy(density):
    '''
    Entropy H(X) of one variable given joint histogram

    density =  histogram

    returns: entropy value
    '''

    nzs = np.where(density>0)
    return -np.sum(density[nzs]*np.log2(density[nzs].ravel()))

def joint_entropy(density2d):
    '''
    Joint entropy H(X,Y) for joint histogram

    density2d = joint histogram (2d array) 

    returns: joint entropy value
    '''

    nzs = np.where(density2d>0)
    return -np.sum(density2d[nzs].ravel()*np.log2(density2d[nzs].ravel()))
    
def conditional_entropy(density2d):
    # conditional on the first variable (X), i.e. H(Y|X)
    '''
    Conditional entropy H(Y|X) for joint histogram

    density = joint histogram (2d array) 

    returns: joint entropy value
    '''
    density = np.sum(density2d, axis=1)
    ex = entropy(density)
    je = joint_entropy(density2d)
    # H(Y|X) = H(X,Y) - H(X)
    return je-ex

def mutual_information(density2d):
    '''
    Mutual information I(X,Y) for joint histogram

    density2d = joint histogram (2d array) 
    '''
    # p(Y)
    density = np.sum(density2d, axis=0)
    # I(X,Y) = H(Y) - H(Y|X)
    return entropy(density)-conditional_entropy(density2d)

#---------------------------------------------------------
# Compute normalised histograms to approxiate probability densities
def prob_density(x, nbins, range):
    H, edges = np.histogram(x.ravel())#, nbins, range)
    H = H.astype(np.float32)
    return H/np.sum(H.ravel())

def prob_densitydd(xlist, nbins, range):
    H, edges = np.histogramdd(xlist) #, nbins, range)
    H = H.astype(np.float32)
    return H/np.sum(H.ravel())

def prob_density2d(x, y, nbins, range):
    H, xedges, yedges = np.histogram2d(x.ravel(), y.ravel()) #, nbins, range)
    H = H.astype(np.float32)
    return H/np.sum(H.ravel())

def prob_density3d(x, y, z, nbins, range):
    H, edges = np.histogramdd([x.ravel(), y.ravel(), z.ravel()]) #, nbins, range)
    H = H.astype(np.float32)
    return H/np.sum(H.ravel())

def prob_density4d(x, y, z, w, nbins, range):
    H, edges = np.histogramdd([x.ravel(), y.ravel(), z.ravel(), w.ravel()]) #, nbins, range)
    H = H.astype(np.float32)
    return H/np.sum(H.ravel())


#---------------------------------------------------------
# Compute entropies of diffs of measurements from Pandas dataframes

def channel_entropy(df, name, nbins=None, hrange=None):
    # Entropy of change (diff) in each measurement with name==name in dataframe
    # Get the diff
    diffs,vals,t = compute_measurement_diff(df, name)
    # Compute the entropy using histogram
    density = prob_density(diffs, nbins, hrange)
    H = entropy(density)
    return H

def channel_entropies(df, nbins, hrange):
    # Calculate the entropies of all channels in the dataframe df
    H = {}
    mnames = df.measurements_name.unique()
    for m in mnames:
        H[m] = channel_entropy(df, m, nbins, hrange)
    return H

def channel_conditional_entropy_2d(df, m1, m2, nbins=None, hrange=None):
    # Compute the conditional entropy H(m2 | m1),
    diff1,vals1,t1 = compute_measurement_diff(df, m1)
    diff2,vals2,t2 = compute_measurement_diff(df, m2)
    density2d = prob_density2d(vals1, diff2, nbins, range)
    # Compute the entropy
    return conditional_entropy(density2d)

def channel_conditional_entropy_3d(df, m1, m2, m3, nbins=None, hrange=None):
    # Compute the conditional entropy H(m2 | m1),
    diff1,vals1,t1 = compute_measurement_diff(df, m1)
    diff2,vals2,t2 = compute_measurement_diff(df, m2)
    diff3,vals3,t3 = compute_measurement_diff(df, m3)
    density3d = prob_density3d(vals1, diff2, diff3, nbins, range)
    # Compute the entropy
    return conditional_entropy(density3d)

def channel_conditional_entropy_4d(df, m1, m2, m3, m4, nbins=None, hrange=None):
    # Compute the conditional entropy H(m2 | m1),
    diff1,vals1,t1 = compute_measurement_diff(df, m1)
    diff2,vals2,t2 = compute_measurement_diff(df, m2)
    diff3,vals3,t3 = compute_measurement_diff(df, m3)
    diff4,vals4,t4 = compute_measurement_diff(df, m4)
    density4d = prob_density4d(vals1, diff2, diff3, diff4, nbins, range)
    # Compute the entropy
    return conditional_entropy(density4d)

def sample_mutual_information_2d(sample_df, m1, m2, nbins=None, hrange=None):
    df = sample_df.sort_values('measurements_time')
    s1 = df[df.measurements_name==m1]
    s2 = df[df.measurements_name==m2]
    d1 = np.diff(s1)
    d2 = np.diff(s2)
    density2d = prob_density2d(d1, d2, nbins, range)
    return mutual_information(density2d)

