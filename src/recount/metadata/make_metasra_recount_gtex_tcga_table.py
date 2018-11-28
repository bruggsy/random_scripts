#!/usr/bin/python

import json
import csv
import re
import sys
import pronto
import string

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

# with open(WORK_DIR + 'data/uberon_doid_mesh.json','r') as in_file:
#     mesh_terms = json.load(in_file)


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

            if 'CVCL' in parent_id:
                continue
            elif 'UBERON' in parent_id:
                parent = uberon[parent_id]
            elif 'CL' in parent_id:
                parent = uberon[parent_id]
            elif 'DOID' in parent_id:
                parent = doid[parent_id]
            elif 'EFO' in parent_id:
                parent = efo[parent_id]
            

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

            if 'CVCL' in term_id:
                continue
            if 'UBERON' in term_id or 'CL' in term_id:
                ont_term = uberon[term_id]
            elif 'DOID' in term_id:
                ont_term = doid[term_id]
            elif 'EFO' in term_id:
                ont_term = efo[term_id]
            else:
                continue

            term_id = re.sub(' \{.*\}','',ont_term.id)

            term_entry = mapped_metadata.get(term_id,None)

            if not term_entry:

                term_entry = {}

                term_entry['name'] = ont_term.name
                term_entry['runs'] = set([samp])

            else:

                term_entry['runs'] |= set([samp])

            mapped_metadata[term_id] = term_entry

            parents = ont_term.rparents()

            for parent in parents:

                parent_id = re.sub(' \{.*\}','',parent.id)

                if 'CVCL' in parent_id:
                    continue
                elif 'UBERON' in parent_id:
                    parent = uberon[parent_id]
                elif 'CL' in parent_id:
                    parent = uberon[parent_id]
                elif 'DOID' in parent_id:
                    parent = doid[parent_id]
                elif 'EFO' in parent_id:
                    parent = efo[parent_id]
                
                term_entry = mapped_metadata.get(parent_id,None)
                
                if not term_entry:

                    term_entry = {}

                    term_entry['name'] = parent.name
                    term_entry['runs'] = set([samp])
                    # term_entry['runs'] = samples_2_runs[sample]

                else:

                    term_entry['runs'] |= set([samp])
                    # term_entry['runs'].extend(samples_2_runs[sample])

                mapped_metadata[parent_id] = term_entry


for key in mapped_metadata.keys():
    mapped_metadata[key]['runs'] = list(mapped_metadata[key]['runs'])

with open(WORK_DIR + 'data/recount/metadata/ontoterm_to_subjects_gtex_recount_tcga.json','w') as out_file:
    json.dump(mapped_metadata,out_file)

# with open(WORK_DIR + 'data/recount/metadata/ontoterm_to_subjects_gtex_recount_tcga.json','r') as in_file:
#     mapped_metadata = json.load(in_file)

# term_2_subjtree = {}

# for key in mapped_metadata.keys():

#     # key = 'UBERON:0001062'

#     meta_entry = mapped_metadata[key]

#     term_runs = meta_entry['runs']

#     if 'CVCL' in key:
#         continue
#     elif 'UBERON' in key or 'CL' in key:
#         term = uberon[key]
#     elif 'DOID' in key:
#         term = doid[key]
#     elif 'EFO' in key:
#         term = efo[key]
#     else:
#         continue

#     children = term.children

#     children_ids = map(lambda x: re.sub(' \{.*\}','',x.id),children)
#     # child_entries = map(lambda x: mapped_metadata.get(x,{}),children_ids)

#     term_tree = {}
#     root_terms = term_runs

#     child_terms = []

#     for run in root_terms:
        
#         run_children_ids = filter(lambda x: run in mapped_metadata.get(x,{}).get('runs',[]),children_ids)

#         if len(run_children_ids) > 0:

#             invLabels = map(lambda x: x+': ' + mapped_metadata[x]['name'] ,run_children_ids)
            
#             run_label = ' + '.join(invLabels)

#             tree_entry = term_tree.get(run_label,[])
#             tree_entry.append(run)
#             term_tree[run_label] = tree_entry
#         else:

#             run_label = key + ': ' + term.name
#             tree_entry = term_tree.get(run_label,[])
#             tree_entry.append(run)
#             term_tree[run_label] = tree_entry

#     # for child in children:

#     #     child_id = re.sub(' \{.*\}','',child.id)
#     #     child_entry = mapped_metadata.get(child_id,{})
#     #     child_samples = child_entry.get('runs',[])

#     #     if len(child_entry) > 0: term_tree[child_id+ ': ' +child.name] = child_samples
#     #     child_terms.extend(child_samples)

#     # root_terms = list(set(root_terms) - set(child_terms))

#     # term_tree[key + ': ' + term.name] = root_terms

#     term_2_subjtree[key] = term_tree
#     if len(term_2_subjtree) % 10 == 0: print len(term_2_subjtree)

# with open(WORK_DIR + 'data/recount/metadata/subjtree_combined_gtex_recount_tcga.json','w') as out_file:
#     json.dump(term_2_subjtree,out_file)

with open(WORK_DIR + 'data/recount/metadata/subjtree_combined_gtex_recount_tcga.json','r') as in_file:
    term_2_subjtree = json.load(in_file)
    
metadata_table = []

for key in term_2_subjtree.keys():

    row = [key,mapped_metadata[key]['name']]

    # del mapped_metadata[key]['name']
    row.append(json.dumps(term_2_subjtree[key]))

    metadata_table.append(row)

with open(WORK_DIR + 'data/recount/metasra/all_recount_metasra_subjtree_table.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')
    writer.writerow(['id','name','termTree'])

    for row in metadata_table:
        writer.writerow(row)


print 'done'

