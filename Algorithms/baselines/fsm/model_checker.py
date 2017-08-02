from __future__ import division
import numpy as np
from collections import deque
pi = 3.141592653
class checker():
    def __init__(self):
        self.buf_size = 100
        self.buf = deque([])
        self.delta = 1.8# lateral safe zone
        self.epsilon = 3 # longitudinal safe zone
        self.tau = 1.5 # human reaction time
        self.accel_min = -5 # maximal decceleration when brake. 
        self.brake_percent = 0.3 # the L_{brake%}, 30%
        self.w_lane = 3.6 # standar US highway lane width
        self.dot_phi_max = 0 # maximal yaw rate of a car model, need to investigate!!!
        
        # order: 'Roll angle', 'Pitch angle', 'P', 'Q', 'R', 'v_vertical', 'accel_z'
        self.mu = [-0.0109763850306648, 0.00785458833041675, -0.000266913782417902, \
        -0.000610899764758911, 0.000381041536040516, 0.241253993822007, -9.87148613000196]

        self.sigma = [0.0365617567359059, 0.0432340161604987, 0.0265829259852617, \
        0.0220461611257807, 0.0801788311332826, 1.82180911686150, 0.586627912723194]

    def run(self, frame):#, road_angle):

        if len(self.buf) >= self.buf_size:
            self.buf.popleft()
        self.buf.append(frame)

        # multi cars check
        if frame['num_obs'] > 0:
            # front car check
            front_ID, left_ID, right_ID = self.front_car_check(frame)
            if len(front_ID) > 0:
                for k in range(len(front_ID)):
                    tailgate_unsafe = self.tailgate_check(frame, front_ID[k])
                    if tailgate_unsafe:
                        pass_unsafe = self.pass_check(frame, front_ID[k], left_ID, right_ID)
                        if pass_unsafe:
                            return True
        return self.threshold_check(frame)

            #    self.lane_change_check(frame, left_ID, right_ID)
        #self.threshold_check(frame)

    def front_car_check(self,frame):
        front_ID = []
        left_ID = []
        right_ID = []
        for i in range(frame['num_obs']):
            if abs(frame['y_obs'][i]) <= self.delta + frame['w_obs'][i]/2:
                front_ID.append(i)
            elif frame['y_obs'][i] >self.delta + frame['w_obs'][i]/2:
                left_ID.append(i)
            elif frame['y_obs'][i] < - self.delta - frame['w_obs'][i]/2:
                right_ID.append(i) 
        return front_ID, left_ID, right_ID

    def tailgate_check(self, frame, i):
        if  frame['x_dot_obs'][i] > 0:
            # ego car is slower, safe
            return False # false - safe, true - unsafe
        else:
            if frame['accel_x'] < 0:
                # ego car is faster but deccelerating 
                return 1/(2*frame['accel_x']) * (frame['x_dot_obs'][i])**2 > frame['x_obs'][i]
            else:
                # ego car is faster but not decelerating
                L_stop = self.stop_distance( -frame['x_dot_obs'][i], frame['accel_x']) # minus means direction
                return L_stop > frame['x_obs'][i] # True means unsafe

    def stop_distance(self, v, a = 0):
        L_0 = (1/2) * a * self.tau**2 + v * self.tau
        v = v + a * self.tau
        L_brake = 0.0042 * v**2 + 0.0386 * v

        return L_brake*(self.brake_percent) + L_0


    def pass_check(self, frame, front_ID, left_ID, right_ID):
        # i j k are front_ID, left_ID, right_ID


        r = 0.5
        #let all road angle between [0,pi]
        #if frame['yaw'] >= 0:
        #    phi0 = road_angle - frame['yaw']
        #else:
        #    phi0 = road_angle - (frame['yaw'])


        # left lane passing check
        if frame['left_conf']:# if there is a left lane
            #if frame['left_type'] == 0 or 5
            y0 = frame['left_dist'] + self.w_lane/2 # left is positive 
        else:# if there is no left lane, 
            y0 = 0

        left_unsafe = self.fit_trajectory(frame, r, y0, front_ID, left_ID)

        # right lane passing check
        if frame['right_conf']:# if there is a right lane
            #if frame['right_type'] == 0 or 5
            y0 = frame['right_dist'] - self.w_lane/2 # right is negative
        else:# if there is no left lane, 
            y0 = 0

        right_unsafe = self.fit_trajectory(frame, r, y0, front_ID, right_ID)
        
        return (left_unsafe or right_unsafe) # if both safe, return False

    def fit_trajectory(self, frame, r, y0, front_ID, obs_ID):
        #ds0 = ds
        #t = -ds0/(v_delta)
        #ds = ds0 + (x_ego + v_delta)*t
        ds = frame['x_obs'][front_ID]
        if ds <= 0:
            return True
        phi0 = -frame['left_heading'] # accoding to Mobileye Document 8.3
        curvature_W = frame['left_curvature'] # according to Mobileye Document 8.3
        x_dot_W = frame['x_dot_ego'] + frame['x_dot_obs'][front_ID]
        x_dot_ego_W = -frame['x_dot_obs'][front_ID] # Assume x_dot_ego in Fw is constant
        phi_dot_W = curvature_W * x_dot_W # yaw rate of traffic window Fw. Positive means CCW

        a1 = -np.tan(phi0)*(r+1)/(2*ds*r) + y0/(r*ds**2)
        b1 = np.tan(phi0)
        c1 = 0

        a2 = r*np.tan(phi0)/(2*(1-r)*ds) - y0/((1-r)*ds**2)
        b2 = 2*y0/((1-r)*ds) - r*np.tan(phi0)/(1-r)
        c2 = (r/(1-r))*(np.tan(phi0)*ds/2-y0)

        #dot_phi_1 = 2*a1*v0/((1+(2*a1*0 + b1)^2)^(3/2))
        #dot_phi_2 = 2*a2*v0/((1+(2*a2*ds + b2)^2)^(3/2))
        dot_phi_1 = 2*a1*x_dot_ego_W/(1+(2*a1*0 + b1)**2) + phi_dot_W # Positive means CCW
        dot_phi_2 = 2*a2*x_dot_ego_W/(1+(2*a2*ds + b2)**2) + phi_dot_W # Positive means CCW
        dot_phi = max(abs(dot_phi_1), abs(dot_phi_2))
        
        #print 'phi_dot_W is: ', phi_dot_W
        #print 'params are: ', a1, ', ', b1, ', ', c1, ', ', a2, ', ', b2, ', ', c2,
        #print 'max yaw rate is: ', dot_phi
        if dot_phi < self.dot_phi_max:
            params = [a1, b1, c1, a2, b2, c2]
            consts = [phi0, r, ds, y0]
            if len(obs_ID) > 0:
                for i in range(len(obs_ID)):
                    self.collision_check(frame, params, consts, front_ID, obs_ID[i])
        else:
            return True

    def collision_check(self, frame, params, consts, front_ID, obs_ID):
        a1, b1, c1, a2, b2, c2 = params
        phi0, r, ds, y0 = consts
        collision = False
        x_dot_ego_W = -frame['x_dot_obs'][front_ID] # Assume x_dot_ego in Fw is constant
        if obs_ID:
            # check side collision
            x_dot_obs_W =  frame['x_dot_obs'][obs_ID] + x_dot_ego_W # velocity of side car in window
            if frame['y_obs'][obs_ID] > 0: #left
                y = frame['y_obs'][obs_ID] - self.delta # assign safe region to side car
            else: # right
                y = frame['y_obs'][obs_ID] + self.delta # assign safe region to side car
            if abs(y)  < abs(y0) + self.delta: # if side car safe region overlaps with traget safe region of ego car 
                # find intersection of trajectories
                # check first trajectory piece
                tmp = np.sqrt(b1**2 - 4*a1*(c1 + self.delta - y))
                x = np.nan
                if ~np.isnan(tmp):
                    x1 = -b1 + tmp
                    x2 = -b1 - tmp
                    if x1 <= r*ds and x1 >= 0:
                        x = x1
                    elif x2 <= r*ds and x2 >= 0:
                        x = x2
                if np.isnan(x):
                    # check second trajectory piece
                    tmp = np.sqrt(b2**2 - 4*a2*(c2 + self.delta - y))
                    if ~np.isnan(tmp):
                        x1 = -b2 + tmp
                        x2 = -b2 - tmp
                        if x1 <= ds and x1 >= r*ds:
                            x = x1
                        elif x2 <= ds and x2 >= r*ds:
                            x = x2
                '''
                if x <= r*ds:
                    L = 1/(3*a1) * ((2*a1*x + b1 + 1)**(3/2) - (b1 + 1)**(3/2))
                else:
                    L = 1/(3*a1) * ((2*a1*r*ds + b1 + 1)**(3/2) - (b1 + 1)**(3/2)) \
                        + 1/(3*a2) * ((2*a2*x + b2 + 1)**(3/2) - (2*a2*r*ds + b2 + 1)**(3/2))
                t = L/v0
                '''
                t = x/x_dot_ego_W # time when ego car enter new lane
                x_delta_t = frame['x_obs'][obs_ID] + x_dot_obs_W * t - x # relative position of side car at time t w.r.t. ego car
                x_dot_2 = frame['x_dot_obs'][obs_ID] # relative velocity of side car w.r.t. ego car
                if x_dot_2 > 0 and x_delta_t < -2 * self.epsilon: # case 1, ego car is in front and slower
                    stop_distance = self.stop_distance(x_dot_2)
                    if -x_delta_t - 2 * self.epsilon < stop_distance:
                        collision =  True
                elif x_dot_2 < 0 and x_delta_t > 2 * self.epsilon: # case 2, ego car is behind and faster
                    stop_distance = self.stop_distance(-x_dot_2)
                    if x_delta_t - 2 * self.epsilon < stop_distance:
                        collision =  True
                 
                elif x_dot_2 <= 0 and x_delta_t < -2 * self.epsilon: # case 3, ego car is in front and faster
                    collision = False
                elif x_dot_2 >= 0 and x_delta_t > 2 * self.epsilon: # case 4, ego car is behind and slower
                    collision = False
                elif x_delta_t <= 2 * self.epsilon and x_delta_t >= -2 * self.epsilon: # case 5, collision when enter lane
                    collision = True
                #v_obs = frame['x_dot_ego'] +frame['x_dot_obs'][obs_ID]
                #if v_obs * t + frame['x_obs'][obs_ID] + self.sigma >= x - self.sigma and\
                #   v_obs * t + frame['x_obs'][obs_ID] - self.sigma <= x + self.sigma:
                #   collision = True
        return collision
                    
                    
    #def lane_change_check(frame, j, k):
    #    # j k are, left_ID, right_ID
    #    if left_ID:
    
    def threshold_check(self, frame):
        # order: 'Roll angle', 'Pitch angle', 'P', 'Q', 'R', 'v_vertical', 'accel_z'
        X_sta = [frame['roll'], frame['pitch'], frame['P_rate'], frame['Q_rate'], \
                frame['R_rate'], frame['v_vertical'], frame['accel_z']]
        for i in range(7):
            #gaussian_model(X_sta[i], i)
            if X_sta[i] <= self.mu[i] - 3 * self.sigma[i] or X_sta[i] >= self.mu[i] + 3* self.sigma[i]:
                # 3 sigma check
                return True
        return False

    #def gaussian_model(x, idx):
    #    (1/(np.sqrt(2 * pi) * self.sigma[idx])) * np.exp(-(x - self.mu[idx])**2 / (2 * self.sigma[idx] **2)) 



