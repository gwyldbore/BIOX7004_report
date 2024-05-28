import sys


with open('error_all_info.txt') as f:
    contig_temp_map = {}
    for line in f:
        split = line.split()
        contig_temp_map[split[0]] = [split[1], split[2]]





def map_query_assembly_description(filename):
    '''
    parse the results of a blast search output into a dictionary containing the query
    as key and then the contig hit, genome accession of contig, temperature of metagenome,
    and original description of the contig hit as values.
    Includes accessing the contigs which threw errors so could not annotate correctly. 
    '''


    id_info = {}
    hit_info = []
    with open(filename) as file:
        for line in file:
            if line.startswith('# Query'):
                if len(hit_info) > 0:
                    id_info[identifier] = hit_info
                    hit_info= []
                identifier = line.split()[2]
                # format to match the tree which has spaces in place of '|'
                identifier = identifier.replace('|', '_')
                # identifier = identifier.replace('_', ' ')

                # initialise the dictionary entry for this query
                id_info[identifier] = ''

            elif line.startswith('#') or line == '\n' or line.startswith('Fields') or \
            line.startswith('Processing'):
                continue

            else:
                fields = line.split('\t')
                assembly = fields[1].split('|')[1]
                if fields[6].startswith('|'):
                    description = fields[6].split('|')[1:]
                    templist = [assembly]
                    for item in description:
                        templist.append(item.strip())
                    hit_info.append(templist)
                else:
                    description = fields[6] #this is the assembly info that was not annotated and threw error
                    hit_info.append([assembly, description])

        id_info[identifier] = hit_info


    for key, value in id_info.items():
        for description in value:
            if len(description) < 4:
                if 'hot springs' in description[1]:
                    description.insert(1, "NaN")
                    description.insert(1, "FIND THE GENOME")
                    print(key, description)
                else:
                    id = description[0][:8]
                    # print(id)
                    genome = contig_temp_map[id][0]
                    temp = contig_temp_map[id][1] 
                    description.insert(1, temp)
                    description.insert(1, genome)
        
    return id_info
    


def output_parsed_results(results: dict[str: list[str]], output_file):
    for query, hits in results.items(): 
        if type(hits) == list:
            for hit in hits:
                output_file.write(query + ',' + hit[2] + '\n')      
        else:
            output_file.write(query + ',' + hits + '\n')

    return


def get_highest_temp_only(results: dict[str: list[str]]):
    highest_temps_only = {}
    for query, hits in results.items():
        highest_temps_only[query] = ''
        highest_temp = float('-inf')
        for hit in hits:
            temp = float(hit[2])
            if temp > highest_temp:
                # print(query, temp, highest_temp)
                highest_temp = temp
                highest_temps_only[query] = str(highest_temp)
    return highest_temps_only


def get_lowest_temp_only(results: dict[str: list[str]]):
    lowest_temps_only = {}
    for query, hits in results.items():
        lowest_temps_only[query] = ''
        lowest_temp = float('inf')
        for hit in hits:
            temp = float(hit[2])
            if temp < lowest_temp:
                lowest_temp = temp
                lowest_temps_only[query] = str(lowest_temp)
    return lowest_temps_only

    


# path = 'test_non0.txt'







if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python parse_results.py -highest|lowest|all <output_file> <filename1> [<filename2> ...]")
        sys.exit(1)


    output_filename = sys.argv[2]
    filenames = sys.argv[3:]
    parse_type = sys.argv[1]

    print("File(s) to parse:", filenames)

    for file in filenames:
        results = map_query_assembly_description(file)


    if parse_type == '-all':
        with open(output_filename, 'w') as output_file:
            output_parsed_results(results, output_file)

    elif parse_type == '-highest':
        high_temps = get_highest_temp_only(results)
        with open(output_filename, 'w') as output_file:
            output_parsed_results(high_temps, output_file)

    elif parse_type == '-lowest':
        low_temps = get_lowest_temp_only(results)
        with open(output_filename, 'w') as output_file:
            output_parsed_results(low_temps, output_file)

    else: 
        print("Usage: python parse_results.py -highest|lowest|all <output_file> <filename1> [<filename2> ...]")
        sys.exit(1)


    print("Parsed results written to", output_filename)