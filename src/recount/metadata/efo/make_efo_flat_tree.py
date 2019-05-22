#!/usr/bin/python

import json
import re
import csv
import copy

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

with open(WORK_DIR + 'data/recount/metadata/efo/efo_ols_hierarchical_children.json','r') as in_file:
    efo_children = json.load(in_file)

with open(WORK_DIR + 'data/recount/metadata/efo/subjtree_efo_recount.json','r') as in_file:
    term_2_subjtree = json.load(in_file)

# efo_keys = {}

# for id in efo_children.keys():

#     children_entry = efo_children[id]
#     children_ids = children_entry['children']

#     id.num = id.split(':')[1]

#     part_ids = map(lambda x: id + '.' + x.split(':')[1],children_ids)
    
#     efo_keys[id] = part_ids


terms_to_process = ['EFO:0000001']

all_keys = {'EFO:0000001':'EFO:0000001'}

while len(terms_to_process) > 0:

    term = terms_to_process.pop(0)

    #### using empty get to pre-filter for those with no children entries, since we build child dict from mapped_metadata anyways

    term_children = efo_children.get(term,{}).get('children',[])
    # term_children = efo_children[term]['children']

    for child in term_children:
        
        child_key = all_keys[term]+'.'+child

        all_keys[child] = child_key

        terms_to_process.append(child)

treeNums = {}
    
for term_id in all_keys.keys():

    all_keys_entry = all_keys[term_id]

    ## further filtering based off entries in efo_children here

    term_name = efo_children.get(term_id,{}).get('name',None)

    if term_name:
        treeNums[all_keys_entry] = [term_name,term_id]


used_keys = treeNums.keys()
used_keys = filter(lambda x: treeNums[x][1] in term_2_subjtree.keys(),used_keys)

used_keys.sort()

used_keys_new = []

for key in used_keys:

    key_split = key.split('.')

    add_flag = True

    for i in range(len(key_split)-1):
        key_check = '.'.join(key_split[0:i+1])

        if not key_check in used_keys:
            add_flag = False
    if add_flag:
        used_keys_new.append(key)

used_keys = used_keys_new

cnt = 0

nested_tree = {'root':{}}

for treeNum in used_keys:

    curr_level = copy.deepcopy(nested_tree['root'])

    treeNumSplit = treeNum.split('.')

    numKey = ''

    for i in range(len(treeNumSplit)-1):

        if len(numKey) == 0:
            numKey = treeNumSplit[i]
        else:
            numKey = numKey + '.' + treeNumSplit[i]

        tree_entry = treeNums[numKey]
        num_label = '%s: %s' % (tree_entry[1], tree_entry[0])
        
        next_level = curr_level.get(num_label)
        curr_level = next_level

    tree_entry = treeNums[treeNum]
    num_label = '%s: %s' % (tree_entry[1], tree_entry[0])

    if isinstance(curr_level,list):
        new_level = {num_label: ['']}

    else:
        
        new_level = curr_level
        new_level[num_label] = ['']

    # curr_level = copy.deepcopy(root_term)

    for i in range(len(treeNumSplit)-1):

        curr_level = copy.deepcopy(nested_tree['root'])

        currNum = '.'.join(treeNumSplit[0:len(treeNumSplit) - 1 - i])

        for j in range(len(treeNumSplit) - 2 - i):
            
            key_str = '.'.join(treeNumSplit[0:j+1])
            
            tree_entry = treeNums[key_str]
            num_label = '%s: %s' % (tree_entry[1], tree_entry[0])

            next_level = curr_level.get(num_label)
            curr_level = next_level

        tree_entry = treeNums[currNum]
        num_label = '%s: %s' % (tree_entry[1], tree_entry[0])

        curr_level[num_label] = new_level

        new_level = curr_level

    nested_tree['root'] = new_level

    cnt = cnt + 1

    if cnt % 50 == 0:
        print cnt



with open(WORK_DIR + 'data/recount/metadata/efo/efo_tree_flat.json','w') as out_file:
    json.dump(nested_tree['root'],out_file)


print 'done'


# for treeNum in used_keys:

#     curr_level = copy.deepcopy(nested_tree['EFO:4: disease'])

#     treeNumSplit = treeNum.split('.')

#     numKey = ''

#     for i in range(len(treeNumSplit)-1):

#         if len(numKey) == 0:
#             numKey = treeNumSplit[i]
#         else:
#             numKey = numKey + '.' + treeNumSplit[i]
            
#     tree_entry = treeNums[numKey]
#     num_label = '%s: %s' % (tree_entry[1], tree_entry[0])

#     if isinstance(curr_level,list):
#         new_level = {num_label: ['']}
#     else:
#         new_level = curr_level
#         new_level[num_label] = ['']

#     for i in range(len(treeNumSplit)-1):

#         curr_level = copy.deepcopy(nested_tree['EFO:4: disease'])

#         currNum = '.'.join(treeNumSplit[0:len(treeNumSplit) - 1 - i])
        
#         for j in range(len(treeNumSplit) - 2 - i):
            
#             key_str = '.'.join(treeNumSplit[0:j+1])
            
#             tree_entry = treeNums[key_str]
#             num_label = '%s: %s' % (tree_entry[1], tree_entry[0])
            
#             next_level = curr_level.get(num_label)
#             curr_level = next_level
        
#         tree_entry = treeNums[currNum]
#         num_label = '%s: %s' % (tree_entry[1], tree_entry[0])

#         curr_level[num_label] = new_level

#         new_level = curr_level

#     nested_tree['EFO:4: disease'] = new_level

#     cnt = cnt + 1

#     if cnt % 50 == 0:
#         print cnt
