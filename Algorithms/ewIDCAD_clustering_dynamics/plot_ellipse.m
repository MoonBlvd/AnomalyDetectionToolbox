clear;clc;
%raw_data = csvread('../../Benchmarks/Time Series Data/IBRL/IBRL_18_25000-28800_temp_hum.csv');
raw_data = csvread('../../Benchmarks/Time Series Data/Car_Simulation/Car_NormalData_1_6D.csv');

mean0 = csvread('cluster0_mean.csv');
covariance_inv0 = csvread('cluster0_cov_inv.csv');
mean1 = csvread('cluster1_mean.csv');
covariance_inv1 = csvread('cluster1_cov_inv.csv');
mean2 = csvread('cluster2_mean.csv');
covariance_inv2 = csvread('cluster2_cov_inv.csv');

nSigma = 3;
d = 2;
data_d = size(mean1,2)-1;
j = 0;

start = size(raw_data,1)- size(mean0,1);
k1 = 1;
k2 = 1;
k0 = 1;
mu1 = nan;
mu2 = nan;
for i = start: size(mean0,1)
    if find(mean1(:,1)==i)
        mu1 = mean1(k1,2:d+1)';
        cov_inv1 = covariance_inv1(data_d*(k1-1)+1:data_d*(k1-1)+d,1:d);
        k1 = k1+1;
    end
    if find(mean2(:,1)==i)
        mu2 = mean2(k2,2:d+1)';
        cov_inv2 = covariance_inv2(data_d*(k2-1)+1:data_d*(k2-1)+d,1:d);
        k2 = k2+1;
    end
    if find(mean0(:,1)==i)
        mu0 = mean0(k0,2:d+1)';
        cov_inv0 = covariance_inv0(data_d*(k0-1)+1:data_d*(k0-1)+d,1:d);
        k0 = k0+1;
    end
    %mu = mean(i,1:d)';
    %cov_inv = covariance_inv(data_d*(i-1)+1:data_d*(i-1)+d,1:d);
%     [V,D] = eig(cov_inv);
%     lam1 = D(1,1);
%     lam2 = D(2,2);
%     v1 = V(:,1);
%     v2 = V(:,2);
%     if v1(1) == 0
%         theta = deg2rad(90);
%     else
%         theta = atan(v1(2)/v1(1));
%     end
%     
%     a = nSigma*lam1;
%     b = nSigma*lam2;
%     
%     np = 500;
%     angle = [0:500]*2*pi/np;
%     R = [cos(theta),-sin(theta);sin(theta), cos(theta)];
%     pts = [mu(1);mu(2)]*ones(size(angle)) + R*[cos(angle)*a; sin(angle)*b];
    
    if ~isnan(mu2)
        j = j+1;
        plot(raw_data(1:i,1), raw_data(1:i,2),'b*');
        hold on
    
        %plot(pts(1,:), pts(2,:), 'r');
        ellipse(cov_inv0, mu0, [1, 0.2, 0.2]) 
        ellipse(cov_inv1, mu1, [1, 0.2, 0.2])
        ellipse(cov_inv2, mu2, [1, 0.2, 0.2]) 
        %xlim([-5,10]);
        %ylim([-5,10]);
        %xlim([20,70]);
        %ylim([20,45]);
%         F(j) = getframe(gcf);
        %pause(0.5)
        xlabel('lateral pos[m]','FontSize',16);ylabel('lateral vel[m/s]','FontSize',16)
        title(['Time step ',num2str(i)]);
        hold off
    end
end    
% video = VideoWriter('model.avi');
% open(video);
% writeVideo(video, F);
% close(video);