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
        self.big_anomalies_index = big_anomalies_index
        self.num_seqs = num_seqs
        self.start = start
    def plot(self, x, y):
        '''
        # plot original data
        plt.figure(1) 
        plt.plot(self.normal_data[:,x], self.normal_data[:,y], 'g*', markersize = 5)
        plt.title('Original data')
        plt.xlabel(self.fields[x])
        plt.ylabel(self.fields[y])
        '''
        # plot original data with big anomalies
        plt.figure(2)
        num_clusters = len(self.clusters)
        plt.plot(self.normal_data[:,x], self.normal_data[:,y], 'g*', markersize = 5)
        #for j in self.anomalies_index:
        #    plt.plot(self.clusters[j].elements[:,x], self.clusters[j].elements[:,y],'ro')
        plt.plot(self.normal_data[self.big_anomalies_index,x], self.normal_data[self.big_anomalies_index,y], 'ro')
        plt.title('Original data with big anomalies')
        plt.xlabel(self.fields[x])
        plt.ylabel(self.fields[y])
        
        # plot original data with big anomalies
        
        plt.figure(3)
        plots = [None]*self.num_sensors
        color = np.zeros([self.num_sensors, 3])
        #color[:,0] = np.array(range(0, self.num_sensors))/(self.num_sensors-1) #R
        color[:,0] = np.zeros(self.num_sensors) #R
        color[:,1] = (np.array(range(0, self.num_sensors)))/(self.num_sensors-1) #G
        color[:,2] = (np.array(range(self.num_sensors, 0, -1))-1)/(self.num_sensors-1) #B
        color = ['y','m','c','k','g','b']

        for i in range (0, len(self.fields)):
            plots[i], = plt.plot(range(0,self.num_seqs),self.normal_data[:,i],color = color[i], label = self.fields[i])
            #plt.plot(self.big_anomalies_index, self.normal_data[self.big_anomalies_index,i],'ro')
        #plt.title('Original data with big anomalies')
        plt.xlabel('Time step')
        plt.ylabel('Data Magnitude')
        plt.legend(handles = plots)
        plt.xlim(0, 350)
        
        # plot original data with all anomalies

        plt.figure(4)
        plots = [None]*self.num_sensors
        for i in range (0, len(self.fields)):
            plots[i], = plt.plot(range(0,self.num_seqs),self.normal_data[:,i],color = color[i], label = self.fields[i])
            plt.plot(self.anomalies_index[1:], self.normal_data[self.anomalies_index[1:],i],'ro')
        plt.title('Original data with all anomalies')
        plt.xlabel('Time step')
        plt.ylabel('Data Magnitude')
        plt.xlim(0,350)
        #plt.legend(handles = plots)
        
        '''
        # plot anomalies on feature data
        num_plots= 2
        labels = ['feature_1', 'feature_2']
        for i in range(len(self.fields)/2):
            plt.figure(5+i)
            plots = [None]*num_plots
            for j in range (num_plots):
                plots[j], = plt.plot(range(0,self.num_seqs),self.normal_data[:,i*2+j],color = [0, 1*j,1*(1-j)], label = labels[j])
                plt.plot(self.anomalies_index[:], self.normal_data[self.anomalies_index[:],i*2+j],'ro')
            plt.title('Show anomalies in extractedfeatures')
            plt.xlabel('Time step')
            plt.ylabel('Magnitude')
            plt.legend(handles = plots)
        
# -------------------------------------------------------------------------------------------------------------------------        
         
        ground_truth = []     
        ground_truth.extend(range(100,120))
        ground_truth.extend(range(300,320))
        ground_truth.extend(range(500,520))
        ground_truth.extend(range(700,720))
        ground_truth.extend(range(1100,1120))
        ground_truth.extend(range(1300,1320))
        ground_truth.extend(range(1500,1520))
        ground_truth.extend(range(1700,1720))
        
 
        plt.figure(5)
        plots[1], = plt.plot(range(0,self.num_seqs),self.normal_data[:,0],color = [0, 1,0], label = self.fields[0])
        plt.plot(self.anomalies_index[:], self.normal_data[self.anomalies_index[:],0],'ro')
        plt.plot(ground_truth, self.normal_data[ground_truth,0],'o', color = [1,0.78,0.17])

        plots[2], = plt.plot(range(0,self.num_seqs),self.normal_data[:,4],color = [0, 0,1], label = self.fields[4])
        plt.plot(self.anomalies_index[:], self.normal_data[self.anomalies_index[:],4],'ro')
        plt.plot(ground_truth, self.normal_data[ground_truth,4],'o', color = [1,0.78,0.17])
#--------------------------------------------------------------------------
        plt.figure(6)
        plots[1], = plt.plot(range(0,self.num_seqs),self.normal_data[:,0],color = [0, 1,0], label = self.fields[0])
        plt.plot(self.anomalies_index[:], self.normal_data[self.anomalies_index[:],0],'ro')
        plt.plot(ground_truth, self.normal_data[ground_truth,0],'o', color = [1,0.78,0.17])
        plots[2], = plt.plot(range(0,self.num_seqs),self.normal_data[:,5],color = [0, 0,1], label = self.fields[5])
        plt.plot(self.anomalies_index[:], self.normal_data[self.anomalies_index[:],5],'ro')
        plt.plot(ground_truth, self.normal_data[ground_truth,5],'o', color = [1,0.78,0.17])
#----------------------------------------------------------------------------
        plt.figure(7) # 
        plots[1], = plt.plot(range(0,self.num_seqs),self.normal_data[:,11],color = [0, 1,0], label = self.fields[11])
        plt.plot(self.anomalies_index[:], self.normal_data[self.anomalies_index[:],11],'ro')
        plt.plot(ground_truth, self.normal_data[ground_truth,11],'o', color = [1,0.78,0.17])
        plots[2], = plt.plot(range(0,self.num_seqs),self.normal_data[:,2],color = [0, 0,1], label = self.fields[2])
        plt.plot(self.anomalies_index[:], self.normal_data[self.anomalies_index[:],2],'ro')
        plt.plot(ground_truth, self.normal_data[ground_truth,2],'o', color = [1,0.78,0.17])
'''

        plt.show()
