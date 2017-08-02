clear;clc;
load data
%IBRL18=csvread('../../../Benchmarks/Time Series Data/IBRL/IBRL_18_25000-28800_temp_hum.csv');
GSB12=csvread('../../../Benchmarks/Time Series Data/GSB/GSB_12_Oct_temp_humi_mean.csv');
%GSB12=csvread('../../../Benchmarks/Time Series Data/S2/S2.csv');
% anomalyID = [11,56,116,167,177,178,179,199];
% normalID = [1:200];
% normalID(anomalyID) = [];
% plot(GSB12(anomalyID,1), GSB12(anomalyID,2),'ro');hold on;
% plot(GSB12(normalID,1), GSB12(normalID,2),'bo');
% xlim([0,60]);ylim([0,35]);




D=2;
Ts=0.98; % gamma
Threshold1 = chi2inv(Ts,D);
Isplot=0;
Reduced = GSB12;%IBRL18;%LG18;

%Reduced1 = [[0:0.1:30]', rand(301,1)];
%Reduced2 = [31*ones(1000,1), rand(1000,1)];%+rand(1000,1)/2-1
%Reduced = [Reduced1;Reduced2];
plot(Reduced(:,1), Reduced(:,2),'*');
n=size(Reduced,1);
firstinitdepth=D+1;
stabilization=10;
Lambda=0.95;
TrackerA=1*eye(D); % init 
TrackerC=mean(Reduced(1:firstinitdepth,1:D)); % init mean

AnomalyIndex3=nan(n,1);
TrackerMult=D+1;
wSum=D;
wPowerSum=D;
Anomalies1=[];
InaRow1=0; % counter for consequtive anomalies
CA=5; % Threshold for consequent anomalies to consider anomaly significant

for i=firstinitdepth+1:1:n
     mahaldist=(Reduced(i,1:D)-TrackerC)*TrackerA*(Reduced(i,1:D)-TrackerC)';
     if(mahaldist>Threshold1) % if distance > chi2
         if(i>stabilization)
             Anomalies1=[Anomalies1;Reduced(i,:)];
             InaRow1 = InaRow1+1;
         end
    else
        InaRow1=0;
    end
    if(InaRow1>CA)
            AnomalyIndex3(i)=1; % Significant changes
    end
    x = Reduced(i,1:D);
     [TrackerA,TrackerC,wSum,wPowerSum]= FFIDCADExact(TrackerA, TrackerC,Lambda,wSum,wPowerSum, Reduced(i,1:D));
    %if isnan(TrackerC(1))
    %    break;
    %end
    if(Isplot==1)
         if(mod(i,100)==0)
            plot(Reduced(1:i,1),Reduced(1:i,2),'b.','MarkerSize',6);
            hold on;
            Ellipse_Plot(TrackerA/Threshold1, TrackerC,[0.2 0.6 0.1]);
            pause(0.5);
            close all;
         end
    end
    if i == 584
        tawd = 213;
    end
end

plot([1:size(Reduced,1)], Reduced(:,1),'g*');hold on;
plot([1:size(Reduced,1)], Reduced(:,2),'g*');hold on;
plot(find(AnomalyIndex3==1), Reduced(find(AnomalyIndex3==1),1),'ro'); hold on;
plot(find(AnomalyIndex3==1), Reduced(find(AnomalyIndex3==1),2),'ro'); hold on;
INDEX = find(AnomalyIndex3 == 1);

figure(2)
plot(Reduced(:,1),Reduced(:,2),'go');hold on;
plot(Anomalies1(:,1), Anomalies1(:,2),'ro');
