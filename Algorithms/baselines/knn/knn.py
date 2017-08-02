from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KDTree
import numpy as np

class knn():
    def __init__(self, k, anomaly_ratio):
        self.k = k 
        self.leaf_size = 30
        self.metric = 'euclidean'
        self.anomaly_ratio = anomaly_ratio
    def run(self,data):
        #find kth nearest neighbor
        kdt = KDTree(data, self.leaf_size, self.metric)
        k_dist, k_index = kdt.query(data, self.k+1) #find the distances and the indexes of k nearest neighbor of all instances
        kth_dist = k_dist[:,self.k] # for each instance, select the distance to the kth nearest neighbor

        return kth_dist
    def detect_anomaly(self, kth_dist):
        # find the instances with largest distances as anomalies
        num_anomalies = self.anomaly_ratio * len(kth_dist) # number of anomalies we are expecting
        distance_descending = np.argsort(kth_dist)[::-1]
        anomalies_index = distance_descending[:num_anomalies]
        return anomalies_index

