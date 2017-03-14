import numpy as np
import csv
from clusters import cluster
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

#from featureExtractor import feature_extractor

# Parameters configuration
_lambda = 0.95 # forgetting factor
gamma = 0.98 # probability of misclassification 
f = np.inf # classification label, False means not belongs to any existing clusters
alpha = 1 # 
beta = 1 #
start = 0 # skip the first 50 points
k = 50 # num of initial samples
classify_type = 'chi_square'
#classify_type = '3_sigma'

def find_min_distance(clusters, new_instance):
    min_distance = np.inf
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
    file_path = '../../Benchmarks/Time Series Data/'
    data_file_name = 'IBRL_18_25000-28800_temp_hum.csv'
    normal_data = read_data(file_path + data_file_name)
    num_seqs, num_sensors = normal_data.shape
    # get initial data
    init_samples = normal_data[start:k][:]
    mean = init_samples.mean(axis = 0)
    cov = np.cov(init_samples.T)

    # initialize the online updator 
    clusters = []
    clusters.append(cluster(init_samples, alpha, beta, _lambda, mean, cov, gamma))
    anomalies = None
    all_anomalies = np.zeros(num_sensors)[None,:]
    cum_anomalies = 3
    j = 0
    print "Start update from the ", k, "th instance to the ", num_seqs,"th instance" 

    for i in range(k, num_seqs):
        print 'Iteration ', i-k
        new_instance = normal_data[i][:]
        # classify the new instance, f is the cluster label
        distance, index = find_min_distance(clusters, new_instance)
        f = clusters[index].classify(index, distance, new_instance, classify_type) 
        if f == np.inf: # add new cluster
            if anomalies == None:
                anomalies = new_instance
            else:
                anomalies = np.vstack([anomalies, new_instance])
            _,_ = clusters[0].update(new_instance)
            j += 1
        else:
            if j > cum_anomalies:
                print"the anomalies are: ", anomalies
                all_anomalies = np.vstack([all_anomalies, anomalies])
            j = 0
            anomalies = None
            _,_ = clusters[f].update(new_instance)

    # print results and plot informations
    num_clusters = len(clusters)
    num_anomalies = all_anomalies.shape[0]-1
    if num_anomalies == 0 and anomalies != None:
        all_anomalies = np.vstack([all_anomalies, anomalies])
    print '# of clusters is: ', num_clusters
    print '# of anomalies is: ', all_anomalies.shape[0]-1
    plt.figure(1) 
    plt.plot(normal_data[:,0], normal_data[:,1], 'g*', markersize = 5)
    plt.xlabel('Temperature [degC]')
    plt.ylabel('Humidity [%]')
    plt.figure(2)
    for j in range (0,num_clusters):
        plt.plot(clusters[j].elements[:,0], clusters[j].elements[:,1],'g*')
    plt.plot(all_anomalies[1:,0], all_anomalies[1:,1], 'ro')
    plt.xlabel('Temperature [degC]')
    plt.ylabel('Humidity [%]')
    plt.show()


#######
##Try to uses python classes to define each cluster, 
#then use for loop in the main function

