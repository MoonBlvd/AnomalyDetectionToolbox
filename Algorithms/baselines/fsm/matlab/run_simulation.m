clear all;clc;
% acquire an anomalous sequence
path = '../../../../Nan_Traffic_Simulator/07122017_data/';
id = 1;
data = csvread([path, 'anomalous_17D_', num2str(id),'.csv']);
label = csvread([path,'anomalous_17D_',num2str(id),'_label.csv']);
anomaly_ID = 1:2000;%310:320;
data1 = data(anomaly_ID,:);

% % insert a dropout frame;
% data1 = insert_dropout(data1);
% % simulate another sensor detection
% data2 = simulate_discrepancy(data1);
% % show the video of this traffic piece
% together = [data1,data2(:,3:end)];
% % plot_frames(together);
% % plot_frames(data1);
% % plot_frames(data2);

% initialization
% global variables
global a0_ego a0_obs
global v0_ego v0_obs
global y0_ego y0_obs
global x_ego x_obs y_ego y_obs
global delta epsilon w_lane
global psi0_ego psi0_obs psi_T_0 gamma0
global time_step

time_step = 0.5;
initialization();

buf = []; % buf stores a short history of data
anomaly_scores = [];
sensor_scores = [];
for i = 1:size(data1,1)
%     v0_ego = 8; % initial velocity of ego car
%     v0_obs = 6; % initial velocity of front car
    v0_ego = data1(i,2);
    v0_obs = v0_ego + data1(i,8);
    x_ego = 0;
    x_obs = data1(i,6);
    y_ego = data1(i,1);
    y_obs = data1(i,7);
    psi0_ego = 0; % vehicle orientation
    psi0_obs = 0; % vehicle orientation
    
    buf = [buf; x_ego,y_ego,v0_ego,x_obs,y_obs,v0_obs]
    
    sensor_scores = [sensor_scores,sensor_check(buf)];
    anomaly_score = safety_check();
    anomaly_scores = [anomaly_scores,mean(anomaly_score)];
    if size(buf,1) ==2
        buf(1,:) = [];
    end
end

function initialization()
    global num_action range 
    global a0_ego a0_obs
    global y0_ego y0_obs
    global delta epsilon w_lane
    global psi_T_0 gamma0
    
    num_action = 5;
    range = [-10, 70];% m

    psi_T_0 = 0; % assume the lane has no curvature.
    gamma0 = 0; % assume the lane has no curvature.

    a0_ego = [0, 0, 0, 3, -3]; % initial acceleration of ego car
    a0_obs = [0, 0, 0, 3, -3]; % initial acceleration of front car

    y0_ego = [5.4, 9, 1.8, 5.4, 5.4]; % distance of ego car to next lane
    y0_obs = [5.4, 9, 1.8, 5.4, 5.4]; % distance of front car to next lane

    delta = 1.2;
    epsilon = 3; 
    w_lane = 3.6;
end
function data1 = insert_dropout(data1)
    dropout = mean(data1(6:7,:));
    dropout(6) = 100; % the close object disappear
    dropout(7) = 9; % the close object disappear
    dropout(8) = 0; % the relative speed of object if it disappear
    data1 = [data1(1:6,:);dropout;data1(7:11,:)];
end
function data2 = simulate_discrepancy(data1)
    discrepancies = randn(12,17);
    discrepancies(:,1:2) = 0;
    discrepancies(:,4) = rand(12,1)/5; % y discrepancy is small, between 0 and 0.2.
    discrepancies(:,7) = rand(12,1)/5;
    discrepancies(:,10) = rand(12,1)/5;
    discrepancies(:,13) = rand(12,1)/5;
    discrepancies(:,16) = rand(12,1)/5;
    data2 = data1 + discrepancies;
end