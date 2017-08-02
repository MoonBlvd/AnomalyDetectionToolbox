clear;clc;
data = textread('ethylene_CO_5mins.txt');
data(:,2:3) = [];
%data(:,end) = [];
d = 8;
t = size(data,1);
time = 300;

new_data = zeros(t,d);
for i = 1:d
    new_data(:,i) = mean(data(:,2*i:2*i+1),2);
end
mean_data = zeros(time,8);
for i = 1:time
    mean_data(i,:) = mean(new_data((i-1)*100+1:i*100,:));
end
TGS2600 = mean_data(:,2);
TGS2602 = mean_data(:,1);
TGS2610 = mean_data(:,3);
TGS2620 = mean_data(:,4);
time = 1:time;
figure(1);
plot(time, TGS2600,'b');
hold on;
plot(time, TGS2602,'r-');
hold on;
plot(time, TGS2610,'y--');
hold on;
plot(time, TGS2620,'m');
legend('TGS2600','TGS2602','TGS2610','TGS2620');

csvwrite('ethylene_CO_5mins.csv',mean_data);