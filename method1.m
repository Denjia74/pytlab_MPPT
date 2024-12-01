function [I, V, P, Rs, Rp, ideality_coef, T, G, Pmax_m, error] = method1(G, T, Vocn, Vmp, Imp, Iscn, Ki, Kv, Ns)
k = 1.3806503e-23;
q = 1.60217646e-19;

G = double(G);
T = double(T) + 273.15;
Tn = 25 + 273.15;
Gn = 1000;

Vocn = double(Vocn);
Iscn = double(Iscn);
Vmp = double(Vmp);
Imp = double(Imp);
Pmax_e = Vmp * Imp;
Ki = double(Ki);
%Kv = double(Kv);
Ns = double(Ns);

algorithm_speed = 0.001;
model_prec = 0.0001;
plot_points = 100;
max_cycle_number = 500000;
isDebugging = 0;

Rs_max = (Vocn - Vmp) / Imp;
Rp_min = Vmp / (Iscn - Imp) - Rs_max;
Rs = 0;
Rp = Rp_min;
Vt  = k * T  / q; 

error = Inf;
cycle_index = 0;
ideality_coef = 1;

while (error > model_prec) && (Rp > 0) && (cycle_index < max_cycle_number)
    cycle_index = cycle_index + 1;
    
    delta_T_Tn = T-Tn;
    nominal_Ipv = (Rs + Rp) / Rp * Iscn; 
    actual_Ipv = (nominal_Ipv + Ki * delta_T_Tn) * G / Gn;
    actual_Isc = (Iscn + Ki * delta_T_Tn) * G / Gn;
    
    Ion = (actual_Ipv - Vocn / Rp) / (exp(Vocn / Vt / ideality_coef / Ns) - 1);
    Io = Ion;
    
    Rs  = Rs + algorithm_speed;
    Rp_ = Rp;
    Rp = Vmp * (Vmp + Imp * Rs) / (Vmp * actual_Ipv - Vmp * Io * exp((Vmp + Imp * Rs) / Vt / Ns / ideality_coef) + Vmp * Io - Pmax_e);

    clear V
    clear I
    
    V_step = Vocn / plot_points;
    V = 0:V_step:Vocn;
    I = zeros(1, size(V, 2));
    options = optimoptions('fsolve', 'Display', 'none');

    for j = 1:size(V, 2)

        current_eq = @(I_j) actual_Ipv ...
            - Io * (exp((V(j) + I_j * Rs) / (Vt * Ns * ideality_coef)) - 1) ...
            - (V(j) + I_j * Rs) / Rp - I_j;

        I(j) = fsolve(current_eq, I(j), options);
    end

    
    if (isDebugging)
        figure(1)
        grid on
        hold on
        title('I-V curve - Adjusting Rs and Rp');
        xlabel('V [V]');
        ylabel('I [A]');
        xlim([0 Vocn]);
        ylim([0 Iscn]);
        plot(V,I,'LineWidth',2,'Color','k')
        plot([0 Vmp Vocn],[Iscn Imp 0],'o','LineWidth',2,'MarkerSize',5,'Color','k')
        
        figure(2)
        grid on
        hold on
        title('P-V curve - Adjusting peak power');
        xlabel('V [V]');
        ylabel('P [W]');
        xlim([0 Vocn])
        ylim([0 Vmp*Imp]);
    end
    
    P = (actual_Ipv-Io*(exp((V+I.*Rs)/Vt/Ns/ideality_coef)-1)-(V+I.*Rs)/Rp).*V;
    Pmax_m = max(P);
    error = (Pmax_m-Pmax_e);
    
    if (isDebugging)
        plot(V,P,'LineWidth',2,'Color','k')
        plot([0 Vmp Vocn],[0 Vmp*Imp 0],'o','LineWidth',2,'MarkerSize',5,'Color','k')
    end
end

if (Rp < 0) Rp = Rp_
end

figure(3)
grid on
hold on
title('Adjusted I-V curve');
xlabel('V [V]');
ylabel('I [A]');
xlim([0 max(V) * 1.1]);
ylim([0 max(I) * 1.1]);
plot(V,I,'LineWidth',2,'Color','k') 
plot([0 Vmp Vocn ],[Iscn Imp 0 ],'o','LineWidth',2,'MarkerSize',5,'Color','k')

figure(4)
grid on
hold on
title('Adjusted P-V curve');
xlabel('V [V]');
ylabel('P [W]');
xlim([0 Vocn * 1.1]);
ylim([0 Vmp * Imp * 1.1]);
plot(V,P,'LineWidth',2,'Color','k') 
plot([0 Vmp Vocn ],[0 Pmax_e 0 ],'o','LineWidth',2,'MarkerSize',5,'Color','k')

disp(sprintf('Complete model\n'));
disp(sprintf('     Rp = %f',Rp));
disp(sprintf('     Rs = %f',Rs));
disp(sprintf('      a = %f',ideality_coef));
disp(sprintf('      T = %f',T-273.15));
disp(sprintf('      G = %f',G));
disp(sprintf(' Pmax,m = %f  (model)',Pmax_m));
disp(sprintf(' Pmax,e = %f  (experimental)',Pmax_e));
disp(sprintf('    tol = %f',model_prec));
disp(sprintf('P_error = %f',error));
disp(sprintf('    Ipv = %f',actual_Ipv));
disp(sprintf('    Isc = %f',actual_Isc));
disp(sprintf('    Ion = %g',Ion));
disp(sprintf('\n\n'));

end
