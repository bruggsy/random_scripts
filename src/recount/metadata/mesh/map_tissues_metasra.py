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
    elif 'CL' in term_id:
        ontology = 'cl'
    else:
        print term_id


    term_id = term_id.replace(':','_')
    # term_id = term.id
    # term_id = term

    # print ontology
    # print term_id

    # term_r = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/parents?id=%s' % (ontology,urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/%s' % term_id))))
    # parents_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/parents?id=%s' % (ontology,term_id))
    parents_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/%s/terms/%s/hierarchicalParents' % (ontology,urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/%s' % term_id))))

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

def map_tissue(term_id,mesh_terms,tissue_terms):

    # print term_id

    mapped = False
    curr_level = [term_id]

    cnt = 0

    tissue_entry = tissue_terms.get(term_id,None)

    if not tissue_entry is None:
        return (tissue_entry,tissue_terms)

    while not mapped:

        # print curr_level

        cnt = cnt + 1
        parent_lists = map(lambda x: getParents(x),curr_level)

        # print curr_level
        # print parent_lists

        parents = []
        for p_list in parent_lists:
            parents.extend(p_list)

        parents = list(set(parents))

        parents_filtered = filter(lambda x: x in mesh_terms.keys(),parents)
        parents_mesh_lists = map(lambda x: mesh_terms[x],parents_filtered)

        parents_mesh = []

        for p_list in parents_mesh_lists: parents_mesh.extend(p_list)

        parents_mesh = list(set(parents_mesh))

        # parents_mesh = []

        # for parent in parents:
            
        #     # parent_mesh,mesh_terms = remap_terms_to_mesh(parent,mesh_terms)

            

        #     parents_mesh.extend(parent_mesh)

        # parents_mesh_fixed = []

        # print cnt
        # print parents
        # print parents_mesh

        parents_mesh = map(lambda x: bad_id_mapping.get(x,x),parents_mesh)

        # print parents_mesh
        
        # for parent in parents_mesh:

        #     if '.' in parent:
        #         parent = bad_id_mapping[parent]

        #     parents_mesh_fixed

        tissue_parents = filter(lambda x: len(filter(lambda y: y['name'] == 'Tissues',mesh_rparents[x]['rparents'])) > 0,parents_mesh)

        # print tissue_parents

        # tissue_parents = filter(lambda x: x['name'] == 'Tissues', mesh_rparents[mesh_term]['rparents'])
        if len(tissue_parents) > 0:
            mapped  = True

            new_tissue_entry = []
            for entry in tissue_parents: new_tissue_entry.append(entry)
            new_tissue_entry = list(set(new_tissue_entry))

            tissue_terms[term_id] = new_tissue_entry
        else:
            curr_level = parents

        if cnt > 20:
            tissue_terms[term_id] = []
            return ([],tissue_terms)

    return (new_tissue_entry,tissue_terms)

def remap_terms_to_mesh(term,mesh_terms):

    mapped = False
    
    curr_level = [term]

    if term in mesh_terms.keys():
        mesh_entry = mesh_terms[term]

        return (mesh_terms[term],mesh_terms)

        # if type(mesh_entry) is list:
        #     return (mesh_entry,mesh_terms)
        # else:
        #     return ([mesh_entry],mesh_terms)

    cnt = 0

    while not mapped:

        cnt = cnt + 1
        
        parent_lists = map(lambda x: getParents(x),curr_level)

        parents = []

        for p_list in parent_lists:
            parents.extend(p_list)

        parents = list(set(parents))
        mesh_parents = filter(lambda x: x in mesh_terms.keys(),parents)


        if len(mesh_parents) > 0:
            
            mapped = True

            mesh_entries = map(lambda x: mesh_terms[x],mesh_parents)

            new_mesh_entry = []

            for entry in mesh_entries: new_mesh_entry.extend(entry)
            new_mesh_entry = list(set(new_mesh_entry))
            
            mesh_terms[term] = new_mesh_entry
            # mesh_terms[term] = map(lambda x: mesh_terms[x],mesh_parents)
            # for parent in mesh_parents: mesh_terms[term] = 

        else:
            # curr_level = mesh_parents
            curr_level = parents

        if cnt > 20:
            mesh_terms[term] = []
            return ([],mesh_terms)

    # return (map(lambda x: mesh_terms[x],mesh_parents),mesh_terms)
    return (new_mesh_entry,mesh_terms)



WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

# with open(WORK_DIR + 'data/recount/metadata/doid_2_mesh.json','r') as in_file:
#     mesh_terms = json.load(in_file)
#     for key in mesh_terms.keys():
#         mesh_terms[key] = [mesh_terms[key]]

if not 'metasra' in locals():
    with open(WORK_DIR + 'downloads/metaSRA/metasra.v1-4.json','r') as in_file:
        metasra = json.load(in_file)
        

with open(WORK_DIR + 'data/recount/metadata/uberon_2_mesh.json','r') as in_file:
    mesh_terms = json.load(in_file)
    for key in mesh_terms.keys():
        mesh_terms[key] = [mesh_terms[key]]

with open(WORK_DIR + 'data/recount/metadata/mesh_tree_recursive_parents.json','r') as in_file:
    mesh_rparents = json.load(in_file)

samples = set([])

# samples_done = set([])

samples_2_runs = {}

# # with open(WORK_DIR + 'data/recount/metadata/mesh_tree_recursive_parents.json','r') as out_file:
# #     recursive_parents = json.load(out_file)

# with open(WORK_DIR + 'data/recount/metadata/mesh_tree_json.json','r') as in_file:
#     anatomy_tree = json.load(in_file)

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

# tissue_mapping = {}

# with open(WORK_DIR + 'data/recount/metadata/mesh/uberon_mesh_tissue_mapping.json','r') as in_file:
#     tissue_mapping = json.load(in_file)

bad_ids = set([])

for sample in (samples - samples_done):

    meta_entry = metasra.get(sample,None)

    if not meta_entry:
        continue

    term_list = meta_entry['mapped ontology terms']

    for term in term_list:

        if not 'UBERON' in term:
            continue

        # mesh_mapped, mesh_terms = remap_terms_to_mesh(term,mesh_terms)
        
        tissue_mapped, tissue_mapping = map_tissue(term,mesh_terms,tissue_mapping)

        for mesh_term in tissue_mapped:

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
                
                    # if '.' in mesh_term:
            #     mesh_term = bad_id_mapping[mesh_term]

            # term_entry = mapped_metadata

            # tissue_term = tissue_mapping.get(mesh_term,None)

            # if not tissue_term:

            #     # term_parents = mesh_rparents[mesh_term]['rparents']

            #     tissue_term = mesh_term
            #     tissue_mapping[mesh_term] = tissue_term

            #     else:

            #         tissue_term = map_tissue(mesh_term)

    samples_done.add(sample)

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

            if 'UBERON' in term_id:
                tissue_mapped, tissue_mapping = map_tissue(term,mesh_terms,tissue_mapping)
                # mesh_mapped, mesh_terms = remap_terms_to_mesh(term_id,mesh_terms)
            else:
                continue

            for mesh_term in tissue_mapped:

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

                


with open(WORK_DIR + 'data/recount/metadata/mesh/uberon_mesh_tissue_mapping.json','w') as out_file:
    json.dump(tissue_mapping,out_file)

for term in mapped_metadata.keys():
    mapped_metadata[term]['runs'] = list(mapped_metadata[term]['runs'])
                                         
with open(WORK_DIR + 'data/recount/metasra/metasra_uberon_as_mesh_tissues.json','w') as out_file:
    json.dump(mapped_metadata,out_file)


print 'done'
