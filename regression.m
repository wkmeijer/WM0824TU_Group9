

slash = filesep();
SETTINGS.slash = slash;
if ~isdeployed
  addpath(genpath([cd, slash, 'ReportLib']));
  addpath(genpath([cd, slash, 'KyosLib']));
  addpath(genpath([cd, slash, 'Data']))
  addpath(genpath([cd, slash, 'ReportLib',slash,'SwingVolumeTool']))
  addpath(genpath([cd, slash, 'ReportLib',slash,'KyPositionTool']))  
end

% IP_Address	Autonomous_System	Country	ASN	Date_First_Seen	isp

[ ColNames11,ColNames12,MatrElements11,MatrElements12] = ReadFileTableMixedValues('data_maraibadpackets_isp_reduced.csv',[1:6]);

[ ColNames21,ColNames22,MatrElements21,MatrElements22] = ReadFileTableMixedValues('names_sec_index.csv',[1:2]);



UniqISP = unique (MatrElements12(:,6));

for ii = 1: size(UniqISP,1)
    [ind,ind1]=ismember(MatrElements12(:,6), UniqISP(ii,1));
    first_ind = find(ind1);    
    UniqISP(ii,2) = MatrElements12(first_ind(1),3);
    NbISP(ii,1) = sum(ind1);
end

% UniqISP - name of the ISP and the country 

% get the corresponding IPS and fill in 
% NbISP -> 1. total new infections 2. size	3. GNI_pc_2017	4.internet_privacy_index	5.rank


for ii = 1: size(UniqISP,1)
    [ind,ind1]=ismember(MatrElements22(:,1), UniqISP(ii,1));
%    [ind,ind1]=ismember( UniqISP(ii,1), MatrElements22(:,1));
    if sum(ind)
        NbISP(ii,2:5) = MatrElements21(find(ind1),:);
    end 
end


% discard the elements with 0 size
ind_dis = NbISP(:,2)==0;

NbISP1= NbISP(~ind_dis,:);
UniqISP1 = UniqISP(~ind_dis,:);
% create the regression line # new infections = b*security_index + a
y1(:,1) = (NbISP1(:,1)./NbISP1(:,2)) * 100;
y11 = mean(y1(:,1));
y1_min_mean = y1(:,1)-y11;

ind_y = y1_min_mean > 20*y11;
if sum(ind_y)    
    NbISP1 = NbISP1(~ind_y,:);
    UniqISP1 = UniqISP1(~ind_y,:);

    y1 = y1(~ind_y,1);
    y11 = mean(y1(:,1));
    y1_min_mean = y1(:,1)-y11;
end


x1(:,1) = NbISP1(:,4);
x11= mean(x1(:,1));
x1_min_mean = x1(:,1)-x11;


A = sum(x1_min_mean.*y1_min_mean);
B = sum(x1_min_mean .*x1_min_mean);

b = A/B;

a = y11 - b* x11;  % y = bx+a

x = linspace(0,1); % <--- much larger range

y = b*x+a;



scatter(x1,y1)
scatter(x1,y1,10,'b','filled');
hold on
plot(x,y)


% %% OR % create the regression line security_index = #new infections * b + a
% A = sum(x1_min_mean.*y1_min_mean);
% B = sum(y1_min_mean .*y1_min_mean);
% 
% b = A/B;
% 
% a = x11 - b* y11;  % y = bx+a
% 
% x = linspace(0,0.08); % <--- much larger range
% 
% y = b*x+a;
% 
% scatter(y1,x1,10,'r','filled');
% hold on
% plot(x,y)



% summarize per country
UniqCountry = unique(UniqISP1(:,2));

% NbISP1 -> 1. total new infections 2. size	3. GNI_pc_2017	4.internet_privacy_index	5.rank

% Country_infect_size -> 1.total new infections 2. size 3.internet_privacy_index
for ii = 1: size(UniqCountry,1)
    [ind,ind1]=ismember(UniqISP1(:,2), UniqCountry(ii,1));
%    [ind,ind1]=ismember( UniqISP(ii,1), MatrElements22(:,1));
    if sum(ind)
        Country_infect_size(ii,1) = sum(NbISP1(ind,1));
        Country_infect_size(ii,2) = sum(NbISP1(ind,2));
        jj = find(ind);
        Country_infect_size(ii,3) = NbISP1(jj(1),4);
    end 
end

% create the regression line # new infections = b*security_index + a
Yy1(:,1) = (Country_infect_size(:,1)./Country_infect_size(:,2)) * 100;
%Yy1(51,:) = [];

% normalize the data for the new infections - to the total 1
% sum_Yy1 = sum(Yy1(:,1));
% Yy1(:,1) = Yy1(:,1) / sum_Yy1;

Yy11 = mean(Yy1(:,1));
Yy1_min_mean = Yy1(:,1)-Yy11;

Xx1(:,1) = Country_infect_size(:,3);
%Xx1(51,:) = [];

Xx11= mean(Xx1(:,1));
Xx1_min_mean = Xx1(:,1)-Xx11;


A = sum(Xx1_min_mean.*Yy1_min_mean);
B = sum(Xx1_min_mean .*Xx1_min_mean);

C1 = sqrt(sum(Xx1_min_mean .*Xx1_min_mean));
C2 = sqrt(sum(Yy1_min_mean .*Yy1_min_mean));
coef_persion = A/ (C1*C2);

b = A/B;

a = Yy11 - b* Xx11;  % y = bx+a

x = linspace(0,1); % <--- much larger range

y = b*x+a;

plot(x,y)

ylabel('Normalized New Infections Observed');
xlabel('Global Cybersecurity Index per country (2017)') 
legend({},{'regression line'},'Location','northwest')
set(gcf,'color','w')
hold on
scatter(Xx1,Yy1,10,'b','filled');


scatter(1:60,Xx1,10,'b','filled');
hold on
scatter(1:60,Yy1*100,10,'r','filled');
ylabel('');
xlabel('Global Cybersecurity Index towards the new infections per country') 
legend({'Global Security Index','Infected IoT'},'Location','northwest')
set(gcf,'color','w')


%% OR % create the regression line security_index = #new infections * b + a
Yy1(:,1) = (Country_infect_size(:,1)./Country_infect_size(:,2))*1000;
%Yy1(:,1) = Country_infect_size(:,1);
Yy11 = mean(Yy1(:,1));
Yy1_min_mean = Yy1(:,1)-Yy11;

Xx1(:,1) = Country_infect_size(:,3);
Xx11= mean(Xx1(:,1));
Xx1_min_mean = Xx1(:,1)-Xx11;



A = sum(Xx1_min_mean.*Yy1_min_mean);
B = sum(Yy1_min_mean .*Yy1_min_mean);

b = A/B;

a = Xx11 - b* Yy11;  % y = bx+a

x = linspace(0,0.45); % <--- much larger range

y = b*x+a;

scatter(Yy1,Xx1,10,'r','filled');
hold on
plot(x,y)




