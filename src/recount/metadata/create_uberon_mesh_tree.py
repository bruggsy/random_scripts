#!/usr/bin/python

import pronto
import re
import csv
import json
import requests

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

with open(WORK_DIR + 'data/uberon_doid_mesh.json','r') as in_file:
    mesh_terms = json.load(in_file)

if not 'uberon' in globals():
    uberon = pronto.Ontology(WORK_DIR + 'downloads/ontologies/uberon_ext.obo')
if not 'efo' in globals():
    efo = pronto.Ontology(WORK_DIR + 'downloads/ontologies/efo.obo')
if not 'doid' in globals() :
    doid = pronto.Ontology(WORK_DIR + 'downloads/ontologies/doid-non-classified.obo')

## first find root terms

uberon_mesh = filter(lambda x: 'UBERON' in x,mesh_terms)

mesh_roots = []

for term_id in uberon_mesh:

    term = uberon[term_id]

    parents = term.rparents()

    mesh_parents = filter(lambda x: x.id in mesh_terms,parents)

    if len(mesh_parents) == 0:
        mesh_roots.append(term_id)





print 'done'

# construct dict of terms to all hierarchical parents
# for each root term:
#   

