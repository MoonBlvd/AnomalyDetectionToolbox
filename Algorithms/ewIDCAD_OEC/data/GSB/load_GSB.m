clear;clc;
data = textread('rawGSB_day_15_25.txt');

date = data(:,4);
temperature = data(:,10);
humidity = data(:,12);
temp = [];
humi = [];
day = [];
for i = 1:5:size(data,1)
    if i+4<size(data,1)
        mean_temp = mean(temperature(i:i+4));
        mean_humi = mean(humidity(i:i+4));
        %if date(i) == date(i+4)
        %    mean_date = date(i);
        %end
    else
        mean_temp = mean(temperature(i:end));
        mean_humi = mean(humidity(i:end));
    end
    mean_date = date(i);
    temp = [temp; mean_temp];
    humi = [humi; mean_humi];
    day = [day; mean_date];
end
csvwrite('GSB_12_Oct_date_temp_humi_mean11111.csv', [day, temp, humi]);
csvwrite('GSB_12_Oct_temp_humi_mea11111n.csv', [temp, humi]);

plot(temp, humi, 'g*');
xlim([-15,30]);
ylim([0,100]);
