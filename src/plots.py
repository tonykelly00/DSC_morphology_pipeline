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
        
        ax1.plot(df.smth)#/d['ex_factor'])
        ax1.plot(peaks, df.diam[peaks], "x") #df.diam[peaks]/d['ex_factor']
    for dsc in d['DSCs']:
            #print(dsc)
            if corrected==1:
                ax1.plot(dsc.length, dsc.smth) 
            else:
                ax1.plot(dsc.smth) 
  
    plt.title(name)
    return fig, ax1


#%% cumulative analysis of all dendrites  
"""
to calculate where the drop in diameter occurs 
total drop in diameter over entire lenght
drop over branch, drop at branch point
mean decrease in diam along branch / um
compared to mean decreas over 10um either side of the branch
"""
def branch_figs(data, plot_path):
    
    mean_ls=[]
    for name, dendrite in data.items():
        Dict=dendrite
        mean_ls.append(Dict['branch_info']['mean'])
         
    df = pd.DataFrame(mean_ls)
    
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.plot(df.transpose())
    ax=df.boxplot(grid=False, showfliers=False)
    plt.ylim(0,2500)
    plt.yticks([0,500,1000,1500,2000,2500])
      
    #fig.savefig(plot_path +'/Diam_branch.svg', bbox_inches = 'tight', format="svg",transparent=True)   

    
    dropAc_ls=[]
    dropAl_ls=[]
    for name, dendrite in data.items():
        Dict=dendrite
        dropAc_ls.append(Dict['branch_info']['dropAcross'])
        dropAl_ls.append(Dict['branch_info']['dropAlong'])
         
    df_ac = pd.DataFrame(dropAc_ls)
    df_al = pd.DataFrame(dropAl_ls)
    
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.plot(df_ac.transpose())
    ax=df_ac.boxplot(grid=False, showfliers=False)
    ax.set_ylim()
    ax.set_yticks([-0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
    ax.set_title("Diam Drop across dendritic branchs")
    
    #fig.savefig(plot_path +'/Diam_dropAcross_branch.svg', bbox_inches = 'tight', format="svg",transparent=True)   
    
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.plot(df_al.transpose())
    ax=df_al.boxplot(grid=False, showfliers=False)
    ax.set_ylim()
    ax.set_yticks([-0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
    ax.set_title("Diam Drop along dendritic branch")
    
    #fig.savefig(plot_path +'/Diam_dropAlong_branch.svg', bbox_inches = 'tight', format="svg",transparent=True)   

    return df

#update below
#def resistance_figs(data):

