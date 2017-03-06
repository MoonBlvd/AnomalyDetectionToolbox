from __future__ import division
import numpy as np


class anomalyDetector():

    def __init__(self, gamma):
        self.gamma = gamma
        

    def classify(self, m, cov_inv, x):
        num_clusters = len(m)
        min_distance = np.inf
        min_t_square = 0
        min_index = 0
        # here x should be 1*W array where W is the number of features
        for i in range (0, num_clusters):
            # compute the chi_square
            # compute the distance criterion
            t_square = (chi_square ** -1)*self.gamma
            # computer the distance
            #print 'means are: ', m
            #print 'cov_invs are: ', cov_inv
            distance = np.dot(np.dot((x-m[i]), cov_inv[i]), (x-m[i]).T)
            #print 'distance is: ',distance
            if distance < min_distance:
                min_distance = distance
                min_t_square = t_square
                min_index = i
        print 'min distance is: ', min_distance
        print 'min criterion is: ', min_t_square
        if  min_distance <= min_t_square:
            f = min_index # output the cluster label
        else:
            f = False # Not belong to any clusters

        return f

