base_url = 'http://aviationweather.gov/products/nws/';      %url for weather data
zones = {'boston';'miami';'ftworth';'chicago';'saltlakecity';'sanfrancisco'};   %each zone
indices = [[2141,3960]; [2142,3471];[2142, 5011]; [2141,5080]; [2150,4389];[2148,3687]]; %indices for each zone
breaks = [1,3,5,8,10,16,18,24,26,32,34,40,42,48,50,55,57,62,64,70];

html = urlread(strcat(base_url, zones{1}));

txt = regexprep(html,'<script.*?/script>','');
txt = regexprep(txt,'<style.*?/style>','');
txt = regexprep(txt,'<.*?>','');

boston = txt(indices(1,1):indices(1,2));
len = size(boston);

northeast = cell(len(2)/70, 10);

for j = 1:10
    for i = 1:(len(2)/70)
        northeast{i,j} = boston((70*(i-1))+breaks((j*2)-1):(70*(i-1) + breaks(j*2)));
    end
end

html = urlread(strcat(base_url, zones{2}));

txt = regexprep(html,'<script.*?/script>','');
txt = regexprep(txt,'<style.*?/style>','');
txt = regexprep(txt,'<.*?>','');

miami = txt(indices(2,1):indices(2,2));
len = size(miami);

southeast = cell(len(2)/70, 10);

for j = 1:10
    for i = 1:(len(2)/70)
        southeast{i,j} = miami((70*(i-1))+breaks((j*2)-1):(70*(i-1) + breaks(j*2)));
    end
end

html = urlread(strcat(base_url, zones{3}));

txt = regexprep(html,'<script.*?/script>','');
txt = regexprep(txt,'<style.*?/style>','');
txt = regexprep(txt,'<.*?>','');

ftworth = txt(indices(3,1):indices(3,2));
len = size(ftworth);

south = cell(len(2)/70, 10);

for j = 1:10
    for i = 1:(len(2)/70)
        south{i,j} = ftworth((70*(i-1))+breaks((j*2)-1):(70*(i-1) + breaks(j*2)));
    end
end

html = urlread(strcat(base_url, zones{4}));

txt = regexprep(html,'<script.*?/script>','');
txt = regexprep(txt,'<style.*?/style>','');
txt = regexprep(txt,'<.*?>','');

chicago = txt(indices(4,1):indices(4,2));
len = size(chicago);

midwest = cell(len(2)/70, 10);

for j = 1:10
    for i = 1:(len(2)/70)
        midwest{i,j} = chicago((70*(i-1))+breaks((j*2)-1):(70*(i-1) + breaks(j*2)));
    end
end

html = urlread(strcat(base_url, zones{5}));

txt = regexprep(html,'<script.*?/script>','');
txt = regexprep(txt,'<style.*?/style>','');
txt = regexprep(txt,'<.*?>','');

saltlake = txt(indices(5,1):indices(5,2));
len = size(saltlake);

rockies = cell(len(2)/70, 10);

for j = 1:10
    for i = 1:(len(2)/70)
        rockies{i,j} = saltlake((70*(i-1))+breaks((j*2)-1):(70*(i-1) + breaks(j*2)));
    end
end

html = urlread(strcat(base_url, zones{6}));

txt = regexprep(html,'<script.*?/script>','');
txt = regexprep(txt,'<style.*?/style>','');
txt = regexprep(txt,'<.*?>','');

sanfrancisco = txt(indices(6,1):indices(6,2));
len = size(sanfrancisco);

west = cell(len(2)/70, 10);

for j = 1:10
    for i = 1:(len(2)/70)
        west{i,j} = sanfrancisco((70*(i-1))+breaks(j*2-1):(70*(i-1) + breaks(j*2)));
    end
end

for i = 1:6
    fileID = fopen(strcat('C:\Users\keshav\Documents\Network\Weather\', zones{i}, date,'.csv'), 'w');
    %Must change file path
    formatSpec = '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s';
    
    if i == 1
        [rows, col] = size(northeast);
        for row = 1:rows
            fprintf(fileID, formatSpec, northeast{row,:});
        end
    end
    if i == 2
        [rows, col] = size(southeast);
        for row = 1:rows
            fprintf(fileID, formatSpec, southeast{row,:});
        end
    end
    if i == 3 
        [rows, col] = size(south);
        for row = 1:rows
            fprintf(fileID, formatSpec, south{row,:});
        end
    end
    if i == 4
        [rows, col] = size(midwest);
        for row = 1:rows
            fprintf(fileID, formatSpec, midwest{row,:});
        end
    end
    if i == 5
        [rows, col] = size(rockies);
        for row = 1:rows
            fprintf(fileID, formatSpec, rockies{row,:});
        end
    end
    if i == 6
        [rows, col] = size(west);
        for row = 1:rows
            fprintf(fileID, formatSpec, west{row,:});
        end
    end
end

  
        
            
        
    
