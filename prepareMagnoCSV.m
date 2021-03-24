clear all; clc;
magnoRootPath = '/Users/glerma/soft/paper-MAGNO';

subSesList    = fullfile(magnoRootPath,'subSesList.txt');
opts          = detectImportOptions(subSesList);
opts = setvartype(opts,{'sub','ses','RUN','anat','dwi','func'},...
                       {'categorical','categorical','logical','logical','logical','logical'});
ssl           = readtable(subSesList,opts); 
unique(ssl.sub);
ssl = ssl(ssl.dwi==true,:);
unique(ssl(:,{'sub','ses'}));

bigCSV  = fullfile(magnoRootPath,'local','RTP_Profile.csv');
dt      = reduceMagno(bigCSV,ssl);
unique(dt(:,{'subID','ses'}))
unique(dt.TCK)

% Convert it to long and to arrays
dtstack = stack(dt,{'curvature','rd','ad','fa','torsion','cl','md','volume'},...
                    'NewDataVariableName','vals');
dtstack.Properties.VariableNames = {'subID','ind','ses','TCK','meas','vals'};


% Convert index to array
dtarray = dtstack(dtstack.ind==1,{'subID','ses','TCK','meas','vals'});
for ii=1:height(dtarray)
    sub = dtarray.subID(ii);
    ses = dtarray.ses(ii);
    TCK = dtarray.TCK(ii);
    meas= dtarray.meas(ii);
    % disp([sub ses TCK meas]);
    
    arr  = dtstack.vals(dtstack.subID==sub & dtstack.ses==ses & ...
                        dtstack.TCK==TCK & dtstack.meas==meas)';
    indx = dtstack.ind(dtstack.subID==sub & dtstack.ses==ses & ...
                        dtstack.TCK==TCK & dtstack.meas==meas);
    valid = true;
    if ~length(arr)==100 || ~isequal(indx,(1:100)') || sum(arr)==0 || isempty(arr)
        disp([sub ses TCK meas]);
        arr   = NaN(100,1);
        valid = false;
    end
    % Edit the array value
    dtarray.arr(ii)   = {arr};
    dtarray.valid(ii) = valid;
end
dtarray = dtarray(:,{'subID','ses','TCK','meas','arr','valid'});
dtarray.Properties.VariableNames = {'subID','ses','TCK','meas','vals','valid'};
dt = dtarray;

% height(dt(dt.TCK=="L_VOF" & dt.meas==meas,:))



% Check
%{
    sum(dt.valid)
    sub = "S030";
    ses = "T01";
    TCK = "L_VOF";
    % TCK = "Left_Arcuate";
    meas= "fa";
    A = dt.vals{dt.subID==sub & dt.ses==ses & dt.TCK==TCK  & dt.meas==meas};
    plot(A,'r');hold on;
%}


% Save it in mat format for sharing
save(fullfile(magnoRootPath,'local','MAGNO_long.mat'),'dt')











%% C2ROI

bigCSV  = fullfile(magnoRootPath,'local','RTP_Profile_C2ROI.csv');
dtc2roi = reduceMagno(bigCSV,ssl);
unique(dtc2roi(:,{'subID','ses'}))
unique(dtc2roi.TCK)

dtc2roi.Properties.VariableNames = {'subID','ind','ses','TCK','curvature',...
                                    'rd','ad','fa','torsion',...
                                    'cl','md','volume'};

% Convert it to long and to arrays
dtstack = stack(dtc2roi,{'curvature','rd','ad','fa','torsion','cl','md','volume'},...
                    'NewDataVariableName','vals');
dtstack.Properties.VariableNames = {'subID','ind','ses','TCK','meas','vals'};


% Convert index to array
dtarray = dtstack(dtstack.ind==1,{'subID','ses','TCK','meas','vals'});
for ii=1:height(dtarray)
    sub = dtarray.subID(ii);
    ses = dtarray.ses(ii);
    TCK = dtarray.TCK(ii);
    meas= dtarray.meas(ii);
    % disp([sub ses TCK meas]);
    
    arr  = dtstack.vals(dtstack.subID==sub & dtstack.ses==ses & ...
                        dtstack.TCK==TCK & dtstack.meas==meas)';
    indx = dtstack.ind(dtstack.subID==sub & dtstack.ses==ses & ...
                        dtstack.TCK==TCK & dtstack.meas==meas);
    valid = true;
    if ~length(arr)==100 || ~isequal(indx,(1:100)') || sum(arr)==0 || isempty(arr)
        disp([sub ses TCK meas]);
        arr   = NaN(100,1);
        valid = false;
    end
    % Edit the array value
    dtarray.arr(ii)   = {arr};
    dtarray.valid(ii) = valid;
end
dtarray = dtarray(:,{'subID','ses','TCK','meas','arr','valid'});
dtarray.Properties.VariableNames = {'subID','ses','TCK','meas','vals','valid'};
dtc2roi = dtarray;
save(fullfile(magnoRootPath,'local','MAGNO_C2ROI_long.mat'),'dtc2roi')

%% Load
load(fullfile(magnoRootPath,'local','MAGNO_long.mat'))
load(fullfile(magnoRootPath,'local','MAGNO_C2ROI_long.mat'))

% Test
%{
    sub = "S025";
    ses = "T01";
    TCK = "Left_Arcuate";
    meas= "fa";    
    length(dt.vals{dt.subID==sub & dt.ses==ses & dt.TCK==TCK & dt.meas==meas})
    A = dt.vals{dt.subID==sub & dt.ses==ses & dt.TCK==TCK  & dt.meas==meas};
    B = dtc2roi.vals{dtc2roi.subID==sub & dtc2roi.ses==ses & dtc2roi.TCK==TCK & dtc2roi.meas==meas};
    plot(A,'r');hold on;plot(B,'b');legend({'normal','C2ROI'})
%}

writetable(dtc2roi,fullfile(magnoRootPath,'local','dtc2roi.xlsx'),"UseExcel",true)
writetable(dt,fullfile(magnoRootPath,'local','dt.xlsx'),"UseExcel",true)

