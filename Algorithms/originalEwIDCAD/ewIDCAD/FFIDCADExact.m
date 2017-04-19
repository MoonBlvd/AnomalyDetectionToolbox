%======================================================
% Author: Masud Moshtaghi
% Created: 2011-03-21
% Calculates one step of recursive formulat update
% 
%=======================================================
function [A,C,wSum,wPowerSum]= FFIDCADExact(PrevA, PrevC,Lambda,wSum,wPowerSum, X)

m2 = Lambda*(wSum^2-wPowerSum)/wSum; % lambda/Chi
PrevA = PrevA/m2; % A_{k-1} = S_{k-1}^{-1}/(lambda/Chi)
wSum=Lambda*wSum+1; % alpha_{k} = lambda * alpha_{k-1} +1
wPowerSum=Lambda^2*wPowerSum+1;% beta_{k} = lambda^2 * beta_{k-1}+1
m1= wSum/(wSum^2-wPowerSum); % Chi = alpha / (alpha^2 - beta)

C = PrevC+(1/wSum)*(X-PrevC); % mean = mean + (x-mean)/alpha
temp1 = 1+(X-C)*PrevA*(X -C)'; % den = (x-mean)^T*A*(x-mean)
num = PrevA*(X-C)'*(X-C)*PrevA;
A = PrevA-((PrevA*(X-C)'*(X-C)*PrevA)/temp1);
A = A/m1;


% C = PrevC+(X-PrevC)/sumlambda;
%     EffectiveN=100;%3*(1/(1-Lambda));
%     MultiplierN = min([MultiplierN EffectiveN]);
%     Shat=(1-Lambda)*((X-C)'*(X-C));
    
        
%     A = (Mplier*PrevA)-((PrevA*(X-PrevC)'*(X-PrevC)*PrevA)/temp1);
%     A = Lambda*PrevA+Shat;
%     A = (MultiplierN-1)*A;
% %     %    C = ((MultiplierN*Lambda*PrevC)+X)/(MultiplierN+1);
%     C = (1-Lambda)*PrevC+Lambda*X;
%     C = PrevC+Lambda*(X-PrevC);
end