!/usr/bin/python

import pronto
import re
import csv
import json

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

with open(WORK_DIR + 'data/uberon_doid_mesh.json','r') as in_file:
    mesh_terms = json.load(in_file)

with open(WORK_DIR + 'data/recount/metadata/subjtree_combined_gtex_recount_tcga.json','r') as in_file:
    term_2_subjtree = json.load(in_file)

if not 'uberon' in globals():
    uberon = pronto.Ontology(WORK_DIR + 'downloads/ontologies/uberon_ext.obo')
if not 'efo' in globals():
    efo = pronto.Ontology(WORK_DIR + 'downloads/ontologies/efo.obo')
if not 'doid' in globals() :
    doid = pronto.Ontology(WORK_DIR + 'downloads/ontologies/doid-non-classified.obo')

# with open(WORK_DIR + 'data/recount/gtex/tsv_friendly_gtex_meta.tsv','r') as in_file:
#     reader = csv.reader(in_file,delimiter='\t')
#     reader.next()

#     for line in reader:

#         sample = line[2]
#         run = line[4]

#         # if run 

#         samples.add(sample)

#         sample_entry = samples_2_runs.get(sample,[])
#         sample_entry.append(run)
#         samples_2_runs[sample] = sample_entry


# with open(WORK_DIR + 'data/recount/metadata/tsv_friendly_recount_meta.tsv','r') as in_file:
#     reader = csv.reader(in_file,delimiter='\t')
#     reader.next()

#     for line in reader:

#         sample = line[2]
#         run = line[4]

#         samples.add(sample)

#         sample_entry = samples_2_runs.get(sample,[])
#         sample_entry.append(run)
#         samples_2_runs[sample] = sample_entry


# with open(WORK_DIR + 'downloads/metaSRA/metasra.v1-4.json','r') as in_file:
#     metasra = json.load(in_file)

mesh_term_2_subjtree = {}    
with open(WORK_DIR + 'data/recount/metadata/ontoterm_to_subjects_gtex_recount_tcga.json','r') as in_file:
    mapped_metadata = json.load(in_file)

# runs_not_in_metasra = []

# mapped_metadata = {}

# for sample in samples:
#     meta_entry.get(sample,None)

#     if not meta_entry:
#         runs_not_in_metasra = runs_not_in_metasra + samples_2_runs[sample]
#         continue

#     term_list = meta_entry['mapped ontology terms']


mesh_keys = filter(lambda x: x in mesh_terms,term_2_subjtree.keys())


for key in mesh_keys:

    if 'CVCL' in key:
        continue
    elif 'UBERON' in key:
        root_term = uberon[key]
    elif 'CL' in key:
        root_term = uberon[key]
    elif 'DOID' in key:
        root_term = doid[key]
    elif 'EFO' in key:
        root_term = efo[key]

    root_label = str(root_term)
    root_label = root_label.strip('<')
    root_label = root_label.strip('>')
    

    # if not key in mesh_terms:
    #     continue

    subjtree = term_2_subjtree[key]

    new_subjtree = {}

    for term_combination in subjtree.keys():

        combination_split = term_combination.split('+')

        mesh_label = ''

        for term in combination_split:

            term_split = term.split(':')

            term_id = '%s:%s' % (term_split[0],term_split[1])

            if term_id in mesh_terms:

                if len(mesh_label) == 0:
                    # print term
                    mesh_label = term
                else:
                    mesh_label = '%s + %s' % (mesh_label, term)

        if len(mesh_label) > 0:

            subj_tree_entry = new_subjtree.get(mesh_label,[])

            subj_tree_entry.extend(subjtree[term_combination])

            new_subjtree[mesh_label] = subj_tree_entry

        else:

            subj_tree_entry = new_subjtree.get(root_label,[])

            subj_tree_entry.extend(subjtree[term_combination])

            new_subjtree[root_label] = subj_tree_entry

    mesh_term_2_subjtree[key] = new_subjtree
        

with open(WORK_DIR + 'data/recount/metadata/subjtree_mesh.json','w') as out_file:
    json.dump(mesh_term_2_subjtree,out_file)

with open(WORK_DIR + 'data/recount/metadata/subjtree_mesh.json','r') as in_file:
    mesh_term_2_subjtree = json.load(in_file)

metadata_table = []

for key in mesh_term_2_subjtree.keys():

    row = [key,mapped_metadata[key]['name']]

    # del mapped_metadata[key]['name']
    row.append(json.dumps(mesh_term_2_subjtree[key]))

    metadata_table.append(row)


with open(WORK_DIR + 'data/recount/metasra/all_recount_mesh_metasra_table.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')
    writer.writerow(['id','name','termTree'])

    for row in metadata_table:
        writer.writerow(row)

print 'done'
