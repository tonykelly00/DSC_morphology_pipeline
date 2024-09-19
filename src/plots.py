import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_dsc(dend,name, corr=0):
    d=dend        
    corrected=corr #use uncorrected to check against data
    
    df=d['data']
    peaks=d['peaks']
    fig, ax1 = plt.subplots()
    if corrected==1:
        
        ax1.plot(df.length*d['res']/d['ex_factor'], df.smth/d['ex_factor'])
        ax1.plot(df.length[peaks]*d['res']/d['ex_factor'], df.diam[peaks]/d['ex_factor'], "x")
    else:
        
        ax1.plot(df.smth/d['ex_factor'])
        ax1.plot(peaks, df.diam[peaks]/d['ex_factor'], "x")
    for dsc in d['DSCs']:
            #print(dsc)
            if corrected==1:
                ax1.plot(dsc.length, dsc.smth) 
            else:
                ax1.plot(dsc.smth) 
  
    plt.title(name)
    return fig, ax1


#%% cumulative analysis of all dendrites 