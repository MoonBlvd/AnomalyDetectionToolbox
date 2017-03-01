import numpy as np

class classifier():
    def classify(gamma, m, cov_inv, x):
        # here x should be 1*W array where W is the number of features
        # compute the chi_square
        chi_square =np.sum (((x - m) ** 2) / m)
        # compute the distance criterion
        t_square = (chi_square ** -1)*gamma

        # anomaly detection
        if (x - m)*cov_inv*((x - m).T) <= t_square:
            f = False # Normal
        else:
            f = True # Anomolous

        return f

