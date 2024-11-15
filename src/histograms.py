import pandas as pd
import matplotlib.pyplot as plt

import numpy as np


from scipy.stats import norm
from scipy.optimize import curve_fit

'''
from histograms import plot_histo, plot_z
df=DGdata[dend_name]['branch_info']['branchs'][branchNo]
fig, ax = plot_histo(df)
fig.savefig(plot_path +'/histo.svg', bbox_inches = 'tight', format="svg",transparent=True)   

fig, ax  = plot_z(df)
fig.savefig(plot_path +'/Z_plot.svg', bbox_inches = 'tight', format="svg",transparent=True)   

'''


def plot_histo(df):
    #df=DGdata[dend_name]['branch_info']['branchs'][branchNo]
    fig, ax = plt.subplots()
    # Plot histogram
    #hist, bins, _ = plt.hist(DGdata['C1_03_cell2_d3']['branch']['smth'], bins=20, color='skyblue', edgecolor='black')
    hist, bins, _ = ax.hist(df['smth'], bins=20, color='skyblue', edgecolor='black')

    # Bin centers
    bin_centers = 0.5 * (bins[1:] + bins[:-1])

    # Fit Gaussian to histogram
    def gaussian(x, mu, sigma, A):
        return A * np.exp(-0.5 * ((x - mu) / sigma)**2)

    popt, _ = curve_fit(gaussian, bin_centers, hist, p0=[df['smth'].mean(), df['smth'].std(), 1])

    # Plot Gaussian fit
    x = np.linspace(df['smth'].min(), df['smth'].max(), 100)
    plt.plot(x, gaussian(x, *popt), 'k--', label='Gaussian Fit')

    # Add labels and title
    plt.title('Histogram with Gaussian Fit')
    plt.xlabel('Value')
    plt.ylabel('Frequency')

    # Show plot
    plt.legend()
    plt.show()

    return fig, ax



def plot_z(df):

    # #df=DGdata['C1_03_cell2_d3']['branch']
    m=df['smth'].median()
    std = df['smth'].std()

    fig, ax1 = plt.subplots()

    ax1.plot(df.length, df.smth)

    # Add a straight line at a certain y-value
    plt.axhline(y=m-(2*std), color='r', linestyle='--', label='Threshold')
    ax1.set_ylim(df.smth.min()-50, 1200)

    df_zscored = (df['smth'] - m) / std

    ax2 = ax1.twinx()
    
    plt.rc("axes.spines", top=False, right=True)
    ax2.plot(df.length, df_zscored) 
    ax2.set_ylim((ax1.get_ylim()[0] - m) / std, (ax1.get_ylim()[1] - m) / std)

    return fig, ax1, df_zscored