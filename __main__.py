import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

PATH_RESULTS = "C:/Users/Edwin Cardenas/My Drive/BELEN/Python/Results"
PATH_DATA = "C:/Users/Edwin Cardenas/My Drive/BELEN/PROD/"

def loading_data():
    print("\n")
    print("loading data...")
    file = []
    
    for (dirpath, dirnames, filenames) in os.walk(PATH_DATA):
        file.extend(filenames)

    path= PATH_DATA + file[0]
    print(path)
    data = pd.read_excel(path, sheet_name="Prod. EXTR",header=0)
    return data

def clean_data(data):
    print("cleaning data...")
    data.dropna(axis =0 , how = 'all', subset='CODIGO', inplace=True )
    data = data[data["FECHA"] != "Total"]
    return data

def transform_data_A(data):

    print("deleting unnecessary columns")
    data = data [['FECHA', 'TURNO', 'GRUPO', 'MÁQ,', 'CODIGO', 'PRODUCCION (PZAS)','TOTAL KG', 'SCRAP']]   
    print("Column FECHA")
    data['FECHA'] = pd.to_datetime(data['FECHA'], format= '%Y-%m-%d')
    data['FECHA'].dt.day 
    data['DIA'] = data.loc[:,'FECHA'].dt.day
    data['NOMBRE_DIA']=data.loc[:,'FECHA'].dt.day_name()
    print('Column TURNO')
    data['TURNO'] = data['TURNO'].astype('category')
    print('Column GRUPO')
    data['GRUPO'] = data['GRUPO'].astype('category')
    print('Column CODIGO')
    data.loc[:,'CODIGO'] = data['CODIGO'].fillna(0)
    print('Column PRODUCCION (PZAS)')
    data['PRODUCCION (PZAS)'] = data['PRODUCCION (PZAS)'].fillna(0)
    data['PRODUCCION (PZAS)'] = data['PRODUCCION (PZAS)'].astype('int64')
    print('Column TOTAL KG')
    df = data['TOTAL KG'].fillna(0)
    data.loc[:,'TOTAL KG'] = df
    data.loc[:,'TOTAL KG'] = data['TOTAL KG'].astype('float')
    print('Column SCRAP')
    data['SCRAP'] = pd.to_numeric(data['SCRAP'], errors='coerce')
    data.loc[:,'SCRAP'] = data['SCRAP'].fillna(0)
    data['SCRAP'] = data['SCRAP'].astype('float')
    return data

    #print("Saving data in csv file...")
    #PATH
    #os.chdir("C:/Users/ecardenas/Dropbox/Belen/Python/Results/")
    #print(os.getcwd())
    #data.to_csv('data.csv', index=False)'''

def machine_working_days(data):
    print(" ")
    print("machines working days function")
    test = data.groupby(['DIA', 'MÁQ,']).sum()
    df_group = data.groupby(['MÁQ,','DIA']).sum()

    print("counting machines")    
    machines = set()
    for day, machine in test.index:
        machines.add(machine)
    
    print("counting days of work")    
    machines_dict = {}
    for machine in machines:
        s = df_group.loc[machine,'TOTAL KG']
        days_of_work = s.where(s > 0).count()
        machines_dict[machine] = days_of_work

    working_days = pd.DataFrame(list(machines_dict.items()), columns=['Machine', 'Working_days'])
    working_days.sort_values(by = 'Working_days' , axis =0, inplace=True, ascending=False)
    return working_days

    # path = 'C:/Users/ecardenas/Dropbox/Belen/Python/Results/'
    #machines_working_days.to_excel('C:/Users/ecardenas/Dropbox/Belen/Python/Results/machines_days_of_work.csv', sep = ',', index = True, header = False)
    #print(machine_working_days.head(20))

    #print('saving file...')
    #machines_days_of_work = pd.Series(data = machines_dict, index =None)
    #machines_days_of_work.sort_values(ascending = True, inplace = True)
    #machine_working_days = pd.read(machine_working_days)
       
def scrap_vs_production(data, days_to_analyze):
    print("\n")
    print("Scrap vs production function")
    #file_data= "D:/Notas de Estudio/Proyectos/production_analysis__project/production_analysis/data/processed/data.csv"
    #print('reading data.csv')
    #df = pd.read_csv("data.csv")
    df_A=data.groupby("MÁQ,").sum()
    df_A['PORCENTAJE'] = df_A['SCRAP']/(df_A['SCRAP']+df_A['TOTAL KG'])*100
    df_A.sort_values(by = ["PORCENTAJE"],ascending = False, inplace = True)
    list_A = df_A.index[0:15]

    print("Creating graph...")
    plt.rcdefaults()
    fig, ax = plt.subplots(figsize = [15,10])
    x_pos = list_A
    y_pos = df_A['PORCENTAJE'].head(15)
    bars = ax.bar(x_pos, y_pos,color = 'green', alpha = 0.9,linewidth = 0)
    ax.set_xlabel('Machines')
    ax.set_ylabel('% of scrap')
    ax.set_title('SCRAP / (SCRAP  + PRODCUTION) * 100')
    ax.bar_label(bars, label_type = "edge", fmt='%0.1f')
    os.chdir(PATH_RESULTS)
    plt.savefig('scrap_vs_production.pdf')

    print("Scrap tendency per machine")
    df_C = data.groupby(['DIA','MÁQ,']).sum()
    days = set(data['DIA'].values)
    
    days_list = list(days)
    days = days_list[-days_to_analyze:]
    
    values_scrap = {}

    for machine in list_A:
        scrap_list = []

        for day in days:
            try:
                scrap = df_C.loc[(day, machine)].loc['SCRAP']
                scrap_list.append(scrap)
            except:
                scrap_list.append(0)
        values_scrap[machine] = scrap_list

        

    y = values_scrap
    titles = []
    for values in y.keys():
        titles.append(values)

    #fig_b = plt.figure(figsize=(20, 40), constrained_layout=True)

    x = days
    y = values_scrap
    colors = ['brown','chocolate','olivedrab','steelblue','indigo','crimson','gray','black','cyan','tomato','gold','springgreen',
          'blueviolet','firebrick','purple']
    sub = 1
    

    for value in y.values():
        plt.subplot(8,2,sub)
        plt.plot( x , value, 'o',ls = '-', markevery=1,c = colors[sub-1])
        
        plt.title(titles[sub-1])
        plt.ylabel('SCRAP')
        plt.xlabel('DAYS')
        plt.ylim(0,max(value)+10) # greater value of list
        sub = sub +1
        plt.grid(True)
        plt.minorticks_on()
    plt.savefig('tendency_scrap_vs_production.pdf')

def scrap_vs_total_scrap(data, days_to_analyze):
    print("\n")
    print("Scrap vs total scrap function")
    #file_data= "D:/Notas de Estudio/Proyectos/production_analysis__project/production_analysis/data/processed/data.csv"
    #print('reading data.csv')
    #df = pd.read_csv("data.csv")
    df_B = data.groupby('MÁQ,').sum()
    df_B.drop('DIA',inplace = True, axis = 1)
    total_scrap = df_B['SCRAP'].sum()
    df_B['SCRAP/TOTAL SCRAP'] = df_B['SCRAP'].apply(lambda x: (x/total_scrap)*100 )
    df_B.sort_values(by = ['SCRAP/TOTAL SCRAP'],ascending = False, inplace = True )
    list_B = df_B.index[0:15]

    print("Creating plot...")
    fig, ax = plt.subplots(figsize = [15,10])
    x_pos = list_B
    y_pos = df_B['SCRAP/TOTAL SCRAP'].head(15)
    bars = ax.bar(x_pos, y_pos,color = 'indianred', alpha = 1 ,linewidth = 1)
    ax.set_xlabel('Machines')
    ax.set_ylabel('% of total scrap')
    ax.set_title('SCRAP/TOTAL SCRAP * 100')
    ax.bar_label(bars, label_type = "edge", fmt='%0.1f')
    plt.savefig('scrap_vs_total_scrap.pdf')

    print("Scrap tendency per machine")
    df_C = data.groupby(['DIA','MÁQ,']).sum()
    days = set(data['DIA'].values)
    days_list = list(days)
    
    days = days_list[-days_to_analyze:]
    values_scrap_b = {}

    for machine in list_B:
        scrap_list = []
        for day in days:
            try:
                scrap = df_C.loc[(day, machine)].loc['SCRAP']
                scrap_list.append(scrap)
            except:
                scrap_list.append(0)
        values_scrap_b[machine] = scrap_list

    y_b = values_scrap_b
    titles_b = []
    for values in y_b.keys():
        titles_b.append(values)

    #fig_b = plt.figure(figsize=(20, 40), constrained_layout=True)

    x = days
    y_b = values_scrap_b
    colors = ['brown','chocolate','olivedrab','steelblue','indigo','crimson','gray','black','cyan','tomato','gold','springgreen',
          'blueviolet','firebrick','purple']
    sub = 1
    for value in y_b.values():
        plt.subplot(8,2,sub)
        plt.plot( x , value, 'o',ls = '-', markevery=1,c = colors[sub-1])
        plt.title(titles_b[sub-1])
        plt.ylabel('SCRAP')
        plt.xlabel('DAYS')
        plt.ylim(0,max(value)+10) # greater value of list
        sub = sub +1
        plt.grid(True)
        plt.minorticks_on()

    plt.savefig('tendency_scrap_vs_total_scrap.pdf')

def scrap_per_machine(data):
    print("\n")
    print("Scrap per machine function")
    datab = data.copy()
    datab.drop(['FECHA', 'TURNO', 'GRUPO', 'CODIGO', 'PRODUCCION (PZAS)', 'DIA', 'NOMBRE_DIA'], inplace = True, axis = 1)
    datab = datab.groupby('MÁQ,').sum()
    datab['PORCENTAJE'] = datab['SCRAP']/(datab['SCRAP']+datab['TOTAL KG'])*100
    datab = datab.loc[datab['SCRAP']>0]
    datab.sort_values(by = 'PORCENTAJE', ascending = True, inplace = True)
    machines = datab.index.values
    machine_number = len(datab.index.values)
    color = ['indianred', 'darkolivegreen','steelblue', 'saddlebrown']
    init_list = [0,15,30,45]
    for i in range(1,5): # 1 to 4
        target = 15 * i 
        if init_list[i-1] < machine_number:
            fig, axs = plt.subplots(figsize = [15,10] )
            x = machines[init_list[i-1]:target]
            y = datab["PORCENTAJE"].iloc[init_list[i-1]:target]
            bars = axs.bar(x, y, color = color[i-1], alpha = 1 ,linewidth = 0.2)
            axs.set_xlabel('Máquinas')
            axs.set_ylabel('% de Scrap')
            axs.set_title('Porcentaje de scrap por máquina')
            axs.bar_label(bars, label_type = "edge", fmt='%0.1f')
            plt.savefig('scrap per machine_'+str(init_list[i-1]))
        else:
            continue
    
def prod_per_day_per_machine(data):

    print("\n")
    print("Production per day per machine")
    
    df_prod = data.groupby(['MÁQ,']).sum()
    prod_month=[]

    for i in range(0,len(df_prod.index)):
        x =df_prod.loc[df_prod.index[i]]['TOTAL KG']
        prod_month.append(x)
    
    
    
    df_days = data.groupby(by=['DIA','MÁQ,']).sum()
    day_list = []
    for i in range(0,len(df_prod.index)):
        d = 0
        for u in range(1,32):
            try:
                x =df_days.loc[(u, df_prod.index[i])]['TOTAL KG']            
                if x > 0:
                    d = d+1   
            except:
                continue
        day_list.append(d)

    data = { 'PRODUCCION': prod_month, 'DIAS': day_list}
    df = pd.DataFrame(data =data, index = df_prod.index)
    df['PRODUCCION X DIA'] = df['PRODUCCION'] / df['DIAS']
    df['PRODUCCION X DIA'] = df['PRODUCCION X DIA'].round(decimals = 0)
    
    return df

def transform_data_B(data):
    
    df_data = data[['FECHA','GRUPO','MÁQ,','TOTAL KG','SCRAP', 'MATERIAL / CLASES']]
    df_data['FECHA'] = pd.to_datetime(df_data['FECHA'], format= '%Y-%m-%d')
    df_data['DAY'] = df_data['FECHA'].dt.day
    df_data['TOTAL KG'] = df_data['TOTAL KG'].astype('float32')
    df_data['SCRAP'] = df_data['SCRAP'].astype('float32')
    
    return df_data

def grouping_by_shift(data_4, day_analysis):

    df_A = data_4[data_4['DAY'] == day_analysis].groupby(by=['MÁQ,','GRUPO']).sum()
    df_A.drop(columns='DAY', axis = 1, inplace=True)
    df_A['%'] = df_A['SCRAP'] / (df_A['SCRAP'] + df_A['TOTAL KG']) * 100
    return df_A

def grouping_by_material(data_4, day_analysis):
    df_B = data_4.copy()
    df_B['MATERIAL'] = df_B['MATERIAL / CLASES'].apply(lambda x: x[0])
    df_B.drop(columns=['FECHA', 'MÁQ,', 'MATERIAL / CLASES'], inplace=True)
    df_C = df_B[df_B['DAY'] == day_analysis].groupby(by = ['GRUPO','MATERIAL']).sum()
    df_C.drop(columns=['DAY'], axis = 1, inplace=True)
    df_C['%'] = (df_C['SCRAP'] / (df_C['SCRAP'] + df_C['TOTAL KG']))*100

    return df_C


def run():
    section = input("daily anlysis = a; large analysis = b; fusion database with last month data = c: " )
    data = loading_data()
    clean_data(data)

    if section == 'b':
        last_days = int(input("Select a number of days to analyze. Consider that the last day will always be yesterday (Used only in the scrap_vs_production and scrap_vs_total_scrap graphs): "))
        data_1 = transform_data_A(data)
        data_2 = machine_working_days(data_1)
        scrap_vs_production(data_1, last_days)
        scrap_vs_total_scrap(data_1, last_days)
        scrap_per_machine(data_1)
        data_3 = prod_per_day_per_machine(data_1)
        
        os.chdir(PATH_RESULTS)

        with pd.ExcelWriter("large_analysis.xlsx") as writer:
            data_2.to_excel(writer, sheet_name="Sheet1")
            data_3.to_excel(writer, sheet_name="Sheet2")
        

        
    elif section == 'a':
        day = int(input('day of analysis: '))
        data_4 = transform_data_B(data)
        data_5 = grouping_by_shift(data_4, day)
        data_6 = grouping_by_material(data_4, day)

        os.chdir(PATH_RESULTS)

        with pd.ExcelWriter("daily_analysis.xlsx") as writer:
            data_5.to_excel(writer, sheet_name="Sheet1")
            data_6.to_excel(writer, sheet_name="Sheet2")
    
    elif section == 'c':
        path = PATH_RESULTS + '/GLOBAL.xlsx'
        global_data = pd.read_excel(path,header=0,sheet_name="global", names=["FECHA","MÁQ,","CODIGO","TOTAL KG","SCRAP"])
        data_7 = transform_data_A(data)
        data_7 = data_7[['FECHA','MÁQ,', 'CODIGO','TOTAL KG', 'SCRAP']]
        print("globa_data: {}".format(global_data.count()))
        print("month_data: {}".format(data_7.count()))
        new_global_data = pd.concat([global_data, data_7])
        print("global_data: {}".format(new_global_data.count()))

        os.chdir(PATH_RESULTS)

        with pd.ExcelWriter("GLOBAL.xlsx") as writer:
            new_global_data.to_excel(writer, sheet_name="global")
            global_data.to_excel(writer, sheet_name="global_before")


    else:
        print('Wrong input')

   

if __name__=='__main__':
    run()