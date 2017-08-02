function score = sensor_check(buf)
    global time_step
    x_thresh = 1; 
    score = 0;
    if size(buf,1) == 1
        return
    end
    % two car scenario
    % check whether a participant disappeared or emerged
    v0_ego =buf(:,3); 
    x_obs = buf(:,4);
    y_obs = buf(:,5);
    v0_obs = buf(:,6);
    x_diff = x_obs(2:end) - x_obs(1:end-1);
    v = v0_obs(1:end-1) - v0_ego(1:end-1);
    
    tmp = x_diff - v*time_step;
    if abs(tmp) > x_thresh
        score = 1;
    end
        
end