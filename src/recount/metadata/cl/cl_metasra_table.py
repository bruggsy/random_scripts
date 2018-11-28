#!/usr/bin/python

import json
import csv
import urllib

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

samples = set([])
samples_2_runs = {}

if not 'metasra' in locals():
    with open(WORK_DIR + 'downloads/metaSRA/metasra.v1-4.json','r') as in_file:
        metasra = json.load(in_file)


with open(WORK_DIR + 'data/recount/metadata/doid/doid_ancestors.json','r') as in_file:
    doid_rparents = json.load(in_file)

with open(WORK_DIR + 'data/recount/metadata/doid/doid_descendants.json','r') as in_file:
    doid_children = json.load(in_file)

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

# with open(WORK_DIR + 'data/recount/metadata/doid/mapped_metadata_doid.json','r') as in_file:
#     mapped_metadata = json.load(in_file)

# for term in mapped_metadata.keys():
#     mapped_metadata[term]['runs'] = set(mapped_metadata[term]['runs'])
    
with open(WORK_DIR + 'data/recount/metadata/doid/mapped_metadata_doid_new.json','r') as in_file:
    mapped_metadata = json.load(in_file)

# for sample in samples:

#     meta_entry = metasra.get(sample,None)

#     if not meta_entry:
#         runs_not_in_metasra = runs_not_in_metasra + samples_2_runs[sample]
#         continue
    
#     term_list = meta_entry['mapped ontology terms']

#     for term in term_list:

#         # term_label = term.replace(':','_')

#         if not 'DOID' in term:
#             continue


#         term_entry = mapped_metadata.get(term,None)

#         if not term_entry:
            
#             term_entry = {}
            
#             # print 'http://www.ebi.ac.uk/ols/api/ontologies/doid/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F%s' % term.replace(':','_')

#             # print 'http://www.ebi.ac.uk/ols/api/ontologies/doid/%s' % urllib.quote(urllib.quote('http://purl.obolibrary.org/obo/%s' % term.replace(':','_'),safe=''),safe='')

#             term_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/doid/terms/%s' % urllib.quote(urllib.quote('http://purl.obolibrary.org/obo/%s' % term.replace(':','_'),safe=''),safe=''))

#             # term_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/doid/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252F%s' % term.replace(':','_'))

#             term_label = term_req.json()['label']

#             term_entry['name'] = term_label

#             term_entry['runs'] = set(samples_2_runs[sample])

#         else:

#             term_entry['runs'] |= set(samples_2_runs[sample])

#         mapped_metadata[term] = term_entry

#         parents = doid_rparents.get(term,None)

#         if not parents:
#             parent_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/doid/terms/%s/ancestors?size=100' % urllib.quote(urllib.quote('http://purl.obolibrary.org/obo/%s' % term.replace(':','_'),safe=''),safe=''))
#             parent_data = parent_req.json()

#             parent_terms = filter(lambda x: x['obo_id'],parent_data['_embedded']['terms'])
            
#             parents = map(lambda x: {'id': x['obo_id'], 'name': x['label']},parent_terms)

#             doid_rparents[term] = parents
            

#         for parent in parents:
            
#             term_entry = mapped_metadata.get(parent['id'],None)

#             if not term_entry:
                
#                 term_entry = {}

#                 term_entry['name'] = parent['name']

#                 term_entry['runs'] = set(samples_2_runs[sample])
#             else:
#                 term_entry['runs'] |= set(samples_2_runs[sample])

#             mapped_metadata[parent['id']] = term_entry


# with open(WORK_DIR + 'data/recount/metadata/tcga_sra_pheno.tsv','r') as in_file:

#     reader = csv.reader(in_file,delimiter='\t')

#     reader.next()

#     for line in reader:
#         samp = line[1].strip('.bw')

#         for term_name in line[3:7]:
#             term_name = re.sub('<','',term_name)
#             term_name = re.sub('>','',term_name)
#             term_split = term_name.split(':')
#             term_id = term_split[0] + ':' + term_split[1]

#             if not 'DOID' in term_id:
#                 continue
# #                 # mesh_mapped = [term_id]

#             # term_entry = mapped_metadata[term_id]

#             term_entry = mapped_metadata.get(term_id,None)

#             if not term_entry:
            
#                 term_entry = {}

#                 term_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/doid/terms/%s' % urllib.quote(urllib.quote('http://purl.obolibrary.org/obo/%s' % term.replace(':','_'),safe=''),safe=''))

#                 term_label = term_req.json()['label']

#                 term_entry['name'] = term_label

#                 term_entry['runs'] = set([samp])

#             else:

#                 term_entry['runs'] |= set([samp])

#             mapped_metadata[term_id] = term_entry
        
#             parents = doid_rparents.get(term_id,None)

#             if not parents:
#                 parent_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/doid/terms/%s/ancestors?size=100' % urllib.quote(urllib.quote('http://purl.obolibrary.org/obo/%s' % term_id.replace(':','_'),safe=''),safe=''))
#                 parent_data = parent_req.json()

#                 parent_terms = filter(lambda x: x['obo_id'],parent_data['_embedded']['terms'])
            
#                 parents = map(lambda x: {'id': x['obo_id'], 'name': x['label']},parent_terms)

#                 doid_rparents[term] = parents

#             for parent in parents:
                
#                 term_entry = mapped_metadata.get(parent['id'],None)

#                 if not term_entry:
                    
#                     term_entry = {}

#                     term_entry['name'] = parent['name']

#                     term_entry['runs'] = set([samp])

#                 else:

#                     term_entry['runs'] |= set([samp])

#                 mapped_metadata[parent['id']] = term_entry


# for term in mapped_metadata.keys():
#     mapped_metadata[term]['runs'] = list(mapped_metadata[term]['runs'])

# with open(WORK_DIR + 'data/recount/metadata/doid/mapped_metadata_doid_new.json','w') as out_file:
#     json.dump(mapped_metadata,out_file)

# with open(WORK_DIR + 'data/recount/metadata/doid/doid_ancestors.json','w') as out_file:
#     json.dump(doid_rparents,out_file)

# term_2_subjtree = {}

# for key in mapped_metadata.keys():

#     meta_entry = mapped_metadata[key]
#     term_runs = meta_entry['runs']

#     children = doid_children.get(key,None)

#     if not children:
#         children_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/doid/terms/%s/children?size=100' % urllib.quote(urllib.quote('http://purl.obolibrary.org/obo/%s' % key.replace(':','_'),safe=''),safe=''))

#         children_data = children_req.json()

#         children_terms = filter(lambda x: x['obo_id'],children_data.get('_embedded',{'terms': []})['terms'])
#         children = map(lambda x: {'id': x['obo_id'], 'name': x['label']},children_terms)

#         doid_children[key] = children

#     # children_ids = list(set(map(lambda x: x['id'],children['children'])))
#     children_ids = list(set(map(lambda x: x['id'],children)))

#     term_tree = {}
#     root_terms = term_runs

#     child_terms = []

#     for run in root_terms:

#         run_children = filter(lambda x: run in mapped_metadata.get(x['id'],{}).get('runs',[]),children)

#         run_children_ids = map(lambda x: x['id'],run_children)
#         run_children_names = map(lambda x: x['name'],run_children)

#         if len(run_children_ids) > 0:
#             run_label = ' + '.join(run_children_names)

#             tree_entry = term_tree.get(run_label,[])
#             tree_entry.append(run)
#             term_tree[run_label] = tree_entry

#         else:

#             run_label = mapped_metadata[key]['name']
#             tree_entry = term_tree.get(run_label,[])
#             tree_entry.append(run)
#             term_tree[run_label] = tree_entry

#     term_2_subjtree[key] = term_tree
#     if len(term_2_subjtree) % 10 == 0: print len(term_2_subjtree)

# with open(WORK_DIR + 'data/recount/metadata/doid/subjtree_doid.json','w') as out_file:
#     json.dump(term_2_subjtree,out_file)

with open(WORK_DIR + 'data/recount/metadata/doid/subjtree_doid.json','r') as in_file:
    term_2_subjtree = json.load(in_file)


metadata_table = []

for key in term_2_subjtree.keys():
    row = [key.replace(':','_'),mapped_metadata[key]['name']]

    row.append(json.dumps(term_2_subjtree[key]))

    metadata_table.append(row)

with open(WORK_DIR + 'data/recount/metadata/doid/doid_subjtree_table.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')
    writer.writerow(['id','name','termTree'])

    for row in metadata_table:
        writer.writerow(row)

with open(WORK_DIR + 'data/recount/metadata/doid/doid_descendants.json','w') as out_file:
    json.dump(doid_children,out_file)


print 'done'
