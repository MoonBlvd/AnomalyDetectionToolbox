import numpy as np

def dataReader():
    # The read-in data should be a N*W matrix,
    # where N is the length of the time sequences,
    # W is the number of sensors/data features


if __name__ == '__main__':
    filepath = '../../benchmarks/Time\ Series\ Data/Intel\ Lab\ Data/'
    filename = 'Temperature/normalSeqs.data.csv'
    normalData = dataReader(filename)

    numSensors, numSeqs = normalData.shape()

    k = 50 # num of initial samples
    initSamples = normalData[:k]

    for i in range(k, numSeqs):
        if i 

