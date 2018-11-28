import pronto
import json
import re
import csv
import numpy as np

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

# uberon = pronto.Ontology(WORK_DIR + 'downloads/ontologies/uberon_ext.obo')
# efo = pronto.Ontology(WORK_DIR + 'downloads/ontologies/efo.obo')
# doid = pronto.Ontology(WORK_DIR + 'downloads/ontologies/doid-non-classified.obo')

with open(WORK_DIR + 'downloads/metaSRA/metasra.v1-4.json','r') as in_file:
    metasra = json.load(in_file)

with open(WORK_DIR + 'data/recount/metadata/tsv_friendly_recount_meta.tsv','r') as in_file:
    reader = csv.reader(in_file,delimiter='\t')
    reader.next()

    samp_ids = map(lambda x: x[2],reader)

mapped_metadata = {}

not_in_metasra = []

for id in np.unique(samp_ids):
    
    metasra_entry = metasra.get(id,None)

    if not metasra_entry:
        not_in_metasra.append(id)
        continue

    term_list = metasra_entry['mapped ontology terms']

    for key_term in term_list:

        if 'CVCL' in key_term:
            continue
        if 'UBERON' in key_term or 'CL' in key_term:
            term = uberon[key_term]
        elif 'DOID' in key_term:
            term = doid[key_term]
        elif 'EFO' in key_term:
            term = efo[key_term]
        else:
            continue

        # first do root term

        term_id = re.sub(' \{.*\}','',term.id)

        term_entry = mapped_metadata.get(term_id,None)

        if not term_entry:

            term_entry = {}

            term_entry['name'] = term.name
            term_entry['samples'] = [id]
        else:

            term_entry['samples'].append(id)

        mapped_metadata[term_id] = term_entry

        # then do parents

        parents = term.rparents()

        for parent in parents:

            parent_id = re.sub(' \{.*\}','',parent.id)
            
            term_entry = mapped_metadata.get(parent_id,None)

            if not term_entry:

                term_entry = {}

                term_entry['name'] = parent.name
                term_entry['samples'] = [id]

            else:

                term_entry['samples'].append(id)

            mapped_metadata[parent_id] = term_entry

            # term_entry.add(id)

            # if(len(term.name) > 0):
                

            # term_entry
    
    # break

for key in mapped_metadata.keys():
    mapped_metadata[key]['samples'] = list(np.unique(mapped_metadata[key]['samples']))

# with open(WORK_DIR + 'data/recount/metadata/ontoterm_to_subjects_recount.json','w') as out_file:
#     json.dump(mapped_metadata,out_file)

# with open(WORK_DIR + 'data/recount/metadata/recount_not_in_metasra.json','w') as out_file:
#     json.dump(not_in_metasra,out_file)

# #### create subject tree
# with open(WORK_DIR + 'data/recount/metadata/ontoterm_to_subjects_recount.json','r') as in_file:
#     mapped_metadata = json.load(in_file)

term_2_subjtree_metasra = {}

for key in mapped_metadata.keys():

    term_entry = mapped_metadata[key]
    
    term_samps = term_entry['samples']

    # term_split = key.split(':')
    # key_term = term_split[0] + ':' + term_split[1]
    # key_term = key_term.strip('<')

    if 'UBERON' in key_term or 'CL' in key:
        term = uberon[key]
    elif 'DOID' in key:
        term = doid[key]
    elif 'EFO' in key:
        term = efo[key]
    else:
        continue
        
    # print term

    children = term.children

    term_tree = {}
    root_terms = term_samps

    child_terms = []

    for child in children:

        child_id = re.sub(' \{.*\}','',child.id)        
        child_entry = mapped_metadata.get(child_id,{})
        child_samples = child_entry.get('samples',[])

        if len(child_entry) > 0: term_tree[child_id] = child_samples
        child_terms.extend(child_samples)

        # child_terms.extend(term_2_subjs_metasra[str(child)])
        # break
                        
    # # = list(diff(set(child_terms),set(root_terms)))

    root_terms = list(set(root_terms) - set(child_terms))
    
    term_tree[key] = root_terms

    term_tree['name'] = term_entry['name']

    term_2_subjtree_metasra[key] = term_tree

    # print term_subjs[1:10]
    # print len(term_subjs)

    # print key

# with open(WORK_DIR + 'data/recount/metasra/term_tree_recount.json','w') as out_file:
#     json.dump(term_2_subjtree_metasra,out_file)

##### make table

with open(WORK_DIR + 'data/recount/metasra/term_tree_recount.json','r') as in_file:
    term_2_subjtree_metasra = json.load(in_file)

out_array = []

for key in term_2_subjtree_metasra.keys():

    term_entry = term_2_subjtree_metasra[key]
    row = [key,term_entry['name']]
    del term_entry['name']
    row.append(term_entry)

    out_array.append(row)

with open(WORK_DIR + 'data/recount/metasra/term_tree_table.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')
    writer.writerow(['id','name','tree'])
    for row in out_array: writer.writerow(row)
    
    
print 'done'


# with open(WORK_DIR + 'data/recount/metadata/recount_metasra.json','r') as in_file:
#     recount_metasra = json.load(in_file)

# term_2_subjs_metasra = {}

# for key in recount_metasra.keys():

#     recount_entry = recount_metasra[key]

#     for parent in recount_entry.keys():

#         parent_entry = term_2_subjs_metasra.get(parent,set([]))

#         if not isinstance(recount_entry[parent],dict):
#             parent_entry.add(key)
#             # parent_entry.add(recount_entry[parent])
#             child_entry = term_2_subjs_metasra.get(recount_entry[parent],set([]))            
#             child_entry.add(key)
#             term_2_subjs_metasra[recount_entry[parent]] = child_entry

#         term_2_subjs_metasra[parent] = parent_entry

#         # if recount_list_metasra[parent]:
#         #     recount_list_metasra[parent].append(key)
#         # else:
#         #     recount_list_metasra[parent] = [key]


# term_2_subjs_json = {}

# for key in term_2_subjs_metasra.keys():
#     term_2_subjs_json[key] = list(term_2_subjs_metasra[key])

# with open(WORK_DIR + 'data/recount/metasra/ontoterm_to_subjects_recount.json','w') as out_file:
#     json.dump(term_2_subjs_json,out_file)
