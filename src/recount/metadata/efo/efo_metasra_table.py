#!/usr/bin/python

import json
import csv
import urllib
import requests
import re
from itertools import islice

def getParents(term_id):

    ontology = 'EFO'
    term_id = term_id.replace(':','_')

    parents_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s/hierarchicalAncestors' % (ontology,urllib.quote_plus(urllib.quote_plus('http://www.ebi.ac.uk/efo/%s' % term_id))))

    parent_ids = map(lambda x: x[u'iri'].split('/')[-1],parents_req.json().get('_embedded',{}).get('terms',[]))
    
    bad_id_inds = filter(lambda x: not '_' in parent_ids[x],range(len(parents_req.json().get('_embedded',{}).get('terms',[]))))

    for ind in bad_id_inds:

        parent_id = parents_req.json().get('_embedded',{}).get('terms',[])[ind]['annotation'].get('EFO_URI',[''])[0].split('/')[-1].replace('_',':')

        parent_ids[ind] = parent_id

    parent_ids = filter(lambda x: x != '',parent_ids)
    
    return parent_ids

def getChildren(term_id):

    term_id = term_id.replace(':','_')

    if 'UBERON' in term_id:
        ontology = 'uberon'
    elif 'DOID' in term_id:
        ontology = 'doid'
    elif 'CL' in term_id:
        ontology = 'cl'
    elif 'MONDO' in term_id:
        ontology = 'mondo'
    elif 'EFO' in term_id:
        ontology = 'EFO'
    else:
        ontology = term_id.split('_')[0].lower()

    if ontology == 'EFO':
        children_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s/hierarchicalChildren' % (ontology,urllib.quote_plus(urllib.quote_plus('http://www.ebi.ac.uk/efo/%s' % term_id))))
        term_req =  requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s' % ('EFO',urllib.quote_plus(urllib.quote_plus('http://www.ebi.ac.uk/efo/%s' % term_id))))

    elif ontology == 'orphanet':
        children_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s/hierarchicalChildren' % ('efo',urllib.quote_plus(urllib.quote_plus('http://www.orpha.net/ORDO/%s' % term_id))))
        term_req =  requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s' % ('efo',urllib.quote_plus(urllib.quote_plus('http://www.orpha.net/ORDO/%s' % term_id))))

    else:
        children_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s/hierarchicalChildren' % ('EFO',urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/%s' % term_id))))
        term_req =  requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s' % ('EFO',urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/%s' % term_id))))



    child_ids = map(lambda x: x[u'iri'].split('/')[-1],children_req.json().get('_embedded',{}).get('terms',[]))
    
    bad_id_inds = filter(lambda x: not '_' in child_ids[x],range(len(children_req.json().get('_embedded',{}).get('terms',[]))))

    for ind in bad_id_inds:

        child_id = children_req.json().get('_embedded',{}).get('terms',[])[ind]['annotation'].get('EFO_URI',[''])[0].split('/')[-1].replace('_',':')

        child_ids[ind] = child_id

    child_ids = filter(lambda x: x != '',child_ids)

    term_label = term_req.json()['label']
    
    return {'name': term_label, 'children': child_ids}


WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

samples = set([])
samples_2_runs = {}

if not 'metasra' in locals():
    with open(WORK_DIR + 'downloads/metaSRA/metasra.v1-4.json','r') as in_file:
        metasra = json.load(in_file)

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

# # with open(WORK_DIR + 'data/recount/metadata/efo/efo_mapped_metadata.json','r') as in_file:
# #     mapped_metadata = json.load(in_file)

# #     for key in mapped_metadata.keys():
# #         mapped_metadata[key]['runs'] = set(mapped_metadata[key]['runs'])

# with open(WORK_DIR + 'data/recount/metadata/efo/efo_rparents.json','r') as in_file:
#     old_efo_rparents = json.load(in_file)
    
# with open(WORK_DIR + 'data/recount/metadata/efo/efo_used_terms.json','r') as in_file:
#     efo_valid = json.load(in_file)

# # ################## COMMENT THIS OUT JAKE ##################################

# i = 0
# mapped_metadata = {}
# efo_rparents = {}

# # ###################### PLEASE ###############################@#############

# samples = list(samples)
# samples.sort()

# # for sample in samples[(i-10):len(samples)]:
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

#         # old_parent = old_efo_rparents.get(term,None)
#         # if not ('EFO:0000408' in old_parent or 'CL:0000010' in old_parent or 'EFO' in term or term == 'CL:0000010'):
#         #     continue

#         try:
#             valid_flag = efo_valid[term]
#         except KeyError:
#             old_parent = old_efo_rparents.get(term,None)
#             valid_flag = not ('EFO:0000408' in old_parent or 'CL:0000010' in old_parent or 'EFO' in term or term == 'CL:0000010')
#             efo_valid[term] = valid_flag

#         if valid_flag:
#             continue

#         parents = efo_rparents.get(term,None)

#         if not parents:

#             parents = getParents(term)
#             efo_rparents[term] = parents

#         # try:
#         #     valid_flag = efo_valid[term]
#         # except KeyError:
#         #     valid_flag = not ('EFO:0000408' in parents or 'CL:0000010' in parents or 'EFO' in term or term == 'CL:0000010')
#         #     efo_valid[term] = valid_flag

#         # if not 'EFO:0000408' in parents and not 'CL:0000010' in parents and not 'EFO' in term and not term == 'CL:0000010':
#         # if valid_flag:
#         #     continue

# #         # term_label = term.replace(':','_')

# # if not 'EFO' in term and term != 'CL:0000010':
#         #     continue

#         term_entry = mapped_metadata.get(term,None)

#         if not term_entry:

#             term_entry = {}

#             term_entry['runs'] = set(samples_2_runs[sample])
#         else:
#             term_entry['runs'] |= set(samples_2_runs[sample])

#         mapped_metadata[term] = term_entry

#         # if not parents:

#         #     parents = getParents(term)

#         #     efo_rparents[term] = parents

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

#     for line in islice(reader,curr_i,None):
#         if i % 50 == 0:
#             print i

#         i = i + 1

#         samp = line[1].strip('.bw')

#         for term_name in line[3:7]:
#             term_name = re.sub('<','',term_name)
#             term_name = re.sub('>','',term_name)
#             term_split = term_name.split(':')
#             term = term_split[0] + ':' + term_split[1]

#             if not 'EFO' in term:
#                 continue

#             parents = efo_rparents.get(term,None)

#             if not parents:

#                 parents = getParents(term)

#                 efo_rparents[term] = parents


#             if not 'EFO:0000408' in parents and not 'CL:0000010' in parents and not term == 'CL:0000010':
#                 continue
#             # if not 'EFO' in term:
#             #     continue

#             term_entry = mapped_metadata.get(term,None)

#             if not term_entry:

#                 term_entry = {}
#                 term_entry['runs'] = set([samp])
#             else:
#                 term_entry['runs'] |= set([samp])

#             mapped_metadata[term] = term_entry


#             for parent in parents:

#                 term_entry = mapped_metadata.get(parent,None)

#                 if not term_entry:
#                     term_entry = {}
#                     term_entry['runs'] = set([samp])

#                 else:
#                     term_entry['runs'] |= set([samp])

#                 mapped_metadata[parent] = term_entry

# with open(WORK_DIR + 'data/recount/metadata/efo/efo_rparents.json','w') as out_file:
#     json.dump(efo_rparents,out_file)

# with open(WORK_DIR + 'data/recount/metadata/efo/efo_used_terms.json','w') as out_file:
#     json.dump(efo_valid,out_file)

# for term in mapped_metadata.keys():
#     mapped_metadata[term]['runs'] = list(mapped_metadata[term]['runs'])

# with open(WORK_DIR + 'data/recount/metadata/efo/efo_mapped_metadata.json','w') as out_file:
#     json.dump(mapped_metadata,out_file)

# with open(WORK_DIR + 'data/recount/metadata/efo/efo_mapped_metadata.json','r') as in_file:
#     mapped_metadata = json.load(in_file)

########### make children ###############

# efo_children = {}

# i = 0

bad_efo_terms = ['EFO:0001443']

for term in mapped_metadata.keys()[i:]:

    if i % 10 == 0:
        print i
    i = i + 1

    if term in bad_efo_terms:
        continue

    efo_children[term] = getChildren(term)

    # term_id = term.replace(':','_')

    # if 'UBERON' in term_id:
    #     ontology = 'uberon'
    # elif 'DOID' in term_id:
    #     ontology = 'doid'
    # elif 'CL' in term_id:
    #     ontology = 'cl'
    # elif 'MONDO' in term_id:
    #     ontology = 'mondo'
    # elif 'EFO' in term_id:
    #     ontology = 'EFO'
    # else:
    #     ontology = term_id.split('_')[0].lower()

    # # if not ontology == 'orphanet':
    # #     continue
    
    # if ontology == 'EFO':

    #     child_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s/hierarchicalChildren' % ('EFO',urllib.quote_plus(urllib.quote_plus('http://www.ebi.ac.uk/efo/%s' % term_id))))

    #     # child_ids = map(lambda x: x[u'obo_id'],child_req.json().get('_embedded',{}).get('terms',[]))
    #     # child_ids = filter(lambda x: not x is None,child_ids)

    #     # child_ids = map(lambda x: x['annotation']['EFO_URI'][0].split('/')[-1].replace('_',':'),child_req.json().get('_embedded',{}).get('terms',[]))
    #     child_ids = map(lambda x: x['iri'].split('/')[-1].replace('_',':'),child_req.json().get('_embedded',{}).get('terms',[]))

    #     term_req =  requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s' % ('EFO',urllib.quote_plus(urllib.quote_plus('http://www.ebi.ac.uk/efo/%s' % term_id))))
    #     term_label = term_req.json()['label']

    #     efo_children[term] = {'name': term_label, 'children': child_ids}

    # elif ontology == 'orphanet':

    #     print 'a'

    #     child_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s/hierarchicalChildren' % ('efo',urllib.quote_plus(urllib.quote_plus('http://www.orpha.net/ORDO/%s' % term_id))))

    #     child_ids = map(lambda x: x[u'obo_id'],child_req.json().get('_embedded',{}).get('terms',[]))
    #     child_ids = filter(lambda x: not x is None,child_ids)

    #     term_req =  requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s' % ('efo',urllib.quote_plus(urllib.quote_plus('http://www.orpha.net/ORDO/%s' % term_id))))
    #     term_label = term_req.json()['label']

    #     efo_children[term] = {'name': term_label, 'children': child_ids}
        

    # else:

    #     child_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s/hierarchicalChildren' % ('EFO',urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/%s' % term_id))))

    #     child_ids = map(lambda x: x[u'obo_id'],child_req.json().get('_embedded',{}).get('terms',[]))
    #     child_ids = filter(lambda x: not x is None,child_ids)

    #     term_req =  requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s' % ('EFO',urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/%s' % term_id))))
    #     term_label = term_req.json()['label']

    #     efo_children[term] = {'name': term_label, 'children': child_ids}


# with open(WORK_DIR + 'data/recount/metadata/efo/efo_ols_hierarchical_children.json','w') as out_file:
#     json.dump(efo_children,out_file)

# with open(WORK_DIR + 'data/recount/metadata/efo/efo_ols_hierarchical_children.json','r') as in_file:
#     efo_children = json.load(in_file)

# term_2_subjtree = {}

# for key in mapped_metadata.keys():

#     meta_entry = mapped_metadata[key]
#     term_runs = meta_entry['runs']

#     children = efo_children[key]
#     children_ids = children['children']

#     term_tree = {}
#     root_terms = term_runs

#     child_terms = []

#     for run in root_terms:
        
#         run_children_ids = filter(lambda x: run in mapped_metadata.get(x,{}).get('runs',[]),children_ids)

#         run_children_names = map(lambda x: efo_children[x]['name'],run_children_ids)

#         if len(run_children_ids) > 0:
#             run_label = ' + '.join(run_children_names)

#             tree_entry = term_tree.get(run_label,[])
#             tree_entry.append(run)
#             term_tree[run_label] = tree_entry
#         else:
            
#             run_label = efo_children[key]['name']
#             tree_entry = term_tree.get(run_label,[])
#             tree_entry.append(run)
#             term_tree[run_label] = tree_entry

#     term_2_subjtree[key] = term_tree
#     if len(term_2_subjtree) % 10 == 0: print len(term_2_subjtree)

# with open(WORK_DIR + 'data/recount/metadata/efo/subjtree_efo_recount.json','w') as out_file:
#     json.dump(term_2_subjtree,out_file)

# with open(WORK_DIR + 'data/recount/metadata/efo/subjtree_efo_recount.json','r') as in_file:
#     term_2_subjtree = json.load(in_file)

# metadata_table = []

# for key in term_2_subjtree.keys():

#     row = [re.sub(':','_',key),efo_children[key]['name']]

#     row.append(json.dumps(term_2_subjtree[key]))
#     metadata_table.append(row)

# with open(WORK_DIR + 'data/recount/metadata/efo/recount_efo_subjtree_table.csv','w') as out_file:
#     writer = csv.writer(out_file,delimiter=',')
#     writer.writerow(['id','name','termTree'])
    
#     for row in metadata_table:
#         writer.writerow(row)

print 'done'
