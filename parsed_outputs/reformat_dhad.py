with open('dhad_lowest_formatted.csv', 'w') as output_file:
    with open('dhad_lowest.csv', 'r') as file:
        
        lines = file.readlines()
        for line in lines:
            line = line.replace('_', '|')
            split = line.split(',')
            identifier = split[0]
            newline = identifier[:-6]
            newline += '_' + identifier[-5:]
            newline += ',' + split[1]
            output_file.write(newline)


with open('dhad_highest_formatted.csv', 'w') as output_file:
    with open('dhad_highest.csv', 'r') as file:
        
        lines = file.readlines()
        for line in lines:
            line = line.replace('_', '|')
            split = line.split(',')
            identifier = split[0]
            newline = identifier[:-6]
            newline += '_' + identifier[-5:]
            newline += ',' + split[1]
            output_file.write(newline)


with open('dhad_all_formatted.csv', 'w') as output_file:
    with open('dhad_all.csv', 'r') as file:
        
        lines = file.readlines()
        for line in lines:
            line = line.replace('_', '|')
            split = line.split(',')
            identifier = split[0]
            newline = identifier[:-6]
            newline += '_' + identifier[-5:]
            newline += ',' + split[1]
            output_file.write(newline)