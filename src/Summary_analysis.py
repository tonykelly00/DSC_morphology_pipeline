# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 13:05:16 2024

@author: Tony Kelly
"""
import pdb

import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


import os
import glob


### update DSC properties list after addition of manual DSCs
def update_DSCs(Branch):
    Dict = Branch
    Dict['DSC_properties'] =[]
    for DSC in Dict['DSCs']:
        # ax1.plot(DSC.diam)
        
        ### plot original size
        # ax1.plot(DSC.length, DSC.smth, color='c')
        
        
        minX=np.argmin(DSC.smth)
        
        start = np.argmax(DSC.deriv2[0:minX]) #+ DSC.index[0])
        end = np.argmax(DSC.deriv2[minX:]) + minX #+ DSC.index[0])
    
        Dict['DSC_properties'].append({'minimum':min(DSC.smth), 'mean':np.mean(DSC.smth[start:end]), 'distance':DSC.length[DSC.length.index[0]], 'length':sum(DSC.pt_distance)})

def update_compartments(Branch):
        Dict = Branch     
        compartments = []
        comp_properties = []
        for i, DSC in enumerate(Dict['DSCs']): #for DSC in DSCs:
        
            
            start_i=Dict['DSCs'][i].index.stop
            
            if i<len(Dict['DSCs'])-1:
                end_i =Dict['DSCs'][i+1].index.start
            
            elif i==len(Dict['DSCs'])-1:
                end_i =Dict['data'].index.stop
                
            
            compartments.append(Dict['data'][start_i:end_i].copy())
            compartments[i].diam*=1/Dict['ex_factor']
            compartments[i].smth*=1/Dict['ex_factor']
            compartments[i].length*=Dict['res']/Dict['ex_factor']
            compartments[i].pt_distance*=Dict['res']/Dict['ex_factor']
            
        for comp in compartments:  
             if comp.empty==False:
                comp_properties.append({'mean':np.mean(comp.smth), 'distance':min(comp.length), 'length':max(comp.length)-min(comp.length)}) #used sum(DSC.pt_distance) but error with old pt distance data
        
            
        Dict['compartments']=compartments
        Dict['compt_properties']=comp_properties
        
#%% update branches

# branch = DGdata['C1_02_cell1_d2']
# DSC=branch['data'][3915:4008].copy()
# DSC.diam*=1/branch['ex_factor']   #if the DSCs overlap each other the scaling applied again. Separate DSC from orig data
# DSC.smth*=1/branch['ex_factor']
# DSC.length*=branch['res']/branch['ex_factor']
# DSC.pt_distance*=branch['res']/branch['ex_factor']
# branch['DSCs'].append(DSC) 

# update_DSCs(branch)
# update_compartments(branch)

#%% cumulative analysis of all dendrites 
 
def cummulative_plot(data):
    # branches = []
    # branches.append(Branch2)
    # branches.append(C1_03_cell2_d3)
    
    all_lenght = []
    for branch in data.keys():
         
        DSCs= data[branch]['DSCs']
         
        DSC_length = []
        
        for DSC in DSCs:
            DSC_length.append(DSC.diam)    
        
        DSC_length1=pd.DataFrame(DSC_length)
        # DSC_length = np.array(DSC_length).flatten(order='C')
        DSC_length = pd.DataFrame(np.array(DSC_length1).flatten(order='C')).dropna()
        
        all_lenght.append(DSC_length)
    
    df = pd.concat(all_lenght, axis=1, ignore_index=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    n_bins=200
        
# plot the cumulative histogra
    n, bins, patches = ax.hist(df, n_bins, density=True, histtype='step', cumulative=True, label='CDF_D3')
    ax.set_xlim([0,300])
    
    fig.savefig('C:/Users/Tony Kelly/Desktop/DSC_Cumulative.eps', bbox_inches = 'tight')

#%% cumulative analysis of DSC properties all dendrites 
# import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
sys.path.append('M:/Tony/codes/python/stats/')
from Mean_CI import plot_stats, CI

def summary_data(data, parameter):
    # branches = []
    # branches.append(Branch2)
    # branches.append(C1_03_cell2_d3)
    
    param = parameter
    
    all_values = []
    for key, value in data.items():
        branch_param = []
        for DSC in value['DSC_properties']:
            branch_param.append(DSC[param])
            
        #branch_param = pd.DataFrame(data=branch_param)    
        #branch_param.columns = key
        all_values.append(branch_param)
    
    all_values = pd.DataFrame(data=all_values)  
    ax, fig = plot_stats(all_values.transpose())
    fig.savefig('C:/Users/Tony Kelly/Desktop/DSC_mean.eps', bbox_inches = 'tight')
    
    return all_values


'''
###cummulative probabliltiy
df= summary_data(HDGdata, 'mean')
CI(df[0])


df1 = pd.concat([df[0], df[1]])
fig, ax = plt.subplots(figsize=(2, 4))
fig.suptitle('DSC Diam', fontsize=24)
ax=sns.boxplot(data=df1.dropna(), showfliers=False)
ax=sns.stripplot(data=df1.dropna(), size=10, color='lightgrey')
ax.set_ylim([400,800])
ax.set_yticks([400,600,800])

df1.mean()
df1.std()

fig.savefig(desktop +'\DSC_mean.svg', bbox_inches = 'tight', format='svg')

fig, ax = plt.subplots(figsize=(4, 4))
n_bins=200
fig.suptitle("DSC_Diam")
# plot the cumulative histogra
n, bins, patches = ax.hist(df.transpose(), n_bins, density=True, histtype='step', cumulative=True)

df=df.stack().reset_index(drop=True)

n, bins, patches = ax.hist(df, n_bins, color='black', density=True, histtype='step', cumulative=True)
ax.set_xlim([0,800])


df= summary_data(HDGdata, 'length')
CI(df[0])

df1 = pd.concat([df[0], df[1]])
fig, ax = plt.subplots(figsize=(2, 4))
fig.suptitle('DSC Length', fontsize=24)
ax=sns.boxplot(data=df1.dropna(), showfliers=False)
ax=sns.stripplot(data=df1.dropna(), size=10, color='lightgrey')
ax.set_ylim([0,10])

df1.mean()
df1.std()

fig.savefig(desktop +'\DSC_length.svg', bbox_inches = 'tight', format='svg')

fig, ax = plt.subplots(figsize=(4, 4))
n_bins=200
fig.suptitle("DSC_length")
# plot the cumulative histogra
n, bins, patches = ax.hist(df.transpose(), n_bins, density=True, histtype='step', cumulative=True)

df=df.stack().reset_index(drop=True)

n, bins, patches = ax.hist(df, n_bins, color='black', density=True, histtype='step', cumulative=True)
ax.set_xlim([0,10])

shaft_diam=[]
for key, value in HDGdata.items():
    #print(value['data']['smth'])
    print(value['data']['smth'][10:data.smth.size-100].mean())
    shaft_diam.append(value['data']['smth'][10:data.smth.size-100].mean())
df=pd.DataFrame(shaft_diam)
CI(df)  

shaft_length=[]
for key, value in HDGdata.items():
    #print(value['data']['smth'])
    shaft_length.append(value['data']['length'][value['data']['length'].size-1]*value['res'])
df=pd.DataFrame(shaft_length)
CI(df)  
df.mean()
df.std()

'''