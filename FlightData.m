function [] = FlightData(url,flightnum,day);
%Takes the data from the url and saves it as 2 CSV files in the python
%folder for both the actual(tracker) and planned (decode/waypoints)
%needs packages getTableFromWeb_mod and getHTMLTableData


fileID = fopen(strcat('C:\Users\keshav\Documents\Network\data\', flightnum, day, '.csv'), 'w');
%Creates the CSV file for the tracker points

formatSpec = '%s, %s, %s, %s, %s, %s, %s, %s, %s\n';    %Formatting specfications (all strings)
table = getTableFromWeb_mod(url, 3); %Reads table from URL
dim = (size(table))';  
small = table(4:dim(1)-2, 1:9); %Resizing table to remove junk
[rows, col] = size(small);      %Dimensions of table


small(1,:) = {num2str(rows),num2str(col),'0','0','0','0','0','0','0'};  %First row contains dimensions of table

for row = 1:rows        %Writes data in each row into the CSV
    fprintf(fileID, formatSpec, small{row,:});
end

fclose(fileID);

fileID = fopen(strcat('C:\Users\keshav\Documents\Network\data\', flightnum,day,'waypoints','.csv'), 'w'); 
%Creates the CSV file for the waypoints

formatSpec = '%s,%s,%s,%s,%s,%s\n'; %Formatting specfications (all strings)
[one, len] = size(url);  %Use for creating URL with waypoints 
table = getTableFromWeb_mod(strcat(url(1:(len-8)), 'route'), 3); %Read waypoint table from URL
[rows, col] = size(table); %Dimensions of table 

table(1,:) = {num2str(rows), num2str(col), '0','0','0','0'}; %First row contains dimentsions of table

for row = 1:rows      %Writes data into each row into CSV
    fprintf(fileID, formatSpec, table{row,:});
end

fclose(fileID);

end

