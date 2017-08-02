import numpy as np
import csv
from clusters import cluster
from plot_results import plot_results
from feature_extraction import extractor
import sys
from scipy.stats import chi2
import time

# Parameters configuration
_lambda = 0.95 # forgetting factor
gamma = 0.98 # probability of misclassification 
f = np.inf # classification label, False means not belongs to any existing clusters
alpha = 2 # initialize alpha and beta
beta = 2 #
start = 3 # size of initial set is 3
stablization = 10
tmp = 0.5
classify_type = 'chi_square'

def find_min_distance(clusters, new_instance):
    min_distance = np.inf
    min_index = 0
    for i in range (0, len(clusters)):
        distance = clusters[i].compute_distance(new_instance)    
        if distance < min_distance:
            min_distance = distance
            min_index = i
    return min_distance, min_index

def loda_files(argv):
    data_name = argv[1] # name of the dataset we tested on 
    file_path = '../data/'+data_name+'/'
    if data_name == 'IBRL':
        data_file_name = 'IBRL_18_25000-28800_temp_hum.csv'
    elif data_name == 'GSB':    
        data_file_name = 'GSB_12_Oct_temp_humi_mean.csv'
    elif data_name == 'LG':
        data_file_name = 'LG_18_Oct_temp_humi_mean.csv'
    elif data_name == 'gas':
        data_file_name = 'ethylene_CO_5mins.csv'
    elif data_name == 'rollover':
        data_file_name = 'Car_RollOverData_1_6D.csv'
    elif data_name[0] == 'S':
        data_file_name = data_name + '.csv'
    elif data_name == 'traffic':
        num = argv[2]
        data_file_name == 'anomalous_17D_8D_' +str(num)+ ".csv"
    fields_file_name = data_name + '_fields.csv'
    normal_data = read_data(file_path + data_file_name)
    fields = read_fields(file_path + fields_file_name)

    return normal_data, fields

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

def read_fields(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter = ',')
        for line in reader:
            for i in range (0, len(line)):
                if line[i] == '':
                    line = line[0:i]
                    break
            return line

def two_separated(state_tracker, clusters):
    separatable = True
    for single_cluster in clusters:
        norm_1 = np.linalg.norm((state_tracker.mean-single_cluster.mean), 1)
        p = len(state_tracker.mean)
        max_eigval_1 = max(np.linalg.eigvals(np.linalg.pinv(state_tracker.cov_inv)))
        max_eigval_2 = max(np.linalg.eigvals(np.linalg.pinv(single_cluster.cov_inv)))
        if norm_1 < 2*np.sqrt(p*max(max_eigval_1, max_eigval_2)):
            separatable = False
    return separatable

if __name__ == '__main__':
    feature_extractor = extractor()
    # initialization
    cum_anomalies = 2
    anomalies = None
    tmp_index = None
    anomalies_index = []
    big_anomalies_index = []
    gamma1 = 0.99
    gamma2 = 0.999
    chi_1 = chi2.ppf(gamma1, num_sensors)
    chi_2 = chi2.ppf(gamma2, num_sensors)
    B = None

    # read data and fields
    #algorithm = sys.argv[1] # the algorithm we use

    normal_data, fields = load_files(sys.argv)
    num_seqs, num_sensors = normal_data.shape

    # feature extractor
    normal_data = feature_extractor.extract(normal_data)
    # get initial samples
    init_samples = normal_data[:start][:]
    #init_samples = feature_extractor.extract(init_samples)
    mean = init_samples.mean(axis = 0)
    cov_inv = np.eye(init_samples.shape[1])

    # initialize the online updator 
    clusters = []
    clusters.append(cluster(init_samples, alpha, beta, _lambda, mean, cov_inv, gamma))
    state_tracker = cluster(init_samples, alpha, beta, _lambda, mean, cov_inv, gamma)
    print "Start update from the ", start, "th instance to the ", num_seqs,"th instance" 

    for i in range(start, num_seqs):
        anomaly = True
        update_clusters = []
        print 'Iteration ', i-start
        new_instance = normal_data[i,:]
        #new_instance = np.reshape(normal_data[i,:], (1,num_sensors))
        
        # extract features
        #new_instance = feature_extractor.extract(new_instance)
 
        for single_cluster in clusters:
            t = single_cluster.compute_distance(new_instance)
            if t < chi_1:
                print "the data belongs to one cluster"
                anomaly = False
            if t > chi_2:
                print "the data is far from one cluster"
                continue
            #clusters.remove(single_cluster)
            update_clusters.append(single_cluster)
        for single_cluster in update_clusters:
            clusters.remove(single_cluster)
        if anomaly:
            print "the new instance is anomaly"
            if B == None:
                B = new_instance
            else:
                B = np.vstack([B, new_instance])
            anomalies_index.append(i)
        else:
            print "the new instance is normal"
            B = None

        for j in range(len(update_clusters)):
            #save_flag = True
            update_clusters[j].update(new_instance)
            #save_flag = False
        state_tracker.update(new_instance)

        if j >= 0:
            clusters.extend(update_clusters) 

        if B != None and len(B) > num_sensors+1:
            print 'Iteration ', i-start
            print "number of consequent anomalies: ", len(B)
            big_anomalies_index.append(i)
            if two_separated(state_tracker, clusters):
                print "It's two separated!"
                mean = np.mean(B, 0)
                cov_inv = np.linalg.pinv(np.cov(B.T))
                clusters.append(cluster(B, alpha, beta, _lambda, mean, cov_inv, gamma))
                B = None

# -------------------------------------------------------------------------
    num_clusters = len(clusters)
    num_anomalies = len(anomalies_index)
    num_big_anomalies = len(big_anomalies_index)
    print '# of clusters is: ', num_clusters
    print '# of anomalies is: ', num_anomalies
    print '# of big anomalies is: ', num_big_anomalies
    print 'big anomalous clusters are: ', big_anomalies_index
    print 'all anomalous clusters are: ', anomalies_index
    # plot results
    plotter = plot_results(normal_data, fields, clusters, anomalies_index, 
            big_anomalies_index, num_seqs, start)
    x_label = 0
    y_label = 1
    plotter.plot(x_label, y_label)
