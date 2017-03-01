import numpy as np
from onlineUpdate import onlineUpdate
from classifier import classifier

def dataReader():
    # The read-in data should be a N*W matrix,
    # where N is the length of the time sequences,
    # W is the number of sensors/data features


if __name__ == '__main__':
    filepath = '../../benchmarks/Time\ Series\ Data/Intel\ Lab\ Data/'
    filename = 'Temperature/normalSeqs.data.csv'
    normal_data = dataReader(filename)
    num_sensors, num_seqs = normal_data.shape()
    
    # Parameters configuration
    _lambda = 0.95 # forgetting factor
    gamma = 0.90 # probability of misclassification 
    f = True # anomaly flag
    alpha = 0 # 
    beta = 0 #

    k = 50 # num of initial samples
    init_samples = normal_data[:k][:]
    mean = init_samples.mean(axis = 0)
    cov = np.cov(init_samples)
    cov_inv = np.linalg.inv(cov) # We update the inverse of the covariance in practice!
    for i in range(k, num_seqs):
        new_intance = normal_data[k]
        # classify the new instance, f is the anomaly flag
        f = classifier.classify(gamma, mean, cov_inv, new_instance)

        # update the model and parameters
        alpha, beta, chi, mean, cov_inv = onlineUpdate.update( \
                alpha, beta, chi,  _lambda, i, mean, cov_inv, new_instance)
