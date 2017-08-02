from __future__ import division
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KDTree
import numpy as np

class lof():
    def __init__(self, k, anomaly_ratio):
        self.k = k 
        self.leaf_size = 30
        self.metric = 'euclidean'
        self.anomaly_ratio = anomaly_ratio
    def run(self,data):
        #find kth nearest neighbor
        kdt = KDTree(data, self.leaf_size, self.metric)
        k_dist, k_index = kdt.query(data, self.k+1)
        k_dist = k_dist[:,1:]# eliminate the 1st nearest neighbor which is itself
        k_index = k_index[:,1:] # eliminate the 1st nearest neighbor which is itself
        
        n = k_dist.shape[0]
        # compute local reach density (lrd)
        lrd_value = []
        for i in range(n):
            lrd_value = np.append(lrd_value, self.compute_lrd(data, i, k_dist, k_index))
        # compute LOF score
        lof_score = []
        for i in range(n):
            lof_score = np.append(lof_score, self.compute_lof_score(i, lrd_value, k_index))
        return lof_score

    def compute_lrd(self, data, idx, k_dist, k_index):
        kth_dist_o = k_dist[k_index[idx,:],self.k-1] # kth distance of the neighbors of the instance
        d_p_o = k_dist[idx,:]
        #input('continue...')
        reach_dist = np.max(np.vstack([kth_dist_o, d_p_o]), axis = 0)
        lrd_value = self.k/sum(reach_dist)
        return lrd_value

    def compute_lof_score(self, idx, lrd_value, k_index):
        lrd_p = lrd_value[idx]
        lrd_o = lrd_value[k_index[idx,:]]
        lof_score = sum(lrd_o/lrd_p)/self.k
        return lof_score

    def detect_anomaly(self, lof_score):
        # find the instances with largest distances as anomalies
        num_anomalies = self.anomaly_ratio * len(lof_score) # number of anomalies we are expecting
        index_descending = np.argsort(lof_score)[::-1]
        distance_descending = np.sort(lof_score)[::-1]
        anomalies_index = index_descending[:num_anomalies]
        return anomalies_index

