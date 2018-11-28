import pronto
import json
import re
import csv
import numpy as np

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

# uberon = pronto.Ontology(WORK_DIR + 'downloads/ontologies/uberon_ext.obo')
# efo = pronto.Ontology(WORK_DIR + 'downloads/ontologies/efo.obo')
# doid = pronto.Ontology(WORK_DIR + 'downloads/ontologies/doid-non-classified.obo')

# with open(WORK_DIR + 'data/recount/gtex/tsv_friendly_gtex_meta.tsv','r') as in_file:
#     reader = csv.reader(in_file,delimiter='\t')
#     reader.next()

#     samp_ids = map(lambda x: x[2],reader)

# mapped_metadata = {}

# with open(WORK_DIR + 'data/recount/metadata/tcga_sra_pheno.tsv','r') as in_file:
#     reader = csv.reader(in_file,delimiter='\t')

#     reader.next()

#     for line in reader:

#         samp_id = line[1].strip('.bw')

#         for term_name in line[3:7]:

#             term_name = re.sub('<','',term_name)
#             term_name = re.sub('>','',term_name)
#             term_split = term_name.split(':')
#             term_id = term_split[0] + ':' + term_split[1]

#             if 'CVCL' in term_id:
#                 continue
#             if 'UBERON' in term_id or 'CL' in term_id:
#                 ont_term = uberon[term_id]
#             elif 'DOID' in term_id:
#                 ont_term = doid[term_id]
#             elif 'EFO' in term_id:
#                 ont_term = efo[term_id]
#             else:
#                 continue

#             term_id = re.sub(' \{.*\}','',ont_term.id)

#             term_entry = mapped_metadata.get(term_id,None)

#             if not term_entry:

#                 term_entry = {}

#                 term_entry['name'] = ont_term.name
#                 term_entry['samples'] = [samp_id]
#             else:

#                 term_entry['samples'].append(samp_id)

#             mapped_metadata[term_id] = term_entry

#             parents = ont_term.rparents()

#             for parent in parents:

#                 parent_id = re.sub(' \{.*\}','',parent.id)

#                 term_entry = mapped_metadata.get(parent_id,None)

#                 if not term_entry:
#                     term_entry = {}

#                     term_entry['name'] = parent.name
#                     term_entry['samples'] = [samp_id]
#                 else:

#                     term_entry['samples'].append(samp_id)

#                 mapped_metadata[parent_id] = term_entry

# for key in mapped_metadata.keys():
#     mapped_metadata[key]['samples'] = list(np.unique(mapped_metadata[key]['samples']))

# with open(WORK_DIR + 'data/recount/metadata/tcga_term_2_samp.json','w') as out_file:
#     json.dump(mapped_metadata,out_file)

# #### create subject tree



with open(WORK_DIR + 'data/recount/metadata/ontoterm_to_subjects_gtex.json','r') as in_file:
    mapped_metadata = json.load(in_file)

term_2_subjtree_metasra = {}

for key in mapped_metadata.keys():

    term_entry = mapped_metadata[key]
    
    term_samps = term_entry['samples']

    # term_split = key.split(':')
    # key_term = term_split[0] + ':' + term_split[1]
    # key_term = key_term.strip('<')

    if 'UBERON' in key or 'CL' in key:
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

with open(WORK_DIR + 'data/recount/metasra/term_tree_tcga.json','w') as out_file:
    json.dump(term_2_subjtree_metasra,out_file)

# #### make table

# with open(WORK_DIR + 'data/recount/metasra/term_tree_gtex.json','r') as in_file:
#     term_2_subjtree_metasra = json.load(in_file)


out_array = []

for key in term_2_subjtree_metasra.keys():

    term_entry = term_2_subjtree_metasra[key]
    row = [key,term_entry['name']]
    del term_entry['name']
    row.append(term_entry)

    out_array.append(row)

with open(WORK_DIR + 'data/recount/metasra/term_tree_table_tcga.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')
    writer.writerow(['id','name','tree'])
    for row in out_array: writer.writerow(row)
    
    
print 'done'
