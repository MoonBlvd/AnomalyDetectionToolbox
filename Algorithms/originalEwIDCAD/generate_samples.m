% % S1
clear all;clc;
mu = [50,25];
sigma = eye(2);
%sigma = sigma'*sigma;
figure(1)
%subplot(2,2,1);
hold on;
X = [];
noise_idx = [];
for i = 1:20
    %sigma = rand(2);%eye(2);
    %sigma = sigma'*sigma;
    x = mvnrnd(mu,sigma,200);
    Ns = randi(20,1);
    idx = sort(randperm(200, Ns)); % noise index
    x(idx,:) = x(idx,:) + rand(Ns,2)*8-4;
    %noise = x(randperm(200, Ns),:) + rand(Ns,2)*8-4;
    %x(randperm(200, Ns),:) = [];
    %X = [X;x;noise];
    X = [X;x];
    normal_idx = [1:200];
    normal_idx(idx) = []; 
    plot(x(normal_idx,1),x(normal_idx,2),'o');
    plot(x(idx,1), x(idx,2),'+');
    
    idx = idx + 200*(i-1);
    noise_idx = [noise_idx, idx];
    
    mu(1) = mu(1)-2.2;
    mu(2) = mu(2)-1;
end
xlim([0 60]);ylim([0 35]);
xlabel('Feature 1','FontSize', 18);ylabel('Feature 2','FontSize', 18);
leg = legend('Normal Data','Outliers');
set(leg,'FontSize',16);
%title('S1','FontSize', 24)
csvwrite('S1.csv',X);
csvwrite('S1_GT.csv',noise_idx);

% S2
clear all;clc;
mu = [50,25];
sigma = eye(2);
figure(2)
%subplot(2,2,2);
hold on;
X = [];
noise_idx = [];
for i = 1:20
    x = mvnrnd(mu,sigma,200);
    Ns = randi(20,1);
    idx = sort(randperm(200, Ns)); % noise index
    x(idx,:) = x(idx,:) + rand(Ns,2)*16-8;
    X = [X;x];
    normal_idx = [1:200];
    normal_idx(idx) = []; 
    plot(x(normal_idx,1),x(normal_idx,2),'o');
    plot(x(idx,1), x(idx,2),'+');
    idx = idx + 200*(i-1);
    noise_idx = [noise_idx, idx];
    mu(1) = mu(1)-2.2;
    mu(2) = mu(2)-1;
end
xlim([0 60]);ylim([0 35]);
xlabel('Feature 1','FontSize', 18);ylabel('Feature 2','FontSize', 18);
leg = legend('Normal Data','Outliers');
set(leg,'FontSize',16);
csvwrite('S2.csv',X);
csvwrite('S2_GT.csv',noise_idx)

%S3
c = [40,40];
mu = c;
sigma = eye(2);
X = [];
all_noise = mvnrnd(c,sigma,200);
figure(3)
%subplot(2,2,3)
hold on;
R = 20;
noise_idx = [];
for i = 1:10
    theta = (2*pi/10) * i;
    mu = c + R*[cos(theta) sin(theta)];
    x = mvnrnd(mu,sigma,200);
    Ns = randi(20,1); % random from 1:20
    idx = sort(randperm(200, Ns)); % noise index
    x(idx,:) = all_noise(idx,:); % replace normal data with noise
    X = [X;x];
    normal_idx = [1:200];
    normal_idx(idx) = [];
    plot(x(normal_idx,1), x(normal_idx,2),'o');
    plot(x(idx,1), x(idx,2),'+');
    
    idx = idx + 200*(i-1);
    noise_idx = [noise_idx, idx];
end
xlim([10 70]);ylim([15 65]);
xlabel('Feature 1','FontSize', 18);ylabel('Feature 2','FontSize', 18);
leg = legend('Normal Data','Outliers');
set(leg,'FontSize',16);
csvwrite('S3.csv',X);
csvwrite('S3_GT.csv',noise_idx)


%S4
target = gendatb([2000,0]);
target = gendatoc(target);
target_outlier = gendatblockout(target,40);
all = target_outlier;
rotate = [cos(pi/2),-sin(pi/2);sin(pi/2),cos(pi/2)];
figure(4);
%subplot(2,2,4)
hold on;
colors = ['c','m','y','g','r'];
X = zeros(12240,2);
noise_idx = [2001:2040];

for i = 1:5
    target = gendatb([2000,0]);
    for j = 1:i
        target = target*rotate;
    end
    target = gendatoc(target);
    target_outlier = gendatblockout(target,40);
    all = [all;target_outlier];

    tmp_index = [2001:2040] + 2040*i;
    noise_idx = [noise_idx, tmp_index];
    
    scatterd(target,[colors(i),'o']);hold on;
    scatterd(target_outlier(2001:end,:),'b+');hold on;

end
for i = 1:24480
    X(i)=all(i);
end
%figure(5)
%plot(X(:,1),X(:,2),'o');
xlim([-15 15]);ylim([-15 15]);
xlabel('Feature 1','FontSize', 18);ylabel('Feature 2','FontSize', 18);
leg = legend('Normal Data','Outliers');
set(leg,'FontSize',16);
csvwrite('S4.csv',X);
csvwrite('S4_GT.csv',noise_idx)

