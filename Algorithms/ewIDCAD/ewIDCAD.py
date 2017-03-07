import numpy as np
import csv
from clusters import cluster
import matplotlib.pyplot as plt

def find_min_distance(clusters, new_instance):
    min_distance = np.inf
    for i in range (0, len(clusters)):
        distance = clusters[i].compute_distance(new_instance)    
        if distance < min_distance:
            min_distance = distance
            min_index = i
    return min_distance, min_index

def dataReader(file_path):
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

if __name__ == '__main__':
    file_path = '../../Benchmarks/Time Series Data/'
    file_name = 'simulating_data_ECG.csv'
    #file_path = '../../Benchmarks/Time Series Data/Intel Lab Data/Temperature/'
    #file_name = 'normalSeqs_data.csv'
    normal_data = dataReader(file_path + file_name)
    normal_data = normal_data[:,2:4]
    #print normal_data.shape
    #normal_data = np.append(normal_data, normal_data[:,[0]]**2, 1)
    #normal_data = np.append(normal_data, normal_data[:,[1]]**2, 1)
    print normal_data
    num_seqs, num_sensors = normal_data.shape
    
    # Parameters configuration
    _lambda = 0.95 # forgetting factor
    gamma = 0.90 # probability of misclassification 
    f = False # classification label, False means not belongs to any existing clusters
    alpha = 1 # 
    beta = 1 #

    start = 50 # skip the first 50 points
    k = 100 # num of initial samples
    init_samples = normal_data[start:k][:]
    mean = init_samples.mean(axis = 0)
    cov = np.cov(init_samples.T)
    #print cov

    # initialize the online updator 
    clusters = []
    clusters.append(cluster(init_samples, alpha, beta, _lambda, mean, cov, gamma))
    print "Start update from the ", k, "th instance to the ", num_seqs,"th instance" 
    for i in range(k, num_seqs):
        print 'Iteration ', i-k
        new_instance = normal_data[i][:]
        # classify the new instance, f is the cluster label
        distance, index = find_min_distance(clusters, new_instance)
        f = clusters[index].classify(index, distance) 
        if f == False: # add new cluster
            mean = new_instance
            cov = np.eye(num_sensors)
            clusters.append(cluster(new_instance, alpha, beta, _lambda, mean, cov, gamma))
        else:
            _,_ = clusters[f].update(new_instance)

    # print results and plot informations
    num_clusters = len(clusters)
    print '# of clusters is: ', num_clusters
    color = np.zeros([num_clusters, 3]) 
    color[:,0] = np.array(range(0,num_clusters))/(num_clusters-1)#R
    color[:,1] = np.array(range(num_clusters,0,-1))/(num_clusters-1)#G
    color[:,2] = np.array(range(num_clusters,0,-1))/(num_clusters-1)#B
    plt.figure(1) 
    plt.plot(normal_data[:,0], normal_data[:,1], '*', markersize = 5)
    plt.xlabel('speed [km/h]')
    plt.ylabel('steering [rad]')
    plt.figure(2)
    for j in range (0,num_clusters):
        plt.plot(clusters[j].elements[:,0], clusters[j].elements[:,1],'*', color = color[j])
    plt.xlabel('speed [km/h]')
    plt.ylabel('steering [rad]')
    plt.show()


#######
##Try to uses python classes to define each cluster, 
#then use for loop in the main function
