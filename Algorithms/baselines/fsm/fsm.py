import numpy as np
from collections import deque

class fsm():
    def __init__(self, buf_size, offset):
        self.lane_width = 3.6
        self.num_lane = 3
        self.car_length = 6
        self.car_width = 2
        self.v_max = 35 # 
        self.v_min = 10 #
        self.a_max = 5
        self.x_max = 100 # maximum of x range 
        self.y_max = self.num_lane*self.lane_width - self.car_width/2
        self.y_min = self.car_width/2
        self.timestamp =0.5
        self.buf_size = buf_size # size of the buffer used for temporal analysis
        self.buf = deque([])
        self.offset = offset
        #dict = {}

    def run(self, data, fields):
        # read data
        dict = {}
        dict['y_ego'] = data[0]
        dict['x_dot_ego'] = data[1]
        dict['x_obs'] = data[[2,5,8,11,14]] # longitudinal range (abs value) from FL car to ego car
        dict['y_obs'] = data[[3,6,9,12,15]] # lateral position of the FL
        dict['x_dot_obs'] = data[[4,7,10,13,16]] # relative velocity: v_ego - v_{FL,FC,FR,RL,RR}
        
        self.buf.append(dict)
        
        if len(self.buf) > self.buf_size:
            self.buf.popleft() 

        anomaly = False
        # do threshold check firstly
        anomaly, point_anomaly_type = self.threshold_check(anomaly, dict)
        if anomaly:
            return anomaly, point_anomaly_type,'Normal'
        # do collision check secondly, include collision from all directions
        anomaly, point_anomaly_type = self.collision_check(anomaly, dict)
        if anomaly:
            return anomaly, point_anomaly_type,'Normal'
        
        # do temporal check over the time-series
        collective_anomaly_type = 'Normal'
        if len(self.buf) >= self.buf_size:
            anomaly, collective_anomaly_type = self.unstability_check(anomaly)
        return anomaly, point_anomaly_type, collective_anomaly_type
    def threshold_check(self, anomaly, dict):
        anomaly_type = 'Normal'
        if dict['y_ego'] > self.y_max or dict['y_ego'] < self.y_min:
            anomaly = True
            anomaly_type = 'Outside road boundary'
            return anomaly, anomaly_type
        elif max(dict['x_obs']) > self.x_max or \
             min(dict['x_obs']) < 0:
            anomaly = True
            anomaly_type = 'Distance is out of the boundary.'
            return anomaly, anomaly_type
        elif dict['x_dot_ego'] > self.v_max - self.offset * 10:
            anomaly = True
            anomaly_type = 'Overspeed'
            return anomaly, anomaly_type
        elif dict['x_dot_ego'] < self.v_min + self.offset * 10:
            anomaly = True
            anomaly_type = 'Speed is too low'
            return anomaly, anomaly_type
        return anomaly, anomaly_type

    def collision_check(self, anomaly, dict):
        anomaly_type = 'Normal'
        for i in range(5):
            if abs(dict['y_obs'][i]-dict['y_ego']) <= self.car_width + self.offset:
                if dict['x_obs'][i] <= self.car_length + self.offset:
                    anomaly = True
                    anomaly_type = 'Collision'
                    return anomaly, anomaly_type
                elif dict['x_obs'][i] + dict['x_dot_obs'][i] * self.timestamp <=0:
                    anomaly = True
                    anomaly_type = 'Potential collision'
                    return anomaly, anomaly_type
        return anomaly, anomaly_type
    def unstability_check(self, anomaly):
        # record the velocity and lateral position of the ego car
        anomaly_type = 'Normal'
        x_dot_ego_list = np.zeros(self.buf_size)
        y_ego_list = np.zeros(self.buf_size)
        lane_violation_flag = 0
        for i in range(0, self.buf_size):
            x_dot_ego_list[i] = self.buf[i]['x_dot_ego']
            y_ego_list[i] = self.buf[i]['y_ego']
            for j in range(1,self.num_lane):
                if y_ego_list[i] >= j*self.lane_width - self.car_width/2 and \
                   y_ego_list[i] <= j*self.lane_width + self.car_width/2:
                    lane_violation_flag += 1
                    break
        # compute accel of the car
        x_accel = (x_dot_ego_list[1:self.buf_size] - x_dot_ego_list[:self.buf_size-1])/self.timestamp
        
        if max(x_accel) > self.a_max or min(x_accel) < -self.a_max:
            anomaly = True
            anomaly_type = 'Big acceleration/deceleration'
            return anomaly, anomaly_type
        # find long-time lane violation 
        if lane_violation_flag >= 4:# * 2/self.timestamp:
            anomaly = True
            anomaly_type = 'Long-term lane violation'
            return anomaly, anomaly_type
        # find car vibration
        y_ego_list -= y_ego_list[0]
        if abs(y_ego_list.mean()) < self.car_width and y_ego_list.var() > self.car_length:
            anomaly = True
            anomaly_type = 'Car vibrating'
            return anomaly, anomaly_type
        return anomaly, anomaly_type


'''

        self.x_FL = data[2]
        self.y_FL = data[3] 
        self.x_dot_FL = data[4] 

        self.x_FC = data[5]
        self.y_FC = data[6]
        self.x_dot_FC = data[7]

        self.x_FR = data[8]
        self.y_FR = data[9]
        self.x_dot_FR = data[10]

        self.x_RL = data[11]
        self.y_RL = data[12]
        self.x_dot_RL = data[13]

        self.x_RR = data[14]
        self.y_RR = data[15]
        self.x_dot_RR = data[16]
'''
