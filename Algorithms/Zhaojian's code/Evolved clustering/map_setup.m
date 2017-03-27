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

out=[out1;out2;out3;out4];
%figure('units','normalized','outerposition',[0 0 1 1])
plot(pot(:,2),pot(:,1),'*r');
hold on
plot(out(:,1),out(:,2),'^b');
plot_google_map
axis off
legend('True anomalies','False alarms')