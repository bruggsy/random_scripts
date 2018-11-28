import json
import csv
import copy

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

with open(WORK_DIR + 'data/recount/metadata/subjtree_uberon_mesh.json','r') as in_file:
    term_2_subjtree = json.load(in_file)

mapped_keys = term_2_subjtree.keys()

with open(WORK_DIR + 'data/recount/metadata/mesh_treenum_hash.json','r') as in_file:
    treeNums = json.load(in_file)

# nested_tree = {'A': {'name': 'Anatomy',
#                      'id': 'A',
#                      'children': {}}}

nested_tree = {'A: Anatomy': {}}

unused_anatomy_children = ['A01','A09','A10','A11','A12','A13','A18','A19','A20','A21']

used_keys = treeNums.keys()
used_keys = filter(lambda x: 'A' in x and len(filter(lambda y: y in x,unused_anatomy_children)) == 0,used_keys)
# used_keys = filter(lambda treeNum: 'A' in treeNum and not 'A01' in treeNum and not 'A09' in treeNum and not 'A13' in treeNum and not 'A18' in treeNum and not 'A19' in treeNum and not 'A20' in treeNum and not 'A21' in treeNum,used_keys)
# used_keys = filter(lambda treeNum: 'A' in treeNum and not 'A01' in treeNum and not 'A09' in treeNum and not 'A13' in treeNum and not 'A18' in treeNum and not 'A19' in treeNum and not 'A20' in treeNum and not 'A21' in treeNum and not 'A10' in treeNum and not 'A11' in treeNum,used_keys)
used_keys = filter(lambda x: treeNums[x][1] in mapped_keys,used_keys)

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

# root_term = nested_tree['A: Anatomy']

cnt = 0

for treeNum in used_keys:

    curr_level = copy.deepcopy(nested_tree['A: Anatomy'])

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

        curr_level = copy.deepcopy(nested_tree['A: Anatomy'])

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

    nested_tree['A: Anatomy'] = new_level

    cnt = cnt + 1

    if cnt % 50 == 0:
        print cnt
        

with open(WORK_DIR + 'data/recount/metadata/mesh_tree_flat.json','w') as out_file:
    json.dump(nested_tree,out_file)


        
print 'done'
