import numpy as np
import csv
from fsm import fsm
import pickle

#def load_dictionary(fileName):
#    return pickle.load(open(fileName, 'rb'))
class carSignal():
    time = []
    speed = []
    yaw = []
    pitch = []
    brake = []
    right_blink = []
    left_blink = []
class lane():
    time = []
    curvature = []
    right_type = []
    right_conf = []
    right_dist = []
    right_heading = []
    left_type = []
    left_conf = []
    left_dist = []
    left_heading = []
class obstacle():
    time = []
    ID = []
    type = []
    x = []
    y = []
    w = []
    l = []
    v = []
    a = []
    phi = []
class TSR():
    time = []
    type = []
    x = []
    y = []
    z = []
class MIDG():
    time = []
    yaw = []
    pitch = []
    roll = []
    v_east = []
    v_north = []
    v_vertical = []
    accel_x = []
    accel_y = []
    accel_z = []
    P_rate = []
    Q_rate = []
    R_rate = []
def load_csv(fileName):
    i = 0
    with open(fileName, 'r') as file:
        tmp = csv.reader(file, delimiter = ',')
        for line in tmp:
            if i == 0:
                data = line
                data = np.array(data)
            else:
                data = np.vstack((data,line))
            i += 1
    data = data.astype(np.float)
    return data

def extract_struct(carSignal_array, lane_array, obstacle_array, TSR_array, MIDG_array):
    carSignals = carSignal()
    lanes = lane()
    obstacles = obstacle()
    TSR_1 = TSR()
    MIDGs = MIDG()
    length = 6
    
    carSignals.time = carSignal_array[:,0]
    carSignals.speed = carSignal_array[:,1]
    carSignals.yaw = carSignal_array[:,2]
    carSignals.pitch = carSignal_array[:,3]
    carSignals.brake = carSignal_array[:,4]
    carSignals.right_blink = carSignal_array[:,8]
    carSignals.left_blink = carSignal_array[:,9]
    
    lanes.time = lane_array[:,0]
    lanes.right_type = lane_array[:,1]
    lanes.left_type = lane_array[:,2]
    lanes.right_conf = lane_array[:,3]
    lanes.left_conf = lane_array[:,4]
    lanes.right_dist = lane_array[:,5]
    lanes.left_dist = lane_array[:,6]
    lanes.right_heading = lane_array[:,7]
    lanes.left_heading = lane_array[:,8]
    lanes.right_curvature = lane_array[:,9]
    lanes.left_curvature = lane_array[:,10]
    lanes.curvature = lane_array[:,11]

    obstacles.time = obstacle_array[:,0]
    obstacles.ID = obstacle_array[:,1]
    obstacles.type = obstacle_array[:,2]
    obstacles.x = obstacle_array[:,5]
    obstacles.y = obstacle_array[:,6]
    obstacles.w = obstacle_array[:,8]
    obstacles.l = obstacle_array[:,9]
    for i in range(len(obstacles.l)):
        if obstacles.l[i]:
            obstacles.l[i] = length
    obstacles.v = obstacle_array[:,11]
    obstacles.a = obstacle_array[:,12]
    obstacles.phi = obstacle_array[:,13]

    TSR_1.time = TSR_array[:,0]
    TSR_1.type = TSR_array[:,1]
    TSR_1.x = TSR_array[:,2]
    TSR_1.y = TSR_array[:,3]
    TSR_1.z = TSR_array[:,4]

    MIDGs.time = MIDG_array[:,0]
    MIDGs.yaw =  MIDG_array[:,1]
    MIDGs.pitch = MIDG_array[:,2]
    MIDGs.roll = MIDG_array[:,3]
    MIDGs.v_east = MIDG_array[:,4]
    MIDGs.v_north = MIDG_array[:,5]
    MIDGs.v_vertical = MIDG_array[:,6]
    MIDGs.accel_x = MIDG_array[:,7]
    MIDGs.accel_y = MIDG_array[:,8]
    MIDGs.accel_z = MIDG_array[:,9]
    MIDGs.P_rate = MIDG_array[:,10]
    MIDGs.Q_rate = MIDG_array[:,11]
    MIDGs.R_rate = MIDG_array[:,12]

    return carSignals, lanes, obstacles, TSR_1, MIDGs

def prepare_data(filePath):

    #filePath = '../../../../circularDataProcess/translated_data/05182017/'
    #fileName = 'translated_data.pkl'
    fileName = 'CarSignalFromMobileye.csv'
    carSignal_array = load_csv(filePath + fileName)
    fileName = 'Lanes.csv'
    lane_array = load_csv(filePath + fileName)
    fileName = 'TSR_1.csv'
    TSR_array = load_csv(filePath + fileName)
    fileName = 'Obstacles.csv'
    obstacle_array = load_csv(filePath + fileName)
    fileName = 'MIDG.csv'
    MIDG_array = load_csv(filePath + fileName)
    return  extract_struct(carSignal_array, lane_array, obstacle_array, TSR_array, MIDG_array)
