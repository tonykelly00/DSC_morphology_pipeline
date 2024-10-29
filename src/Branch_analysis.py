"""
Created on Wed Dec 15 13:01:26 2021

@author: Tony Kelly
"""

from os.path import dirname, join as pjoin
from scipy.io import loadmat
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from pathlib import Path

def branch_dsc(path, res, ex_factor):
    Branch = {}
    Dict = Branch
    Dict['res'] = res #resolution of 0.0676 already accounted for in matlab
    Dict['ex_factor'] = ex_factor
    Dict['file'] = Path(path).name
    Dict['path'] = path #path.split("\\")[0]
   
    
    # Dict['data'] = pd.read_csv (r'tables\Branch1_Comp_Local Diameter.csv',
    #                     names=['diam', 'length', 'pt_distance','value','x','y','z','j']) #place "r" before the path string to address special character, such as '\'. Don't forget to put the file name at the end of the path + '.xlsx'
    Dict['data'] = pd.read_csv (path, names=['diam', 'length', 'pt_distance','value','x','y','z','j']) #place "r" before the path string to address special character, such as '\'. Don't forget to put the file name at the end of the path + '.xlsx'
    
    
    df = Dict['data'][['diam', 'length', 'pt_distance', 'x', 'y', 'z']]
    ###scaling here causes problems with DSC detection due to changes in the derivative
    # df.diam*=1/C1_d3['ex_factor']
    # df.length*=C1_d3['res']/C1_d3['ex_factor']
    # df.pt_distance*=C1_d3['res']/C1_d3['ex_factor']
    
    def smooth(y, box_pts):
        box = np.ones(box_pts)/box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth
    
    smth = smooth(df.diam, 10)
    df['smth'] = smth
    
    diam_diff=np.diff(df.smth)
    diam_diff = np.insert(diam_diff, 0, 0)
    df['deriv'] = diam_diff
    
    diam_deriv2=np.diff(df.deriv)
    diam_deriv2= np.insert(diam_deriv2, 0, 0)
    df['deriv2'] = diam_deriv2
    
    #important varibles 
    p = 200 # prominence the steepness of the drop in diameter
    peak_diff = 5 # peak derivative used to find start and end of DSC
    r = 0.7 # min recovery factor of Diam after diam 
    l = 12 # number of points to average to get peak diff when finding stable start and end (try to avoid short drops) 
    
    #this finds all local minimums and scans each minimum if DSC
    def find_DSCs():
        #finds all local minimum and put into peak. Peaks is then x location of all possible DSCs
        from scipy.signal import find_peaks       
        peaks, dic = find_peaks(df.smth*-1., prominence=p) #reduced to 100 peaks, dic = find_peaks(df.smth*-1., prominence=1000)
        
            
        #to find if Peak is DSC meet criterea <baseline/2 and diam after returns to 80% baseline
        # def find_DSCs_minima():
        start = []
        end =[]
        DSCs = []
        DSC_properties = []
                
        peaks = peaks[(df.smth[peaks]/Dict['ex_factor']<500)]
        for rows in peaks:
            #print(rows)
            if rows < 5: #skips peak within 5 point from begining
                continue
            
            i=5
            rows = rows - 5 + np.argmin(df.smth[rows-5:rows+5])
            while diam_diff[rows-i-l:rows-i].mean() <= +peak_diff and rows-i-l>0: #and that rows-1 is at start of trace and valued >0 
                #print("previous decrease i {}, diam {}".format(i, df.diam[rows-i], df.deriv[rows-i]) )
                i+=1
            
            start_i=df.smth[rows-i-l: rows].idxmax() # index of max diam between begining and middle of DSC
            start.append(df.loc[start_i,:])
            
            i=5
            while diam_diff[rows+i:rows+i+l].mean() >= -peak_diff:
                # print("next decrease i {}, diam {}".format(i, df.diam[i+1]) )
               
                if rows+i+5==diam_diff.size:    #skips if end after the length of the segment
                    break
                i+=1
                
            end_i=rows+i
            end_i=df.smth[rows: rows+i+l].idxmax()
            end.append(df.loc[end_i,:])
            
            if df.smth[rows]< df.smth[start_i]/2 and df.smth[end_i] > df.smth[start_i]*r:  # if df.smth[rows]< df.smth[start_i]/2 and df.smth[end_i] > df.smth[start_i]*0.75:
                i=0
                while diam_diff[start_i+i] >= 0:
                    # print("start decrease i {}, diam {}".format(i, df.diam[i+1]) )
                    i+=1
            
                start_i=start_i+i-1
                #start.append(df.loc[rows-i,:])
            
                i=0
                while diam_diff[end_i-i] <= -peak_diff:
                    # print("end increse i {}, diam {}".format(i, df.diam[i+1]) )
                    i+=1
                end_i=end_i+i
            
                DSCs.append(df[start_i:end_i].copy())
            
            elif df.smth[rows]< df.smth[end_i]/2 and df.smth[start_i] > df.smth[end_i]*r:
                i=0
                while diam_diff[start_i+i] >= 0:
                    # print("start decrease i {}, diam {}".format(i, df.diam[i+1]) )
                    i+=1
            
                start_i=start_i+i-1
                #start.append(df.loc[rows-i,:])
            
                i=0
                while diam_diff[end_i-i] <= -peak_diff:
                    # print("end increse i {}, diam {}".format(i, df.diam[i+1]) )
                    i+=1
                end_i=end_i+i
                
            
                DSCs.append(df[start_i:end_i].copy())
       
        # *C1_d3['res'] conver to um *C1_d3['res']/ex_factor convert to corrected um
        
        for DSC in DSCs:
            
            DSC.diam*=1/Dict['ex_factor']   #if the DSCs overlap each other the scaling applied again. Separate DSC from orig data
            DSC.smth*=1/Dict['ex_factor']
            DSC.length*=Dict['res']/Dict['ex_factor']
            DSC.pt_distance*=Dict['res']/Dict['ex_factor']  
            
            minX=np.argmin(DSC.smth)
            
            start = np.argmin(DSC.deriv2[0:minX-3]) #+ DSC.index[0])
            end = np.argmax(DSC.deriv2[minX+3:]) + minX+3 #+ DSC.index[0])
        
            DSC_properties.append({'minimum':min(DSC.smth), 'mean':np.mean(DSC.smth[start:end]), 'distance':DSC.length[DSC.length.index[0]], 'length':(DSC.length[DSC.length.index[0]+end])-(DSC.length[DSC.length.index[0]+start])}) #'length':max(DSC.length)-min(DSC.length) #used sum(DSC.pt_distance) but error with old pt distance data       
        
        return DSCs, DSC_properties, peaks
    
    
    DSCs, DSC_properties, peaks = find_DSCs()
    Dict['DSCs']=DSCs
    Dict['DSC_properties']=DSC_properties
    Dict['peaks']=peaks
    

    def find_compartments():
        
        compartments = []
        comp_properties = []
        for i, DSC in enumerate(DSCs): #for DSC in DSCs:
        
            
            start_i=DSCs[i].index.stop
            
            if i<len(DSCs)-1:
                end_i =DSCs[i+1].index.start
            
            elif i==len(DSCs)-1:
                end_i =df.index.stop
                
            
            compartments.append(df[start_i:end_i].copy())
            compartments[i].diam*=1/Dict['ex_factor']
            compartments[i].smth*=1/Dict['ex_factor']
            compartments[i].length*=Dict['res']/Dict['ex_factor']
            compartments[i].pt_distance*=Dict['res']/Dict['ex_factor']
            
        for comp in compartments:  
             if comp.empty==False:
                comp_properties.append({'mean':np.mean(comp.smth), 'distance':min(comp.length), 'length':max(comp.length)-min(comp.length)}) #used sum(DSC.pt_distance) but error with old pt distance data
        
        return compartments, comp_properties
        
        
    Dict['compartments'], Dict['compt_properties']=find_compartments() 

    Dict['data']=df  #update origniak data with smth and derivative
    return Dict 

## add manual to the data dictionary 
##add manual DSC6 -DSC 6 and 7 together and baseline did not return to minimum value between the 2 DSCs 

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
    
        Dict['DSC_properties'].append({'minimum':min(DSC.smth), 'mean':np.mean(DSC.smth[start:end]), 'distance':DSC.length[DSC.length.index[0]], 'length':(DSC.length[DSC.length.index[0]+end])-(DSC.length[DSC.length.index[0]+start])}) #'length':max(DSC.length)-min(DSC.length) #used sum(DSC.pt_distance) but error with old pt distance data       

        
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


def add_branch(data):
    
    branch={}
    branch['C1_03_cell2_d3']={}
    branch['C1_03_cell2_d3']['name']='C1_03_cell2_d3'
    branch['C1_03_cell2_d3']['branchNo'] = [[0,0],[1,31],[2,49],[3,130]]
    
    branch['C1_03_cell2_d2']={}
    branch['C1_03_cell2_d2']['name']='C1_03_cell2_d2'
    branch['C1_03_cell2_d2']['branchNo'] = [[0,0],[1,31],[2,47],[3,94], [4,140],[5,180]]#branch 5 small side branch does not seem to be equal daughter 
    
    
    branch['C1_02_cell1_d2']={}
    branch['C1_02_cell1_d2']['name']='C1_02_cell1_d2'
    branch['C1_02_cell1_d2']['branchNo'] = [[0,0],[1,17],[2,48],[3,110]]
    
    branch['dendrite1'] = {}
    branch['dendrite1']['name'] = 'dendrite1'
    branch['dendrite1']['branchNo'] =  [[0,0],[1,17],[2,137]]
    
    branch['dendrite3'] = {}
    branch['dendrite3']['name'] = 'dendrite3'
    branch['dendrite3']['branchNo'] =  [[0,7],[1,13],[2,96],[3,201]]

    branch['dendrite4'] = {}
    branch['dendrite4']['name'] = 'dendrite4'
    branch['dendrite4']['branchNo'] =  [[0,0],[1,1], [2,160]]
    
    for name, dendrite in branch.items():
        # print(dendrite)
        data[name]['branchNo'] = dendrite['branchNo']

def FindBranch(data):
    
    branch_dic={}
    mean_dic={}
    for name, dendrite in data.items():
        Dict=dendrite
        df=dendrite['data']
        # print(data)
    
        # fig, ax = plt.subplots()
        # ax.plot(df.length*Dict['res']/Dict['ex_factor'], df.diam/Dict['ex_factor'])
        # plt.xlim(0,130)
    
        # branchNo = [[0,0],[1,31],[2,49],[3,130]]
        branchNo = Dict['branchNo']
        
    # plt.Figure(figsize(2,2))
    
        # fig.dpi=80
        # fig.figure
    
        # plt.title('Binned_Diameters')
        # plt.ylim(0,1500)
        # plt.yticks([0,500,1000,1500])
    
    
        df['branchNo']=0    #set branchNo to 0
    
        for i in branchNo:  #finds and sets branch No
            print(i)
            print(i[1])
            df.loc[df['length']*Dict['res']/Dict['ex_factor'] > i[1], 'branchNo' ]=i[0]
            
        a=[]    
        for i in branchNo: 
            a.append(df.loc[df['branchNo'] == i[0]].diam.mean()/Dict['ex_factor'])
        
        # branch_df =[]
        # branch_start=[]
        # branch_end =[]
        # for i in branchNo: 
        #       branch_df=df[['diam', 'length']].loc[df['branchNo'] == 1]

        #       branch_start = branch_df.diam.iloc[50:200].mean()/3.8

        #       branch_end = branch_df.diam.iloc[-200:-1].mean()/3.8
        a_df = pd.DataFrame(a)
        mean_dic[name]=a_df
        
        
        
        branch_data =[]
        branch_mean=[]
        branch_start=[]
        branch_end =[]
        for i in range(0, df.branchNo.max()+1, 1): 
            print(i) 
            branch_df=(df[['smth', 'length']].loc[df['branchNo'] == i])
            branch_df.length=branch_df.length*Dict['res']/Dict['ex_factor']
            branch_df.smth=branch_df.smth/Dict['ex_factor']
            branch_data.append(branch_df)
            branch_mean.append(branch_df['smth'].mean())
            branch_start.append(branch_df.smth.iloc[50:200].mean())
            branch_end.append(branch_df.smth.iloc[-200:-50].mean())
        
        branch_info={'branchs':branch_data, 'mean':branch_mean, 'start_diam': branch_start, 'end_diam':branch_end}
        
        
        dropAlongBranch=[]
        dropAcrossBranch=[]
        for i in range(0, df.branchNo.max(), 1):
            total_drop=branch_info['start_diam'][0]-branch_info['end_diam'][-1]
            dropAlongBranch.append((branch_info['start_diam'][i]-branch_info['end_diam'][i]) / total_drop)        
            dropAcrossBranch.append((branch_info['end_diam'][i]-branch_info['start_diam'][i+1]) / total_drop)   
        
        branch_info.update({'total_drop':total_drop, 'dropAlong':dropAlongBranch, 'dropAcross': dropAcrossBranch})
        Dict['branch_info'] = branch_info
    
   
    df=pd.concat(mean_dic, axis=1)

def resistances(dend_name, branchNo, data):
    dend_name
    branchNo

    p = 180 # resistivity ohms cm
    l = 0.0001 # 1um length in cm
    pi = 3.14
    MegaOhm = 10 **-6 # scale to mega Ohms

    branch_info=data[dend_name]['branch_info']
    Rdend=[]
    for branch_data in branch_info['branchs']:
        m=branch_data['smth'].median()
        r=(m/2) * 10 **-7 #cm
        #calculate the resistance of dendritic shaft /um
        Rd=(p*l)/(pi*(r**2)) * MegaOhm
        Rdend.append(Rd)
    
    branch_info['Rdend']=Rdend

    DSC_props= data[dend_name]['DSC_properties']
    
    for dsc in DSC_props:
        r=dsc['mean']/2 * 10 **-7 #nm diam to cm radius
        #l = dsc['length'] * 10 **-4 #cm

        dsc['Rmorph'] = (p*l)/(pi*(r**2)) * MegaOhm
