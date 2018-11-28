#!/usr/bin/python

import pronto
import json
import requests

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'


# if not uberon:
#     uberon = pronto.Ontology(WORK_DIR + 'downloads/ontologies/uberon_ext.obo')
# if not efo:
#     efo = pronto.Ontology(WORK_DIR + 'downloads/ontologies/efo.obo')
# if not doid:
#     doid = pronto.Ontology(WORK_DIR + 'downloads/ontologies/doid-non-classified.obo')


# mesh_terms = {}

# term_req = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/doid/terms')

# terms = term_req.json()

# number_pages = terms['page']['totalPages']

# print number_pages

# mesh_flag = False

# for i in range(number_pages):

#     print i

#     term_req = requests.get('https://www.ebi.ac.uk/ols/api/ontologies/doid/terms?page=%d&size=20' % (i+1))

#     terms = term_req.json()

#     for term in terms['_embedded']['terms']:

#         if term['obo_xref']:
#             mesh_xrefs = filter(lambda x: x['database'] == 'MESH', term['obo_xref'])
#         else:
#             mesh_xrefs = []



#         if len(mesh_xrefs) > 0:
#             mesh_terms[term['obo_id']] = mesh_xrefs[0]['id']

#     #     if mesh_flag: break


#     # if mesh_flag: break

# with open(WORK_DIR + 'data/recount/metadat/doid_2_mesh.json','w') as out_file:
#     json.dump(mesh_terms,out_file)


with open(WORK_DIR + 'data/recount/metadata/mesh_treenum_hash.json','r') as in_file:
    treeNum_dict = json.load(in_file)

with open(WORK_DIR + 'data/recount/metadata/doid_2_mesh.json','r') as in_file:
    mesh_doid = json.load(in_file)

with open(WORK_DIR + 'data/recount/metadata/uberon_2_mesh.json','r') as in_file:
    mesh_uberon = json.load(in_file)

fixed_mesh = {}

for key in mesh_doid.keys():

    mesh_term = mesh_doid[key]

    if '.' in mesh_term:

        print mesh_term
        print treeNum_dict[mesh_term]
        fixed_mesh[key] = treeNum_dict[mesh_term][1]
        print mesh_doid[key]
        break
    else:
        fixed_mesh[key] = mesh_term
        
term_2_fix = []

for key in mesh_uberon.keys():

    mesh_term = mesh_uberon[key]

    if '.' in mesh_term:

        print mesh_term
        print treeNum_dict[mesh_term]
        fixed_mesh[key] = treeNum_dict[mesh_term][1]
        print mesh_uberon[key]
        break
    else:
        fixed_mesh[key] = mesh_term
        
    

# for term_id in uberon.terms.keys():

#     id_num = term_id.split(':')[0]

#     term_request = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/uberon/terms/%s' % (urllib.quote_plus(urllib.quote_plus('http://purl.obolibrary.org/obo/UBERON_%s' % id_num))))

#     break

    # xrefs = uberon[term_id].other.get('xref',[])

    # mesh = filter(lambda x: 'MESH' in x,xrefs)

    # # for mesh_term in mesh:

    # if len(mesh) > 0:
    #     mesh_terms[term_id] = mesh_term

    # if len(mesh) > 0:


        
    #     mesh_terms.append(term_id)


# for term_id in doid.terms.keys():

#     xrefs = doid[term_id].other.get('xref',[])

#     mesh = filter(lambda x: 'MESH' in x,xrefs)

#     # for mesh_term in mesh:
#     if len(mesh) > 0:
#         mesh_terms[term_id] = mesh_term

#     # if len(mesh) > 0:
#     #     mesh_terms.append(term_id)


# with open(WORK_DIR + 'data/uberon_doid_mesh.json','w') as out_file:
#     json.dump(mesh_terms,out_file)


print 'done'
