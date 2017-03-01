from __future__ import division
import numpy as np

class onlineUpdate():
    def update(alpha, beta, chi, _lambda, k, m, cov_inv, x):
        # here x should be 1*W array where W is the number of features

        # update parameters
        alpha = alpha*_lambda + 1
        beta = beta*_lambda**2 + 1
        A = cov_inv/(_lambda * chi) # Note that this is the A_{k-1}
        chi = alpha/(alpha**2-beta)

        # update mean
        m = m + (x - m)/alpha

        # update inverse of covariance
        num = A*((x - m).T)*(x - m)*A
        den = 1+((x - m).T)*A*(x - m)
        cov_inv = (1/chi) * (A - num / den )
        return alpha, beta, chi, m, cov_inv

