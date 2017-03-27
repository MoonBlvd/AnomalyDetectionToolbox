
%% Generate random reports

function report=generate_reports(lon,lat,Min,Max,day,sigma)

% Generate random reports based on true pothole locations
% lon, lat--true pothole locations
% [Min, Max]--Number of reports range
% day--number of days 

n=size(lon,1);    % number of true anomalies
pot_set=1:1:n;    % pothole ID

% Magnify lon and lat


% report structure
for i=1:1:day
    report(i).num=[];
    report(i).seq=[];
    report(i).GPS=[];
end

% Generate reports
for i=1:1:day
    % random number of reports within [Min Max]
  rng(100)
  report(i).num=round((Max-Min)*rand+Min); 
    % random report sequence 
report(i).seq=randsample(pot_set,report(i).num,1);
  
    for j=1:1:report(i).num
        pot_ind=report(i).seq(j);
        GPS=mvnrnd([lon(pot_ind) lat(pot_ind)],sigma);
         report(i).GPS=[report(i).GPS; GPS];
    end
end
