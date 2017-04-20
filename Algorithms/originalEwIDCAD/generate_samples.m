% % S1
clear all;clc;
mu = [50,25];
sigma = eye(2);
%sigma = sigma'*sigma;
figure(1)
hold on;
X = [];
for i = 1:20
    %sigma = rand(2);%eye(2);
    %sigma = sigma'*sigma;
    x = mvnrnd(mu,sigma,200);
    Ns = randi(20,1);
    noise = x(randperm(200, Ns),:) + rand(Ns,2)*8-4;
    x(randperm(200, Ns),:) = [];
    X = [X;x;noise];
    plot(x(:,1),x(:,2),'o');
    plot(noise(:,1), noise(:,2),'+');
    mu(1) = mu(1)-2.2;
    mu(2) = mu(2)-1;
end
xlim([0 60]);ylim([0 35]);
csvwrite('S1.csv',X);

% % S2
% clear all;clc;
% mu = [50,25];
% sigma = eye(2);
% figure(2)
% hold on;
% X = [];
% for i = 1:20
%     x = mvnrnd(mu,sigma,200);
%     Ns = randi(20,1);
%     noise = x(randperm(200, Ns),:) + rand(Ns,2)*16-8;
%     x(randperm(200, Ns),:) = [];
%     X = [X;x;noise];
%     plot(x(:,1),x(:,2),'o');
%     plot(noise(:,1), noise(:,2),'+');
%     mu(1) = mu(1)-2.2;
%     mu(2) = mu(2)-1;
% end
% xlim([0 60]);ylim([0 35]);
% %csvwrite('S2.csv',X);
% 
% %S3
% c = [40,40];
% mu = c;
% sigma = eye(2);
% X = [];
% all_noise = mvnrnd(c,sigma,200);
% figure(3)
% hold on;
% R = 20;
% for i = 1:10
%     theta = (2*pi/10) * i;
%     mu = c + R*[cos(theta) sin(theta)];
%     x = mvnrnd(mu,sigma,200);
%     Ns = randi(20,1);
%     x(randperm(200, Ns),:) = [];
%     noise = all_noise(randperm(200, Ns),:);
%     X = [X;x;noise];
%     Ns = randi(20,1);
%     %x(randperm(200, Ns),:)
%     plot(x(:,1), x(:,2),'o');
%     plot(noise(:,1), noise(:,2),'+');
%     good = 1;
% end
% %csvwrite('S3.csv',X);

% %S4
% target = gendatb([2000,0]);
% target = gendatoc(target);
% target_outlier = gendatblockout(target,40);
% all = target_outlier;
% rotate = [cos(pi/2),-sin(pi/2);sin(pi/2),cos(pi/2)];
% figure(4);
% hold on;
% colors = ['c','m','y','g','r'];
% X = zeros(12240,2);
% for i = 1:5
%     target = gendatb([2000,0]);
%     for j = 1:i
%         target = target*rotate;
%     end
%     target = gendatoc(target);
%     target_outlier = gendatblockout(target,40);
%     all = [all;target_outlier];
%     scatterd(target,[colors(i),'o']);hold on;
%     scatterd(target_outlier(2001:end,:),'b+');hold on;
% 
% end
% for i = 1:24480
%     X(i)=all(i);
% end
% figure(5)
% plot(X(:,1),X(:,2),'o');
% csvwrite('S4.csv',X);


