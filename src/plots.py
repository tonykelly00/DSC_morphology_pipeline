
def plot_dsc(Dict)
Dict_data=Dict        
for name, d  in Dict_data.items():
        df=d['data']
        fig, ax1 = plt.subplots()
        ax1.plot(df.length*d['res']/d['ex_factor'], df.diam/d['ex_factor']) 
        ax1.plot(df.length*d['res']/d['ex_factor'], df.smth/d['ex_factor']) 
        for dsc in d['DSCs']:
                #print(dsc)
                ax1.plot(dsc.length, dsc.smth)   
                # ax1.plot(dic['left_bases'], df.diam[dic['left_bases']], "o", color="red")
                # ax1.plot(df.length[dic['left_bases']], df.diam[dic['left_bases']], "o", color="red")
                # ax1.plot(df.length*Dict['res']/Dict['ex_factor'], df.diam[peaks]/Dict['ex_factor'], "x") #ax1.plot(df.length, df.diam[peaks], "x")
        #ax1.plot(df.length[peaks]*Dict['res']/Dict['ex_factor'], df.diam[peaks]/Dict['ex_factor'], "x")
                # plt.xlim(270,285)
                # plt.ylim(200,1250)
        plt.title(name)