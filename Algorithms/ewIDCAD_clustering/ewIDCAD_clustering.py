import numpy as np
import csv
from clusters import cluster
from plot_results import plot_results
from feature_extraction import extractor
import sys
from scipy.stats import chi2
import time
#from featureExtractor import feature_extractor

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

def read_fields(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter = ',')
        for line in reader:
            for i in range (0, len(line)):
                if line[i] == '':
                    line = line[0:i]
                    break
            return line

def two_separated(curr_cluster, clusters):
    separatable = True
    for single_cluster in clusters:
        norm_1 = np.linalg.norm((curr_cluster.mean-single_cluster.mean), 1)
        p = len(curr_cluster.mean)
        max_eigval_1 = max(np.linalg.eigvals(np.linalg.pinv(curr_cluster.cov_inv)))
        max_eigval_2 = max(np.linalg.eigvals(np.linalg.pinv(single_cluster.cov_inv)))
        if norm_1 < 2*np.sqrt(p*max(max_eigval_1, max_eigval_2)):
            separatable = False
    return separatable


if __name__ == '__main__':
    # read data and fields
    #file_path = '../../Benchmarks/Time Series Data/IBRL/'
    #data_file_name = 'IBRL_18_25000-28800_temp_hum.csv'
    #fields_file_name = 'IBRL_fields.csv'
    #data_file_name = 'GSB_12_Oct_temp_humi_mean.csv'
    #fields_file_name = 'GSB_fields.csv'
    #data_file_name = 'LG_18_Oct_temp_humi_mean.csv'
    #fields_file_name = 'LG_fields.csv'

    #file_path = '../../Benchmarks/Time Series Data/Car_Simulation/'
    #data_file_name = 'Car_NormalData_1_6D.csv'
    #fields_file_name = 'rollover_fields.csv'

    #file_path = '../../Nan_Traffic_Simulator/anomalous_data/'
    #data_file_name = 'anomalous_2.csv'
    #fields_file_name = 'traffic_fields.csv'

    file_path = '../../Nan_Traffic_Simulator/anomalous_data/'
    data_file_name = 'anomalous_5D.csv'
    fields_file_name = '5D_fields.csv'

    normal_data = read_data(file_path + data_file_name)
    fields = read_fields(file_path + fields_file_name)
    num_seqs, num_sensors = normal_data.shape

    # init feature extractor
    feature_extractor = extractor()

    # get initial samples
    init_samples = normal_data[:start][:]
    init_samples = feature_extractor.extract(init_samples)
    mean = init_samples.mean(axis = 0)
    cov_inv = np.eye(num_sensors)

    # initialize the online updator 
    clusters = []
    init_type = 'normal'
    clusters.append(cluster(init_samples, alpha, beta, _lambda, mean, cov_inv, gamma, tmp, init_type))
    anomalies = None
    cum_anomalies = 2
    j = 0
    tmp_index = None
    anomalies_index = np.array([0])
    big_anomalies_index = np.zeros(1)
    print "Start update from the ", start, "th instance to the ", num_seqs,"th instance" 
    k = 0
    curr_cluster = cluster(init_samples, alpha, beta, _lambda, mean, cov_inv, gamma, tmp, init_type)
    #curr_cluster = clusters[k]
    
    gamma1 = 0.99
    gamma2 = 0.999
    chi_1 = chi2.ppf(gamma1, num_sensors)
    chi_2 = chi2.ppf(gamma2, num_sensors)


    anomalies_index = []
    big_anomalies_index = []
    #omega = []
    B = None
    for i in range(start, num_seqs):
        anomaly = True
        update_clusters = []
        print 'Iteration ', i-start
        new_instance = normal_data[i][:]
        # extract features
        new_instance = feature_extractor.extract(new_instance)
 
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
            #omega.append(np.exp(-t/2))
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
        #omega = omega/sum(omega)


        for j in range(len(update_clusters)):
            update_clusters[j].update(new_instance)
        curr_cluster.update(new_instance)

        if j >= 0:
            clusters.extend(update_clusters) 

        if B != None and len(B) > num_sensors+1:
            print 'Iteration ', i-start
            print "number of consequent anomalies: ", len(B)
            big_anomalies_index.append(i)
            if two_separated(curr_cluster, clusters):
                print "It's two separated!"
                mean = np.mean(B, 0)
                cov_inv = np.linalg.pinv(np.cov(B.T))
                clusters.append(cluster(B, alpha, beta, _lambda, mean, cov_inv, gamma, tmp, init_type))
                B = None

# -------------------------------------------------------------------------
        '''
        distance = curr_cluster.compute_distance(new_instance)
        if distance < curr_cluster.chi_square:
            clusters[k].update(new_instance)
            curr_cluster = clusters[k]
        else:
            if curr_cluster.type is 'normal':
                k += 1
                curr_cluster.update(new_instance)
                clusters.append(cluster(new_instance, curr_cluster.alpha, curr_cluster.beta,\
                                        _lambda, curr_cluster.mean, curr_cluster.cov_inv,\
                                        gamma, curr_cluster.tmp, 'anomalous'))
                curr_cluster = clusters[k]
            elif curr_cluster.type is 'anomalous':
                k += 1
                curr_cluster.update(new_instance)
                clusters.append(cluster(new_instance, curr_cluster.alpha, curr_cluster.beta,\
                                        _lambda, curr_cluster.mean, curr_cluster.cov_inv,\
                                        gamma, curr_cluster.tmp, 'normal'))
                curr_cluster = clusters[k]
        '''
# ----------------------------------------------------------------------------
        '''
                curr_cluster.update(x)
                distance, index = find_min_distance(clusters, new_instance)
                
                if distance < clusters[index].chi_square:
                    clusters[index].augment_element(new_instance)
                else:
                    k += 1
                    clusters.append(cluster(x, curr_cluster.alpha, curr_cluster.beta,\
                                            _lambda, curr_cluster.mean, curr_cluster.cov_inv,\
                                            gamma, curr_cluster.tmp, 'anomalous'))
                    curr_cluster = clusters[k]
        '''     
# ---------------------------------------------------------------------------        
        '''
        # classify the new instance, f is the cluster label
        distance, index = find_min_distance(clusters, new_instance)
        f = clusters[index].classify(index, distance, new_instance, classify_type) 
        if f == np.inf: # add new anomaly to a temperal anomaly list.
            if i > stablization:
                if tmp_index == None:
                #if anomalies == None:
                    #anomalies = new_instance
                    tmp_index = i
                else:
                    #anomalies = np.vstack([anomalies, new_instance])
                    tmp_index = np.vstack([tmp_index, i])
                anomalies_index = np.vstack([anomalies_index, i])
                j += 1
        else: # no new anomalies detected, reset the temperal anomaly list.
            if j > cum_anomalies: # if there are consecutive anomalies
                print"the anomalies are: ", anomalies
                big_anomalies_index = np.vstack([big_anomalies_index, tmp_index])
            j = 0
            tmp_index = None
        mean, cov_inv, alpha, beta, tmp = clusters[index].update(new_instance)
        '''
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
    '''
    # print results and plot informations
    j = 0
    num_anomalies = 0
    num_big_anomalies = 0
    anomalies_index = []
    big_anomalies_index = []
    num_clusters = len(clusters)
    for single_cluster in clusters:
        if single_cluster.type is 'anomalous':
            tmp = len(single_cluster.elements)
            num_anomalies += tmp
            anomalies_index.append(j)
            if tmp > cum_anomalies:
                num_big_anomalies += 1
                big_anomalies_index.append(j)
        j += 1
    if num_anomalies == 0:
        print 'No anomalies are detected!'
        sys.exit()
    #num_big_anomalies = len(big_anomalies_index)-1
    #big_anomalies_index = np.ndarray.tolist(big_anomalies_index)
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
    '''
