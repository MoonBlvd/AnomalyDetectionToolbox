clear;clc;
data = csvread('anomalous_2.csv');
fields = readtable('traffic_fields.csv');
fields = fields.Properties.VariableNames;
time_step = 1:size(data,1);
num_sensors = size(data,2);
color = zeros(num_sensors,3);
colors(:,1) = (1:num_sensors)/num_sensors;
colors(:,2) = (num_sensors:-1:1)/num_sensors;
colors(:,3) = (num_sensors:-1:1)/num_sensors;
figure(1)
for i = 1:6
    plot(time_step,data(:,i),'color',colors(i*2,:));
    hold on;
end
legend(fields{1:6});
colors = colors([1,3,5,7,9,11],:);
figure(2)
for i = 7:12
    plot(time_step,data(:,i),'color',colors(i-6,:));
    hold on;
end
legend(fields{7:12});