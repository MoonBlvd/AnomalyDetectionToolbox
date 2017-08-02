clear;clc;
%raw_data = csvread('../../Benchmarks/Time Series Data/IBRL/IBRL_18_25000-28800_temp_hum.csv');
%raw_data = csvread('../../Benchmarks/Time Series Data/Car_Simulation/Car_RollOverData_1_6D.csv');
raw_data = csvread('../../Benchmarks/Time Series Data/LG/LG_18_Oct_temp_humi_mean.csv');
%raw_data = csvread('../../Benchmarks/Time Series Data/GSB/GSB_12_Oct_temp_humi_mean.csv');

mean1 = csvread('LG_ewIDCAD_mean.csv');
covariance_inv1 = csvread('LG_ewIDCAD_cov_inv.csv');
%mean2 = csvread('LG_IDCAD_mean.csv');
%covariance_inv2 = csvread('LG_IDCAD_cov_inv.csv');
mean2 = csvread('LG_ffIDCAD_mean.csv');
covariance_inv2 = csvread('LG_ffIDCAD_cov_inv.csv');

nSigma = 3;
d = 2;
data_d = size(mean1,2);

j = 0;

start = size(raw_data,1)- size(mean1,1);
for i = 1: size(mean1,1)
    mu1 = mean1(i,1:d)';
    cov_inv1 = covariance_inv1(data_d*(i-1)+1:data_d*(i-1)+d,1:d);
    mu2 = mean2(i,1:d)';
    cov_inv2 = covariance_inv2(data_d*(i-1)+1:data_d*(i-1)+d,1:d);
    %if(~mod(i,100))
    if i == 97 || i == 997 || i ==2771
        j = j+1;
        tmp_img = plot(raw_data(1:i+start,1), raw_data(1:i+start,2),'o','MarkerEdgeColor',[0.2,0.2,1]);
        xlabel('Feature\_1','FontSize',16);
        ylabel('Feature\_2','FontSize',16);
        hold on
        %plot(pts(1,:), pts(2,:), 'r');
        ellipse(cov_inv1, mu1, [0.2, 1, 0.2]);
        ellipse(cov_inv2, mu2, [1, 0.2, 0.2]);
        xlim([-15,15]);
        ylim([5,100]);
        %F(j) = getframe(gcf);
%         F(j) = getframe(gcf);
        %xlim([20,70]);
        %ylim([20,45]);
        %title(['Time step ',num2str(i)]);
        %set(gca,'fontsize',20)
        %pause(0.5)
        lgd = legend('Time-series','ewIDCAD','IDCAD');
        set(lgd,'FontSize',16);
        hold off
        pause(0.5)
    end
end    
% video = VideoWriter('model.avi');
% open(video);
% writeVideo(video, F);
% close(video);
