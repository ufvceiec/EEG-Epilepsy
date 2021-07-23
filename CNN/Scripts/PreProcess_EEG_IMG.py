#!pip install stellargraph
#!pip install eegraph              #For Google Collab or Kaggle

import networkx as nx
from EEGRAPH import eegraph
import os
import numpy as np

#Functions that Transform EEG files to Graphs and to Images
#==========================================================================================================
def search(values, searchFor):
    for k in values:
        if (searchFor == k):
            return (values[k])

    
def search_key(values, searchFor):
    for key, value in values.items():
        if value[0] == searchFor:
            return key

def test_identical(c_m):
    print('Identical')
    if type(c_m) != list:
        c_m = c_m.round(decimals=2)
        result = []
        for i in range(len(c_m)):
            for j in range(len(c_m)):
                if(i != j):
                    val = (np.sum(c_m[i] == c_m[j]) / c_m[i].size)
                    if (val > 0.9):
                        result.append(val)
                        print(val)
    print('None')
    
def test_empty(graphs, conn_empty_values, conn):
    conn_empty_aux = [0] * len(conn_empty_values)
    for i in range(len(graphs)):
        if(nx.is_empty(graphs[i])):
            conn_empty_aux[conn] += 1
    
    conn_empty_values[conn] = conn_empty_values[conn] + conn_empty_aux[conn]
    print('Empty:',conn_empty_values)
    return conn_empty_values
        
        

def modelate_with_different_connectivity(window_size, label, connectivity_number_total, G, conn_empty_values, filename):
    total_graphs, total_labels = [], []
    for i in range(connectivity_number_total):
        conn = search_key(connectivity_measures, i)
        bands = search(connectivity_measures, conn)[1]
        

        graphs, c_m = G.modelate(window_size = window_size, connectivity = conn, bands = bands)                         #<--------------- THRESHOLD   , threshold = 0.65

                   
        test_identical(c_m)
        conn_empty_values = test_empty(graphs, conn_empty_values, i)
        
        for i in range(len(graphs)):
            G.visualize(graphs[i],'IMG'+'/'+ str(window_size)+'-seg'+'/'+conn+'/'+label+'/'+ filename + conn + ' - ' + str(i))

    return conn_empty_values

def open_data_directories(path, window_size_class_0, window_size_class_1, connectivity_number_total, exclude):
    conn_empty_values = [0] * connectivity_number_total
    graphs, labels = [], []
    class_files = os.listdir(path)
    for entry in class_files:
        eeg_files = os.listdir(path + '/' + entry)
        for eeg in eeg_files:
            eeg_path = (path + '/' + entry + '/' + eeg)
            print(eeg_path, entry)
            G = eegraph.Graph() 
            G.load_data(path= eeg_path, exclude = exclude)
            
            if(entry == '1'):
                window_size = window_size_class_1
            elif (entry == '0'):
                window_size = window_size_class_0
            
            eeg_name = eeg.split('.')[0]
            conn_empty_values = modelate_with_different_connectivity(window_size, entry ,con_number_total, G, conn_empty_values, eeg_name)
            
 
 

    
#Calls the functions above. 
#====================================================
#['delta', 'theta', 'alpha', 'beta', 'gamma']
#connectivity_measures = {'pearson_correlation': (0, [None])}

connectivity_measures = {'squared_coherence': (0, ['theta', 'alpha', 'beta'])}


path = 'data/data_vigilia'                                      #<--------------- PATH TO FOLDER CONTAINING EEGs
window_size_class_0 = 1                                #<--------------- CLASS 0 WINDOW SIZE
window_size_class_1 = 1                               #<--------------- CLASS 1 WINDOW SIZE
con_number_total = 1                                     #<--------------- NUMBER OF CONNECTIVITY MEASURES USED, MUST BE THE SAME AS LENGTH OF DICTIONARY 'connectivity_measures'
exclude = [] 
open_data_directories(path, window_size_class_0, window_size_class_1, con_number_total, exclude = exclude)

