function PCA_Example()
    clear;clc;
    %file_path = '../../../benchmarks/Time Series Data/NASA Shuttle Valve Data/unseenSeqs.data.csv';
    %filepath = '../../../Nan_Traffic_Simulator/05172017_data/anomalous_17D_1.csv'
    %file_path = '../../../../Advanced_car_anomaly_detection/data/05182017_IMU_data_7D.csv';
    % roll	pitch	P	Q	R	v_vertical	accel_z
    file_path = '../../../../Advanced_car_anomaly_detection/data/05182017_IMU_data_14D.csv';
    % lat	long	roll	pitch	yaw	P	Q	R	v_north	v_east	v_vertical	accel_x	accel_y	accel_z
    data = csvread(file_path);
    mean_data = mean(data);
    var_data = var(data);
    
    figure(1)
    plot(1:size(data,1),data(:,14));
    
    window_size = 10;
    for i = 1:size(data,1)-window_size
        var_accel_y(i) = var(data(i:i+window_size-1,14));
        mean_accek_y(i) = mean(data(i:i+window_size-1,14));
    end
    figure(2)
    plot(1:i,var_accel_y)
    figure(3)
    plot(1:i,mean_accek_y)
    
    data = (data-mean_data)./repmat(var_data,size(data,1),1);
    
    figure(4)
    plot(1:size(data,1),data(:,14))
    
    window_size = 10;
    for i = 1:size(data,1)-window_size
        new_var_accel_y(i) = var(data(i:i+window_size-1,14));
        new_mean_accek_y(i) = mean(data(i:i+window_size-1,14));
    end
    figure(5)
    plot(1:i,new_var_accel_y)
%     max_data = [];
%     for i = 1:size(data,2)
%         MAX = max(data(:,i));
%         if max(data(:,i)) < 0
%             MAX = min(data(:,i)) ;    
%         end
%         max_data = [max_data MAX];
%     end
    %max_data
    %data = data(29:27628,:);
    %data(:,7) = data(:,7)/mean;
    
    %data = data./repmat(max_data,size(data,1),1);
    
    %data = data';
    n = size(data,1);
    r = 0.01;
    beta = 1/(r*n);
%     beta = 0.6; 
%     [index, pca_scores, u] = OD_onlinePCA(data, beta);
    [index, pca_scores, u] = osPCA(data, beta);
    %pca_scores(find(pca_scores>0.4e-7)) = 0.4e-7;
    
    pca_idx = 1:length(pca_scores);
    figure(1);
    plot(pca_idx, pca_scores);
    [M, idx] = max(pca_scores);
    anomalous_frame = find(pca_scores> 0.4e-6);
%     ratio = 0.5;
%     wpca_scores = OD_wpca(data', ratio);
%     wpca_idx = 1:length(wpca_scores);
%     figure(2)
%     plot(wpca_idx, wpca_scores);
%     [M, idx] = max(wpca_scores);
%     point = 1;
    csvwrite('IMU_score_pca_0.01.csv',pca_scores)
end