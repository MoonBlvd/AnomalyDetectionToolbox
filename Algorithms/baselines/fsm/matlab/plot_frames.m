function plot_frames(anomalies)

    n_lane = 3;
    w_lane = 3.6;
    l_car = 6; % car length
    w_car = 2; % car width

    for j = 1:size(anomalies,1)
        anomaly = anomalies(j,:);

        %anomaly = data(j,:);

        x_host = 0;
        y_host = anomaly(1);
        %x_others = anomaly(2:6);
        %x_others = anomaly([3,6,9,12,15,18,21,24,27,30]);
        x_others = anomaly([3,6,9,12,15]);

        %y_others = anomaly(13:end);
        %y_others = anomaly([4,7,10,13,16,19,22,25,28,31]);
        y_others = anomaly([4,7,10,13,16]);
        
        fig=figure(1);clf(fig);hold on
        plot_range = [x_host-50 x_host+100];
        for(lane=0:n_lane)
            plot(plot_range,plot_range.*0+lane*w_lane,'k-');
        end
        %     h1 = plot(x_others,y_others,'ro','MarkerSize',16);
        %     set(h1,'MarkerEdgeColor','none','MarkerFaceColor','r');
%         colors = ((0:15:155)/255)';
%         colors = [colors,((255:-25:0)/255)'];
%         colors = [colors,((100:15:255)/255)'];
        colors = {'g','b','c','m','y','g','b','c','m','y'};
        for(i=1:length(x_others))
            if isnan(y_others(i))
                continue;
            else
                if i > 5
                    rectangle('Position',[x_others(i)-l_car/2,y_others(i)-w_car/2,l_car,w_car],'EdgeColor',colors{i},'LineWidth',2);%,'FaceColor','r');
                else
                    rectangle('Position',[x_others(i)-l_car/2,y_others(i)-w_car/2,l_car,w_car],'EdgeColor',colors{i},'FaceColor',colors{i});
                end
            end
        end
        %     h2 = plot(x_host,y_host,'bo','MarkerSize',16);
        %     set(h2,'MarkerEdgeColor','none','MarkerFaceColor','b');
        rectangle('Position',[x_host-l_car/2,y_host-w_car/2,l_car,w_car],'EdgeColor','r','FaceColor','r')
        title(['Frame ',num2str(j)]);
        xlim([x_host-50 x_host+100])
        ylim([0-10 3*w_lane+10])
        %F(j) = getframe(gcf);
        %saveas(gcf,['anomalous_exp_', num2str(j),'.png']);
        set(fig, 'Position', [100, 100, 1000, 250]);
        set(gca,'fontsize',18);
        pause(1)
    end
end