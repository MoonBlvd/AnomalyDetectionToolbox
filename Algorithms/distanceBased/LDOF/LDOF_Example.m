function LDOF_Example()
    clear;clc;
    filepath = '../../../benchmarks/Time Series Data/NASA Shuttle Valve Data/unseenSeqs.data.csv';
    data = csvread(filepath);
    k = 10; % k for knn
    ldof_scores = LDOF(data', k);
    ldof_idx = 1:length(ldof_scores);
    plot(ldof_idx, ldof_scores);
    [M, idx] = max(ldof_scores)
    point = 1;
end