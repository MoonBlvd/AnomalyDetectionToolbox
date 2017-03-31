from __future__ import division
import numpy as np
from scipy.stats import chi2
import csv

#def chi_square(elements, mean, cov):
    #den = np.ones_like(elements)
    #sigma_square = np.diag(cov)
    #sigma_square = np.diag(wigma_square)
    #den = np.dot(den, sigma_square)
    #print 'The den for computing chi_square is: ', den 

    #num_elements = len(a)
    #np.sum((elements-mean)**2/den, axis = 1)

class cluster():
    def __init__(self, elements, alpha, beta, _lambda, mean, cov_inv, gamma, tmp, cluster_type):
        self.elements = elements # initial the elements of this cluster
        self.alpha = alpha
        self.beta = beta
        self.tmp = tmp
        self._lambda = _lambda
        self.mean = mean
        self.cov_inv = cov_inv # Initialize as identical matrix
        self.gamma = gamma
 
        # parameters for model reset
        self.sigma = 1
        self.overlap_flag = 0
        # initialize the chi_square of the cluster
        #self.chi_square = 1/chi2.ppf((1-self.gamma), len(cov))
        self.chi_square = chi2.ppf(self.gamma, len(self.cov_inv))
        self.type = cluster_type

    def update(self, x):
        # here x should be 1*W array where W is the number of features
        self.elements = np.vstack([self.elements, x])
        # update parameters
        A = self.cov_inv/(self._lambda / self.tmp) # Note that this is the A_{k-1}
        self.alpha = self.alpha*self._lambda + 1
        self.beta = self.beta*self._lambda**2 + 1

        new_tmp = self.alpha/(self.alpha**2-self.beta)
        # update mean
        self.mean = self.mean + (x - self.mean)/self.alpha
        self.tmp = new_tmp

        # update inverse of covariance
        num = np.dot(np.dot(np.dot(A,(x - self.mean).T),(x - self.mean)), A)
        #den = 1 + np.dot(np.dot((x - self.mean).T, A), (x - self.mean))
        den = 1 + np.dot(np.dot((x - self.mean), A), (x - self.mean).T)
        self.cov_inv = (1/self.tmp) * (A - num / den )

        self.cov_inv = (self.sigma**self.overlap_flag) * self.cov_inv + \
                       (1-self.sigma**self.overlap_flag) * np.eye(len(self.cov_inv)) 
        '''
        # save the trajectory of means and covs
        meanfile = open('new_mean.csv', 'a')
        writer = csv.writer(meanfile, delimiter = ',')
        writer.writerow(self.mean)
        meanfile.close

        cov_inv_file = open('new_cov_inv.csv', 'a')
        writer = csv.writer(cov_inv_file, delimiter = ',')
        for i in range (0, len(self.cov_inv)):
            writer.writerow(self.cov_inv[i])
        cov_inv_file.close
        '''
    def augment_element(self, x):
        self.elements = np.vstack([self.elements, x])

    def compute_distance(self, x):
        distance = np.dot(np.dot((x - self.mean), self.cov_inv), (x - self.mean).T)
        return distance

    def classify(self, index, distance, new_instance, classify_type):
        #print "the distance is: ", distance
        #print "the chi_square is: ", self.chi_square
        if classify_type == 'chi_square':
            if distance < self.chi_square:
                if distance < 0.05 * self.chi_square: # find out the too close data instance
                    self.overlap_flag += 1
                else:
                    self.overlap_flag = 0
                f = index
            else:
                f = np.inf
        elif classify_type == '3_sigma':
            dist = self.compute_dist_to_ellipse(new_instance) 
            #print "the distance to the ellipse is: ", dist
            if dist < 7.378:
                f = index
            else:
               f = np.inf
        return f

    def compute_dist_to_ellipse(self, new_instance):
        #eig_vectors, eig_values = np.linalg.eig(self.cov)
        std = np.sqrt(np.diag(self.cov_inv))
        dist = np.sum((new_instance/std)**2)
        return dist


        
