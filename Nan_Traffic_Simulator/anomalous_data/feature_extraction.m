clear;clc;
data = csvread('anomalous_2.csv');

range = 1:size(data,1);

y = data(:,1);
x_FL = data(:,2);
x_RL = data(:,5);
x_FR = data(:,4);
x_RR = data(:,6);

f_1 = exp(y-4.5)./(x_FL.*x_RL+1);
f_2 = exp(4.5-y)./(x_FR.*x_RR+1);

figure(1)
subplot(2,1,1)
plot(range, f_1);
subplot(2,1,2)
plot(range, f_2);

features = [f_1 f_2];
csvwrite('features.csv', features);

