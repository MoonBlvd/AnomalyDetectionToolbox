import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

class plot_results():
    def __init__(self, normal_data, fields, clusters, anomalies_index, big_anomalies_index, num_seqs, start):
        self.normal_data = normal_data
        self.fields = fields
        self.num_sensors = len(self.fields)
        self.clusters = clusters
        self.anomalies_index = anomalies_index
        self.big_anomalies_index = big_anomalies_index[1:]
        self.num_seqs = num_seqs
        self.start = start
    def plot(self, x, y):
        # plot original data
        plt.figure(1) 
        plt.plot(self.normal_data[:,x], self.normal_data[:,y], 'g*', markersize = 5)
        plt.title('Original data')
        plt.xlabel(self.fields[x])
        plt.ylabel(self.fields[y])

        # plot original data with big anomalies
        plt.figure(2)
        num_clusters = len(self.clusters)
        for j in range (0,num_clusters):
            plt.plot(self.clusters[j].elements[:,x], self.clusters[j].elements[:,y],'g*')
        plt.plot(self.normal_data[self.big_anomalies_index,x], self.normal_data[self.big_anomalies_index,y], 'ro')
        plt.title('Original data with big anomalies')
        plt.xlabel(self.fields[x])
        plt.ylabel(self.fields[y])
        
        # plot original data with big anomalies
        plt.figure(3)
        plots = [None]*self.num_sensors
        color = np.zeros([self.num_sensors, 3])
        color[:,0] = np.array(range(0, self.num_sensors))/(self.num_sensors-1) #R
        color[:,1] = (np.array(range(self.num_sensors, 0, -1))-1)/(self.num_sensors-1) #G
        color[:,2] = (np.array(range(self.num_sensors, 0, -1))-1)/(self.num_sensors-1) #B
        for i in range (0, len(self.fields)):
            plots[i], = plt.plot(range(0,self.num_seqs-self.start),self.normal_data[:,i],'*',color = color[i], label = self.fields[i])
            plt.plot(self.big_anomalies_index, self.normal_data[self.big_anomalies_index,i],'ro')
        plt.title('Original data with big anomalies')
        plt.xlabel('Time step')
        plt.ylabel('Data Magnitude')
        #plt.legend(handles = plots)
        
        # plot original data with all anomalies
        plt.figure(4)
        plots = [None]*self.num_sensors
        for i in range (0, len(self.fields)):
            plots[i], = plt.plot(range(0,self.num_seqs-self.start),self.normal_data[:,i],'*',color = color[i], label = self.fields[i])
            plt.plot(self.anomalies_index[1:], self.normal_data[self.anomalies_index[1:],i],'ro')
        plt.title('Original data with all anomalies')
        plt.xlabel('Time step')
        plt.ylabel('Data Magnitude')
        plt.legend(handles = plots)

        plt.show()
