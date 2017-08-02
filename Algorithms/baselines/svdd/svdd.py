from __future__ import division
import numpy as np
from sklearn import svm
from sklearn.metrics.pairwise import rbf_kernel
import time

class ocsvm():
    def __init__(self, train_data):
        self.outlier_fraction, self.kernel_s = 0.05, 1.3
        self.nu = self.outlier_fraction if train_data.shape[0] * self.outlier_fraction > 1 else 1./train_data.shape[0]
        self.kernel='rbf'
        self.gamma=0.5/(self.kernel_s * self.kernel_s)
    def run(self, train_data, test_data, outlier_fraction):
        import time

        # run One class SVM
        start = time.time()
        classifier = svm.OneClassSVM(nu = self.nu, kernel = self.kernel , gamma = self.gamma)
        classifier.fit(train_data)
        end = time.time()
        time = end-start

        svdd_score = classifier.predict(test_data)

        #print("full svdd took {0} seconds to train".format(time))

        num_outliers = train_data.shape[0] * outlier_fraction
        score_descending_index = np.argsort(svdd_score)[::-1]
        anomalies_index = score_descending_index[:num_outliers]
        return anomalies_index, classifier
class svdd():
    def __init__(self, train_data, train_data_label):
        
        self.train_data = train_data
        self.train_data_label = train_data_label

        self.index_p = np.where(train_data_label == 1)[0]
        self.index_n = np.where(train_data_label == -1)[0]
        self.data_p = train_data[self.index_p,:] # positive (normal) data
        self.data_n = train_data[self.index_n,:] # negative (anomalous) data
        #l_p = index_p.shape[0]
        #l_n = index_n.shape[0]
        self.len = len(self.train_data_label) # length of data
        self.C_p, self.C_n = 0.1, 0.1 # parameter C for possitive and negative labelled data
        #self.alpha_p, self.gamma_p = 0.1*np.ones(l_p), 0.1*np.ones(l_p) # Lagrange multipliers for positive instances
        #self.alpha_n, self.gamma_n = 0.1*np.ones(l_n), 0.1*np.ones(l_n) # Lagrange multipliers for negative instances
        self.alpha = (1/self.len) * np.ones(self.len) # use alpha' = label * alpha, so that the sum of all alpha is 1
        self.R = 0 # radius of the model
        self.center = 0 # center of the model
        self.max_iter = 1
        self.kernel_type = 'IP' # use inner product kernel as default
        self.terminate = 0.00000001

    def run(self):
        
        # solve the optimization of the Lagrange function w.r.t. Lagrange multipliers alpha
        self.solve()

        #self.center = sum(self.alpha_p * self.data_p - self.alpha_n * self.data_n)
        # compute center & radius
        self.center = sum(self.alpha.reshape(self.len,1) * self.train_data_label.reshape(self.len,1) * self.train_data)
        
        sum_dist_p = sum(np.sqrt(np.sum((self.data_p - self.center)**2, axis = 1)))
        sum_dist_n = sum(np.sqrt(np.sum((self.data_n - self.center)**2, axis = 1)))
        
        self.R = (sum_dist_p+sum_dist_n)/self.len
        
        print 'Center is: ', self.center
        print 'Radius is: ', self.R
    def solve(self):
        num_iter = 0
        kernel_matrix = self.kernel() # compute kernel matrix
        while (num_iter < self.max_iter):
            start = time.time()
            # select alpha_i and alpha_j to update
            print num_iter + 1
            for i in range(self.len):
                for j in np.random.permutation(self.len):
                    if i != j:
                        C_i = self.C_p if self.train_data_label[i] >0 else self.C_n
                        C_j = self.C_p if self.train_data_label[j] >0 else self.C_n

                        #sum_ik, sum_jk = 0, 0
                        sum_ik = self.train_data_label * self.alpha * kernel_matrix[i,:]
                        sum_ik[i] = 0
                        sum_ik = sum(sum_ik)
                        sum_jk = self.train_data_label * self.alpha * kernel_matrix[j,:]
                        sum_jk[j] = 0
                        sum_jk = sum(sum_jk)
                        #for k in range(self.len):
                        #    sum_ik = sum_ik + self.train_data_label[k] * self.alpha[k] * kernel_matrix[i,k]
                        #    sum_jk = sum_ik + self.train_data_label[k] * self.alpha[k] * kernel_matrix[j,k]
            
                        # compute the gradient
                        delta_i = self.train_data_label[i] * kernel_matrix[i,i] - \
                                  sum_ik * self.train_data_label[i]
                        delta_j = self.train_data_label[j] * kernel_matrix[j,j] - \
                                  sum_jk * self.train_data_label[j]
                        alpha_i_prev, alpha_j_prev = self.alpha[i], self.alpha[j]
                        self.alpha[i] += delta_i
                        self.alpha[j] += delta_j
                        self.constraint_check(i, j, C_i, C_j)
                        # terminate if not changing
                        diff = max(abs(self.alpha[i] - alpha_i_prev), abs(self.alpha[j] - alpha_j_prev))
                        #if diff <= self.terminate:
                        #    return
            print 'Time cost of one iteration is', time.time() - start
            num_iter += 1



    def kernel(self):
        if self.kernel_type == 'IP':
            return np.dot(self.train_data, self.train_data.T)

    def constraint_check(self, i, j, C_i, C_j):
        diff = self.alpha[i] - self.alpha[j]
        if diff > 0: # if alpha_i > alpha_j
            if self.alpha[j] < 0: # constraint alpha > 0:
                self.alpha[j] = 0
                self.alpha[i] = diff
            if self.alpha[i] > C_i:# constraint 0 <= alpha_i <= C_i
                self.alpha[i] = C_i
                self.alpha[j] = C_i - diff
            if diff > C_i:
                self.alpha[i] = C_i
                self.alpha[j] = 0
        else: # if alpha_i <= alpha_j
            if self.alpha[i] < 0: # constraint alpha > 0
                self.alpha[i] = 0
                self.alpha[j] = - diff
            if self.alpha[j] > C_j: # constraint 0 <= alpha_j <= C_j
                self.alpha[j] = C_j
                self.alpha[i] = C_j + diff
            if diff < - C_j:
                self.alpha[i] = 0
                self.alpha[j] = C_j
            '''
            if diff > C_i - C_j: # constraint 0 <= alpha_i <= C_i
                if self.alpha[i] > C_i:
                    self.alpha[i] = C_i
                    self.alpha[j] = C_i - diff
			else:
                if self.alpha[j] > C_j:
					self.alpha[j] = C_j
					self.alpha[i] = C_j + diff
		    '''

        '''
    	if self.train_data_label[i] > 0 and self.train_data_label[j] > 0:
            diff = self.alpha[i] - self.alpha[j]
            if diff > 0: # if alpha_i > alpha_j
                if self.alpha[j] < 0: # constraint alpha > 0:
                    self.alpha[j] = 0
                    self.alpha[i] = diff
                if self.alpha[i] > C_i:# constraint 0 <= alpha_i <= C_i
                    self.alpha[i] = C_i
                    self.alpha[j] = C_i - diff 
            else: # if alpha_i <= alpha_j
                if self.alpha[i] < 0: # constraint alpha > 0
                    self.alpha[i] = 0
                    self.alpha[j] = - diff
                if self.alpha[j] > C_j: # constraint 0 <= alpha_j <= C_j
                    self.alpha[j] = C_j
                    self.alpha[i] = C_j + diff
        if self.train_data_label[i] < 0 and self.train_data_label[j] < 0:
        	diff = self.alpha[i] - self.alpha[j]
            if diff > 0: # if alpha_i > alpha_j
                if self.alpha[i] > 0: # constraint alpha > 0:
                    self.alpha[i] = 0
                    self.alpha[j] = - diff
                if self.alpha[j] < - C_i:# constraint 0 <= alpha_i <= C_i
                    self.alpha[j] = - C_i
                    self.alpha[i] = - C_i + diff 
            else: # if alpha_i <= alpha_j
                if self.alpha[j] > 0: # constraint alpha > 0
                    self.alpha[j] = 0
                    self.alpha[i] = diff
                if self.alpha[i] < - C_i: # constraint 0 <= alpha_j <= C_j
                    self.alpha[i] = - C_i
                    self.alpha[j] = - C_i - diff
        if self.train_data_label[i] != self.train_data_label[j]:
        	diff = self.alpha[i] - self.alpha[j]
            if diff > 0: # if alpha_i > alpha_j
                if self.alpha[i] < 0: # constraint alpha > 0:
                    self.alpha[i] = 0
                    #self.alpha[j] = - diff
                if self.alpha[i] > C_i:# constraint 0 <= alpha_i <= C_i
                    self.alpha[i] = C_i
                    #self.alpha[j] = C_i - diff
                if self.alpha[j] > 0:
                    self.alpha[j] = 0
                    #self.alpha[i] = diff
                if self.alpha[j] < - C_j:
                    self.alpha[j] = - C_j
                    #self.alpha[i] = - C_j + diff 
            else: # if alpha_i <= alpha_j
                if self.alpha[i] > 0: # constraint alpha > 0:
                    self.alpha[i] = 0
                    #self.alpha[j] = - diff
                if self.alpha[i] < - C_i:# constraint 0 <= alpha_i <= C_i
                    self.alpha[i] = - C_i
                    #self.alpha[j] = C_i - diff
                if self.alpha[j] < 0:
                    self.alpha[j] = 0
                    #self.alpha[i] = diff
                if self.alpha[j] > C_j:
                    self.alpha[j] = C_j
                    #self.alpha[i] = - C_j + diff 
        '''
    def detect_anomalies(self, test_data):
        num_data = test_data.shape[0]
        dists = np.sqrt(np.sum((test_data - self.center)**2, axis = 1))
        anomalies_index = np.where(dists > self.R)
        return anomalies_index







