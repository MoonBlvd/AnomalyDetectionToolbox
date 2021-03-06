function [suspicious_index suspicious_score u] = OD_onlinePCA(A, beta)
%
% Outlier detection via over-sampling online PCA
%
% This function is used for outlier detection. The main idea is using 
% the variation of the first principal direction detect the outlierness
% of each instance(event) in the leave one out procedure. Here the 
% over-sampling on target instance is also used for enlarge the 
% outlierness
%
%
% input
%   A: the data matrix, each row represents an instance
%   beta: forgetting factor
%         For example, beta=0.9 means we decrease the influence of previous
%         data by a factor of 0.9
% output
%   suspicious_score: the suspicious score for each instance
%   suspicious_index: the ranking of instances according to their
%                     suspicious score
%                     For example, suspicious_index(i)=j means the ith 
%                     instance is in jth position in the ranking.
%
% References
% Anomaly Detection via Over-Sampling Principal Component Analysis                                                                     
% Send your comment and inquiry to Dr. Yi-Ren Yeh (yirenyeh@gmail.com)        
%

[n p]= size(A);

A_m = mean(A);
d = 0.0001;
u = ones(p,1);
for i = 1:2000
    [u d] = Track_w(A(i,:)-A_m, u, d, 1);
end
u_norm = u/norm(u);

sim_pool = zeros(n,1);
ratio = 1/(n*beta);
%%%------ test some changes
sum_product = zeros(1,p);
sum_squre = 0;
%%%
num_normal = 0;
mu = A_m;
prev_w = u;
prev_w_norm = u_norm;
for i = 2001:n
    %%%----- test some changes
%     if i == 1
%         mu = A_m;
%         temp_mu = mu;
%     else
%         temp_mu = (mu+ratio*A(i,:))/(1+ratio);
%     end
    %%%-----
    x = A(i,:)-mu;%temp_mu;
    %%%------try changes
%     if i>1
%         [w,tmp] = Track_w(x, prev_w, prev_tmp, beta);
        [w,y] = compute_w(x,prev_w,sum_product,sum_squre,beta);
%     else
%         [w,tmp] = Track_w(x, u, 0.0001, beta);
%     end
    prev_w = w;
    %%%-------
%     [w,tmp] = Track_w(x, u, d, beta); 
    w = w/norm(w);
    %%%-------- try changes
    sim_pool(i,:) = abs(diag(prev_w_norm'*w));
%     if sim_pool(i,:) > 0.5 % use new point if similarity greater than 0.5
        sum_product = sum_product + y*x;
        sum_squre = sum_squre + y^2;
        %prev_tmp = tmp;
        mu = (mu*num_normal + A(i,:))/(1+num_normal);
        num_normal = num_normal + 1;
%     else
        prev_tmp = prev_tmp;
%     end
    %%%-------- 
    %sim_pool(i,:) = abs(diag(u'*w));
    if (~mod(i,10000))
        display(['Iteration ',num2str(i)])
    end
    prev_w_norm = w;
end

[non,suspicious_index]=sort(sim_pool);
suspicious_score = 1-sim_pool;



%==========================================================================
function [w,d] = Track_w(x, w, d, beta)
y = x*w;
d = beta*d+y^2; % self.b
e = x'-w*y; % error
w = w + (y*e)/d; % self.u


function [w,y] = compute_w(x,w,sum_product,sum_squre,beta)
y = x*w;
w = (beta*sum_product + y*x)/(beta*sum_squre+y^2);
w = w';

