%% Function to update the clusters with new reports
function cluster_new=cluster_update(cluster_old,report,day)

% Chi-square threshold
prob=.9973;
%prob=0.9545;
%prob=0.8;
% Forgetting factor
p=2;
% chi-square threshold in p dimension with prob
chi2_score_p = chi2inv(prob,p);
%chi2_score_p=40;
% parameter to become an main cluster
ho=80;

% parameter to initialize the inverse covariance matrix
gamma=1e8;


n=size(cluster_old,2);      % cluster numbers

if n==1   % check whether the cluster is empty
    if isempty(cluster_old(n).c)
       cluster_old(n).w=1;
       cluster_old(n).c=report;
       cluster_old(n).SigInv=gamma*eye(2);
       cluster_old(n).t=day;
       cluster_old(n).L=0;
   
    cluster_new=cluster_old;
    return 
    end
end


% Find the cluster with minimum Mahalanobis to the new report
Mah_Dist=zeros(1,n);
for i=1:n
    Mah_Dist(i)=(cluster_old(i).c-report)*cluster_old(i).SigInv*(cluster_old(i).c-report)';
end

[Min_dist, Min_ind]=min(Mah_Dist);
    
% short notations
    w=cluster_old(Min_ind).w;
    v=cluster_old(Min_ind).c;
    x=report;
    S=cluster_old(Min_ind).SigInv;
% check if the minimum distance is smaller than the bound
if Min_dist<chi2_score_p    % within the bound
    % Update the covariance inverse
    K=(x-v)'*(w+(x-v)*S*(x-v)')^(-1)*(x-v);

    cluster_old(Min_ind).SigInv=(1+1/w)*S*(eye(2)-K*S);

    % Update the center
   cluster_old(Min_ind).c=(w*v+x)/(w+1);
   
    % Update the weight
    cluster_old(Min_ind).w=w+1;
    
    % check the weight if an outlier becomes an main cluster
    if cluster_old(Min_ind).L==0 && cluster_old(Min_ind).w>ho
        cluster_old(Min_ind).L=1;
    end
    
else 
    % create a new cluster
    cluster_old(n+1).w=1;
    cluster_old(n+1).c=x;
    cluster_old(n+1).SigInv=gamma*eye(2);
    cluster_old(n+1).t=day;
    cluster_old(n+1).L=0;
end

cluster_new=cluster_old;
return
    
    
    