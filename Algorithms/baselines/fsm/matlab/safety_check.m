    
    %% check safety of a two car scenario - ego car and front car
function anomaly_scores = safety_check()
    % action: maintain (A1), left lane change (A2), right lane change (A3),
    % accelerate (A4), decelerate (A5)
    global num_action range 
    global a0_ego a0_obs
    global v0_ego v0_obs
    global y0_ego y0_obs
    global x_ego x_obs y_ego y_obs
    global delta epsilon w_lane
    global psi0_ego psi0_obs psi_T_0 gamma0
%     num_action = 5;
%     range = [-10, 70];% m
% 
%     psi_T_0 = 0; % assume the lane has no curvature.
%     gamma0 = 0; % assume the lane has no curvature.
% 
%     a0_ego = [0, 0, 0, 3, -3]; % initial acceleration of ego car
%     v0_ego = 8; % initial velocity of ego car
%     a0_obs = [0, 0, 0, 3, -3]; % initial acceleration of front car
%     v0_obs = 6; % initial velocity of front car
% 
%     y0_ego = [0, 3.6, -3.6, 0, 0]; % distance of ego car to next lane
%     y0_obs = [0, 3.6, -3.6, 0, 0]; % distance of front car to next lane
%     psi0_ego = 0; % vehicle orientation
%     psi0_obs = 0; % vehicle orientation
%     x_ego = 0; % location of ego car.
%     y_ego = 0; % location of ego car.
%     x_obs = 10; % location of obs car.
%     y_obs = 0; % location of obs car.
%     delta = 1.2;
%     epsilon = 3; 
%     w_lane = 3.6;

    p_ego = [0.1, 0.45, 0.3,0.10,0.05]; % ego car action probability given current state.
    p_obs = [0.4,0.1,0.2,0.05,0.25]; % obstacle car action probability given current state.

%     fig = figure(1);
%     figure(fig)
    actions = {'A1', 'A2', 'A3','A4', 'A5'};%{'maintain', 'left lane change', 'right lane change','accel', 'decel'};
    anomaly_scores = [];
    for i = 1:num_action % ego car
        state_ego = [psi0_ego, psi_T_0, gamma0, a0_ego(i), v0_ego, ...
                     y0_ego(i), x_ego, y_ego];
        for j = 1:num_action % obstacle car
            state_obs = [psi0_obs, psi_T_0, gamma0, a0_obs(j), v0_obs, ...
                         y0_obs(j), x_obs, y_obs];
            % plot lanes and cars
%             subplot(num_action,num_action, num_action*(i-1)+j);
%             plot(range,[0, 0],'k--','LineWidth',3);hold on;
%             plot(range,[w_lane, w_lane],'k--','LineWidth',3);hold on;
%             plot(range,[w_lane*2, w_lane*2],'k--','LineWidth',3);hold on;
%             plot(range,[w_lane*3, w_lane*3],'k--','LineWidth',3);hold on;
% 
%             rectangle('Position',[x_ego - epsilon, y_ego-delta,2*epsilon,2*delta],...
%                       'EdgeColor','r','LineWidth',2);hold on;
%             rectangle('Position',[x_obs - epsilon, y_obs-delta,2*epsilon,2*delta],...
%                       'EdgeColor','c','LineWidth',2);hold on;
%             title(['Ego: ',actions{i},'; Obs: ',actions{j}, '; R: ',num2str(score)],...
%                       'FontSize',16);
            % compute all trajectories
            [long_params_ego, lat_params_ego] = trajectory_prediction(state_ego, 'b');hold on;
            [long_params_obs, lat_params_obs] = trajectory_prediction(state_obs, 'g');hold on;

            % compute violation
            T = 0:0.2:5;
            m = length(T);
            T_long = [T.^4;T.^3;T.^2;T;T.^0];
            T_lat = [T.^5;T.^4;T.^3;T.^2;T;T.^0];
            long_ego = long_params_ego * T_long;
            lat_ego = lat_params_ego * T_lat;
            long_obs = long_params_obs * T_long;
            lat_obs = lat_params_obs * T_lat;
            k = size(long_ego,1);
            long_ego = repmat(long_ego,k,1);
            lat_ego = repmat(lat_ego,k,1);
            long_obs = kron(long_obs,ones(k,1)); %kronecker product
            lat_obs = kron(lat_obs,ones(k,1)); %kronecker product

            long_diff = abs(long_obs - long_ego);
            lat_diff = abs(lat_obs - lat_ego);
            [row, col] = find(long_diff <= 2*epsilon);
            counter = 0;
            for idx1 = 1:size(long_ego,1)
                mode = mod(idx1,k);
                if mode == 0
                    mode = k;
                end
                tmp = min(m-k+ceil(idx1/k), m-k + mode);% max time length to check
                long_close = find(long_diff(idx1,1:tmp) < 2*epsilon);
                for idx2 = long_close
                    if lat_diff(idx1,idx2) < 2*delta
                        counter = counter +1;
                        break;
                    end
                end
            end
            score = counter/idx1;
            anomaly_scores = [anomaly_scores, score];
            
        end
    end
    
end
