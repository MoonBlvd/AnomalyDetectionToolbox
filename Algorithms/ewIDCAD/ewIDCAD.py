import numpy as np
import csv
from onlineUpdate import onlineUpdator
from classifier import anomalyDetector

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
    file_path = '../../../circularDataProcess/data/'
    file_name = 'simulating_data_ECG.csv'
    #file_path = '../../Benchmarks/Time Series Data/Intel Lab Data/Temperature/'
    #file_name = 'normalSeqs_data.csv'
    normal_data = dataReader(file_path + file_name)
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
    cov_inv = np.linalg.inv(cov) # We update the inverse of the covariance in practice!
    #print cov_inv
    clusters = [] # a list of arries, each array stores instances of one cluster
    clusters_means = [] # a list of cluster means
    clusters_cov_invs = [] # a list of the inverses of cluster covariances
    chi_square_dists = [] # a list of the chi square distance of each cluster

    clsuters.append(init_samples)
    chi_square_dists.append()
    clusters_means.append(mean) 
    clusters_cov_invs.append(cov_inv)

    # initialize the online updator 
    updators = []
    updators.append(onlineUpdator(alpha, beta, _lambda, mean, cov_inv))
    # initialize the classifier
    classifier = anomalyDetector(gamma)
    print "Start update from the ", k, "th instance to the ", num_seqs,"th instance" 
    for i in range(k, num_seqs):
        print 'Iteration ', i-k
        new_instance = normal_data[i]
        # classify the new instance, f is the cluster label
        f = classifier.classify(clusters_means, clusters_cov_invs, new_instance)
        if f == False: # need a new cluster
            clusters.append(new_instance) # add new cluster
            clusters_means.append(new_instance) # add new instance as the mean of new cluster
            clusters_cov_invs.append(np.ones([num_sensors, num_sensors]))
            updators.append(onlineUpdator(alpha, beta, _lambda, 
                new_instance, np.ones([num_sensors, num_sensors])))
            clusters.append(new_instance)
        else: # update ohe existing cluster
            mean, cov_inv = updators[f].update(i, new_instance)
            cluster[f] = np.vstack(clusters[f], new_instance)
            clusters_means[f] = mean
            clusters_cov_invs[f] = cov_inv
    #print clusters_means
    print '# of clusters is: ', len(clusters_means)


#######
##Try to uses python classes to define each cluster, 
#then use for loop in the main function
