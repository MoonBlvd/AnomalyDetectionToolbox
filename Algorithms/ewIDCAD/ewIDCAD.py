import numpy as np
import csv
from onlineUpdate import onlineUpdate
from classifier import classifier

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
    normal_data = dataReader(file_path + file_name)
    num_sensors, num_seqs = normal_data.shape
    
    # Parameters configuration
    _lambda = 0.95 # forgetting factor
    gamma = 0.90 # probability of misclassification 
    f = True # anomaly flag, true means anomalous
    alpha = 0 # 
    beta = 0 #

    k = 200 # num of initial samples
    init_samples = normal_data[:k][:]
    mean = init_samples.mean(axis = 0)
    print init_samples
    cov = np.cov(init_samples)
    print cov
    cov_inv = np.linalg.inv(cov) # We update the inverse of the covariance in practice!
    print cov_inv
    '''
    for i in range(k, num_seqs):
        new_intance = normal_data[k]
        # classify the new instance, f is the anomaly flag
        f = classifier.classify(gamma, mean, cov_inv, new_instance)

        if f == False: # the new data is not anomalous
            # update the model and parameters
            alpha, beta, chi, mean, cov_inv = onlineUpdate.update( \
                alpha, beta, chi,  _lambda, i, mean, cov_inv, new_instance)
        #else:
            # add a new cluster
'''
