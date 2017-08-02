load anomaly_scores
load sensor_scores
path = '../../../../Nan_Traffic_Simulator/07122017_data/';
id = 1;
label = csvread([path,'anomalous_17D_',num2str(id),'_label.csv']);
truth = find(label == -1);
num_data = length(label);
CP = length(truth); % condition positive (reality)
CN = num_data - CP; % condition negative (reality)

TPR = [];
FPR = [];
for threshold = 1:-0.1:0
    positive = find(anomaly_scores >= threshold);
    P = length(positive);

    TP = 0;
    for i = 1:length(truth)
        idx = find(positive == truth(i));
        if idx
            TP = TP + 1;
        end
    end
    FP = P - TP;

    TPR = [TPR, TP/CP]; % true positive rate, recall, or sensiticity
    FPR = [FPR, FP/CN]; % false positive rate, fall-out, or probability of false alarm
end
plot(FPR, TPR);