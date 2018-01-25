x = 0:0.01:20;
y = tanh(0.5 * x);
plot(x,y,'g');hold on
y = tanh(0.2 * x);
plot(x,y,'b')
y = tanh(0.1 * x);
plot(x,y,'r')
legend('\omega=0.5','\omega=0.2','\omega=0.1')
xlabel('D_t','FontSize',16)
ylabel('Probability','FontSize',16)
lgd = legend('\omega=0.5','\omega=0.2','\omega=0.1');
set(lgd,'FontSize',16);