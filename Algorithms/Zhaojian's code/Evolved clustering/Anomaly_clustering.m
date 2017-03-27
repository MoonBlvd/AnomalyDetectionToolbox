
%% Anomaly clustering demonstration
clear all;close all;clc;

%% Anomaly locations

% Initialization
n=12;                % Number of potholes
pot=zeros(n,2);
T=5;
alpha=2;
gamma=0.2;
hm=50;

% Anomaly cluster 1, 3 true pothole locations
pot(1,:)=[42.292568, -83.718719];
pot(2,:)=[42.292701, -83.718746];
pot(3,:)=[42.292634, -83.718728];
pot(4,:)=[42.292755, -83.718753];
pot(5,:)=[42.292806, -83.718767];

% cluster 2
pot(6,:)=[42.294977, -83.716797];

% cluster 3
pot(7,:)=[42.293969, -83.715155];

% cluster 4, 3 true potholes
pot(8,:)=[42.291740, -83.712332];
pot(9,:)=[42.291680, -83.712286];
pot(10,:)=[42.291780, -83.712368];

% cluster 5
pot(11,:)=[42.293999, -83.711350];

% cluster 6
pot(12,:)=[42.293146, -83.712632];


% Several outliers (lon first)
out1=[-83.717473,42.292686];
out2=[ -83.712658,42.292178];
out3=[-83.717872,42.292726];
out4=[-83.717668,42.293976];

%% Generate random reports
Min=190;      % Minimum and maximum reports a day
Max=200;

% Generate a sigma based on X-Y plane analysis

lat=42.292568;
lon=-83.718719;
[X, Y]=sp_proj('2113','forward',lon,lat,'m');

sigma=3*eye(2);
XY=mvnrnd([X Y],sigma,10000);

[Lon, Lat]=sp_proj('2113','inverse',XY(:,1),XY(:,2),'m');
sigma=cov([Lon Lat]);


% first five days---cluster 1--5
report1=generate_reports(pot(1:11,2),pot(1:11,1),Min,Max,5,sigma);

% Day 3 and day 5 add some outliers
% report1(3).GPS=[report1(3).GPS;out1;out2];
% N1=size(report1(3).GPS,1);
% N_new=randperm(N1);
% report1(3).GPS=report1(3).GPS(N_new,:)
% 
% report1(5).GPS=[report1(5).GPS;out3;out4];
% N2=size(report1(5).GPS,1);
% N2_new=randperm(N2);
% report1(5).GPS=report1(5).GPS(N2_new,:)

% Each day add 5 false alarms around each of the pothole locations
for i=1:1:5
FA1=mvnrnd(out1,sigma,5);
FA2=mvnrnd(out2,sigma,5);
FA3=mvnrnd(out3,sigma,5);
FA4=mvnrnd(out4,sigma,5);
report1(i).GPS=[report1(i).GPS;FA1;FA2;FA3;FA4];
N1=size(report1(i).GPS,1);
N_new=randperm(N1);
report1(i).GPS=report1(i).GPS(N_new,:);
end


% next 10 days---cluster 1 fixed, add cluster 6
report2=generate_reports(pot([1:7,11:12],2),pot([1:7,11:12],1),Min,Max,10,sigma);

% Each day add 5 false alarms around each of the pothole locations
for i=1:1:10
FA1=mvnrnd(out1,sigma,5);
FA2=mvnrnd(out2,sigma,5);
FA3=mvnrnd(out3,sigma,5);
FA4=mvnrnd(out4,sigma,5);
report2(i).GPS=[report2(i).GPS;FA1;FA2;FA3;FA4];
N1=size(report2(i).GPS,1);
N_new=randperm(N1);
report2(i).GPS=report2(i).GPS(N_new,:);
end

%% Cluster 
% 1. center
% 2. covariance matrix inverse
% 3. time
% 4. weight
% 5. label
clusters(1).c=[];
clusters(1).SigInv=[];
clusters(1).t=[];
clusters(1).w=[];
clusters(1).L=[];

% Animation
XX=[];
YY=[];

%% Plot true potholes and google map
%fig=figure('DeleteFcn',@closefigurefcn);               % Close window to end animation

 for i=1:1:size(pot,1)
marker(i)=plot(pot(i,2),pot(i,1),'*r','MarkerSize',5);hold on;
%Text(i)=text(pot(i,2),pot(i,1),[num2str(i)],'VerticalAlignment','top','FontSize',5,'Color','b'); % Pothole number
 end
 
 % Last cluster not developed
set(marker(12),'Visible','Off')
% set(Text(10),'Visible','Off')
plot_google_map('MapType','terrain','Refresh',1);
set(gca,'XTick',[],'YTick',[])

% empty handles
h1=[];
h2=[];
h3=[];
h4=[];
h5=[];
h6=[];
% Compute the error
Est_center4=zeros(15,2);

% First five days
for i=1:1:5
       
    for j=1:1:size(report1(i).GPS,1)
        
        %% Delete previous plots
         if ishandle(h1)
             delete(h1)
         end
         if ishandle(h2)
            delete(h2)
         end
         
         if ishandle(h3)
            delete(h3)
         end
         
         if ishandle(h4)
             delete(h4)
         end
         
         if ishandle(h5)
             delete(h5)
         end
         if ishandle(h6)
             delete(h6)
         end
        
        XX=[XX report1(i).GPS(j,1)];
        YY=[YY report1(i).GPS(j,2)];
 clusters=cluster_update(clusters,report1(i).GPS(j,:),i);   
% Plots
h1=plot(XX,YY,'.'); % plot reports
h2=plot(report1(i).GPS(j,1),report1(i).GPS(j,2),'xr','MarkerSize',7);
h3=title(['Day ',num2str(i),],'FontSize',15,'FontWeight','bold');



% Plot cluster
for k=1:1:size(clusters,2)
    [x,y]=plotGauss_2(clusters(k).c,inv(clusters(k).SigInv),0.95);
    if clusters(k).L==0
    h4(k)=plot(x,y,'k','linewidth',1);                   
    h5(k)=plot(clusters(k).c(1),clusters(k).c(2),'og');%hold on;
    elseif clusters(k).L==1
    h4(k)=plot(x,y,'r','linewidth',2);                   
    h5(k)=plot(clusters(k).c(1),clusters(k).c(2),'og');%hold on;

    end
    
    if clusters(k).L~=2                                                                          
                 h6(k)=text(clusters(k).c(1),clusters(k).c(2),...
           {'\color{red} \it' [' W=',num2str(round(clusters(k).w*alpha^(-gamma) * 100)/100)]},'VerticalAlignment','bottom','FontSize',10); 
    end
end
pause(0.01)
    end
    % Update the weights and delete outliers
    for j=1:1:size(clusters,2)
        clusters(j).w=clusters(j).w*alpha^(-gamma);
        if clusters(j).L==1 && clusters(j).w<hm
            clusters(j).L=0;
            clusters(j).t=i;
        elseif clusters(j).L==0 && i-clusters(j).t>=T
             clusters(j).L=2;
        end
    end
    Est_center4(i,:)=clusters(4).c;
 if i==1 || i==5
     pause
 end

end


%% Next 10 days cluster 1 fixed, cluster 2
 set(marker(12),'Visible','On')
 set(marker(8:10),'Visible','Off')
 
for i=6:1:15
    for j=1:1:size(report2(i-5).GPS,1)
        
        %% Delete previous plots
      
        if ishandle(h1)
             delete(h1)
         end
         if ishandle(h2)
            delete(h2)
         end
         
         if ishandle(h3)
            delete(h3)
         end
         
         if ishandle(h4)
             delete(h4)
         end
         
         if ishandle(h5)
             delete(h5)
         end
         if ishandle(h6)
             delete(h6)
         end

        
        XX=[XX report2(i-5).GPS(j,1)];
        YY=[YY report2(i-5).GPS(j,2)];
 clusters=cluster_update(clusters,report2(i-5).GPS(j,:),i);   
% Plots
h1=plot(XX,YY,'.'); % plot reports
h2=plot(report2(i-5).GPS(j,1),report2(i-5).GPS(j,2),'xr','MarkerSize',7);
h3=title(['Day ',num2str(i),],'FontSize',15,'FontWeight','bold');
% Plot cluster
for k=1:1:size(clusters,2)
    [x,y]=plotGauss_2(clusters(k).c,inv(clusters(k).SigInv),0.95);
    if clusters(k).L==0
    h4(k)=plot(x,y,'k','linewidth',1);                   
    h5(k)=plot(clusters(k).c(1),clusters(k).c(2),'og');
    elseif clusters(k).L==1
    h4(k)=plot(x,y,'r','linewidth',2);                   
    h5(k)=plot(clusters(k).c(1),clusters(k).c(2),'og');
        else
            h4(k)=plot(x,y,'r','linewidth',2);                   
    h5(k)=plot(clusters(k).c(1),clusters(k).c(2),'og');%hold on;
    set(h4(k),'Visible','Off')
     set(h5(k),'Visible','Off')
    end
    
                                                                          
      h6(k)=text(clusters(k).c(1),clusters(k).c(2),...
     {'\color{red} \it' [' W=',num2str(round(clusters(k).w * 100)/100)]},'VerticalAlignment','bottom','FontSize',10); 
    if clusters(k).L==2      
     set(h6(k),'Visible','Off')
    end
end
pause(0.01)
    end
    % Update the weights and delete outliers
    for j=1:1:size(clusters,2)
        clusters(j).w=clusters(j).w*alpha^(-gamma);
        if clusters(j).L==1 && clusters(j).w<hm
            clusters(j).L=0;
            clusters(j).t=i;
        elseif clusters(j).L==0 && i-clusters(j).t>=T
             clusters(j).L=2;
        end
    end
    Est_center4(i,:)=clusters(4).c;
    if i==10 || i==15
        pause
    end
end

%% Plot cluster  center convergence
figure('units','normalized','outerposition',[0 0 1 1])

plot(Est_center4(:,1),Est_center4(:,2)),hold on
plot(Est_center4(end,1),Est_center4(end,2),'o'),hold on
plot(pot(6,2),pot(6,1),'r*')
plot(pot(5,2),pot(5,1),'r*')
plot_google_map

format long
[X1, Y1]=sp_proj('2113','forward',Est_center4(:,2),Est_center4(:,1),'m');
[X2, Y2]=sp_proj('2113','forward',pot(6,1),pot(6,2),'m');
dist=sqrt((X1-X2).^2+(Y1-Y2).^2);
figure('units','normalized','outerposition',[0 0 1 1])
plot(dist)