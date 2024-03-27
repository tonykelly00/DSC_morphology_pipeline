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
