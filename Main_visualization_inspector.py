import numpy as np
import time
import configparser
import os
import pandas as pd
import csv




def allocate_electrodes():
    electrodes = [True for i in range(1,101)]
    print_electrodes(electrodes) 
    return electrodes   

def print_electrodes(electrodes):
    Spline_name = ['A','B','C','D','E','F','G','H','I','J']
    print('*************************')
    output =''
    for i, elec in enumerate(electrodes):
        if elec:            
            output += Spline_name[(i)//10]
            output += str(i+1-10*((i)//10))            
            output += ' '
    # print(f'{electrodes}')
    print(output)

def Run_Thread():    
    config = configparser.ConfigParser()
    path_ = os.getcwd()
    configuration = config.read(path_+'/config.ini')    
    folder_path = config['Carto_Path']['Carto_Path']
    catheter = config['Carto_Path']['Catheter']
    tolerance = float(config['Carto_Path']['Tolerance'])
    print(f'Looking into {folder_path}')
    electrodes= allocate_electrodes()
    files = os.listdir(folder_path)    
    if len(files):
        for file in files:
            electrodes = File_analyzer(os.path.join(folder_path,file),electrodes,tolerance)

    while True :
        files = os.listdir(folder_path)
        # if len(files) == 0:
        #     print('The folder is empty')
        #     break
        electrodes = File_analyzer(os.path.join(folder_path,files[-1]),electrodes,tolerance)
        # print(Data.head(5))
        print_electrodes(electrodes)
        try:
            first_elec = electrodes.index(True)
            filename = os.path.join(folder_path,files[-1])
            Data = Read_file_data(filename)
            Data_np = np.array(Data)
            Navi_Elec = Data_np[:,0:3]            
            Basket_Elec = Get_electrode_data(first_elec,Data_np)
            min_dist = (Basket_Elec - Navi_Elec)
            distance_to_next_elec = np.sqrt(min_dist[:,0]*min_dist[:,0] +min_dist[:,1]*min_dist[:,1]+min_dist[:,2]*min_dist[:,2])
            print(f'Distance to the next electrode: {np.round(distance_to_next_elec[-1],2)}')
        except:
            print('Sequence complete......')
            print('Exiting......')
            time.sleep(5)
            exit()

        time.sleep(0.5)


def Get_electrode_data(elec_id,Data_np):
    return Data_np[:,33+3*elec_id:36+3*elec_id]

def File_analyzer(filename,electrodes,tolerance):
    Data = Read_file_data(filename)
    Data_np = np.array(Data)
    Navi_Elec = Data_np[:,0:3]
    for el_num, el in enumerate(electrodes):            
        if el:
            try:
                Basket_Elec = Get_electrode_data(el_num,Data_np)
                min_dist = (Basket_Elec - Navi_Elec)
                dist = np.sqrt(min_dist[:,0]*min_dist[:,0] +min_dist[:,1]*min_dist[:,1]+min_dist[:,2]*min_dist[:,2])
                # print(f'Electrode # {el_num}, distance {np.min(dist)}')
                if np.min(dist)<=tolerance:
                    electrodes[el_num] = False
            except:
                pass
    return electrodes

def Read_file_data(path_):
    Data = []
    with open(path_,'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count +=1
                continue
            else:
                Data.append([float(i) for i in row if len(i)])
            line_count+=1
    return Data

if __name__ == "__main__":
    print('Starting visualization POD pivot')
    Run_Thread()
    
