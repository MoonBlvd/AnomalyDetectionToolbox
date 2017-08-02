import numpy as np

class pca():
    def __init__(self, n, d, mean):
        self.n = n # length of time-series
        self.d = d # dimension of data
        self.r = 0.1 # oversampling ratio
        self.beta = 1/(self.n * self.r) # beta = 1/(n*r)
        self.mu = mean
        self.y_square_sum = 0
        self.b = 0.0001
        self.yx_sum = 0
        self.u = np.ones((self.d,1)) # d*1
        
    def run_ospca(self, data):
        for i in range(self.n):
            x = data[i,:].reshape(1, self.d)
            x_bar = x - self.mu
            self.update(x_bar)
        self.u = self.u/np.linalg.norm(self.u)

    def run_online_ospca(self, data):
        pca_scores = []
        self.run_ospca(data)
        print self.u
        for i in range(self.n):
            x = data[i,:].reshape(1, self.d) # 1*d
            mu = (self.mu + self.r*x) / (1 + self.r)
            x_bar = x - mu
            y = np.dot(x_bar,self.u) # approximation, y_i = U_{i-1} * x_bar_i
            U = (self.beta * self.yx_sum + y * x_bar) / (self.beta * self.y_square_sum + y**2)
            U = U/np.linalg.norm(U)
            score = 1- np.dot(U, self.u)
            pca_scores = np.append(pca_scores, score)
        return pca_scores

    def update(self, x_bar):
        y = np.dot(x_bar, self.u)
        self.b = self.beta * self.b + y**2
        e = x_bar.T - self.u * y
        self.u = self.u + (y*e)/self.b
        self.yx_sum = self.yx_sum + y*x_bar
        self.y_square_sum = self.y_square_sum + y**2
