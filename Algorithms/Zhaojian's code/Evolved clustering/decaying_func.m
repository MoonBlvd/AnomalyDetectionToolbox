%% Plot for the decaying function

clear all;close all;clc;
T=30;
t=0:1:T;

lambda=0.2:0.2:1;

f=zeros(length(lambda),T+1);

for i=1:1:length(lambda)
    f(i,:)=2.^(-lambda(i)*t);
end

figure,hold on
plot(t,f(1,:));plot(t,f(2,:),'r');plot(t,f(3,:),'c');plot(t,f(4,:),'m');
legend
hold off