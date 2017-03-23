clear;clc;
load data
IBRL18=csvread('../../../Benchmarks/Time Series Data/IBRL/IBRL_18_25000-28800_temp_hum.csv');
D=2;
Ts=0.98;
Threshold1 = chi2inv(Ts,D);
Isplot=1;
Reduced = IBRL18;%LG12;%
n=size(Reduced,1);
firstinitdepth=D+1;
stabilization=10;
Lambda=0.95;
TrackerA=1*eye(D);
TrackerC=mean(Reduced(1:firstinitdepth,1:D));

AnomalyIndex3=nan(n,1);
TrackerMult=D+1;
wSum=D;
wPowerSum=D;
Anomalies1=[];
InaRow1=0;
CA=5; % Threshold for consequent anomalies to consider anomaly significant

for i=firstinitdepth+1:1:n
     mahaldist=(Reduced(i,1:D)-TrackerC)*TrackerA*(Reduced(i,1:D)-TrackerC)';
     if(mahaldist>Threshold1)
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
     [TrackerA,TrackerC,wSum,wPowerSum]= FFIDCADExact(TrackerA, TrackerC,Lambda,wSum,wPowerSum, Reduced(i,1:D));
    if(Isplot==1)
         if(mod(i,100)==0)
            plot(Reduced(1:i,1),Reduced(1:i,2),'b.','MarkerSize',6);
            hold on;
            Ellipse_Plot(TrackerA/Threshold1, TrackerC,[0.2 0.6 0.1]);
            pause(0.5);
            close all;
         end
    end
end