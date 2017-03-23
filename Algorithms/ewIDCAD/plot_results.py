import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

class plot_results():
    def __init__(self, normal_data, clusters, big_anomalies_index, num_seqs, start):
        self.normal_data = normal_data
        self.clusters = clusters
        self.big_anomalies_index = big_anomalies_index
        self.num_seqs = num_seqs
        self.start = start
    def plot(self):
        plt.figure(1) 
        plt.plot(self.normal_data[:,0], self.normal_data[:,1], 'g*', markersize = 5)
        plt.title('Original data')
        plt.xlabel('Temperature [degC]')
        plt.ylabel('Humidity [%]')

        plt.figure(2)
        num_clusters = len(self.clusters)
        for j in range (0,num_clusters):
            plt.plot(self.clusters[j].elements[:,0], self.clusters[j].elements[:,1],'g*')
        plt.plot(self.normal_data[self.big_anomalies_index,0], self.normal_data[self.big_anomalies_index,1], 'ro')
        plt.title('Original data with big anomalies')
        plt.xlabel('Temperature [degC]')
        plt.ylabel('Humidity [%]')
        
        plt.figure(3)
        plt.plot(range(0,self.num_seqs-self.start),self.clusters[0].elements[:,0],'g*')
        plt.plot(range(0,self.num_seqs-self.start),self.clusters[0].elements[:,1],'b*')
        
        plt.plot(self.big_anomalies_index, self.normal_data[self.big_anomalies_index,0],'ro')
        plt.plot(self.big_anomalies_index, self.normal_data[self.big_anomalies_index,1],'ro')

        plt.title('Original data with big anomalies')
        plt.xlabel('Time step')
        plt.ylabel('Data Magnitude [%]')
        
        plt.show()