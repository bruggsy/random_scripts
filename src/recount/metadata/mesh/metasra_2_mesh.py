#!/usr/bin/python

import pronto
import re
import csv
import json
import requests
import urllib

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
    parents_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s/hierarchicalAncestors' % (ontology,urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/%s' % term_id))))

    # parents_req = requests.get(

    parent_ids = map(lambda x: x[u'obo_id'],parents_req.json()['_embedded']['terms'])
    parent_ids = filter(lambda x: not x is None,parent_ids)
    
    parents = []

    # for p_id in parent_ids:

    #     if 'UBERON' in p_id:
    #         parents.append(uberon[p_id])
    #     elif 'DOID' in p_id:
    #         parents.append(doid[p_id])
    #     elif 'cl' in p_id:
    #         parents.append(uberon[p_id])


    return parent_ids

# def remap_terms_to_mesh(term,mesh_terms):
def remap_terms_to_mesh(term,total_mesh_terms):
    mapped = False
    
    curr_level = [term]

    # if term in mesh_terms.keys():
    if term in total_mesh_terms.keys():
        # mesh_entry = mesh_terms[term]
        mesh_entry = total_mesh_terms[term]

        return (total_mesh_terms[term],total_mesh_terms)
        # return (mesh_terms[term],mesh_terms)

        # if type(mesh_entry) is list:
        #     return (mesh_entry,mesh_terms)
        # else:
        #     return ([mesh_entry],mesh_terms)

    # cnt = 0

    parent_lists = map(lambda x: getParents(x),curr_level)

    parents = []
    for p_list in parent_lists:
        parents.extend(p_list)

    parents = list(set(parents))

    parents = map(lambda x: bad_id_mapping.get(x,x),parents)

    mesh_parents = filter(lambda x: x in mesh_terms.keys(),parents)

    mesh_entries = map(lambda x: mesh_terms[x],mesh_parents)

    new_mesh_entry = []

    for entry in mesh_entries: new_mesh_entry.extend(entry)
    new_mesh_entry = list(set(new_mesh_entry))

    mesh_terms[term] = new_mesh_entry
    
    

    # while not mapped:

    #     cnt = cnt + 1
        
    #     parent_lists = map(lambda x: getParents(x),curr_level)

    #     parents = []

    #     for p_list in parent_lists:
    #         parents.extend(p_list)

    #     parents = list(set(parents))
    #     mesh_parents = filter(lambda x: x in mesh_terms.keys(),parents)

    #     if len(mesh_parents) > 0:
            
    #         mapped = True

    #         mesh_entries = map(lambda x: mesh_terms[x],mesh_parents)

    #         new_mesh_entry = []

    #         for entry in mesh_entries: new_mesh_entry.extend(entry)
    #         new_mesh_entry = list(set(new_mesh_entry))
            
    #         mesh_terms[term] = new_mesh_entry
    #         # mesh_terms[term] = map(lambda x: mesh_terms[x],mesh_parents)
    #         # for parent in mesh_parents: mesh_terms[term] = 

    #     else:
    #         curr_level = parents

    #     if cnt > 20:
    #         mesh_terms[term] = []
    #         return ([],mesh_terms)

    # return (map(lambda x: mesh_terms[x],mesh_parents),mesh_terms)
    return (new_mesh_entry,mesh_terms)
            
    
WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

if not 'uberon' in globals():
    uberon = pronto.Ontology(WORK_DIR + 'downloads/ontologies/uberon_ext.obo')
if not 'efo' in globals():
    efo = pronto.Ontology(WORK_DIR + 'downloads/ontologies/efo.obo')
if not 'doid' in globals() :
    doid = pronto.Ontology(WORK_DIR + 'downloads/ontologies/doid-non-classified.obo')

mesh_children = {}

with open(WORK_DIR + 'data/recount/metadata/mesh_tree_table.csv','r') as in_file:

    reader = csv.reader(in_file,delimiter=',')
    reader.next()

    for line in reader:
        mesh_children[line[0]] = {'name': line[1], 'children': json.loads(line[2])}


if not 'metasra' in locals():
    with open(WORK_DIR + 'downloads/metaSRA/metasra.v1-4.json','r') as in_file:
        metasra = json.load(in_file)

mesh_terms = {}

# with open(WORK_DIR + 'data/recount/metadata/doid_2_mesh.json','r') as in_file:
#     mesh_terms = json.load(in_file)
#     for key in mesh_terms.keys():
#         mesh_terms[key] = [mesh_terms[key]]

with open(WORK_DIR + 'data/recount/metadata/uberon_2_mesh.json','r') as in_file:
    uberon_mesh = json.load(in_file)
    for key in uberon_mesh.keys():
        mesh_terms[key] = [uberon_mesh[key]]

total_mesh_terms = {}

# with open(WORK_DIR + 'data/recount/metadata/uberon_doid_mesh_mapping_parents.json','r') as in_file:
#     mesh_terms = json.load(in_file)

with open(WORK_DIR + 'data/recount/metadata/mesh_tree_recursive_parents.json','r') as in_file:
    mesh_rparents = json.load(in_file)

# if not 'mesh_terms' in locals():
#     with open(WORK_DIR + 'data/uberon_doid_mesh.json','r') as in_file:
#         mesh_terms = json.load(in_file)

samples = set([])

samples_2_runs = {}

# with open(WORK_DIR + 'data/recount/metadata/mesh_tree_recursive_parents.json','r') as out_file:
#     recursive_parents = json.load(out_file)

with open(WORK_DIR + 'data/recount/metadata/mesh_tree_json.json','r') as in_file:
    anatomy_tree = json.load(in_file)

with open(WORK_DIR + 'data/recount/metadata/bad_mesh_ids_remapped.json','r') as in_file:
    bad_id_mapping = json.load(in_file)

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

runs_not_in_metasra = []

bad_ids = set([])

# # ONLY do UBERON & DOID, leave EFO & CL for a separate organizing script
# # only doing UBERON b/c mesh disease is not compatible with the way we're trying to do things.
for sample in samples:

    # if true:
    #     break

    # if sample == 'SRS282710':
    #     break

    meta_entry = metasra.get(sample,None)

    if not meta_entry:
        runs_not_in_metasra = runs_not_in_metasra + samples_2_runs[sample]
        continue
    
    term_list = meta_entry['mapped ontology terms']

    terms_used = filter(lambda x: 'UBERON' in x or 'DOID' in x or 'CL' in x,term_list)

    if len(terms_used) == 0:
        runs_not_in_metasra = runs_not_in_metasra + samples_2_runs[sample]

    for term in term_list:
        
        # if 'CVCL' in key_term:
        #     continue
        # elif 'UBERON' in key_term:
        #     term = uberon[key_term]
        # elif 'CL' in key_term:
        #     term = uberon[key_term]
        # elif 'DOID' in key_term:
        #     term = doid[key_term]
        # elif 'EFO' in key_term:
        #     term = efo[key_term]
        # else:
        #     no_ont_runs |= set(samples_2_runs[sample])

        # if 'UBERON' in term or 'DOID' in term:
        if 'UBERON' in term:
            # mesh_mapped, mesh_terms = remap_terms_to_mesh(term,mesh_terms)
            mesh_mapped, total_mesh_terms = remap_terms_to_mesh(term,total_mesh_terms)
        else:
            continue
            # mesh_mapped = [term]

        for mesh_term in mesh_mapped:

            if '.' in mesh_term:
                mesh_term = bad_id_mapping[mesh_term]
                # bad_ids.add(mesh_term)

            term_entry = mapped_metadata.get(mesh_term,None)

            if not term_entry:

                term_entry = {}
                try: 
                    term_entry['name'] = mesh_rparents[mesh_term]['name']
                except KeyError:
                    bad_ids.add(mesh_term)

                term_entry['runs'] = set(samples_2_runs[sample])
            else:
                term_entry['runs'] |= set(samples_2_runs[sample])

            mapped_metadata[mesh_term] = term_entry

            parents = mesh_rparents[mesh_term]['rparents']
            
            # if not 'EFO' in term and not 'CVCL' in term:
            #     parents = mesh_rparents[mesh_term]
            # else:
            #     parents = []

            # for parent in parents:

            #     term_entry = mapped_metadata.get(parent,None)

            #     if not term_entry:
            #         term_entry = {}

            #         term_entry['runs'] = set(samples_2_runs[sample])
            #     else:
            #         term_entry['runs'] |= set(samples_2_runs[sample])

            #     mapped_metadata[parent] = term_entry

            # parents = recursive_parents[mesh_term]['rparents']

            for parent in parents:

                term_entry = mapped_metadata.get(parent['id'],None)

                if not term_entry:
                    term_entry = {}
                    try:
                        term_entry['name'] = parent['name']
                    except KeyError:
                        bad_ids.add(mesh_term)

                    term_entry['runs'] = set(samples_2_runs[sample])
                else:
                    term_entry['runs'] |= set(samples_2_runs[sample])

                mapped_metadata[parent['id']] = term_entry
    # samples_done.add(sample)

with open(WORK_DIR + 'data/recount/metadata/tcga_sra_pheno.tsv','r') as in_file:

# with open(WORK_DIR + 'tmp/lung_metasra.tsv','r') as in_file:

    reader = csv.reader(in_file,delimiter='\t')

    reader.next()

    for line in reader:
        samp = line[1].strip('.bw')

        for term_name in line[3:7]:
            term_name = re.sub('<','',term_name)
            term_name = re.sub('>','',term_name)
            term_split = term_name.split(':')
            term_id = term_split[0] + ':' + term_split[1]

            if 'UBERON' in term_id:
                mesh_mapped, mesh_terms = remap_terms_to_mesh(term_id,mesh_terms)
            else:
                continue

            for mesh_term in mesh_mapped:

                if '.' in mesh_term:
                    mesh_term = bad_id_mapping[mesh_term]
                # else:
                #     continue

                term_entry = mapped_metadata.get(mesh_term,None)

                if not term_entry:

                    term_entry = {}
                    try:
                        term_entry['name'] = mesh_rparents[mesh_term]['name']
                    except KeyError:
                        bad_ids.add(mesh_term)
                        
                    term_entry['runs'] = set([samp])
                else:
                    term_entry['runs'] |= set([samp])

                mapped_metadata[mesh_term] = term_entry

                parents = mesh_rparents[mesh_term]['rparents']

                for parent in parents:

                    term_entry = mapped_metadata.get(parent['id'],None)

                    if not term_entry:
                        term_entry = {}

                        try:
                            term_entry['name'] = parent['name']
                        except KeyError:
                            bad_ids.add(mesh_term)

                        term_entry['runs'] = set([samp])
                    else:
                        term_entry['runs'] |= set([samp])

                    mapped_metadata[parent['id']] = term_entry


with open(WORK_DIR + 'data/recount/metadata/mesh_tcga_gtex_mapped.tsv','r') as in_file:

# with open(WORK_DIR + 'tmp/lung_metasra.tsv','r') as in_file:

    reader = csv.reader(in_file,delimiter='\t')

    reader.next()

    for line in reader:
        samp = line[0]

        for term_name in line[1:3]:


            for mesh_term in mesh_mapped:

                term_entry = mapped_metadata.get(mesh_term,None)

                if not term_entry:

                    term_entry = {}
                    try:
                        term_entry['name'] = mesh_rparents[mesh_term]['name']
                    except KeyError:
                        bad_ids.add(mesh_term)
                        
                    term_entry['runs'] = set([samp])
                else:
                    term_entry['runs'] |= set([samp])

                mapped_metadata[mesh_term] = term_entry

                parents = mesh_rparents[mesh_term]['rparents']

                for parent in parents:

                    term_entry = mapped_metadata.get(parent['id'],None)

                    if not term_entry:
                        term_entry = {}

                        try:
                            term_entry['name'] = parent['name']
                        except KeyError:
                            bad_ids.add(mesh_term)

                        term_entry['runs'] = set([samp])
                    else:
                        term_entry['runs'] |= set([samp])

                    mapped_metadata[parent['id']] = term_entry
                


for term in mapped_metadata.keys():
    mapped_metadata[term]['runs'] = list(mapped_metadata[term]['runs'])
                                         
with open(WORK_DIR + 'data/recount/metasra/metasra_uberon_as_mesh.json','w') as out_file:
    json.dump(mapped_metadata,out_file)

with open(WORK_DIR + 'data/recount/metasra/uberon_mesh_mapping.json','w') as out_file:
    json.dump(mesh_terms,out_file)

# ######################

with open(WORK_DIR + 'data/recount/metasra/metasra_uberon_as_mesh.json','r') as in_file:
    mapped_metadata = json.load(in_file)

term_2_subjtree = {}

for key in mapped_metadata.keys():

#     # if key == 'D014599':
#     #     break
    
    meta_entry = mapped_metadata[key]
    term_runs = meta_entry['runs']

    children = mesh_children.get(key,{'children': []})
    children_ids = list(set(map(lambda x:  x['id'],children['children'])))

    term_tree = {}
    root_terms = term_runs

    child_terms = []

    for run in root_terms:
        
        run_children_ids = filter(lambda x: run in mapped_metadata.get(x,{}).get('runs',[]),children_ids)

        run_children_names = map(lambda x: mesh_rparents[x]['name'],run_children_ids)

        if len(run_children_ids) > 0:
            run_label = ' + '.join(run_children_names)

            tree_entry = term_tree.get(run_label,[])
            tree_entry.append(run)
            term_tree[run_label] = tree_entry
        else:

            run_label = mesh_rparents[key]['name']
            tree_entry = term_tree.get(run_label,[])
            tree_entry.append(run)
            term_tree[run_label] = tree_entry

    term_2_subjtree[key] = term_tree
    if len(term_2_subjtree) % 10 == 0: print len(term_2_subjtree)


with open(WORK_DIR + 'data/recount/metadata/subjtree_uberon_mesh.json','w') as out_file:
    json.dump(term_2_subjtree,out_file)


with open(WORK_DIR + 'data/recount/metadata/subjtree_uberon_mesh.json','r') as in_file:
    term_2_subjtree = json.load(in_file)


anatomy_entry = term_2_subjtree['A']
new_anatomy_entry = {}

unused_systems = ['Animal Structures','Tissues','Cells','Body Regions','Sense Organs','Fluids and Secretions']

for key in anatomy_entry.keys():

    key_split = key.split(' + ')
    key_split = filter(lambda x: not x in unused_systems,key_split)
    key_split.sort()

    if len(key_split) == 0:
        continue

    new_key = ' + '.join(key_split)

    key_entry = new_anatomy_entry.get(new_key,[])
    key_entry.extend(anatomy_entry[key])
    new_anatomy_entry[new_key] = key_entry


term_2_subjtree['A'] = new_anatomy_entry

metadata_table = []

for key in term_2_subjtree.keys():

    if key == 'A':
        row = [key,'Anatomy']
    else:        
        row = [key,mesh_rparents[key]['name']]

    row.append(json.dumps(term_2_subjtree[key]))

    metadata_table.append(row)

with open(WORK_DIR + 'data/recount/metasra/mesh_uberon_subjtree_table.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')
    writer.writerow(['id','name','termTree'])

    for row in metadata_table:
        writer.writerow(row)

print 'done'
