function dt = reduceMagno(bigCSV,ssl)
magnoRootPath = '/Users/glerma/soft/paper-MAGNO';
DT            = readtable(bigCSV);

DT.subID = categorical(DT.subID);
DT.ses   = categorical(DT.ses);
DT.TCK   = categorical(DT.TCK);

%Rename one MAGNO subject Mengxing renamed
alt = height(DT(DT.subID=="TOT7729F" & DT.ses=="T02","subID"));
DT(DT.subID=="TOT7729F" & DT.ses=="T02","ses") = cellstr(repmat("Ttmp",[alt,1]));
DT(DT.subID=="TOT7729F" & DT.ses=="Ttmp","subID") = cellstr(repmat("S030",[alt,1]));
DT(DT.subID=="S030" & DT.ses=="Ttmp","ses") = cellstr(repmat("T01",[alt,1]));
DT.subID = categorical(DT.subID);

% Delete the data we do not want
dt = DT(contains(string(DT.subID),string(ssl.sub)),:);

% Now select only the structs we want
selectTheseTracts = {...
     'Callosum_Forceps_Major'
     'Callosum_Forceps_Minor'
     'Left_Arcuate'
     % 'Left_Cingulum_Cingulate'
     % 'Left_Cingulum_Hippocampus'
     % 'Left_Corticospinal'
     'Left_IFOF'
     'Left_ILF'
     'Left_Optic_Radiation_V1'
     'Left_Optic_Radiation_V1V2'
     'Left_Optic_Radiation_V1V2R3'
     'Left_SLF'
     % 'Left_Thalamic_Radiation'
     % 'Left_Uncinate'
     'Right_Arcuate'
     % 'Right_Cingulum_Cingulate'
     % 'Right_Cingulum_Hippocampus'
     % 'Right_Corticospinal'
     'Right_IFOF'
     'Right_ILF'
     'Right_Optic_Radiation_V1'
     'Right_Optic_Radiation_V1V2'
     'Right_Optic_Radiation_V1V2R3'
     'Right_SLF'
     % 'Right_Thalamic_Radiation'
     % 'Right_Uncinate'
     'L_Arcuate_Posterior'
     'L_VOF'
     'L_posteriorArcuate_vot'
     'R_Arcuate_Posterior'
     'R_VOF'
     'R_posteriorArcuate_vot'};
dt = dt(contains(string(dt.TCK),selectTheseTracts),:);

return