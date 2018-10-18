filename = 'data_miraibadpackets.csv';
data = readtable(filename);
isps = data( : , 2 );
unique_isps = size(unique(isps), 1)

dates = table2array(data( : , 5 ));

dates = datetime(dates,'InputFormat','yyyy-MM-dd HH:mm:ss');
low = min(dates);
high = max(dates);
date_bins = low:caldays(14):high;
date_counts = [];

prev = low;
i = 1;
for date = low:caldays(14):high
    date_counts(i) = sum(isbetween(dates,prev,date));
    prev = date;
    i = i+1;
end

nbins = 10;
duration = days(high - low);
avg_infections_isp_year = (size(data, 1) / unique_isps) * (365 / duration)

date_counts = date_counts / unique_isps;
plot(date_counts);

set(gca,'xticklabel', datestr(linspace(low, high, nbins), 'dd/mm/yy'));
ylabel(gca, 'Average number of infections per ISP');
saveas(gcf,'date_counts.png')