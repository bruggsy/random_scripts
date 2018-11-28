#!/usr/bin/python

import json
import csv
import re
import sys
import pronto

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

uberon = pronto.Ontology(WORK_DIR + 'downloads/ontologies/uberon_ext.obo')
efo = pronto.Ontology(WORK_DIR + 'downloads/ontologies/efo.obo')
doid = pronto.Ontology(WORK_DIR + 'downloads/ontologies/doid-non-classified.obo')

samples = set([])

samples_2_runs = {}

with open(WORK_DIR + 'data/recount/gtex/tsv_friendly_gtex_meta.tsv','r') as in_file:
    reader = csv.reader(in_file,delimiter='\t')
    reader.next()

    for line in reader:

        sample = line[2]
        run = line[4]

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


with open(WORK_DIR + 'downloads/metaSRA/metasra.v1-4.json','r') as in_file:
    metasra = json.load(in_file)

runs_not_in_metasra = []

uberon_runs = set([])
efo_runs = set([])
doid_runs = set([])
cvcl_runs = set([])
no_ont_runs = set([])
cl_runs = set([])

mapped_metadata = {}

for sample in samples:

    meta_entry = metasra.get(sample,None)

    if not meta_entry:
        runs_not_in_metasra = runs_not_in_metasra + samples_2_runs[sample]
        continue

    term_list = meta_entry['mapped ontology terms']
    
    for key_term in term_list:

        if 'CVCL' in key_term:
            continue
        elif 'UBERON' in key_term:
            term = uberon[key_term]
        elif 'CL' in key_term:
            term = uberon[key_term]
        elif 'DOID' in key_term:
            term = doid[key_term]
        elif 'EFO' in key_term:
            term = efo[key_term]
        else:
            no_ont_runs |= set(samples_2_runs[sample])
        
        
        term_entry = mapped_metadata.get(key_term,None)

        if not term_entry:

            term_entry = {}

            term_entry['name'] = term.name
            # term_entry['runs'] = samples_2_runs[sample]
            term_entry['runs'] = set(samples_2_runs[sample])
        else:
            term_entry['runs'] |= set(samples_2_runs[sample])
            # term_entry['runs'].extend(samples_2_runs[sample])

        mapped_metadata[key_term] = term_entry

        parents = term.rparents()

        for parent in parents:

            parent_id = re.sub(' \{.*\}','',parent.id)

            term_entry = mapped_metadata.get(parent_id,None)

            if not term_entry:

                term_entry = {}

                term_entry['name'] = parent.name
                term_entry['runs'] = set(samples_2_runs[sample])
                # term_entry['runs'] = samples_2_runs[sample]

            else:

                term_entry['runs'] |= set(samples_2_runs[sample])
                # term_entry['runs'].extend(samples_2_runs[sample])

            mapped_metadata[parent_id] = term_entry


for key in mapped_metadata.keys():
    mapped_metadata[key]['runs'] = list(mapped_metadata[key]['runs'])

with open(WORK_DIR + 'data/recount/metadata/ontoterm_to_subjects_gtex_recount.json','w') as out_file:
    json.dump(mapped_metadata,out_file)


print 'done'
