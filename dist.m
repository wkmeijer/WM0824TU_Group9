close all;

x = [0:.001:1];
norm = normpdf(x,.70,.05);

figure;
plot(x,norm)