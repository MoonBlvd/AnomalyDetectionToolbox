function PCA_Example()
    clear;clc;
    filepath = '../../../benchmarks/Time Series Data/NASA Shuttle Valve Data/unseenSeqs.data.csv';
    data = csvread(filepath);
    beta = 0.9; % k for knn
    pca_scores = OD_onlinePCA(data', beta);
    pca_idx = 1:length(pca_scores);
    figure(1);
    plot(pca_idx, pca_scores);
    [M, idx] = max(pca_scores)
    
    ratio = 0.5;
    wpca_scores = OD_wpca(data', ratio);
    wpca_idx = 1:length(wpca_scores);
    figure(2)
    plot(wpca_idx, wpca_scores);
    [M, idx] = max(wpca_scores);
    point = 1;
end