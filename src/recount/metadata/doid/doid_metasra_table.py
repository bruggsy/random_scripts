#!/usr/bin/python

import json
import csv
import urllib
import requests
import re

def getParents(term_id):

    if 'UBERON' in term_id:
        ontology = 'uberon'
    elif 'DOID' in term_id:
        ontology = 'doid'
    elif 'cl' in term_id:
        ontology = 'cl'


    term_id = term_id.replace(':','_')
    # term_id = term.id
    # term_id = term

    # print ontology
    # print term_id

    # term_r = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/parents?id=%s' % (ontology,urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/%s' % term_id))))
    # parents_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/parents?id=%s' % (ontology,term_id))
    # parents_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s/hierarchicalParents' % (ontology,urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/%s' % term_id))))
    # term_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s' % (ontology,urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/%s' % term_id))))

    parents_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s/hierarchicalAncestors' % (ontology,urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/%s' % term_id))))

    # parents_req = requests.get(

    parent_ids = map(lambda x: x[u'obo_id'],parents_req.json()['_embedded']['terms'])
    parent_ids = filter(lambda x: not x is None,parent_ids)
    
    # parents = []

    # for p_id in parent_ids:

    #     if 'UBERON' in p_id:
    #         parents.append(uberon[p_id])
    #     elif 'DOID' in p_id:
    #         parents.append(doid[p_id])
    #     elif 'cl' in p_id:
    #         parents.append(uberon[p_id])


    return parent_ids

# WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

# samples = set([])
# samples_2_runs = {}

# if not 'metasra' in locals():
#     with open(WORK_DIR + 'downloads/metaSRA/metasra.v1-4.json','r') as in_file:
#         metasra = json.load(in_file)


# # with open(WORK_DIR + 'data/recount/metadata/doid/doid_ancestors.json','r') as in_file:
# #     doid_rparents = json.load(in_file)

# # with open(WORK_DIR + 'data/recount/metadata/doid/doid_descendants.json','r') as in_file:
# #     doid_children = json.load(in_file)

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


# mapped_metadata = {}

# # with open(WORK_DIR + 'data/recount/metadata/doid/mapped_metadata_doid.json','r') as in_file:
# #     mapped_metadata = json.load(in_file)

# # for term in mapped_metadata.keys():
# #     mapped_metadata[term]['runs'] = set(mapped_metadata[term]['runs'])

# with open(WORK_DIR + 'data/recount/metadata/doid/doid_rparents.json','r') as in_file:
#     doid_rparents = json.load(in_file)
    
# # with open(WORK_DIR + 'data/recount/metadata/doid/mapped_metadata_doid_new.json','r') as in_file:
# #     mapped_metadata = json.load(in_file)

# i = 0

# for sample in samples:

#     if i % 50 == 0:
#         print i

#     i = i + 1

#     meta_entry = metasra.get(sample,None)

#     if not meta_entry:
#         # runs_not_in_metasra = runs_not_in_metasra + samples_2_runs[sample]
#         continue
    
#     term_list = meta_entry['mapped ontology terms']

#     # terms_used = filter(lambda x: 'DOID' in x,term_list)
    
#     for term in term_list:

# #         # term_label = term.replace(':','_')

#         if not 'DOID' in term:
#             continue

#         term_entry = mapped_metadata.get(term,None)

#         if not term_entry:

#             term_entry = {}

#             term_entry['runs'] = set(samples_2_runs[sample])
#         else:
#             term_entry['runs'] |= set(samples_2_runs[sample])

#         mapped_metadata[term] = term_entry

#         parents = doid_rparents.get(term,None)

#         if not parents:

#             parents = getParents(term)

#             doid_rparents[term] = parents

#         for parent in parents:

#             term_entry = mapped_metadata.get(parent,None)

#             if not term_entry:
#                 term_entry = {}
#                 term_entry['runs'] = set(samples_2_runs[sample])
#             else:

#                 term_entry['runs'] |= set(samples_2_runs[sample])

#             mapped_metadata[parent] = term_entry

# with open(WORK_DIR + 'data/recount/metadata/tcga_sra_pheno.tsv','r') as in_file:

#     reader = csv.reader(in_file,delimiter='\t')

#     reader.next()

#     for line in reader:
#         if i % 50 == 0:
#             print i

#             i = i + 1


#         samp = line[1].strip('.bw')

#         for term_name in line[3:7]:
#             term_name = re.sub('<','',term_name)
#             term_name = re.sub('>','',term_name)
#             term_split = term_name.split(':')
#             term = term_split[0] + ':' + term_split[1]

#             if not 'DOID' in term:

#                 continue

#             term_entry = mapped_metadata.get(term,None)

#             if not term_entry:

#                 term_entry = {}
#                 term_entry['runs'] = set([samp])
#             else:
#                 term_entry['runs'] |= set([samp])

#             mapped_metadata[term] = term_entry

#             parents = doid_rparents.get(term,None)

#             if not parents:

#                 parents = getParents(term)

#                 doid_rparents[term] = parents

#             for parent in parents:

#                 term_entry = mapped_metadata.get(parent,None)

#                 if not term_entry:
#                     term_entry = {}
#                     term_entry['runs'] = set([samp])

#                 else:
#                     term_entry['runs'] |= set([samp])

#                 mapped_metadata[parent] = term_entry

# with open(WORK_DIR + 'data/recount/metadata/doid/doid_rparents.json','w') as out_file:
#     # doid_rparents = json.load(in_file)
#     json.dump(doid_rparents,out_file)

# for term in mapped_metadata.keys():
#     mapped_metadata[term]['runs'] = list(mapped_metadata[term]['runs'])

# with open(WORK_DIR + 'data/recount/metadata/doid/doid_mapped_metadata.json','w') as out_file:
#     json.dump(mapped_metadata,out_file)

# with open(WORK_DIR + 'data/recount/metadata/doid/doid_mapped_metadata.json','r') as in_file:
#     mapped_metadata = json.load(in_file)

# ########### make children ###############

# doid_children = {}

# i = 0

# for term in mapped_metadata.keys():

#     if i % 10 == 0:
#         print i
#     i = i + 1
    
#     term_id = term.replace(':','_')

#     child_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s/hierarchicalChildren' % ('DOID',urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/%s' % term_id))))

#     child_ids = map(lambda x: x[u'obo_id'],child_req.json().get('_embedded',{}).get('terms',[]))
#     child_ids = filter(lambda x: not x is None,child_ids)

#     term_req =  requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s' % ('DOID',urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/%s' % term_id))))
#     term_label = term_req.json()['label']

#     doid_children[term] = {'name': term_label, 'children': child_ids}

# with open(WORK_DIR + 'data/recount/metadata/doid/doid_ols_hierarchical_children.json','w') as out_file:
#     json.dump(doid_children,out_file)

with open(WORK_DIR + 'data/recount/metadata/doid/doid_ols_hierarchical_children.json','r') as in_file:
    doid_children = json.load(in_file)

# term_2_subjtree = {}

# for key in mapped_metadata.keys():

#     meta_entry = mapped_metadata[key]
#     term_runs = meta_entry['runs']

#     children = doid_children[key]
#     children_ids = children['children']

#     term_tree = {}
#     root_terms = term_runs

#     child_terms = []

#     for run in root_terms:
        
#         run_children_ids = filter(lambda x: run in mapped_metadata.get(x,{}).get('runs',[]),children_ids)

#         run_children_names = map(lambda x: doid_children[x]['name'],run_children_ids)

#         if len(run_children_ids) > 0:
#             run_label = ' + '.join(run_children_names)

#             tree_entry = term_tree.get(run_label,[])
#             tree_entry.append(run)
#             term_tree[run_label] = tree_entry
#         else:
            
#             run_label = doid_children[key]['name']
#             tree_entry = term_tree.get(run_label,[])
#             tree_entry.append(run)
#             term_tree[run_label] = tree_entry

#     term_2_subjtree[key] = term_tree
#     if len(term_2_subjtree) % 10 == 0: print len(term_2_subjtree)

# with open(WORK_DIR + 'data/recount/metadata/doid/subjtree_doid_recount.json','w') as out_file:
#     json.dump(term_2_subjtree,out_file)

with open(WORK_DIR + 'data/recount/metadata/doid/subjtree_doid_recount.json','r') as in_file:
    term_2_subjtree = json.load(in_file)

metadata_table = []

for key in term_2_subjtree.keys():

    row = [re.sub(':','_',key),doid_children[key]['name']]

    row.append(json.dumps(term_2_subjtree[key]))
    metadata_table.append(row)

with open(WORK_DIR + 'data/recount/metadata/doid/recount_doid_subjtree_table.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')
    writer.writerow(['id','name','termTree'])
    
    for row in metadata_table:
        writer.writerow(row)

print 'done'
