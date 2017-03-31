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
        f_1 = np.exp(y-5.4)/(x_FL * x_RL + 1)

        # y, x_FR and x_RR
        x_FR = data[:,2]
        x_RR = data[:,4]
        f_2 = np.exp(5.4-y)/(x_FR * x_RR + 1)

        features = np.transpose(np.concatenate(([f_1],[f_2]),0))
        return features

