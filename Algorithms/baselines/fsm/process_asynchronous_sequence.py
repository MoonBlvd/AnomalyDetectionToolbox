from __future__ import division
import numpy as np
import prepare_data as prep
import sys
import csv
import matplotlib.pyplot as plt
from model_checker import checker
import data_reader as reader

pi = 3.1415926
def save_csv(filePath, fileName, trajectory):
    with open(filePath + fileName,'w') as csvfile:
        fieldsNames = ['Time', 'x_dot_ego', 'v_east', 'v_north', 'v_vertical', 'accel_x', 'accel_y', 'accel_z', \
                       'yaw', 'pitch', 'roll', 'P_rate', 'Q_rate', 'R_rate', 'x_obs', 'y_obs', \
                       'x_dot_obs', 'x_ddot_obs', 'w_obs', 'l_obs', 'left_dist', 'right_dist', \
                       'left_conf', 'right_conf', 'left_type', 'right_type','left_heading', \
                       'right_heading','left_curvature', 'right_curvature', 'curvature']
        writer = csv.DictWriter(csvfile, fieldsNames)
        writer.writeheader()
        for i in range(len(trajectory)):
            writer.writerow({'Time': trajectory[i]['time'], \
                             'x_dot_ego': trajectory[i]['x_dot_ego'],\
                             'v_east': trajectory[i]['v_east'],\
                             'v_north': trajectory[i]['v_north'],\
                             'v_vertical': trajectory[i]['v_vertical'],\
                             'accel_x': trajectory[i]['accel_x'],\
                             'accel_y': trajectory[i]['accel_y'],\
                             'accel_z': trajectory[i]['accel_z'],\
                             'yaw': trajectory[i]['yaw'], \
                             'pitch': trajectory[i]['pitch'], \
                             'roll': trajectory[i]['roll'], \
                             'P_rate': trajectory[i]['P_rate'], \
                             'Q_rate': trajectory[i]['Q_rate'],\
                             'R_rate': trajectory[i]['R_rate'],\
                             'x_obs': trajectory[i]['x_obs'], \
                             'y_obs': trajectory[i]['y_obs'],\
                             'x_dot_obs': trajectory[i]['x_dot_obs'],\
                             'x_ddot_obs': trajectory[i]['x_ddot_obs'],\
                             'w_obs': trajectory[i]['w_obs'], \
                             'l_obs': trajectory[i]['l_obs'], \
                             'left_dist': trajectory[i]['left_dist'], 
                             'right_dist': trajectory[i]['right_dist'], \
                             'left_conf': trajectory[i]['left_conf'], \
                             'right_conf': trajectory[i]['right_conf'], \
                             'left_type': trajectory[i]['left_type'], \
                             'right_type': trajectory[i]['right_type'],\
                             'left_heading': trajectory[i]['left_heading'],\
                             'right_heading': trajectory[i]['right_heading'],\
                             'left_curvature': trajectory[i]['left_curvature'],\
                             'right_curvature': trajectory[i]['right_curvature'],\
                             'curvature': trajectory[i]['curvature']})

def run_real_data(model_checker, file_path):
    MIN = 0.001
    carSignals, lanes, obstacles, TSR_1, MIDGs = prep.prepare_data(file_path)
    k_obstacle = 0 # counter of obstacle index
    num_obstacles = len(obstacles.time)
    k_MIDG = 0 # counter of MIDG signal index
    num_MIDGs = len(MIDGs.time)
    start = 0
    end = len(lanes.time)
    trajectory = []
    for i in range(start, end):
        # use lanes signal as frame base
        frame = {}
        frame['time'] = lanes.time[i]
        frame['left_dist'] = -lanes.left_dist[i] # let left be positive
        frame['right_dist'] = -lanes.right_dist[i] # let right be negative
        frame['left_conf'] = lanes.left_conf[i]
        frame['right_conf'] = lanes.right_conf[i]
        frame['left_type'] = lanes.left_type[i]
        frame['right_type'] = lanes.right_type[i]
        frame['left_heading'] = lanes.left_heading[i]
        frame['right_heading'] = lanes.right_heading[i]
        frame['left_curvature'] = lanes.left_curvature[i]
        frame['right_curvature'] = lanes.right_curvature[i]
        frame['curvature'] = lanes.curvature[i]
        frame['x_dot_ego'] = carSignals.speed[i]/3.6 
        # acquire all obstalces in this frame
        j = k_obstacle
        frame['num_obs'] = 0
        while k_obstacle <= num_obstacles and \
            carSignals.time[i] >= obstacles.time[k_obstacle] + MIN:
            # when obstacle time is less than lane time, 
            # the obstacle is within this frame
            num_obstacles += 1
            k_obstacle += 1
            frame['num_obs'] += 1
        if k_obstacle > j:
            frame['x_obs'] = obstacles.x[j:k_obstacle]
            frame['y_obs'] = obstacles.y[j:k_obstacle]
            frame['w_obs'] = obstacles.w[j:k_obstacle]
            frame['l_obs'] = obstacles.l[j:k_obstacle]
            frame['x_dot_obs'] = obstacles.v[j:k_obstacle]
            frame['x_ddot_obs'] = obstacles.a[j:k_obstacle]
        #frame['phi_obs'] = obstacles.phi[j:k_obstacle]
        # acquire MIDG data for this frame
        while k_MIDG <= num_MIDGs and lanes.time[i] >= MIDGs.time[k_MIDG]:
            k_MIDG += 1
        frame['yaw'] = MIDGs.yaw[k_MIDG]
        frame['pitch'] = MIDGs.pitch[k_MIDG]
        frame['roll'] = MIDGs.roll[k_MIDG]
        frame['v_east'] = MIDGs.v_east[k_MIDG]
        frame['v_north'] = MIDGs.v_north[k_MIDG]
        frame['v_vertical'] = MIDGs.v_vertical[k_MIDG]
        frame['accel_x'] = MIDGs.accel_x[k_MIDG]
        frame['accel_y'] = MIDGs.accel_y[k_MIDG]
        frame['accel_z'] = MIDGs.accel_z[k_MIDG]
        frame['P_rate'] = MIDGs.P_rate[k_MIDG]
        frame['Q_rate'] = MIDGs.Q_rate[k_MIDG]
        frame['R_rate'] = MIDGs.R_rate[k_MIDG]
        
        #model_checker.run(frame, road_angle)
        
        if i >= 8138 and i <= 8210: # high-risk pass, failed
            trajectory.append(frame)
            # street direction is 206.97 - 207.12 degrees
            anomaly = model_checker.run(frame)
            print 'Anomalous at time ',frame['time'],' is: ', anomaly
        if i == 8210:
            fileName = 'unsafe_passing_1.csv'
            save_csv(file_path, file_name, trajectory)
            trajectory = []
        
        if i >= 8782 and i <= 8814: # close to crash
            trajectory.append(frame)
            # street direction is 319.73-319.90 degress
            anomaly = model_checker.run(frame)
            print 'Anomalous at time ',frame['time'],' is: ', anomaly
        if i == 8814:
            fileName = 'close_to_crash_1.csv'
            save_csv(file_path, file_name, trajectory)
            trajectory = []
        
def run_synthetic_data(model_checker, file_path, file_name, label_name):
    MIN = 0.000000000001
    # y_ego, x_dot_ego
    # x_FL, y_FL, x_dot_FL
    # x_FC, y_FC, x_dot_FC,
    # x_FR, y_FR, x_dot_FR,
    # x_RL, y_RL, x_dot_RL,
    # x_RR, y_RR, x_dot_RR
    data = reader.read_data(file_path + file_name)
    label = reader.read_data(file_path + label_name)

    start = 0
    end = 2000
    anomalies = []
    for i in range(start,end):
        X = data[i, :]
        frame = {}
        frame['time'] = i 
        if X[0] <= 3.6:
            frame['left_dist'] = 3.6 - X[0] # let left be positive
            frame['right_dist'] = 0 - X[0] # let right be negative
            frame['left_conf'] = 3
            frame['right_conf'] = 0
            frame['left_type'] = 0
            frame['right_type'] = 1
        elif X[0] <= 7.2:
            frame['left_dist'] = 7.2 - X[0] # let left be positive
            frame['right_dist'] = 3.6 - X[0] # let right be negative
            frame['left_conf'] = 3
            frame['right_conf'] = 3
            frame['left_type'] = 0
            frame['right_type'] = 0
        elif X[0] <= 10.8:
            frame['left_dist'] = 10.8 - X[0] # let left be positive
            frame['right_dist'] = 7.2 - X[0] # let right be negative
            frame['left_conf'] = 0
            frame['right_conf'] = 3
            frame['left_type'] = 1
            frame['right_type'] = 0
        frame['left_heading'] = MIN
        frame['right_heading'] = MIN
        frame['left_curvature'] = MIN
        frame['right_curvature'] = MIN
        frame['curvature'] = MIN
        frame['x_dot_ego'] = X[1]

        frame['num_obs'] = 5
        frame['x_obs'] = [X[2], X[5], X[8], X[11], X[14]] #FL FC FR RL RR
        frame['y_obs'] = [X[3], X[6], X[9], X[12], X[15]] - X[0]
        frame['w_obs'] = [2, 2, 2, 2, 2] 
        frame['l_obs'] = [6, 6, 6, 6, 6]
        frame['x_dot_obs'] = [X[4], X[7], X[10], -X[13], -X[16]]
        frame['x_ddot_obs'] = [0, 0, 0, 0, 0, 0]
            
        frame['yaw'] = 0 
        frame['pitch'] = 0
        frame['roll'] = 0
        frame['v_east'] = X[1]
        frame['v_north'] = 0
        frame['v_vertical'] = 0
        frame['accel_x'] = 0
        frame['accel_y'] = 0
        frame['accel_z'] = -9.81
        frame['P_rate'] = 0
        frame['Q_rate'] = 0
        frame['R_rate'] = 0

        anomaly = model_checker.run(frame)
        anomalies.append(1) if anomaly else anomalies.append(0)
    #print anomalies
    anomalies = np.array(anomalies)
    print np.where(anomalies == 1)[0] 
    TP = 0
    FP = 0
    for i in range(start, end):
        if anomalies[i] == 1 and label[i] == -1:
            TP += 1
        elif anomalies[i] == 1 and label[i] == 1:
            FP += 1
    num_positive = len(np.where(label == -1)[0])
    num_negative = len(np.where(label == 1)[0])
    
    TPR = TP/num_positive
    FPR = FP/num_negative
    print 'TPR: ', TPR
    print 'FPR: ', FPR
    return anomalies

if __name__ == '__main__':
    type = sys.argv[1]
    model_checker = checker() # init the model_checker
    if type == 'simulate':
        file_path = '../../../Nan_Traffic_Simulator/07122017_data/'
        for i in range(10):
            file_name = 'anomalous_17D_' + str(i+1) + '.csv'
            label_name = 'anomalous_17D_' + str(i+1) +'_label.csv'
            run_synthetic_data(model_checker, file_path, file_name, label_name)

    elif type == 'real':
        file_path = '../../../../circularDataProcess/translated_data/05182017/'
        run_real_data(model_checker, file_path)

    #road_angle = 27.05 * pi/180# angle of road, in [0, 180] deg
