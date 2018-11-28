#!/usr/bin/python

import json
import csv

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

samples = set([])
samples_2_runs = {}

if not 'metasra' in locals():
    with open(WORK_DIR + 'downloads/metaSRA/metasra.v1-4.json','r') as in_file:
        metasra = json.load(in_file)


with open(WORK_DIR + 'data/recount/gtex/tsv_friendly_gtex_meta.tsv','r') as in_file:
    reader = csv.reader(in_file,delimiter='\t')
    reader.next()

    for line in reader:

        sample = line[2]
        run = line[4]

        # if run 

        samples.add(sample)

        sample_entry = samples_2_runs.get(sample,[])
        sample_entry.append(run)
        samples_2_runs[sample] = sample_entry


with open(WORK_DIR + 'data/recount/metadata/tsv_friendly_recount_meta.tsv','r') as in_file:
    reader = csv.reader(in_file,delimiter='\t')
    reader.next()

    for line in reader:

        sample = line[2]
        run = line[4]

        samples.add(sample)

        sample_entry = samples_2_runs.get(sample,[])
        sample_entry.append(run)
        samples_2_runs[sample] = sample_entry


mapped_metadata = {}

for sample in samples:

    meta_entry = metasra.get(sample,None)

    if not meta_entry:
        runs_not_in_metasra = runs_not_in_metasra + samples_2_runs[sample]
        continue
    
    term_list = meta_entry['mapped ontology terms']

    for term in term_list:

        # term_label = term.replace(':','_')

        if not 'DOID' in term:
            continue

        term_entry = mapped_metadata.get(term,None)

        if not term_entry:
            
            term_entry = {}

            term_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/doid/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F%s' % term.replace(':','_'))

            term_label = term_req.json()['label']

            term_entry['name'] = term_label

            term_entry['runs'] = set(samples_2_runs[sample])

        else:

            term_entry['runs'] |= set(samples_2_runs[sample])

        mapped_metadata[term] = term_entry

with open(WORK_DIR + 'data/recount/metadata/tcga_sra_pheno.tsv','r') as in_file:

    reader = csv.reader(in_file,delimiter='\t')

    reader.next()

    for line in reader:
        samp = line[1].strip('.bw')

        for term_name in line[3:7]:
            term_name = re.sub('<','',term_name)
            term_name = re.sub('>','',term_name)
            term_split = term_name.split(':')
            term_id = term_split[0] + ':' + term_split[1]

            if not 'DOID' in term_id:
                continue
                # mesh_mapped = [term_id]

            term_entry = mapped_metadata[term_id]

            if not term_entry:
            
                term_entry = {}

                term_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/doid/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F%s' % term)

                term_label = term_req.json()['label']

                term_entry['name'] = term_label

                term_entry['runs'] = set([samp])

        else:

            term_entry['runs'] |= set(samples_2_runs[sample])

        mapped_metadata[term] = term_entry

            

#             for mesh_term in mesh_mapped:

#                 if '.' in mesh_term:
#                     mesh_term = bad_id_mapping[mesh_term]
#                 else:
#                     continue

#                 term_entry = mapped_metadata.get(mesh_term,None)

#                 if not term_entry:

#                     term_entry = {}
#                     try:
#                         term_entry['name'] = mesh_rparents[mesh_term]['name']
#                     except KeyError:
#                         bad_ids.add(mesh_term)
                        
#                     term_entry['runs'] = set(samples_2_runs[sample])
#                 else:
#                     term_entry['runs'] |= set(samples_2_runs[sample])

#                 mapped_metadata[mesh_term] = term_entry

#                 parents = mesh_rparents[mesh_term]['rparents']

#                 for parent in parents:

#                     term_entry = mapped_metadata.get(parent['id'],None)

#                     if not term_entry:
#                         term_entry = {}

#                         try:
#                             term_entry['name'] = parent['name']
#                         except KeyError:
#                             bad_ids.add(mesh_term)

#                         term_entry['runs'] = set(samples_2_runs[sample])
#                     else:
#                         term_entry['runs'] |= set(samples_2_runs[sample])

#                     mapped_metadata[parent['id']] = term_entry

                


