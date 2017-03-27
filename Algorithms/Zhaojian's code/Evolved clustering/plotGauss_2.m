function [XX,YY] = plotGauss_2(mu,covar,p,CoLoR)
% Plots bivariate Gaussian contour
% Program by Baruah. P, baruah@wayne.edu July. 2003
% Original by Rowis

if nargin < 4, CoLoR = 'b'; end

t = -pi:0.1:pi;
k = length(t);
x = sin(t);
y = cos(t);

R = covar;
mu_1 = mu(1);
mu_2 = mu(2);
[vv, dd] = eig(R);

A = real((vv * sqrt(dd))');
z = [x' y']*A*sqrt(chi2inv(p,2));
% plot(z(:,1)+mu_1,z(:,2)+mu_2,CoLoR);
XX = z(:,1)+mu_1;
YY = z(:,2)+mu_2;
