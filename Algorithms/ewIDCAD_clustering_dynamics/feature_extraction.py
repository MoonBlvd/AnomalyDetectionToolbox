from __future__ import division
import numpy as np

class extractor():

    def __init__(self):
        self.num = 2
    def extract(self, data):
        data.shape
        # y, x_FL and x_Rl
        y = data[:,0]
        x_FL = data[:,1]
        x_RL = data[:,3]
        #f_1 = np.exp(y-5.4)/(x_FL * x_RL + 1)
        #f_1 = 1/(1 + np.exp(-(y-5.4) + np.log(x_FL*x_RL)))
        f_1 = 1/(1 + np.exp(2*(5.4-y) + np.log(x_FL*x_RL+0.5)))
        for i in range(len(y)):
            if y[i]<3.6:
                f_1[i] = 1/(1 + np.exp(2*(1.8-y[i]) + np.log(x_FL[i]*x_RL[i]+0.5)))

        # y, x_FR and x_RR
        x_FR = data[:,2]
        x_RR = data[:,4]
        #f_2 = np.exp(5.4-y)/(x_FR * x_RR + 1)
        #f_2 = 1/(1 + np.exp(-(5.4-y) + np.log(x_FR*x_RR)))
        f_2 = 1/(1 + np.exp(2*(y-5.4) + np.log(x_FR*x_RR+0.5)))
        for i in range(len(y)):
            if y[i]>7.2:
                f_2[i] = 1/(1 + np.exp(2*(y[i]-9) + np.log(x_FR[i]*x_RR[i]+0.5)))
            

        features = np.transpose(np.concatenate(([f_1],[f_2]),0))
        return features

