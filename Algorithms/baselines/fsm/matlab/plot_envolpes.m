clear all; clc;
% set constant parameters
global l_car w_car x_ego y_ego range w_lane dot_phi_max
global red green blue
global epsilon delta
global tau
w_lane = 3.6;
l_car = 5; % m
w_car = 2; % m
x_ego = 0; y_ego = 0; % m
range = [-10, 40];% m
dot_phi_max = deg2rad(25); % rad
name = {'red.png', 'green.png', 'blue.png'};
[red, green, blue] = image_read(name);
epsilon = 2.5;
delta = 1;
tau = 0;
% set variables, f(y0, v0, phi0, r, ds) = 0
y0 = 3.6; % meter
v0 = 25; % m/s
v_obs = 20;
phi0 = 0:0.05:0.8; % radians
r = 0.1:0.05:0.9; % ratio, (0,1)
ds = 5:4:70; % m
params = [phi0', ds', r'];

fig = figure(1);

% plot lanes
figure(fig)
plot(range,[-w_lane/2, -w_lane/2],'k--','LineWidth',3);hold on;
plot(range,[w_lane/2, w_lane/2],'k--','LineWidth',3);
plot(range,[w_lane*3/2, w_lane*3/2],'k--','LineWidth',3);
plot(range,[-w_lane*3/2, -w_lane*3/2],'k--','LineWidth',3);hold on;

% plot a two car passing scenario
%two_car_passing(fig)

% lane changing with side car
lane_changing(fig)

%% two car passing 
function two_car_passing(fig)
    global red green blue
    dot_phi_list = [];
    y0 = 3.6;v0 = 20;v_obs = 16;phi0 = 0;ds = 25;r = 0.5;
    for r = 0.1:0.01:0.9
        dot_phi, tmp = quadratic_motion(y0, v0,v_obs,phi0, ds, r, fig, nan);hold on;
        dot_phi_list = [dot_phi_list, dot_phi];
    end
    %x_ego - l_car/2, y_ego-w_car/2,l_car,w_car
    title(['\phi_0 = ',num2str(phi0),', ds = ', num2str(ds), ', v_0 = ', num2str(v0)]);

    % plot cars
    axes('pos',[.20 .455 .25 .125]);
    imshow(red); hold on;
    axes('pos',[.685 .455 .25 .125]);
    imshow(blue); hold on;
    axes('pos',[.565 .7 .25 .125]);
    imshow(red); hold on;
end
%% lane changing
function lane_changing(fig)
    global w_lane l_lane range
    global red green blue
    global epsilon delta
    dot_phi_list = [];
    x_star_list = [];
    y0 = 3.6; v0 = 20; phi0 = 0; accel = 0;
    v_obs_2 = 16; x_obs_2 = 15; y_obs_2 = 3.6;
    r = 0.5;
    T = 7; % max time is 7 seconds
    Lstop = stop_distance(v0, v_obs_2, accel);
    % trajectory 1
    ds1 = x_obs_2 - Lstop;
    for r = 0.1:0.05:0.9
        [dot_phi, x_star] = quadratic_motion(y0, v0, v_obs_2, phi0, ds1, r, fig, nan); hold on;
        dot_phi_list = [dot_phi_list, dot_phi];
        x_star_list = [x_star_list, x_star];
    end
    ds1 = ds1 - 2*epsilon; % for plot purpose!!!
    r = 0.1:0.05:0.9; % for reward computing purpose
    reward_1 = compute_reward(dot_phi_list, x_star_list, x_obs_2, r, nan, Lstop); % nan means do not need to check collision
    
    % trajectory 2
    dot_phi_list = [];
    x_star_list = [];
    ds2 = (v0 - v_obs_2) * T + 2*epsilon; % no front car, so don't consider epsilon
    for r = 0.1:0.05:0.9
        [dot_phi,x_star] = quadratic_motion(y0, v0, v_obs_2, phi0, ds2, r, fig, y_obs_2); hold on;
        dot_phi_list = [dot_phi_list, dot_phi];
        x_star_list = [x_star_list, x_star];
    end
    ds2 = ds2 - 2*epsilon; % for plot purpose!!!
    r = 0.1:0.05:0.9; % for reward computing purpose
    reward_2 = compute_reward(dot_phi_list, x_star_list, x_obs_2, r, ds2, Lstop);
    
    % plot ruler
    figure(fig)
    plot([x_obs_2, x_obs_2], [-w_lane*3/2, w_lane*3/2], 'k--', 'LineWidth',1);hold on;
    plot([ds1, ds1], [-w_lane*3/2, w_lane*3/2], 'k--', 'LineWidth',1);hold on;
    plot([ds2, ds2], [-w_lane*3/2, w_lane*3/2], 'k--', 'LineWidth',1);hold on;
    %plot safe bounds
    plot(range, [y_obs_2 - delta,y_obs_2 - delta], 'b--', 'LineWidth',2);hold on;
    
    title(['\phi_0 = ',num2str(phi0),', ds_2 = ', num2str(ds2), ...
        ', v_{ego/W} = ', num2str(v0 - v_obs_2), ', reward_1 = ', num2str(reward_1), ...
        ', reward_2 = ', num2str(reward_2)]);

    axes('pos',[.16 .455 .25 .125]);
    imshow(red); hold on;
%     axes('pos',[.685 .455 .25 .125]);
%     imshow(blue); hold on;
    axes('pos',[.39 .7 .25 .125]);
    imshow(green); hold on;
    axes('pos',[.59 .7 .25 .125]);
    imshow(red); hold on;
    axes('pos',[.31 .7 .25 .125]);
    imshow(red); hold on;
    
end

%% Quadratic motion
function [dot_phi, x_star]= quadratic_motion(y0, v0, v_obs, phi0, ds, r, fig, y_obs_2)
    global l_car w_car x_ego y_ego range w_lane dot_phi_max
    global red green blue
    global epsilon delta
    
    t = ds/(v0 - v_obs);
    ds0 = ds;
    ds = ds - 2*epsilon;
    %ds = ds0 + v_obs * t;
    v0 = v0 - v_obs;
    
    a1 = -tan(phi0)*(r+1)/(2*ds*r) + y0/(r*ds^2);
    b1 = tan(phi0);
    c1 = 0;
    a2 = r*tan(phi0)/(2*(1-r)*ds) - y0/((1-r)*ds^2);
    b2 = 2*y0/((1-r)*ds) - r*tan(phi0)/(1-r);
    c2 = (r/(1-r))*(tan(phi0)*ds/2-y0);
    params = [a1,b1,c1,a2,b2,c2];
    if isnan(y_obs_2)
        x_star = nan;
    else
        x_star = compute_intersection(params, y_obs_2, ds, r);
    end
    
    %max_phi = atan(2*a1*r*ds + b1);
    %delta = cos(pi/2 - max_phi - acos(l_car/(sqrt(l_car^2 + w_car^2)))) * sqrt(l_car^2 + w_car^2);
    
    %tmp_x = r*ds;
    tmp_x = 0;
    pho = (1+(2*a1*tmp_x + b1)^2)^(3/2)/(2*abs(a1));
    v = v0*sqrt(1+2*a1*tmp_x + b1);
    dot_phi_1 = v/pho;
    
    tmp_x = ds;
    pho = (1+(2*a2*tmp_x + b2)^2)^(3/2)/(2*abs(a2));
    v = v0*sqrt(1+2*a2*tmp_x + b2);
    dot_phi_2 = v/pho;
    dot_phi = max(dot_phi_1, dot_phi_2);
%     dot_phi_1 = 2*a1*v0/((1+(2*a1*0 + b1)^2)^(3/2));
%     dot_phi_2 = 2*a2*v0/((1+(2*a2*ds + b2)^2)^(3/2));
%     dot_phi = max(dot_phi_1, dot_phi_2);
    %set(fig, 'Position', [100, 100, 1000, 300]);
    % plot cars
%     rectangle('Position',[x_ego - l_car/2, y_ego-w_car/2,l_car,w_car],'EdgeColor','r');hold on;
%     rectangle('Position',[x_ego + ds0 - l_car/2, y_ego-w_car/2,l_car,w_car],'EdgeColor','b','FaceColor','b');hold on;
%     rectangle('Position',[x_ego + ds - 1*l_car/2, y_ego+y0-w_car/2,l_car,w_car],'EdgeColor','r','LineStyle','--');hold on;
%     
    %plot trajectory
    if dot_phi <= dot_phi_max
        color = 'g-';
    else
        color = 'r-';
    end
    if r == 0.5
        color = 'k-';
    end
    
    x = x_ego:0.05:x_ego+ds*r;
    y1 = a1*x.^2 + b1*x + c1;
    figure(fig)
    plot(x,y1,color,'LineWidth',2);hold on;
    if r == 0.85
        plot(x, y1+delta,'b--','LineWidth',2);hold on;
    end
    
    x = x_ego+ds*r:0.05:x_ego + ds;
    y2 = a2*x.^2 + b2*x + c2;
    figure(fig)
    plot(x,y2,color,'LineWidth',2);hold on;
    if r == 0.85
        plot(x, y2+delta,'k-','LineWidth',2);hold on;
    end
    x = x_ego + ds0 + l_car/2 :0.05: x_ego + ds + l_car/2;
    plot(x,ones(size(x))*y_ego,'b--','LineWidth',2);hold on;
    % safety check
%     if dot_phi > dot_phi_max
%         str = 'Unsafe to pass!';
%         text(0.5,0.8,str);
%     else
%         str = 'Safe to pass!';
%         text(0.5,0.8,str);
%     end
end
%% compute_intersection
function x = compute_intersection(params, y_obs_2, ds, r)
    global epsilon delta
    a1 = params(1);b1 = params(2);c1 = params(3);a2 = params(4);b2 = params(5);c2 = params(6);
    tmp = b1^2 - 4*a1*(c1 + 2*delta - y_obs_2);
    x = nan;
    if tmp >= 0
        x = (-b1 + sqrt(tmp))/(2*a1);
        if x > r * ds
            tmp = b2^2 - 4*a2*(c2 + 2*delta - y_obs_2);
            if tmp >= 0
                x = (-b2 + sqrt(tmp))/(2*a2);
            end
        end
    else
        tmp = b2^2 - 4*a2*(c2 + 2*delta - y_obs_2);
        if tmp >= 0
            x = (-b2 + sqrt(tmp))/(2*a2);
        end
    end
end
%% compute reward
function reward = compute_reward(dot_phi_list, x_star_list, x_obs_2, r, ds, Lstop)
    global epsilon dot_phi_max
    flag1 = true; flag2 = false;
    [r_max, max_ID] = max(r); % initialize
    [r_min, min_ID] = min(r); % initialize
    for i = 1:length(r)
        if dot_phi_list(i) < dot_phi_max & flag1
            r_min = r(i);
            flag1 = false;
            flag2 = true;
            min_ID = i;
        end
        if dot_phi_list(i) > dot_phi_max & flag2
            r_max = r(i);
            max_ID = i;
            break;
        end
    end
    if ~flag2 % if all unsafe
        r_max = r_min;
        reward = 0; % 0, means not safe at all
        return
    end
    R_slip = (r_max-r_min)/(max(r) - min(r)); %slip safety reward, from 0 to 1, the higher, the safer
    if isnan(ds)
        reward = R_slip;
        return
    end
    x_min = x_star_list(min_ID);x_max = x_star_list(max_ID);
    if x_obs_2 < x_min - 2*epsilon
        R_collid = 1; %collid safety reward, from 0 to 1, the higher the safer.
    elseif x_obs_2 >= x_min - 2*epsilon & x_obs_2 < x_max - 2*epsilon
        R_collid = 1 - (x_obs_2 + 2*epsilon - x_min)/(x_max-x_min);
    elseif x_obs_2 >= x_max - 2*epsilon & x_obs_2 <= ds + Lstop + 2*epsilon
        R_collid = 0;
    else
        R_collid = 1;
    end
    reward = R_collid * R_slip;
end
%% stop distance
function Lstop = stop_distance(v_ego, v_obs, a)
    global tau
    brake_percent = 1.3; % 100% + 30%
    v = v_ego - v_obs;
    L_0 = (1/2) * a * tau^2 + v * tau;
    v = v + a * tau;
    L_brake = 0.0042 * v^2 + 0.0386 * v;

    Lstop = L_brake*brake_percent + L_0;
end
%% image read
function [red, green, blue] = image_read(name)
    red = imread(name{1});
    red = imresize(red,1);
    for i = 1:size(red,1)
        for j = 1:size(red,2)
            if red(i,j,1) + red(i,j,2) + red(i,j,3) == 0
                red(i,j,1) = 255;
                red(i,j,2) = 255;
                red(i,j,3) = 255;
            end
        end
    end
    green = imread(name{2});
    green = imresize(green,1);
    for i = 1:size(green,1)
        for j = 1:size(green,2)
            if green(i,j,1) + green(i,j,2) + green(i,j,3) == 0
                green(i,j,1) = 255;
                green(i,j,2) = 255;
                green(i,j,3) = 255;
            end
        end
    end
    blue = imread(name{3});
    blue = imresize(blue,1);
end
