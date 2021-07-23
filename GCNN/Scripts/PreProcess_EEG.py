#!pip install stellargraph
#!pip install eegraph              #For Google Collab or Kaggle

import networkx as nx
import pandas as pd
import numpy as np
import eegraph
import stellargraph as sg
from stellargraph import StellarGraph
import os
import pickle

#Functions that Transform EEG files to Graphs for StellarGraph with Connectivity Matrix and Feature Matrix
#==========================================================================================================
def search(values, searchFor):
    for k in values:
        if (searchFor == k):
            return (values[k])

    
def search_key(values, searchFor):
    for key, value in values.items():
        if value[0] == searchFor:
            return key
        
        
def convert_Graphs(graphs, connectivity_matrix, bands_number, connectivity_measure, label):
    
    output_graphs, labels = [], []
    
    count = -1
    for i in range (len(graphs)):
        
        if(count>= (bands_number-1)):
            count = 0
        else:
            count += 1
        
        #Obtain graph nodes, and nodes without connections
        graph_nodes = list(graphs[i])
        nodes_with_no_edges = list(nx.isolates(graphs[i]))
        edges = [e for e in graphs[i].edges]
        
        #Create feature matrix (NxD, N: Number of Nodes, D: Number of connectivity measures)
        features_matrix = np.zeros(shape = (len(graph_nodes), bands_number))
        #Create array of 1´s, for each node
        x = np.ones(len(graph_nodes))
    
        #If the node has no connections, change its value to 0
        for j in range(len(nodes_with_no_edges)):
            index = graph_nodes.index(nodes_with_no_edges[j])
            x[index] = 0

        #Change the column for the desire connectivity measure with the node´s values. 
        features_matrix[:,count] = x
        
        
        features_pd = pd.DataFrame({'0': list(features_matrix[:,0]), '1': list(features_matrix[:,1]), '2': list(features_matrix[:,2])}, index = graph_nodes)
        
        """
        features_pd = pd.DataFrame({'0': list(features_matrix[:,0]), '1': list(features_matrix[:,1]), '2': list(features_matrix[:,2]), 
                                    '3': list(features_matrix[:,3]), '4': list(features_matrix[:,4]), '5': list(features_matrix[:,5]),
                                   '6': list(features_matrix[:,6]), '7': list(features_matrix[:,7]), '8': list(features_matrix[:,8]),
                                   '9': list(features_matrix[:,9]), '10': list(features_matrix[:,10]), '11': list(features_matrix[:,11])}, index = graph_nodes)
        """

        s = StellarGraph.from_networkx(graphs[i], node_features = features_pd)
        

        output_graphs.append(s)
        labels.append(str(label))

    return output_graphs, labels


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
        
        

def modelate_with_different_connectivity(window_size, label, bands_number, G, conn_empty_values):
    total_graphs, total_labels = [], []
    for i in range(connectivity_number_total):
        conn = search_key(connectivity_measures, i)
        bands = search(connectivity_measures, conn)[1]
        
        graphs, c_m = G.modelate(window_size = window_size, connectivity = conn, bands = bands)                         #<--------------- THRESHOLD , threshold = 0.2
        test_identical(c_m)
            
        conn_empty_values = test_empty(graphs, conn_empty_values, i)

        output_graphs, labels = convert_Graphs(graphs, c_m, bands_number, conn, label)

        total_graphs = total_graphs + output_graphs
        total_labels = total_labels + labels


    return total_graphs, total_labels, conn_empty_values

def open_data_directories(path, window_size_class_0, window_size_class_1, bands_number, exclude, connectivity_number_total):
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
            
            final_graphs, final_labels, conn_empty_values = modelate_with_different_connectivity(window_size, entry ,bands_number, G, conn_empty_values)
            
            graphs = graphs + final_graphs
            labels = labels + final_labels
        
    return graphs, labels


"""
connectivity_measures = {'cross_correlation': (0, [None]), 'pearson_correlation': (1, [None]), 'squared_coherence': (2, ['delta', 'theta', 'alpha', 'beta']),
                         'imag_coherence': (3, ['delta', 'theta', 'alpha', 'beta']), 'corr_cross_correlation': (4, [None]),  
                         'power_spectrum': (5, ['delta', 'theta', 'alpha', 'beta']), 'spectral_entropy': (6, ['delta', 'theta', 'alpha', 'beta']), 
                         'shannon_entropy': (7, [None]), 'dtf':(8,['delta', 'theta', 'alpha', 'beta'])}   
"""  
 

connectivity_measures = {'squared_coherence': (0, ['theta', 'alpha', 'beta'])}   #CONNECTIVITY MEASURES USED


#Calls the functions above. 
#====================================================
path = 'data/data_vigilia'                                            #<--------------- PATH TO FOLDER CONTAINING EEGs
window_size_class_0 = 1                                 #<--------------- CLASS 0 WINDOW SIZE
window_size_class_1 = 1                               #<--------------- CLASS 1 WINDOW SIZE
connectivity_number_total = 1
bands = 3                                     #<--------------- NUMBER OF FREQUENCY BANDS USED
exclude = [] 
graphs, x1_labels = open_data_directories(path, window_size_class_0, window_size_class_1, bands, exclude, connectivity_number_total)





#Print generated graphs details. 
#====================================================
labels = pd.Series(x1_labels, dtype='category', name='label')
print(labels)

summary = pd.DataFrame(
    [(g.number_of_nodes(), g.number_of_edges()) for g in graphs],
    columns=["nodes", "edges"],
)
print(summary.describe().round(1))

print(labels.value_counts().to_frame())




#Save graphs and labels. 
#====================================================
with open("graphs.txt", "wb") as fp:   # Pickling
    pickle.dump(graphs, fp)

with open("labels.txt", "wb") as fp:   # Pickling
    pickle.dump(labels, fp)