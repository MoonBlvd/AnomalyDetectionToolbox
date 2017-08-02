import numpy as np
import matplotlib.pyplot as plt

def plot_scores(scores, n):
    plt.plot(range(1,n+1), scores)
    plt.title('Anomaly scores of the data')
    plt.show()

def plot_ROC(FPR, TPR, color, label):
        if len(FPR) > 1:
	    plot, = plt.plot(FPR, TPR, '-', color = color, linewidth = 2, label = label)
        elif len(FPR) == 1:
	    plot, = plt.plot(FPR, TPR, 's', color = color, linewidth = 2, label = label)
	plt.title('ROC curve')
	plt.xlabel('False positive rate')
	plt.ylabel('True positive rate')

	return plot
	
