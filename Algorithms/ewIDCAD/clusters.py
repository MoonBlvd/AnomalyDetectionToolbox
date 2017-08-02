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
    def __init__(self, elements, _lambda, mean, cov, gamma, algorithm):
        self.k = 3 # number of iterations

        self.elements = elements # initial the elements of this cluster
        print 'initial elements are: ', self.elements
        self._lambda = _lambda
        '''
        if algorithm == 'ewIDCAD':
            self.alpha = 0
            self.beta = 0
            mean_num = 0
            cov_term_2 = 0
            for i in range(self.k):
                self.alpha += self._lambda**(self.k-i-1)
                self.beta += self._lambda**(2*(self.k-i-1))
                mean_num += (self._lambda**(self.k-i-1))*self.elements[i] 
                cov_term_2 += (self._lambda**(self.k-i-1))* \
                              np.dot(self.elements[i:i+1].T,(self.elements[i:i+1]))
            self.tmp = self.alpha/(self.alpha**2-self.beta)
            self.mean = mean_num/self.alpha 

            self.cov = self.tmp*cov_term_2
            self.cov_inv = np.linalg.inv(self.cov) # Initialize as identical matrix
            self.cov_inv = np.eye(len(cov))

        else:
        '''
        self.alpha = 2
        self.beta = 2
        self.mean = mean
        #self.cov_inv = np.linalg.inv(cov)
        self.cov_inv = np.eye(len(cov))
        self.gamma = gamma

        print "init mean is:", self.mean
        print "init cov_inv is:", self.cov_inv
        #input('Press Enter to continue...')

        # parameters for model reset
        self.sigma = 1
        self.overlap_flag = 0
        # initialize the chi_square of the cluster
        #self.chi_square = 1/chi2.ppf((1-self.gamma), len(cov))
        self.chi_square = chi2.ppf(self.gamma, len(cov))
        print "self.chi_square is: ", self.chi_square

    def update_ewIDCAD(self, x):
        # here x should be 1*W array where W is the number of features
        self.elements = np.vstack([self.elements, x])
        # update parameters
        self.tmp = self.alpha/(self.alpha**2-self.beta)
        A = self.cov_inv/(self._lambda / self.tmp) # Note that this is the A_{k-1}
        self.alpha = self.alpha*self._lambda + 1
        self.beta = self.beta*self._lambda**2 + 1

        new_tmp = self.alpha/(self.alpha**2-self.beta)
        # update mean
        self.mean = self.mean + (x - self.mean)/self.alpha
        self.tmp = new_tmp

        # update inverse of covariance
        diff = (x-self.mean)[None] # make it to be 2D array, 1*2
        num = np.dot(np.dot(np.dot(A,diff.T),diff), A)
        den = 1 + np.dot(np.dot(diff, A), diff.T)
        self.cov_inv = (1/self.tmp) * (A - num / den )
        #self.cov_inv = (self.sigma**self.overlap_flag) * self.cov_inv + \
        #               (1-self.sigma**self.overlap_flag) * np.eye(len(self.cov_inv)) 
        # save the trajectory of means and covs

        #print "updated mean is:", self.mean
        #print "updated cov_inv is:", self.cov_inv
        #if self.k >=800:
        #    input('Press Enter to continue...')
        #self.k += 1
        #if np.isnan(self.mean[0]):
        #    input('Press Enter to continue...')

        meanfile = open('new_mean.csv', 'a')
        writer = csv.writer(meanfile, delimiter = ',')
        writer.writerow(self.mean)
        meanfile.close

        cov_inv_file = open('new_cov_inv.csv', 'a')
        writer = csv.writer(cov_inv_file, delimiter = ',')
        for i in range (0, len(self.cov_inv)):
            writer.writerow(self.cov_inv[i])
        cov_inv_file.close
        
        return self.mean, self.cov_inv
    def update_ffIDCAD(self, x):
        # here x should be 1*W array where W is the number of features
        self.elements = np.vstack([self.elements, x])

        # update inverse of covariance
        diff = (x-self.mean)[None] # make it to be 2D array, 1*2
        num = np.dot(np.dot(diff.T, diff), self.cov_inv)
        den = (self.k-1)/self._lambda + np.dot(np.dot(diff, self.cov_inv), diff.T)
        self.cov_inv = np.dot((self.k*self.cov_inv/(self._lambda*(self.k-1))),\
                (np.eye(len(self.mean)) - num / den ))

        # update mean
        self.mean = self._lambda*self.mean + (1-self._lambda)*x
        self.k += 1
        #self.cov_inv = (self.sigma**self.overlap_flag) * self.cov_inv + \
        #               (1-self.sigma**self.overlap_flag) * np.eye(len(self.cov_inv)) 
        #  save the trajectory of means and covs
        meanfile = open('new_mean.csv', 'a')
        writer = csv.writer(meanfile, delimiter = ',')
        writer.writerow(self.mean)
        meanfile.close

        cov_inv_file = open('new_cov_inv.csv', 'a')
        writer = csv.writer(cov_inv_file, delimiter = ',')
        for i in range (0, len(self.cov_inv)):
            writer.writerow(self.cov_inv[i])
        cov_inv_file.close
        
        return self.mean, self.cov_inv
    def update_IDCAD(self, x):
        # here x should be 1*W array where W is the number of features
        self.elements = np.vstack([self.elements, x])


        # update inverse of covariance
        diff = (x-self.mean)[None] # make it to be 2D array, 1*2
        num = np.dot(np.dot(diff.T, diff), self.cov_inv)
        den = (self.k**2-1)/self.k + np.dot(np.dot(diff, self.cov_inv), diff.T)
        self.cov_inv = np.dot((self.k*self.cov_inv/(self.k-1)), \
                (np.eye(len(self.mean)) - num / den ))
        # update mean
        self.mean = self.mean+(1/(self.k+1))*(x-self.mean)
        self.k += 1
        #self.cov_inv = (self.sigma**self.overlap_flag) * self.cov_inv + \
        #               (1-self.sigma**self.overlap_flag) * np.eye(len(self.cov_inv)) 
        #  save the trajectory of means and covs
        meanfile = open('new_mean.csv', 'a')
        writer = csv.writer(meanfile, delimiter = ',')
        writer.writerow(self.mean)
        meanfile.close

        cov_inv_file = open('new_cov_inv.csv', 'a')
        writer = csv.writer(cov_inv_file, delimiter = ',')
        for i in range (0, len(self.cov_inv)):
            writer.writerow(self.cov_inv[i])
        cov_inv_file.close
        
        return self.mean, self.cov_inv
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
        std = np.sqrt(np.diag(self.cov))
        dist = np.sum((new_instance/std)**2)
        return dist


        
