from __future__ import division
import numpy as np
from scipy.stats import chi2

#def chi_square(elements, mean, cov):
    #den = np.ones_like(elements)
    #sigma_square = np.diag(cov)
    #sigma_square = np.diag(wigma_square)
    #den = np.dot(den, sigma_square)
    #print 'The den for computing chi_square is: ', den 

    #num_elements = len(a)
    #np.sum((elements-mean)**2/den, axis = 1)

class cluster():
    def __init__(self, elements, alpha, beta, _lambda, mean, cov, gamma, tmp = 0.5):
        self.elements = elements # initial the elements of this cluster
        self.alpha = alpha
        self.beta = beta
        self.tmp = tmp
        self._lambda = _lambda
        self.mean = mean
        self.cov = cov
        self.cov_inv = np.linalg.inv(self.cov)
        self.gamma = gamma
        # initialize the chi_square of the cluster
        #self.chi_square = chi_square(self.elements, self.mean, self.cov)
        self.chi_square = chi2.ppf(self.gamma, len(cov))
    def update(self, x):
        # here x should be 1*W array where W is the number of features
        self.elements = np.vstack([self.elements, x])
        # update parameters
        self.alpha = self.alpha*self._lambda + 1
        self.beta = self.beta*self._lambda**2 + 1
        A = self.cov_inv/(self._lambda * self.tmp) # Note that this is the A_{k-1}
        self.tmp = self.alpha/(self.alpha**2-self.beta)
        # update mean
        self.mean = self.mean + (x - self.mean)/self.alpha

        # update inverse of covariance
        num = np.dot(np.dot(np.dot(A,((x - self.mean).T)),(x - self.mean)), A)
        den = 1 + np.dot(np.dot(((x - self.mean).T), A), (x - self.mean))
        self.cov_inv = (1/self.tmp) * (A - num / den )
        #print 'A is: ', A
        #print 'x - m is: ', x - self.mean
        #print 'num is: ', num
        #print 'den is: ', den
        #print 'cov_inv is: ', self.cov_inv
        return self.mean, self.cov_inv
    def compute_distance(self, x):
        distance = np.dot(np.dot((x - self.mean), self.cov_inv), (x - self.mean).T)
        return distance
    def classify(self, index, distance):
        if distance < self.chi_square:
            f = index
        else:
            f = False
        return f
