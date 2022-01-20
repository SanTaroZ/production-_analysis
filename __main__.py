import numpy as np
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

def loading_data():
    print("\n")
    print("loading data function")
    path = "D:/Notas de Estudio/Proyectos/production_analysis__project/production_analysis/data/raw/"
    file = []

    for (dirpath, dirnames, filenames) in os.walk("D:/Notas de Estudio/Proyectos/production_analysis__project/production_analysis/data/raw"):
        file.extend(filenames)
        print("Loading file...")
        print(file[1]) 

    path = path + file[1]
    data = pd.read_excel(path, sheet_name="Prod. EXTR",header=0)
    print("cleaning data...")
    print("deleting unnecessary columns")
    data = data [['FECHA', 'TURNO', 'GRUPO', 'MÁQ.', 'CODIGO', 'PRODUCCION (PZAS)','TOTAL KG', 'SCRAP']]
    print("Column FECHA")
    data = data[data["FECHA"].notna()]
    data = data[data["FECHA"] != "Total"]
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
    data.loc[:,'SCRAP'] = data['SCRAP'].fillna(0)
    data['SCRAP'] = data['SCRAP'].astype('float')
    print("Saving data in csv file...")
    #PATH
    os.chdir("D:/Notas de Estudio/Proyectos/production_analysis__project/production_analysis/data/processed/")
    print(os.getcwd())
    data.to_csv('data.csv', index=False)

def machine_working_days():
    print("\n")
    print("machines working days function")
    #file_data= "D:/Notas de Estudio/Proyectos/production_analysis__project/production_analysis/data/processed/data.csv"
    print('reading data.csv')
    df = pd.read_csv("data.csv", header = 0, index_col = False)
    test = df.groupby(['DIA', 'MÁQ.']).sum()
    df_group = df.groupby(['MÁQ.','DIA']).sum()

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

    print('saving file...')
    machines_days_of_work = pd.Series(data = machines_dict, index =None)
    machines_days_of_work.sort_values(ascending = True, inplace = True)
    machines_days_of_work.to_csv('machines_days_of_work.csv', index = True, header = False)
      
def scrap_vs_production():
    print("\n")
    print("Scrap vs production function")
    #file_data= "D:/Notas de Estudio/Proyectos/production_analysis__project/production_analysis/data/processed/data.csv"
    print('reading data.csv')
    df = pd.read_csv("data.csv")
    df_A=df.groupby("MÁQ.").sum()
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
    plt.savefig('scrap_vs_production.pdf')

    print("Scrap tendency per machine")
    df_C = df.groupby(['DIA','MÁQ.']).sum()
    days = set(df['DIA'].values)
    days_list = list(days)
    days = days_list[-7:]
    values_scrap = {}

    for machine in list_A:
        scrap_list = []
        for day in days:
            scrap = df_C.loc[(day, machine)].loc['SCRAP']
            scrap_list.append(scrap)
        values_scrap[machine] = scrap_list
    
    y = values_scrap
    titles = []
    for values in y.keys():
        titles.append(values)

    fig_b = plt.figure(figsize=(20, 40), constrained_layout=True)

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

def scrap_vs_total_scrap():
    print("\n")
    print("Scrap vs total scrap function")
    #file_data= "D:/Notas de Estudio/Proyectos/production_analysis__project/production_analysis/data/processed/data.csv"
    print('reading data.csv')
    df = pd.read_csv("data.csv")
    df_B = df.groupby('MÁQ.').sum()
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
    df_C = df.groupby(['DIA','MÁQ.']).sum()
    days = set(df['DIA'].values)
    days_list = list(days)
    days = days_list[-7:]
    values_scrap_b = {}

    for machine in list_B:
        scrap_list = []
        for day in days:
            scrap = df_C.loc[(day, machine)].loc['SCRAP']
            scrap_list.append(scrap)
        values_scrap_b[machine] = scrap_list

    y_b = values_scrap_b
    titles_b = []
    for values in y_b.keys():
        titles_b.append(values)

    fig_b = plt.figure(figsize=(20, 40), constrained_layout=True)

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

def cross_information():
    print("\n")
    print("Cross information function")
    #file_data= "D:/Notas de Estudio/Proyectos/production_analysis__project/production_analysis/data/processed/data.csv"
    print('reading data.csv')
    df = pd.read_csv("data.csv")
    print("table A")
    df_main = df.groupby('MÁQ.').sum()
    df_main.drop('DIA', inplace = True, axis = 1)
    df_A=df.groupby("MÁQ.").sum()
    df_A['PORCENTAJE'] = df_A['SCRAP']/(df_A['SCRAP']+df_A['TOTAL KG'])*100
    df_A.sort_values(by = ["PORCENTAJE"],ascending = False, inplace = True)
    print("table B")
    df_B = df.groupby('MÁQ.').sum()
    df_B.drop('DIA',inplace = True, axis = 1)
    total_scrap = df_B['SCRAP'].sum()
    df_B['SCRAP/TOTAL SCRAP'] = df_B['SCRAP'].apply(lambda x: (x/total_scrap)*100 )
    df_B.sort_values(by = ['SCRAP/TOTAL SCRAP'],ascending = False, inplace = True )
    print("common list")
    list_A = set(df_A.index[0:15])
    list_B = set(df_B.index[0:15])
    common_list = list_A.intersection(list_B)
    common_list= list(common_list)
    common_list= pd.Series(common_list)
    common_list.to_csv("common list.txt",sep = '\t',header = False)

def scrap_per_machine():
    print("\n")
    print("Scrap per machine function")
    data = pd.read_csv("data.csv")
    data.drop(['FECHA', 'TURNO', 'GRUPO', 'CODIGO', 'PRODUCCION (PZAS)', 'DIA', 'NOMBRE_DIA'], inplace = True, axis = 1)
    data = data.groupby('MÁQ.').sum()
    data['PORCENTAJE'] = data['SCRAP']/(data['SCRAP']+data['TOTAL KG'])*100
    data = data.loc[data['SCRAP']>0]
    data.sort_values(by = 'PORCENTAJE', ascending = True, inplace = True)
    machines = data.index.values
    n = 1
    mac = len(machines)
    while mac>15:
        mac = mac -15
        n=n+1

    color = ['indianred', 'darkolivegreen','steelblue', 'saddlebrown']
    fig = plt.subplots(figsize = [20,40],constrained_layout=True)

    initial_value = 0 
    last_value = 15
    for i in range(n):
        plt.subplot(4,1,i+1)
        x = machines[initial_value:last_value]
        y = data["PORCENTAJE"].iloc[initial_value:last_value]
        bars = plt.bar(x, y, color = color[i], alpha = 1, linewidth = 0.2)
        plt.xlabel('Máquinas')
        plt.ylabel('Scrap')
        plt.title('Porcentaje de scrap por máquina')
        plt.bar_label(bars, label_type = "edge", fmt='%0.1f')
        plt.minorticks_on()
    
        
    
        initial_value = initial_value + 15
        last_value = last_value +15

            
    #plt.show()
    plt.savefig('scrap per machine')
    

def run():
    loading_data()
    machine_working_days()
    scrap_vs_production()
    scrap_vs_total_scrap()
    cross_information()
    scrap_per_machine()
    
      


if __name__=='__main__':
    run()