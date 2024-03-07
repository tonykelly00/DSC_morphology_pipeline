import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_dsc(Dict):
    Dict_data=Dict        
    corrected=1 #use uncorrected to check against data
    for name, d  in Dict_data.items():
            df=d['data']
            fig, ax1 = plt.subplots()
            if corrected==1:
                ax1.plot(df.length*d['res']/d['ex_factor'], df.diam/d['ex_factor']) 
                ax1.plot(df.length*d['res']/d['ex_factor'], df.smth/d['ex_factor'])
            else:
                ax1.plot(df.length, df.diam/d['ex_factor']) 
                ax1.plot(df.length, df.smth/d['ex_factor'])
            for dsc in d['DSCs']:
                    #print(dsc)
                    if corrected==1:
                        ax1.plot(dsc.length, dsc.smth) 
                    else:
                        ax1.plot(dsc.length/d['res']*d['ex_factor'], dsc.smth) 
                    # ax1.plot(dic['left_bases'], df.diam[dic['left_bases']], "o", color="red")
                    # ax1.plot(df.length[dic['left_bases']], df.diam[dic['left_bases']], "o", color="red")
                    # ax1.plot(df.length*Dict['res']/Dict['ex_factor'], df.diam[peaks]/Dict['ex_factor'], "x") #ax1.plot(df.length, df.diam[peaks], "x")
            #ax1.plot(df.length[peaks]*Dict['res']/Dict['ex_factor'], df.diam[peaks]/Dict['ex_factor'], "x")
                    # plt.xlim(270,285)
                    # plt.ylim(200,1250)
            plt.title(name)


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
    
    return fig, ax


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