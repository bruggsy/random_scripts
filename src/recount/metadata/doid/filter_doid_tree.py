#!/usr/bin/python

import json

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

with open(WORK_DIR + 'data/recount/metadata/doid/subjtree_doid.json','r') as in_file:
    term_2_subjtree = json.load(in_file)

used_keys = term_2_subjtree.keys()

# with open(WORK_DIR + 'data/recount/metadata/mesh_tree_json.json','r') as in_file:
#     anatomy_tree = json.load(in_file)

with open(WORK_DIR + 'data/recount/metadata/doid/doid_descendants.json','r') as in_file:
    doid_children = json.load(in_file)

with open(WORK_DIR + 'data/recount/metadata/doid/doid_ancestors.json','r') as in_file:
    doid_rparents = json.load(in_file)

with open(WORK_DIR + 'data/recount/metadata/doid/mapped_metadata_doid_new.json','r') as in_file:
    mapped_metadata = json.load(in_file)

filtered_tree = {}
filtered_tree['root'] = []
# filtered_tree['root'] = anatomy_tree['root']

# mesh_rparents['A'] = {'name': 'Anatomy'}

for key in doid_children.keys():

    if not key in used_keys:
        continue

    tree_entry = doid_children[key]

    children_list = []

    for child in tree_entry:
        
        if child['id'] in used_keys:
            
            if len(term_2_subjtree[child['id']]) == 1 and term_2_subjtree[child['id']].keys()[0] == mapped_metadata[child['id']]['name']:
                children_list.append({'id': child['id'].replace(':','_'), 'text': child['name'], 'children': False})
            else:
                children_list.append({'id': child['id'].replace(':','_'), 'text': child['name'], 'children': True})

    
    # tree_entry['children'] = children_list
    # tree_entry['children'] = filter(lambda x: x['id'] in used_keys, tree_entry['children'])

    tree_entry = children_list

    filtered_tree[key] = tree_entry

    if len(doid_rparents.get(key,[1])) == 0:
        filtered_tree['root'].append({'id': key.replace(':','_'), 'text': 'DOID: ' + mapped_metadata[key]['name'],'children': True})


mesh_table = []

for key in filtered_tree.keys():
    tree_entry = filtered_tree[key]
    # line = [key,tree_entry['name'],json.dumps(tree_entry['children'])]

    if key == 'root':
        line = [key.replace(':','_'),'root',json.dumps(tree_entry)]
    else:
        line = [key.replace(':','_'),mapped_metadata[key]['name'],json.dumps(tree_entry)]
    mesh_table.append(line)

with open(WORK_DIR + 'data/recount/metadata/doid_tree_filtered.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')
    writer.writerow(['id','name','children'])
    for line in mesh_table:
        writer.writerow(line)


print 'done'
