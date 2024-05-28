# get map of genome accession to contig project accession data
import json
file_path = '../genome_data/ncbi_dataset/data/assembly_data_report.jsonl'

data = []
with open(file_path, 'r') as file:
    for line in file:
        data.append(json.loads(line))
    

accession_to_project = {}

for assembly in data:
    accession = assembly['accession']
    project = assembly['wgsInfo']['wgsProjectAccession']
    accession_to_project[project] = accession

print('Genomes mapped to project accession')


#create map of genome accession to temperature
accession_temp_data = []
accession_to_temp = {}
file_path_2 = '../accession_temp_valid.txt'
with open(file_path_2, 'r') as file:
    for line in file:
        accession_temp_data.append(line.strip())

for accession in accession_temp_data:
    acc, temp = accession.split(' ')
    if acc in accession_to_project.values():
        accession_to_temp[acc] = temp 

print('Genomes mapped to temperature')




# # alternative to adding to fasta file - have a map of them stored in a .txt for reference later. 
# # may save space on another 83GB fasta file lol
values = []
with open('project_accession_temp.txt', 'w') as file:
        for key, value in accession_to_project.items():
            file.write(f"{key} {value} {accession_to_temp[value]}\n")
            values.append(f"{key} {value} {accession_to_temp[value]}")


with open('unique_errors.txt', 'r') as file:
    for line in file:
        current = line.strip()
        if current.startswith('KeyError'):
            split = current.split(' ')
            project = split[3]
            id = project[:8]
            genome = accession_to_project[id]
            temp = accession_to_temp[genome]
            print(f"{id} {genome} {temp}")


