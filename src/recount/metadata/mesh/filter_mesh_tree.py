#!/usr/bin/python

import json

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

with open(WORK_DIR + 'data/recount/metadata/subjtree_uberon_mesh.json','r') as in_file:
    term_2_subjtree = json.load(in_file)

used_keys = term_2_subjtree.keys()

with open(WORK_DIR + 'data/recount/metadata/mesh_tree_json.json','r') as in_file:
    anatomy_tree = json.load(in_file)

filtered_tree = {}
filtered_tree['root'] = anatomy_tree['root']

mesh_rparents['A'] = {'name': 'Anatomy'}

for key in anatomy_tree.keys():

    if not key in used_keys:
        continue

    tree_entry = anatomy_tree[key]

    children_list = []

    for child in tree_entry['children']:
        
        if child['id'] in used_keys:
            
            if len(term_2_subjtree[child['id']]) == 1 and term_2_subjtree[child['id']].keys()[0] == mesh_rparents[child['id']]['name']:
                children_list.append({'id': child['id'], 'text': child['text'], 'children': False})
            else:
                children_list.append(child)

    
    tree_entry['children'] = children_list
    # tree_entry['children'] = filter(lambda x: x['id'] in used_keys, tree_entry['children'])

    filtered_tree[key] = tree_entry


mesh_table = []

for key in filtered_tree.keys():
    tree_entry = filtered_tree[key]
    line = [key,tree_entry['name'],json.dumps(tree_entry['children'])]
    mesh_table.append(line)

with open(WORK_DIR + 'data/recount/metadata/mesh_tree_table_filtered.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')
    writer.writerow(['id','name','children'])
    for line in mesh_table:
        writer.writerow(line)


print 'done'
