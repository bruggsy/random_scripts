#!/usr/bin/python

import json
import csv
import xml.etree.ElementTree as ET
# from lxml import etree

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'


if not 'tree' in locals():
    tree = ET.parse(WORK_DIR + 'downloads/mesh/desc2018.xml')

# parser = etree.XMLParser(dtd_validation=True)
# tree = etree.parse(WORK_DIR + 'downloads/mesh/desc2018.xml',parser)

# class XmlListConfig(list):
#     def __init__(self, aList):
#         for element in aList:
#             if element:
#                 # treat like dict
#                 if len(element) == 1 or element[0].tag != element[1].tag:
#                     self.append(XmlDictConfig(element))
#                 # treat like list
#                 elif element[0].tag == element[1].tag:
#                     self.append(XmlListConfig(element))
#             elif element.text:
#                 text = element.text.strip()
#                 if text:
#                     self.append(text)


# class XmlDictConfig(dict):
#     '''
#     Example usage:

#     >>> tree = ElementTree.parse('your_file.xml')
#     >>> root = tree.getroot()
#     >>> xmldict = XmlDictConfig(root)

#     Or, if you want to use an XML string:

#     >>> root = ElementTree.XML(xml_string)
#     >>> xmldict = XmlDictConfig(root)

#     And then use xmldict for what it is... a dict.
#     '''
#     def __init__(self, parent_element):
#         if parent_element.items():
#             self.update(dict(parent_element.items()))
#         for element in parent_element:
#             if element:
#                 # treat like dict - we assume that if the first two tags
#                 # in a series are different, then they are all different.
#                 if len(element) == 1 or element[0].tag != element[1].tag:
#                     aDict = XmlDictConfig(element)
#                 # treat like list - we assume that if the first two tags
#                 # in a series are the same, then the rest are the same.
#                 else:
#                     # here, we put the list in dictionary; the key is the
#                     # tag name the list elements all share in common, and
#                     # the value is the list itself 
#                     aDict = {element[0].tag: XmlListConfig(element)}
#                 # if the tag has attributes, add those to the dict
#                 if element.items():
#                     aDict.update(dict(element.items()))
#                 self.update({element.tag: aDict})
#             # this assumes that if you've got an attribute in a tag,
#             # you won't be having any text. This may or may not be a 
#             # good idea -- time will tell. It works for the way we are
#             # currently doing XML configuration files...
#             elif element.items():
#                 self.update({element.tag: dict(element.items())})
#             # finally, if there are no child tags and no attributes, extract
#             # the text
#             else:
#                 self.update({element.tag: element.text})

# with open(WORK_DIR + 'downloads/mesh/desc2018.xml','r') as in_file:
#     fileStr = in_file.read()


root = tree.getroot()

# xmldict = XmlDictConfig(root)

# mesh_anatomy = []

treeNum_dict = {}

for child in root:

    for descName in child.iter('DescriptorName'):
        
        for str in descName.iter('String'):
            
            name = str.text

            break

        break

    treeNums = []

    for descID in child.iter('DescriptorUI'):

        id = descID.text

        break

    for treeNumList in child.iter('TreeNumberList'):

        for treeNum in treeNumList.iter('TreeNumber'):

            treeNums.append(treeNum.text)

            treeNum_dict[treeNum.text] = [name,id]


        
    # if len(filter(lambda x: 'A' in x, treeNums)) > 0:

    #     mesh_anatomy.append([id,name,treeNums])

anatomy_keys = filter(lambda x: 'A' in x ,treeNum_dict.keys())
# disease_keys = filter(lambda x: 'C' in x, treeNum_dict.keys())

prev_split_len = 0

anatomy_tree = {}

recursive_parents = {}

for key in anatomy_keys:
    
    key_split = key.split('.')

    child_info = treeNum_dict[key]
    child_id = child_info[1]
    child_name = child_info[0]

    child_entry = recursive_parents.get(child_id,{'name': child_name, 'rparents': [{'name': 'Anatomy', 'id': 'A'}]})

    if len(key_split) > 1:

        parent_key = ''

        for parent_part in key_split:
            
            if len(parent_key) > 0:
                parent_key = parent_key + '.' + parent_part
            else:
                parent_key = parent_part

            parent_info = treeNum_dict[parent_key]
            parent_id = parent_info[1]
            parent_name = parent_info[0]

            child_entry['rparents'].append({'name': parent_name, 'id': parent_id})

    recursive_parents[child_id] = child_entry

# for key in disease_keys:
    
#     key_split = key.split('.')

#     child_info = treeNum_dict[key]
#     child_id = child_info[1]
#     child_name = child_info[0]

#     child_entry = recursive_parents.get(child_id,{'name': child_name, 'rparents': [{'name': 'Disease', 'id': 'C'}]})

#     if len(key_split) > 1:

#         parent_key = ''

#         for parent_part in key_split:
            
#             if len(parent_key) > 0:
#                 parent_key = parent_key + '.' + parent_part
#             else:
#                 parent_key = parent_part

#             parent_info = treeNum_dict[parent_key]
#             parent_id = parent_info[1]
#             parent_name = parent_info[0]

#             child_entry['rparents'].append({'name': parent_name, 'id': parent_id})

#     recursive_parents[child_id] = child_entry
            
        
with open(WORK_DIR + 'data/recount/metadata/mesh_tree_recursive_parents.json','w') as out_file:
    json.dump(recursive_parents,out_file)

for key in anatomy_keys:

    key_split = key.split('.')

    child_info = treeNum_dict[key]
    child_id = child_info[1]
    child_name = child_info[0]

    if len(key_split) > 1:

        parent_treenum = '.'.join(key_split[0:len(key_split)-1])
        parent_info = treeNum_dict[parent_treenum]

        parent_id = parent_info[1]
        parent_name = parent_info[0]

        parent_entry = anatomy_tree.get('%s' % parent_id,{'name': parent_name, 'children': []})
        child_entry = {'text': 'MESH:%s: %s' % (child_id,child_name),
                       'children': True,
                       'id': child_id}
                       

        parent_entry['children'].append(child_entry)

        anatomy_tree['%s' % parent_id] = parent_entry

    else:

        # print key

        entry = anatomy_tree.get('A',{'name': 'Anatomy', 'children': []})

        child_entry = {'text': 'MESH:%s: %s' % (child_id,child_name),
                       'children': True,
                       'id': child_id}

        entry['children'].append(child_entry)
        anatomy_tree['A'] = entry

# for key in disease_keys:

#     key_split = key.split('.')

#     child_info = treeNum_dict[key]
#     child_id = child_info[1]
#     child_name = child_info[0]

#     if len(key_split) > 1:

#         parent_treenum = '.'.join(key_split[0:len(key_split)-1])
#         parent_info = treeNum_dict[parent_treenum]

#         parent_id = parent_info[1]
#         parent_name = parent_info[0]

#         parent_entry = anatomy_tree.get('%s' % parent_id,{'name': parent_name, 'children': []})
#         child_entry = {'text': 'MESH:%s: %s' % (child_id,child_name),
#                        'children': True,
#                        'id': child_id}
                       

#         parent_entry['children'].append(child_entry)

#         anatomy_tree['%s' % parent_id] = parent_entry

#     else:

#         # print key

#         entry = anatomy_tree.get('C',{'name': 'Disease', 'children': []})

#         child_entry = {'text': 'MESH:%s: %s' % (child_id,child_name),
#                        'children': True,
#                        'id': child_id}

#         entry['children'].append(child_entry)
#         anatomy_tree['C'] = entry


anatomy_tree['root'] = {'name': 'root', 'children': [{'text': 'MESH: Anatomy',
                                                       'children': True,
                                                       'id': 'A'}]# ,
                                                     # {'text': 'MESH: Disease',
                                                     #  'children': True,
                                                     #  'id': 'C'}]
}


mesh_table = []

with open(WORK_DIR + 'data/recount/metadata/mesh_tree_json.json','w') as out_file:
    json.dump(anatomy_tree,out_file)

for key in anatomy_tree.keys():
    tree_entry = anatomy_tree[key]
    line = [key,tree_entry['name'],json.dumps(tree_entry['children'])]
    mesh_table.append(line)

# with open(WORK_DIR + 'data/recount/metadata/mesh_keys_used.json','w') as out_file:
#     json.dump(anatomy_tree.keys(),out_file)

with open(WORK_DIR + 'data/recount/metadata/mesh_tree_table.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')
    writer.writerow(['id','name','children'])
    for line in mesh_table:
        writer.writerow(line)
    

        # parent_info = key_split[0:len(key_split)-1]

    

    # if len(key_split) <= prev_split_len:

    #     #do stuff

    #     print 'do stuff'

    # else:

    #     parent  
            


# anatomy_tree = {}

# for row in mesh_anatomy:
    
#     for treeNum in row[2]:
        
#         tree_comps = treeNum.split('.')

#         if len(tree_comps) > 1:

#             parent_entry = anatomy_tree.get(tree_comps[-2])
            
                                            

print 'done'
