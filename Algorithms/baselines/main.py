from __future__ import division
import numpy as np
import sys
import data_reader as reader
import plot_results as plt_res
import matplotlib.pyplot as plt
from knn.knn import knn
from lof.lof import lof
from fsm.fsm import fsm
from pca.pca import pca
from svdd.svdd import ocsvm, svdd


sys.dont_write_bytecode = True
    
def run_knn(test_data, test_label, color = 'r'):
    TPR = []
    FPR = [] 
    k = 5
    num_positive = len(np.where(test_label == -1)[0])
    num_negative = test_data.shape[0] - num_positive        
    for anomaly_ratio in np.arange(0, 1 + 0.05, 0.05):
        
        # init a knn to detect anomalies
        KNN = knn(k, anomaly_ratio)
        k_dist = KNN.run(test_data)
        anomalies_index = KNN.detect_anomaly(k_dist)
        anomalies_index = sorted(anomalies_index)
        num_TP = 0
        num_FP = 0
        for i in anomalies_index:
            if test_label[i] == -1:
                num_TP = num_TP + 1
            else:
                num_FP = num_FP + 1
        TPR.append(num_TP/num_positive) # True positive rate = # of TP / # of Positive
        FPR.append(num_FP/num_negative) # False positive rate = # of FP / # of Negative
    plot = plt_res.plot_ROC(FPR, TPR, color, 'KNN')
    return plot
        
def run_lof(test_data, test_label, color = 'r'):
    TPR = []
    FPR = []
    k = 5
    num_positive = len(np.where(test_label == -1)[0])
    num_negative = test_data.shape[0] - num_positive
    for anomaly_ratio in np.arange(0, 1 + 0.05, 0.05):
        # init a lof to detect anomalies
        LOF = lof(k, anomaly_ratio)
        lof_score = LOF.run(test_data)
        anomalies_index = LOF.detect_anomaly(lof_score)
        anomalies_index = sorted(anomalies_index)
        num_TP = 0
        num_FP = 0
        for i in anomalies_index:
            if test_label[i] == -1:
                num_TP = num_TP + 1
            else:
                num_FP = num_FP + 1

        TPR.append(num_TP/num_positive) # True positive rate = # of TP / # of Positive
        FPR.append(num_FP/num_negative) # False positive rate = # of FP / # of Negative
        #print anomalies_index
    plot = plt_res.plot_ROC(FPR, TPR, color, 'LOF')
    return plot

def run_fsm(test_data, test_label, fields, color = 'r'):
    n = test_data.shape[0]
    # fsm is running online
    buf_size = 4
    TPR = []
    FPR = []
    num_positive = len(np.where(test_label == -1)[0])
    num_negative = test_data.shape[0] - num_positive
    offset_list = np.arange(0, 2 + 0.1, 0.1)
    for offset in offset_list:
        anomalies_index = []
        anomaly_types = []
        FSM = fsm(buf_size, offset)
        for i in range(n):
            anomaly, point_anomaly_type, collective_anomaly_type = FSM.run(test_data[i,:], fields)
            if anomaly:
                if collective_anomaly_type != 'Normal':
                    anomalies_index = np.append(anomalies_index, range(i-buf_size+1,i+1))
                    anomaly_types.append(collective_anomaly_type)
                elif point_anomaly_type != 'Normal':
                    anomalies_index = np.append(anomalies_index, i)
                    anomaly_types.append(point_anomaly_type)
        print 'FRM: anomaly types are:', anomaly_types
        print 'FRM: anomaly index are:', anomalies_index
        # record TP and FP
        num_TP = 0
        num_FP = 0
        for i in anomalies_index:
            if test_label[i] == -1:
                num_TP += 1
            else:
                num_FP += 1
        TPR.append(num_TP/num_positive)
        FPR.append(num_FP/num_negative)
        input('Press..')
    # plot ROC
    plot = plt_res.plot_ROC(FPR, TPR, color, 'FRM')

    return plot

def run_pca(test_data, test_label, color = 'r'):
    mean = test_data.mean(axis = 0)
    n = test_data.shape[0] # number of instances
    d = test_data.shape[1] # dimension of each instance
    PCA = pca(n, d, mean)
    pca_scores = PCA.run_online_ospca(test_data)
    #plt.plot_scores(pca_scores, n)

    # plot ROC
    num_positive = len(np.where(test_label == -1)[0])
    num_negative = test_data.shape[0] - num_positive
    TPR = []
    FPR = []
    for threshold in np.arange(1.20,0.15,-0.05):
        anomalies_index = np.where(pca_scores > threshold)[0]
        num_TP = 0
        num_FP = 0
        for i in anomalies_index:
            if test_label[i] == -1:
                num_TP = num_TP + 1
            else:
                num_FP = num_FP + 1

        TPR.append(num_TP/num_positive) # True positive rate = # of TP / # of Positive
        FPR.append(num_FP/num_negative) # False positive rate = # of FP / # of Negative
        #print anomalies_index
    plot = plt_res.plot_ROC(FPR, TPR, color, 'osPCA')
    return plot

def run_svm(train_data, test_data, test_label, color = 'r'):
    # prepare for ROC plotting
    num_positive = len(np.where(test_label == -1)[0])
    num_negative = test_data.shape[0] - num_positive
    TPR = []
    FPR = []
    # train One class SVM (OCSVM) using train_data
    # OCSVM is an unsupervised method
    OCSVM = ocsvm(train_data)
    for outlier_fraction in np.arange(0,1 + 0.05, 0.05):
        # evaluate OCSVM using test_data
        anomalies_index, classifier = OCSVM.run(train_data, test_data, outlier_fraction) 
        num_TP = 0
        num_FP = 0
        for i in anomalies_index:
            if test_label[i] == -1:
                num_TP = num_TP + 1
            else:
                num_FP = num_FP + 1

        TPR.append(num_TP/num_positive) # True positive rate = # of TP / # of Positive
        FPR.append(num_FP/num_negative) # False positive rate = # of FP / # of Negative
        #print anomalies_index
    plot = plt_res.plot_ROC(FPR, TPR, color, 'ocSVM')
    return plot

def run_svdd(train_data, train_label, test_data, test_label):
    # train Support Vector Data Description () method using train_data and evaluate it using test_data
    # SVDD is an supervised method:
    # the normal instances are labelled as 1 while anomalous instances are labelled as -1
    SVDD = svdd(train_data, train_label)
    SVDD.run()
    anomalies_index = SVDD.detect_anomalies(test_data)

if __name__ == '__main__':

    algorithm = sys.argv[1] # the algorithm we use
    #data_name = sys.argv[2] # name of the dataset we tested on 

    #file_path = '../../Nan_Traffic_Simulator/04132017_data/'
    #data_file_name = 'anomalous_17D_8D_6.csv'
    #fields_file_name = '8D_fields.csv'
    train_file_path = '../../Nan_Traffic_Simulator/05172017_data/'
    train_file_name = 'anomalous_17D_1.csv'
    train_label_name = 'anomalous_17D_1_label.csv'

    test_file_path = '../../Nan_Traffic_Simulator/05172017_data/'
    test_file_name = 'anomalous_17D_2.csv'
    test_label_name = 'anomalous_17D_2_label.csv'

    fields_file_name = '17D_fields.csv'

    train_data = reader.read_data(train_file_path + train_file_name)
    train_label = reader.read_data(train_file_path + train_label_name)
    test_data = reader.read_data(test_file_path + test_file_name)
    test_label = reader.read_data(test_file_path + test_label_name)
    fields = reader.read_fields(train_file_path + fields_file_name)

    # Run different algorithms
    if algorithm == 'knn': # offline, unsupervised
        _ = run_knn(test_data, test_label)
        plt.show()
    if algorithm == 'lof': # offline, unsupervised
        _ = run_lof(test_data, test_label)
        plt.show()
    if algorithm == 'fsm': # online, no ML
        run_fsm(test_data, test_label, fields)
        plt.show()
    if algorithm == 'pca':
        _ = run_pca(test_data, test_label)
        plt.show()
    if algorithm == 'svm':
        _ = run_svm(train_data, test_data, test_label)
        plt.show()
    if algorithm == 'svdd':
        run_svdd(train_data, train_label, test_data, test_label)
    if algorithm == 'all':
        colors = ['r','g','b','y','c']
        plots = [None] * 6
        plots[0] = run_knn(test_data, test_label, colors[0])
        plots[1] = run_lof(test_data, test_label, colors[1])
        plots[2] = run_pca(test_data, test_label, colors[2])
        plots[3] = run_svm(train_data, test_data, test_label, colors[3])
        #plots[4] = run_fsm(test_data, test_label, fields, colors[4])
        plots[4] = plt_res.plot_ROC([0.00406914], [0.3667],'c','conf_1')
        plots[5] = plt_res.plot_ROC([0.00964467], [0.6],'m', 'conf_2')
        plt.plot([0,1],[0,1],'k--')
        plt.legend(handles = plots, loc=5)
        plt.grid()
        plt.show()
        #TPR:  0.457142857143
        #FPR:  0.0351145038168
    #print 'anomalies index are: ', anomalies_index
