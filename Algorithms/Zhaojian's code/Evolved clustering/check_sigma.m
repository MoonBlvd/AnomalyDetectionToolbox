
% Generate data points around a certain point

lat=42.292568;
lon=-83.718719;
[X, Y]=sp_proj('2113','forward',lon,lat,'m');

sigma=2*eye(2);
XY=mvnrnd([X Y],sigma,10000);

[Lon, Lat]=sp_proj('2113','inverse',XY(:,1),XY(:,2),'m');
sigma=cov([Lon Lat])
% plot(Lon,Lat,'.b')
% hold on
% sigma=1e-8*[0.3913 0.0031;0.0031 0.2197];
% XY=mvnrnd([lon lat],sigma,10000);
% mu=mean(XY);
% (XY(100,:)-mu)*inv(sigma)*(XY(100,:)-mu)'
% plot(XY(:,1),XY(:,2),'.r')

lat1=42.275824;
lon1=-83.731002;

lat2=42.275873;
lon2=-83.731112;

lat3=42.275905;
lon3=-83.731158;

lat4=42.275848;
lon4=-83.730605;

XY1=mvnrnd([lon1 lat1],sigma,100);
XY2=mvnrnd([lon2 lat2],sigma,100);
XY3=mvnrnd([lon3 lat3],sigma,100);
XY4=mvnrnd([lon4 lat4],sigma,100);

XY=[XY1;XY2;XY3];
Cov=cov(XY);
mu=mean(XY);
[X,Y]=plotGauss_2(mu,Cov,0.95);

Cov1=cov(XY4);
mu1=mean(XY4);
[X1,Y1]=plotGauss_2(mu1,Cov1,0.95);
XY=[XY;XY4];
figure
plot(XY(:,1),XY(:,2),'.b');hold on
plot_google_map

plot(X,Y,'c','LineWidth',2)
plot(X1,Y1,'r','LineWidth',2)
plot([lon1;lon2; lon3; lon4],[lat1;lat2; lat3; lat4],'*r')
plot(mu1(1),mu1(2),'og')
axis off
legend('Anomaly reports','Cluster 1','Cluster 2','True anomalies','Center of cluster 2')