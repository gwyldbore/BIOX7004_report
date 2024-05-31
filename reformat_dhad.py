with open('/Users/georgiawyldbore/Desktop/UQ_2024/Sem1/BIOX7004/retrievingdatatest/files_for_server/files_from_server/dhad_highest_formatted.csv', 'w') as output_file:
    with open('/Users/georgiawyldbore/Desktop/UQ_2024/Sem1/BIOX7004/retrievingdatatest/files_for_server/files_from_server/dhad_highest.csv', 'r') as file:
        
        lines = file.readlines()
        for line in lines:
            line = line.replace('_', '|')
            split = line.split(',')
            identifier = split[0]
            newline = identifier[:-6]
            newline += '_' + identifier[-5:]
            newline += ',' + split[1]
            output_file.write(newline)

