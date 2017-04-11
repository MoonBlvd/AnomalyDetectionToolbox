from __future__ import division
import numpy as np

class extractor():

    def __init__(self):
        self.num = 2
        self.w_1 = 2
        #self.w_2 = 1
        self.w_2 = 0.1
        self.sigma_12 = -5
        self.w_3 = 1
        self.w_4 = 1
        self.w_5 = 2
        self.w_6 = 1
        self.sigma_3 = -5
        self.sigma_4 = 0
    def extract(self, data):
        data.shape
        # y, x_FL and x_Rl
        y = data[:,0]
        x_FL = data[:,1]
        x_RL = data[:,3]
        x_FL_dot = data[:,8]
        x_RL_dot = data[:,10]
        # y, x_FR and x_RR
        x_FR = data[:,2]
        x_RR = data[:,4]
        x_FR_dot = data[:,9]
        x_RR_dot = data[:,11]
        # x_dot, x_FC and x_FC_dot
        x_FC = data[:,5]
        x_FC_dot = data[:,6]
        x_dot = data[:,7]
#------------------------- lane changing features -------------------------------
        #f_1 = np.exp(y-5.4)/(x_FL * x_RL + 1)
        # sigmoid feature extraction
        '''
        f_1 = 1/(1 + np.exp(2*(5.4-y) + np.log(x_FL*x_RL+0.5)))
        for i in range(len(y)):
            if y[i]<3.6:
                f_1[i] = 1/(1 + np.exp(2*(1.8-y[i]) + np.log(x_FL[i]*x_RL[i]+0.5)))
        '''
        # sigmoid and min feature extraction
        f_1 = np.zeros([len(y), 1])
        for i in range(len(y)):
            if y[i] >= 5.4:
                #f_1[i] = 1/(1 + np.exp(self.w_1*(9-y[i]) + self.w_2*min(x_FL[i], x_RL[i]) + self.sigma_12))
                f_1[i] = 1/(1 + np.exp(self.w_1*(9-y[i]) + self.w_2*min(x_FL[i]+self.w_5*(x_FL_dot[i]-x_dot[i]), x_RL[i]+self.w_5*(x_dot[i]-x_RL_dot[i])) + self.w_2*self.sigma_12))
            else:
                #f_1[i] = 1/(1 + np.exp(self.w_1*(5.4-y[i]) + self.w_2*min(x_FL[i], x_RL[i]) + self.sigma_12))
                f_1[i] = 1/(1 + np.exp(self.w_1*(5.4-y[i]) + self.w_2*min(x_FL[i]+self.w_5*(x_FL_dot[i]-x_dot[i]), x_RL[i]+self.w_5*(x_dot[i]-x_RL_dot[i])) + self.w_2*self.sigma_12))


        #f_2 = np.exp(5.4-y)/(x_FR * x_RR + 1)
        # sigmoid feature extraction
        '''
        f_2 = 1/(1 + np.exp(2*(y-5.4) + np.log(x_FR*x_RR+0.5)))
        for i in range(len(y)):
            if y[i]>7.2:
                f_2[i] = 1/(1 + np.exp(2*(y[i]-9) + np.log(x_FR[i]*x_RR[i]+0.5)))
        '''    
        f_2 = np.zeros([len(y), 1])
        for i in range(len(y)):
            if y[i] > 5.4:
                #f_2[i] = 1/(1 + np.exp(self.w_1*(y[i]-5.4) + self.w_2*min(x_FR[i], x_RR[i]) + self.sigma_12))
                f_2[i] = 1/(1 + np.exp(self.w_1*(y[i]-5.4) + self.w_2*min(x_FR[i]+self.w_5*(x_FR_dot[i]-x_dot[i]), x_RR[i]+self.w_5*(x_dot[i]-x_RR_dot[i])) + self.w_2*self.sigma_12))
            else:
                #f_2[i] = 1/(1 + np.exp(self.w_1*(y[i]-1.8) + self.w_2*min(x_FR[i], x_RR[i]) + self.sigma_12))
                f_2[i] = 1/(1 + np.exp(self.w_1*(y[i]-1.8) + self.w_2*min(x_FR[i]+self.w_5*(x_FR_dot[i]-x_dot[i]), x_RR[i]+self.w_5*(x_dot[i]-x_RR_dot[i])) + self.w_2*self.sigma_12))


        
#------------------------- forward collision features -------------------------------
        
        f_3 = np.zeros([len(y), 1])
        f_4 = np.zeros([len(y), 1])
        for i in range(len(y)):
            f_3[i] = 1/(1 + np.exp(self.w_3*x_FC[i] + self.sigma_3))
            f_4[i] = 1/(1 + np.exp(self.w_4*(x_FC_dot[i] - x_dot[i]) + self.sigma_4))
#------------------------- concatenate all featrues --------------------------------

        #features = np.transpose(np.concatenate(([f_1],[f_2]),0))
        features = np.hstack([f_1, f_2, f_3, f_4])
        return features

