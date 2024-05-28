#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# create fasta file containing all sequences
get_ipython().system('cat genome_data/ncbi_dataset/data/GCA_*/*.fna > all_genome_seqs.fasta')


# In[ ]:


print('All sequences in fasta file')
print()

# get map of genome accession to contig project accession data
import json
file_path = './genome_data/ncbi_dataset/data/assembly_data_report.jsonl'

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


# In[ ]:


#create map of genome accession to temperature
accession_temp_data = []
accession_to_temp = {}
file_path_2 = 'accession_temp_valid.txt'
with open(file_path_2, 'r') as file:
    for line in file:
        accession_temp_data.append(line.strip())

for accession in accession_temp_data:
    acc, temp = accession.split(' ')
    if acc in accession_to_project.values():
        accession_to_temp[acc] = temp 

print('Genomes mapped to temperature')


# In[ ]:


# add genome accessions and temperatures to fasta file headers 
from Bio import SeqIO

fasta_file = 'all_genome_seqs.fasta'

output_file = 'all_genome_seqs_annotated.fasta'

# Read the FASTA file, modify the identifier lines, and write the modified sequences to a new file
with open(fasta_file, 'r') as input_file, open(output_file, 'w') as output_file:
    for record in SeqIO.parse(input_file, "fasta"):
        if 'hot spring' in record.description:
            SeqIO.write(record, output_file, "fasta")
            continue
        identifier = record.id[0:6]
        whole_id = record.id
        try:
            genome_accession = accession_to_project[identifier]
            record.description = record.description.replace(whole_id, '| ' + genome_accession + ' | ' + accession_to_temp[genome_accession] + ' |')
        except KeyError:
            print(f"KeyError for contig: {whole_id}.")
        SeqIO.write(record, output_file, "fasta")


#optional - remove the original fasta file
# !rm all_genome_seqs.fasta

print('Sequences ready to be turned into a database')
print()


# In[ ]:


# make the blast db
print('Making the blast database')
get_ipython().system('makeblastdb -in all_genome_seqs_modified.fasta -out annotated_genome_db -dbtype nucl -title "annotated_genome_db" -parse_seqids')

print('Database created: "annotated_genome_db"')

