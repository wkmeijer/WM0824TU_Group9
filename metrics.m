filename = 'data_miraibadpackets.csv';
data = readtable(filename);
isps = data( : , 2 );

asn = categorical(table2array(asn));
asn = table(categories(asn),countcats(asn))

asn = sortrows(asn,2,'descend');
asn = asn(1:10, :);

asn_labels = table2array(asn(:, 1))';
asn_values = table2array(asn(:, 2))';

figure('rend','painters','pos',[0 0 1100 600]);
bar(asn_values);
set(gca,'xticklabel',asn_labels);
xlabel(gca, 'Autonomous System Number, 10 most frequent.');
ylabel(gca, 'Number of unique Mirai botnets targeting the ASN.');
saveas(gcf,'frequently.png')