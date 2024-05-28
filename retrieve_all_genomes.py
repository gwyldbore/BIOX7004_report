#!/usr/bin/env python
# coding: utf-8

# In[4]:


#Taxon id for ecolocial metagenomies is 410657
# use datasets to download it

get_ipython().system('datasets summary genome taxon 410657 > ecological_metagenomes.json')


# In[15]:


#get the list of accessions, project names, and temperatures

import json
file_path = 'ecological_metagenomes.json'

with open(file_path, 'r') as file:
    data = json.load(file)
temps = []
accessions = []
accession_temp_pairing = {}

print("Number of metagenomes available:", len(data['reports']))

for report in data['reports']:

    if 'biosample' in report['assembly_info']:
        if 'attributes' in report['assembly_info']['biosample']:
            attributes = report['assembly_info']['biosample']['attributes']

            for attribute in attributes:
                if attribute['name'] == 'isolation_source':
                    isolation_source = attribute['value']

                    if 'temperature' in isolation_source and ';' in isolation_source:
                        temperature = isolation_source.split(';')[1].split()[1]

                        temps.append(temperature)
                        accessions.append(report['accession'])
                        accession_temp_pairing[report['accession']] = temperature
                        break

                elif attribute['name'] == 'temp':
                    temperature = attribute['value']

                    temps.append(temperature)
                    accessions.append(report['accession'])
                    accession_temp_pairing[report['accession']] = temperature

print("Temperature retrieval finished")
print()


# In[16]:


#check we have a good number of accessions and no duplicates
print('Number of accessions with temperatures:', len(accessions))
print('No duplicates' if len(set(accessions)) == len(accessions) else 'duplicates found')
print()


# In[ ]:


#create .txt file with accession and temp for easier viewing
output = 'accession_temp.txt'

with open(output, 'w') as file:
    for key, value in accession_temp_pairing.items():
            file.write(f"{key} {value}\n")


# In[ ]:


# get accession vs temp data for filtering

file_path = 'accession_temp.txt'

data = []
with open(file_path, "r") as file:
    for line in file:

        contents = line.strip().split()

        if 'O2' in contents[1]:
            continue

        if 'i' in contents[1]:
            contents[1] = contents[1].replace('i', '')

        for char in contents[1]:
            if not char.isdigit():
                if char == '.' or char == '-':
                    continue

                contents[1] = contents[1].replace(char, '')
        data.append((contents[0], float(contents[1])))


# In[ ]:


# get valid temperatures - e.g. filter out those with values like -999

print("Filtering out invalid temperatures - keeping only those in range -100 to 150...")

valid_pairs = [(acc, temp) for acc, temp in data if -100 < temp < 150]

#sort data by temp so txt file is easy to read 
valid_pairs = sorted(valid_pairs, key=lambda x: x[1])

#dict for easy txt writing
valid_pairs_mapping = {acc: temp for acc, temp in valid_pairs}


print(f"Filtered out {len(data) - len(valid_pairs)} invalid temperatures, {len(valid_pairs)} remain.")
print()


#create .txt file with valid accessions and temperatures in case its needed later
output = 'accession_temp_valid.txt'

with open(output, 'w') as file:
    for key, value in valid_pairs_mapping.items():
            file.write(f"{key} {value}\n")


# In[ ]:


### creating file with all useful accession numbers

accession_file = open("all_valid_accessions.txt", 'w')
for accession, _ in valid_pairs:
    accession_file.write(accession+'\n')
accession_file.close()

print(f".txt file created with all accessions of valid temperature data.")


# In[ ]:


#download dehydrated genomes
print("Downloading dehydrated genomes...")
get_ipython().system('datasets download genome accession --dehydrated --inputfile all_valid_accessions.txt --filename all_accessions.zip')


# In[ ]:


#uncompress zip file
print("Uncompressing zip file...")
get_ipython().system('unzip all_accessions.zip -d genome_data')


# In[ ]:


#rehydrate all genome data
print("Rehydrating genomes...")
get_ipython().system('datasets rehydrate --directory genome_data/')

print("All genomes rehydrated.")

