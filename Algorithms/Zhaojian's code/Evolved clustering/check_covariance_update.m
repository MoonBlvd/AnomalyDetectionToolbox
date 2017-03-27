%% 

x=[5 10];
v=[6 8];
w=10;
sigma=10*eye(2);
sigmainv=inv(sigma);

% standard update
Cov1=(w*sigma+(x-v)'*(x-v))/(w+1)

% woodbury update

K=(x-v)'*inv(w+(x-v)*sigmainv*(x-v)')*(x-v);

Cov2=(1+1/w)*sigmainv*(eye(2)-K*sigmainv);
cov2=inv(Cov2)


