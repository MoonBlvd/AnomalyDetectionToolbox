clear;clc;
%raw_data = csvread('../../Benchmarks/Time Series Data/IBRL/IBRL_18_25000-28800_temp_hum.csv');
raw_data = csvread('../../Benchmarks/Time Series Data/Car_Simulation/Car_RollOverData_1_6D.csv');

mean = csvread('new_mean.csv');
covariance = csvread('new_cov.csv');
covariance_inv = csvread('new_cov_inv.csv');
nSigma = 3;
d = 2;
data_d = size(mean,2);

j = 0;

start = size(raw_data,1)- size(mean,1);
for i = 1: size(mean,1)
    mu = mean(i,1:d)';
    cov = covariance(data_d*(i-1)+1:data_d*(i-1)+d,1:d);
    cov_inv = covariance_inv(data_d*(i-1)+1:data_d*(i-1)+d,1:d);
    [V,D] = eig(cov_inv);
    lam1 = D(1,1);
    lam2 = D(2,2);
    v1 = V(:,1);
    v2 = V(:,2);
    if v1(1) == 0
        theta = deg2rad(90);
    else
        theta = atan(v1(2)/v1(1));
    end
    
    a = nSigma*lam1;
    b = nSigma*lam2;
    
    np = 500;
    angle = [0:500]*2*pi/np;
    R = [cos(theta),-sin(theta);sin(theta), cos(theta)];
    pts = [mu(1);mu(2)]*ones(size(angle)) + R*[cos(angle)*a; sin(angle)*b];
    
    %if(mod(i,10)==0)
        j = j+1;
        tmp_img = plot(raw_data(1:i+start,1), raw_data(1:i+start,2),'*');
        xlabel('lateral pos [m]');
        ylabel('lateral vel [m/s]');
        hold on
        %plot(pts(1,:), pts(2,:), 'r');
        ellipse(cov_inv, mu, [1, 0.2, 0.2])
        xlim([-5,10]);
        ylim([-5,10]);
        F(j) = getframe(gcf);
        %xlim([20,70]);
        %ylim([20,45]);
    
        %pause(0.5)
        hold off

    %end
end    
video = VideoWriter('model.avi');
open(video);
writeVideo(video, F);
close(video);