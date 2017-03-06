from __future__ import division
import numpy as np

class onlineUpdator():
    def __init__(self, alpha, beta, _lambda, mean, cov_inv, chi = 0):
        self.alpha = alpha
        self.beta = beta
        self.chi = chi
        self._lambda = _lambda
        self.mean = mean
        self.cov_inv = cov_inv

    def update(self, k, x):
        # here x should be 1*W array where W is the number of features

        # update parameters
        self.alpha = self.alpha*self._lambda + 1
        self.beta = self.beta*self._lambda**2 + 1
        A = self.cov_inv/(self._lambda * self.chi) # Note that this is the A_{k-1}
        self.chi = self.alpha/(self.alpha**2-self.beta)

        # update mean
        self.mean = self.mean + (x - self.mean)/self.alpha

        # update inverse of covariance
        num = A*((x - self.mean).T)*(x - self.mean)*A
        den = 1+((x - self.mean).T)*A*(x - self.mean)
        self.cov_inv = (1/self.chi) * (A - num / den )

        return self.mean, self.cov_inv

