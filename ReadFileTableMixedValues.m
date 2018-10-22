function [ ColNames1,ColNames2,MatrElements1,MatrElements2] = ReadFileTableMixedValues(FileName,NbTextColumns) 
% Function to read  mixed data from a table in a csv file with name
% FileName and NbTextColumns - array with the column numbers which have
% text values
%
%   Output:
%   ColNames1- the names of fields in the first row which are for numerical
%               values;
%   ColNames2- the names of fields in the first row which are for text 
%               values;
%
%   MatrElements1 - the matrix of the numerical values of the csv file from
%                   the 2nd to the last row
%   MatrElements1 - the matrix of the text values of the csv file from
%                   the 2nd to the last row
%
%   Last Change: 07/12/2015 - Yorgova
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    slash = filesep();
    if ~exist('NbTextColumns','var')
        NbTextColumns =[];
        nbColumensTable2 = 0;
    else
        nbColumensTable2 = length(NbTextColumns);
    end
    
    
    ColNames1=[];   
    ColNames2=[];    
    FileName_long = [cd,slash,FileName];
    
    if ~exist(FileName_long,'file')     
       str = sprintf('%s does not exist!', FileName);
       disp(str)       
       %error('%s does not exist!', FileName)  
    else

        % Open the InputFileSpot
        fid = fopen(FileName_long);
        % Read the title line and create a cell array with the names
        tline = fgetl(fid); 
        tline = tline(tline~=' '); %Remove empty spaces
        tline = strtrim(tline);
        tline = deblank(tline);
        CommaID=strfind(tline,','); % find the places of commas
        ColNames1=cell(1,(length(CommaID)+1)-nbColumensTable2);
        ColNames2=cell(1,nbColumensTable2);
                
        start=1;
        colID1 = 0;
        colID2 = 0;        
        for colID=1:length(CommaID)
            if ~ismember(colID,NbTextColumns)
                colID1 = colID1 + 1;
                ColNames1{colID1}=tline(start:CommaID(colID)-1);                 
            else
                colID2 = colID2 + 1;
                ColNames2{colID2}=tline(start:CommaID(colID)-1);                
            end
            start=CommaID(colID)+1;
        end
        if ~ismember(colID+1,NbTextColumns)
            colID1 = colID1 + 1;
            ColNames1{colID1}=tline(start:end);
        else
            colID2 = colID2 + 1;
            ColNames2{colID2}=tline(start:end);
        end
    
        
        NbColumns = colID+1;
        nbColumensTable1 = length(ColNames1);
        MatrElements1 = [];        
        MatrElements2 = [];
        
        % READING input csv file
        
        lineIndex = 1;
        
        tline = fgetl(fid);       %# Read the first line from the file
        while ~isequal(tline,-1)        %# Loop while not at the end of the file
            tline = tline(tline~=' '); %Remove empty spaces
            tline = strtrim(tline);
            tline = deblank(tline);
            CommaID=strfind(tline,','); % find the places of commas
            
            ColElements1 = NaN(1,nbColumensTable1);
            ColElements2 = cell(1,nbColumensTable2);
           
            start=1;
            
            colID1 = 0;
            colID2 = 0; 
            for colID=1:length(CommaID)
                tempElem = tline(start:CommaID(colID)-1);
                start=CommaID(colID)+1;
                
                if ismember(colID,NbTextColumns)
                    colID2 = colID2 + 1;
                    ColElements2{colID2} = tempElem;
                else
                    colID1 = colID1 + 1;
                    if ~isempty( tempElem )
                        ColElements1(colID1) = str2num(tempElem);
                    end
                end
            end
            
            tempElem=tline(start:end);
            if ismember(colID+1,NbTextColumns)
                colID2 = colID2 + 1;
                ColElements2{colID2} = tempElem;
            else
                colID1 = colID1 + 1;
                if ~isempty( tempElem )  
                    ColElements1(colID1) = str2num(tempElem);
                end
            end
            
            tline = fgetl(fid); 
            
            
            MatrElements1 = [MatrElements1; ColElements1];
            MatrElements2 = [ MatrElements2;cellstr(ColElements2) ];
        end
        
        fclose(fid);
        
        
    end
% end of function
end