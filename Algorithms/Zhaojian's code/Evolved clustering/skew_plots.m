
clear all;close all;clc;

% Plot ellipsoids with skewd orientation

% Initialization
n=8;                % Number of potholes
pot=zeros(n,2);
% cluster 1, 3 true pothole locations
pot(1,:)=[42.296225, -83.711022];
pot(2,:)=[42.296340, -83.710692];
pot(3,:)=[42.296391, -83.710415];

% cluster 2, 2 true pothole locations
pot(4,:)=[42.296450, -83.712202];
pot(5,:)=[42.296374, -83.712221];

% cluster 3, 4 true potholes
pot(6,:)=[42.296890, -83.709296];
pot(7,:)=[42.296991, -83.709353];
pot(8,:)=[42.297064, -83.709383];

% Specify sigma
Sig=1*eye(2);

%% Generate random reports
for i=1:n
XY(i*100-99:i*100,:)=mvnrnd(pot(i,:)*1e5,Sig,100);
end


% Cluster 1
XY1=XY(1:300,:);
Sigma1=cov(XY1);
mu1=mean(XY1);
p=0.98;
[xx1, yy1]=plotGauss_2(mu1,Sigma1,p);

% Cluster 2
XY2=XY(301:500,:);
Sigma2=cov(XY2);
mu2=mean(XY2);
[xx2, yy2]=plotGauss_2(mu2,Sigma2,p);

% Cluster 3
XY3=XY(501:800,:);
Sigma3=cov(XY3);
mu3=mean(XY3);
[xx3, yy3]=plotGauss_2(mu3,Sigma3,p);



%% Plot
hold on
plot(XY(:,2)/1e5,XY(:,1)/1e5,'.b')
%plot(mu(:,2)/1e5,mu(:,1)/1e5,'og','Markersize',3)
plot(pot(:,2),pot(:,1),'*r','MarkerSize',3)
plot_google_map
plot(yy1/1e5,xx1/1e5,'g','LineWidth',2)
plot(yy2/1e5,xx2/1e5,'g','LineWidth',2)
plot(yy3/1e5,xx3/1e5,'g','LineWidth',2)
axis off
legend('Anomaly reports','True anomaly locations','Cluster boundary')
hold off

% Generate random distributions around a true pothole
pot=[42.293543, -83.712571];
XY=mvnrnd(pot*1e5,Sig,300);
Sigma=cov(XY);
mu=mean(XY);
[xx, yy]=plotGauss_2(mu,Sigma,p);
% plot
figure
hold on
plot(XY(:,2)/1e5,XY(:,1)/1e5,'.b')
%plot(mu(:,2)/1e5,mu(:,1)/1e5,'og','Markersize',3)
plot(pot(:,2),pot(:,1),'*r','MarkerSize',4)
plot_google_map
plot(mu(:,2)/1e5,mu(:,1)/1e5,'+g','MarkerSize',4)
plot(yy/1e5,xx/1e5,'c','LineWidth',2)
axis off
legend('Anomaly reports','True anomaly location','Cluster center','Cluster boundary')
hold off



