import copy
import json

tissue_flat_tree = {
    'T0: Tissue': {
        'T01: Connective Tissue': {
            'T011: Blood': [""],
            'T012: Adipose Tissue': {
                'T0121: Subcutaneous Adipose Tissue': [""],
                'T0122: Omentum': [""]
            }
        },
        'T02: Epithelium': {
            'T021: Bladder Epithelium': [""],
            'T022: Alveolar Epithelium': [""],
            'T023: Epidermis': [""],
            'T024: Endothelium': {
                'T0241: Endothelium, Vascular': [""]},
            'T025: Mesothelium': {
                'T0251: Pleura': [""]
            }
        },
        'T03: Glandular Tissue': {
            'T031: Exocrine Glands': {
                'T0311: Prostate': [""],
                'T0312: Mammary Gland': [""],
                'T0313: Salivary Gland': [""]
            },
            'T032: Endocrine Glands': {
                'T0321: Pancreas': [""],
                'T0322: Pituitary Gland': [""],
                'T0323: Adrenal Tissue': [""],
                'T0324: Thyroid Gland': [""]
            }
        },
        'T04: Lymphoid Tissue': {
            'T041: Spleen': [""],
            'T042: Thymus': [""],
            'T043: Lymph nodes': [""],
            'T044: Bone Marrow': [""]
        },
        'T05: Muscles': {
            'T051: Smooth Muscle': {
                'T0511: Muscularis Mucosae': [""],
                'T0512: Bladder Wall': [""]
            },
            'T052: Striated Muscle': {
                'T0521: Myocardium': [""],
                'T0522: Skeletal Muscle Tissue': {
                    'T05221: Sphincter': {
                        'T052211: Gastroesophageal Junction': [""]
                        }
                    }
                }
            },
        'T06: Nerve Tissue': {
            'T061: Central Nervous Tissue': {
                'T0611: Brain': [""],
                'T0612: Spinal Cord': [""]
            },
            'T062: Peripheral Nervous Tissue': {
                'T0621: Tibial Nerve': [""]
            }
        },
        'T07: Membranes': {
            'T071: Mucous Membrane': {
                'T0711: Intestinal Mucosa': [""],
                'T0712: Endometrium': [""],
                'T0713: Esophageal Mucosa': [""],
                'T0714: Gastric Mucosa': [""],
                'T0715: Vaginal Mucosa': [""],
                'T0716: Fallopian Tube Mucosa': [""],
                'T0717: Respiratory Mucosa': [""],
                'T0818: Bile Duct Mucosa': [""]
            }
        },
        'T08: Parenchymal Tissue': {
            'T081: Liver Parenchyme': [""],
            'T082: Kidney Parenchyme': {
                'T0821: Kidney Cortex': [""]
            },
            'T083: Ovary': [""],
            'T084: Testis': [""]
        }
    }
}

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

trees_to_parse = [['T0: Tissue', tissue_flat_tree['T0: Tissue']]]

tissue_children = {}

while len(trees_to_parse) > 0:
    
    key = trees_to_parse.pop(0)
    key_split = key[0].split(': ')

    key_tree = key[1]

    entry = {'name': key_split[1]}

    if type(key_tree) is list:
        entry['children'] = []

    else:
        
        children = key_tree.keys()
        children_ids = map(lambda x: x.split(': ')[0],children)

        entry['children'] = children_ids

        for child in children:
            
            trees_to_parse.append([child, key_tree[child]])
    
    tissue_children[key_split[0]] = entry

trees_to_parse = [['T0: Tissue', tissue_flat_tree['T0: Tissue']]]

tissue_parents = {'T0': {'name': 'Tissue', 'parents': []}}

while len(trees_to_parse) > 0:
    
    key = trees_to_parse.pop(0)
    key_split = key[0].split(': ')

    key_tree = key[1]

    if not type(key_tree) is list:
        
        children = key_tree.keys()

        for child in children:
            
            child_split = child.split(': ')

            tissue_parents[child_split[0]] = {'name': child_split[1], 'parents': [key_split[0]]}

            trees_to_parse.append([child,key_tree[child]])

tissue_rparents = copy.deepcopy(tissue_parents)

for key in tissue_parents.keys():

    parents_to_check = copy.deepcopy(tissue_parents[key]['parents'])

    rparents = copy.deepcopy(tissue_parents[key]['parents'])

    while len(parents_to_check) > 0:
        
        parent_to_check = parents_to_check.pop(0)

        parent_entry = tissue_rparents[parent_to_check]
        
        rparents.extend(parent_entry['parents'])

        parents_to_check.extend(parent_entry['parents'])

    tissue_rparents[key]['rparents'] = rparents

with open(WORK_DIR + 'data/recount/metadata/tissue/tissue_rparents.json','w') as out_file:
    json.dump(tissue_rparents,out_file)

with open(WORK_DIR + 'data/recount/metadata/tissue/tissue_children.json','w') as out_file:
    json.dump(tissue_children,out_file)

with open(WORK_DIR + 'data/recount/metadata/tissue/tissue_flat_tree.json','w') as out_file:
    json.dump(tissue_flat_tree,out_file)

print 'done'
