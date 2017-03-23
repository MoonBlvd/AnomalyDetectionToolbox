import numpy as np
import csv
from clusters import cluster
from plot_results import plot_results
import sys

#from featureExtractor import feature_extractor

# Parameters configuration
_lambda = 0.95 # forgetting factor
gamma = 0.98 # probability of misclassification 
f = np.inf # classification label, False means not belongs to any existing clusters
alpha = 2 # initialize alpha and beta
beta = 2 #
start = 1 # skip the first 50 points
k = 3 # k-stary is the num of initial samples
stablization = 10
classify_type = 'chi_square'
#classify_type = '3_sigma'

def find_min_distance(clusters, new_instance):
    min_distance = np.inf
    min_index = 0
    for i in range (0, len(clusters)):
        distance = clusters[i].compute_distance(new_instance)    
        if distance < min_distance:
            min_distance = distance
            min_index = i
    return min_distance, min_index

def read_data(file_path):
    # The read-in data should be a N*W matrix,
    # where N is the length of the time sequences,
    # W is the number of sensors/data features
    i = 0
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter = ',')
        for line in reader:
            line = np.array(line, dtype = 'float') # str2float
            if i == 0:
                data = line
            else:
                data = np.vstack((data, line))
            i += 1
    return data

def read_data_fields(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter = ',')
        for line in reader:
            for i in range (0, len(line)):
                if line[i] == '':
                    line = line[0:i]
                    break
            return line

if __name__ == '__main__':
    # read data and fields
    #file_path = '../../Benchmarks/Time Series Data/IBRL/'
    #data_file_name = 'IBRL_18_25000-28800_temp_hum.csv'
    file_path = '../../Benchmarks/Time Series Data/Car_Simulation/'
    data_file_name = 'simulating_data_ref.csv'
    normal_data = read_data(file_path + data_file_name)
    num_seqs, num_sensors = normal_data.shape
    # get initial samples
    init_samples = normal_data[start:k][:]
    mean = init_samples.mean(axis = 0)
    cov = np.cov(init_samples.T)

    # initialize the online updator 
    clusters = []
    clusters.append(cluster(init_samples, alpha, beta, _lambda, mean, cov, gamma))
    anomalies = None
    cum_anomalies = 4
    j = 0
    tmp_index = None
    big_anomalies_index = np.zeros(1)
    print "Start update from the ", k, "th instance to the ", num_seqs,"th instance" 

    for i in range(k, num_seqs):
        print 'Iteration ', i-k
        new_instance = normal_data[i][:]
        # classify the new instance, f is the cluster label
        distance, index = find_min_distance(clusters, new_instance)
        f = clusters[index].classify(index, distance, new_instance, classify_type) 
        if f == np.inf: # add new anomaly to a temperal anomaly list.
            if i > stablization:
                if anomalies == None:
                    anomalies = new_instance
                    tmp_index = i
                else:
                    anomalies = np.vstack([anomalies, new_instance])
                    tmp_index = np.vstack([tmp_index, i])
                j += 1
        else: # no new anomalies detected, reset the temperal anomaly list.
            if j > cum_anomalies: # if there are consecutive anomalies
                print"the anomalies are: ", anomalies
                big_anomalies_index = np.vstack([big_anomalies_index, tmp_index])
            j = 0
            tmp_index = None
        _,_ = clusters[index].update(new_instance)

    # print results and plot informations
    num_clusters = len(clusters)
    num_anomalies = anomalies.shape[0]-1
    num_big_anomalies = len(big_anomalies_index)
    big_anomalies_index = np.ndarray.tolist(big_anomalies_index)
    if num_anomalies == 0 and anomalies != None:
        print 'No anomalies are detected!'
        sys.exit()
    print '# of clusters is: ', num_clusters
    print '# of anomalies is: ', num_anomalies
    print '# of big anomalies is: ', num_big_anomalies
    print big_anomalies_index
    
    # plot results
    plotter = plot_results(normal_data, clusters, big_anomalies_index, num_seqs, start)
    plotter.plot()
