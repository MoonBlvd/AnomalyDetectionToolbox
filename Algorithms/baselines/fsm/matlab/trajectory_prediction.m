% this trajectory prediction uses Quintic model.
% Houenou A, Bonnifait P, Cherfaoui V, Yao W. 
%    Vehicle trajectory prediction based on motion model and maneuver recognition. 
%    InIntelligent Robots and Systems (IROS), 2013 IEEE/RSJ International Conference on 2013 Nov 3 (pp. 4363-4369). IEEE.
function [long_param_list, lat_param_list] = trajectory_prediction(state, color)
    T = 1:0.2:5; % time of the maneuver
    % vehicle orientation
    % assume the lane has no curvature.
    % assume the lane has no curvature.
    % initial acceleration
    % initial velocity
    % distance to next lane]
    %state = [psi0, psi_T_0, gamma0, a0, v0, y0];

    long_param_list = [];
    lat_param_list = [];
    for t1 = 1:0.2:5 % for different ending time
        [lat_params, long_params] = compute_params(t1, state);
        long_param_list = [long_param_list; long_params'];
        lat_param_list = [lat_param_list; lat_params'];
        plot_trajectory(t1, lat_params, long_params, color);hold on;
    end
end

function plot_trajectory(time, lat_params, long_params, color)
    t = 0:0.2:time;
    lat = lat_params(1) * t.^5 +  lat_params(2) * t.^4 +  lat_params(3) * t.^3 + ...
           lat_params(4) * t.^2 + lat_params(5) * t.^1 + lat_params(6);
    long = long_params(1) * t.^4 + long_params(2) * t.^3 + long_params(3) * t.^2 + ...
          long_params(4) * t.^1 + long_params(5);
    %plot(long, lat, color);
end

function [lat_params, long_params] = compute_params(t1, state)
    psi0 = state(1); % vehicle orientation
    psi_T_0 = state(2); % assume the lane has no curvature.
    gamma0 = state(3); % assume the lane has no curvature.
    a0 = state(4); % initial acceleration
    v0 = state(5); % initial velocity
    y0 = state(6); % distance to next lane
    x_car = state(7); % start location of the car.
    y_car = state(8); % start location of the car.
    t0 = 0;
    
    d0 = y_car; % assume it start from the lane center.
    d0_dot = v0*sin(psi0 - psi_T_0);
    d0_ddot = sqrt(a0^2 + gamma0 * v0^2) * sin(psi0 - psi_T_0);
    s0 = x_car; % start location of the car.
    s0_dot = v0*cos(psi0 - psi_T_0);
    s0_ddot = sqrt(a0^2 + gamma0 * v0^2) * cos(psi0 - psi_T_0);

    d1 = y0; % assume it ends at target lane center
    d1_dot = 0;
    d1_ddot = 0;
    s1 = nan; % s1 is unknown
    s1_dot = v0 + a0 * t1;
    s1_ddot = sqrt(a0^2 + gamma0 * v0^2) * cos(psi0 - psi_T_0);

    init = [d0, d0_dot, d0_ddot, s0, s0_dot, s0_ddot ];
    final = [d1, d1_dot, d1_ddot, s1_dot, s1_ddot];
    lat_conditions = [d0, d1, d0_dot, d1_dot, d0_ddot, d1_ddot];
    long_conditions = [s0, s0_dot, s1_dot, s0_ddot, s1_ddot];
    lat_coeffs = [t0^5,    t0^4,    t0^3,   t0^2,   t0^1, 1;...
                   t1^5,    t1^4,    t1^3,   t1^2,   t1^1, 1;...
                   5*t0^4,  4*t0^3,  3*t0^2, 2*t0^1, 1,    0;...
                   5*t1^4,  4*t1^3,  3*t1^2, 2*t1^1, 1,    0;...
                   20*t0^3, 12*t0^2, 6*t0^1, 2,      0,    0;...
                   20*t1^3, 12*t1^2, 6*t1^1, 2,      0,    0];
    long_coeffs = [t0^4,    t0^3,   t0^2,   t0^1, 1;...
                  4*t0^3,  3*t0^2, 2*t0^1, 1,    0;...
                  4*t1^3,  3*t1^2, 2*t1^1, 1,    0;...
                  12*t0^2, 6*t0^1, 2,      0,    0;...
                  12*t1^2, 6*t1^1, 2,      0,    0];
    lat_params = pinv(lat_coeffs) * lat_conditions';
    long_params = pinv(long_coeffs) * long_conditions';
end 
    