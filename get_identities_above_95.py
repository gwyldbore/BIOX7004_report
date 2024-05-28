import re
import sys

def order_hits(hits):
    # sort the hits by field 3 (index 2) - this is the percent identity
    # as hits are in format query id, subject id, % identity, % positives, evalue, bit score, subject titles 
    # (sub titles include temp and genome)
    hits.sort(key=lambda x: float(x.split('\t')[2]), reverse=True)
    return hits


# print version of process_file
# def process_file(file):

#     '''
#     Print out the hits that have a percent identity greater than 95%.
#     Will not print out any query sequences which found no hits in the database.

#     each hit starts, as example, with:
#     # TBLASTN 2.9.0+
#     # Query: sp|Q9HVA2|ILVC_PSEAE
#     # Database: ../../annotated_genome_db
#     # Fields: query id, subject id, % identity, % positives, evalue, bit score, subject titles
#     # 6827 hits found
#     '''
#     hits = []
#     with open(file) as f:
#         # read the file line by line
#         for line in f:
#             # skip comments (or maybe leave as it is)


            
#             if line.startswith('#'): # skip the general info that is the same for all
#                 if 'BLAST' in line or 'Fields' in line or 'Database' in line:
#                     continue

#                 elif line.startswith('# Query'): #grab the query sequence name
#                     hits = order_hits(hits)

#                     if len(hits) > 0:
#                         print(num_hits)
#                         print(line, end='')
#                         print('# of hits above 95% identity:', len(hits))
#                         for hit in hits:
#                             print(hit, end='')
#                         print()

#                     query = line
#                     hits = []
#                     continue
#                 elif re.match(hit_pattern, line): # pattern is hit_pattern = r'^#\s\d' (i.e. # *somedigits* )
#                     num_hits = '# of hits total: ' + line.split()[1]
#                     continue

#             else:
#                 # split fields
#                 fields = re.split('\t', line)
#                 # check if the 3rd field is greater than 95%
#                 if float(fields[2]) > 95:
#                     # output the matched line
#                     hits.append(line)


def process_file(file, output_file):
    '''
    Write the hits that have a percent identity greater than 95% to the output file.
    Will not write any query sequences which found no hits in the database.
    '''
    hits = []
    with open(file) as f:
        # read the file line by line
        for line in f:
            # skip comments (or maybe leave as it is)
            if line.startswith('#'): # skip the general info that is the same for all
                if 'BLAST' in line or 'Fields' in line or 'Database' in line:
                    continue

                elif line.startswith('# Query'): #grab the query sequence name
                    hits = order_hits(hits)

                    if len(hits) > 0:
                        output_file.write(num_hits + '\n')
                        output_file.write(line)
                        output_file.write('# of hits above 95% identity: {}\n'.format(len(hits)))
                        for hit in hits:
                            output_file.write(hit)
                        output_file.write('\n')

                    query = line
                    hits = []
                    continue
                elif re.match(hit_pattern, line): # pattern is hit_pattern = r'^#\s\d' (i.e. # *somedigits* )
                    num_hits = '# of hits total: ' + line.split()[1]
                    continue
            else:
                # split fields
                fields = re.split('\t', line)
                # check if the 3rd field is greater than 95%
                if float(fields[2]) > 95:
                    # output the matched line
                    hits.append(line)



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_file> <filename1> [<filename2> ...]")
        sys.exit(1)

    hit_pattern = r'^#\s\d'
    output_filename = sys.argv[1]
    filenames = sys.argv[2:]

    print("Output file:", output_filename)
    print("Files to process:", filenames)

    # for filename in filenames:
    #     #print("Processing file:", filename)
    #     print("Fields: query id, subject id, %identity, %positives, evalue, bit score, genome accession, temp, metagenome")
    #     print()
    #     print()
    #     process_file(filename)

    with open(output_filename, 'w') as output_file:
        output_file.write("Fields: query id, subject id, %identity, %positives, evalue, bit score, genome accession, temp, metagenome\n\n")
        
        for filename in filenames:
            process_file(filename, output_file)
            output_file.write("\n\n")
