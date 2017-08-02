
fig = figure(1);
x_ego = 11;y_ego = 11;x_obs = 16;y_obs = 12;
c_ego = [x_ego;y_ego];
c_obs = [x_obs;y_obs];
epsilon = 3; delta = 1;
% rectangle('Position',[x_ego - epsilon, y_ego-delta,2*epsilon,2*delta],...
%                   'EdgeColor','r','LineWidth',2);hold on;
% rectangle('Position',[x_obs - epsilon, y_obs-delta,2*epsilon,2*delta],...
%                   'EdgeColor','c','LineWidth',2);hold on;
% poly1 = [x_ego - epsilon, x_ego + epsilon, x_ego + epsilon, x_ego - epsilon, x_ego - epsilon;...
%          y_ego - delta, y_ego - delta, y_ego + delta, y_ego + delta, y_ego - delta;...
%          1,1,1,1,1];
% poly2 = [x_obs - epsilon, x_obs + epsilon, x_obs + epsilon, x_obs - epsilon, x_obs - epsilon;...
%          y_obs - delta, y_obs - delta, y_obs + delta, y_obs + delta, y_obs - delta;...
%          1,1,1,1,1];

% T1 = [1 0 -x_ego;...
%       0 1 -y_ego;...
%       0 0 1];
% T2 = [1 0 -x_obs;...
%       0 1 -y_obs;...
%       0 0 1];
psi1 = 0:0.1:1;
psi2 = 0:0.1:1;
len = sqrt(delta^2 + epsilon^2);
alpha = atan(delta/epsilon);
for i = 1:10
%     R1 = [cos(psi1(i)), -sin(psi1(i)), 0;...
%           sin(psi1(i)),  cos(psi1(i)), 0;...
%                      0,             0, 1];
    dx1 = cos(psi1(i)+alpha)*len;
    dy1 = sin(psi1(i)+alpha)*len; 
    dx2 = cos(psi1(i)-alpha)*len;
    dy2 = sin(psi1(i)-alpha)*len; 
    clear fig;
    fig = figure(1);
    set(fig, 'Position', [0, 0, 25, 25]);
    poly1 = [x_ego - dx1, x_ego + dx2, x_ego + dx1, x_ego - dx2, x_ego - dx1;...
             y_ego - dy1, y_ego + dy2, y_ego + dy1, y_ego - dy2, y_ego - dy1];
    for j = 1:10
        dx1 = cos(psi2(j)+alpha)*len;
        dy1 = sin(psi2(j)+alpha)*len; 
        dx2 = cos(psi2(j)-alpha)*len;
        dy2 = sin(psi2(j)-alpha)*len;
        poly2 = [x_obs - dx1, x_obs + dx2, x_obs + dx1, x_obs - dx2, x_obs - dx1;...
                 y_obs - dy1, y_obs + dy2, y_obs + dy1, y_obs - dy2, y_obs - dy1];
%         R2 = [cos(psi2(j)), -sin(psi2(j)), 0;...
%               sin(psi2(j)),  cos(psi2(j)), 0;...
%                          0,             0, 1];
%         poly1_new = inv(T1)*R1*T1*poly1;
%         poly2_new = inv(T2)*R2*T2*poly2;
        plot(poly1(1,:), poly1(2,:),'r');hold on;
        plot(poly2(1,:), poly2(2,:),'c');hold on;
    end
end