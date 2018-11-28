import json
import csv
import re
import sys

#### NOW MODIFIED TO COMBINE TABLES


WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

total_table = []

csv.field_size_limit(sys.maxsize)

with open(WORK_DIR + 'data/recount/metasra/mesh_uberon_subjtree_table.csv','r') as in_file:
    reader = csv.reader(in_file,delimiter=',')
    reader.next()
    for line in reader:
        total_table.append(line)

with open(WORK_DIR + 'data/recount/metadata/doid/doid_subjtree_table.csv','r') as in_file:
    reader = csv.reader(in_file,delimiter=',')
    reader.next()
    for line in reader:
        total_table.append(line)

with open(WORK_DIR + 'data/recount/metasra/all_ontologies_subjtree_table.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')

    writer.writerow(['id','name','termtree'])
    for line in total_table:
        writer.writerow(line)



# with open(WORK_DIR + 'data/recount/metasra/term_tree_gtex.json','r') as in_file:
#     term_2_subjtree_gtex = json.load(in_file)

# with open(WORK_DIR + 'data/recount/metasra/term_tree_recount.json','r') as in_file:
#     term_2_subjtree_recount = json.load(in_file)

# with open(WORK_DIR + 'data/recount/metasra/term_tree_tcga.json','r') as in_file:
#     term_2_subjtree_tcga = json.load(in_file)


# samples_2_runs = {}

# with open(WORK_DIR + 'data/recount/gtex/tsv_friendly_gtex_meta.tsv','r') as in_file:
#     reader = csv.reader(in_file,delimiter='\t')
#     reader.next()
    
#     for line in reader:

#         sample = line[2]
#         run = line[4]

#         sample_entry = samples_2_runs.get(sample,[])
#         sample_entry.append(run)
#         samples_2_runs[sample] = sample_entry

# with open(WORK_DIR + 'data/recount/metadata/tsv_friendly_recount_meta.tsv','r') as in_file:
#     reader = csv.reader(in_file,delimiter='\t')
#     reader.next()
    
#     for line in reader:

#         sample = line[2]
#         run = line[4]

#         sample_entry = samples_2_runs.get(sample,[])
#         sample_entry.append(run)
#         samples_2_runs[sample] = sample_entry

# all_keys = set(term_2_subjtree_gtex.keys() +
#                term_2_subjtree_recount.keys() +
#                term_2_subjtree_tcga.keys())


# mapped_metadata = {}

# for key in all_keys:
    
#     recount_entry = term_2_subjtree_recount.get(key,{})
#     tcga_entry = term_2_subjtree_tcga.get(key,{})    
#     gtex_entry = term_2_subjtree_gtex.get(key,{})

#     combined_entry = {}

#     if len(recount_entry) > 0:
#         combined_entry['name'] = recount_entry['name']
#     elif len(tcga_entry) > 0:
#         combined_entry['name'] = tcga_entry['name']
#     elif len(gtex_entry) > 0:
#         combined_entry['name'] = gtex_entry['name']
#     else:
#         print key
#         print "combined key doesn't exist in any tree?"
#         continue
#     # remap gtex
        


#     children_keys = set(recount_entry.keys() +
#                         tcga_entry.keys() +
#                         gtex_entry.keys())

#     children_keys.remove('name')

#     for child in children_keys:

#         tcga_child = tcga_entry.get(child,[])
#         gtex_child = gtex_entry.get(child,[])
#         recount_child = recount_entry.get(child,[])

#         if u's' in recount_child:
#             print child

#         gtex_runs = reduce(lambda x,y: x+samples_2_runs[y],gtex_child,[])
#         recount_runs = reduce(lambda x,y: x+samples_2_runs[y],recount_child,[])

#         combined_entry[child] = gtex_runs + recount_runs + tcga_child

#     mapped_metadata[key] = combined_entry

# with open(WORK_DIR + 'data/recount/metasra/ontoterm_to_subjects_recount.json','w') as out_file:
#     json.dump(mapped_metadata,out_file)

# with open(WORK_DIR + 'data/recount/metasra/ontoterm_to_subjects_recount.json','r') as in_file:
#     mapped_metadata = json.load(in_file)

# metadata_table = []

# for key in mapped_metadata.keys():

#     row = [key,mapped_metadata[key]['name']]

#     del mapped_metadata[key]['name']
#     row.append(json.dumps(mapped_metadata[key]))

#     metadata_table.append(row)

# with open(WORK_DIR + 'data/recount/metasra/all_recount_metasra_table.csv','w') as out_file:
#     writer = csv.writer(out_file,delimiter=',')
#     writer.writerow(['id','name','termTree'])

#     for row in metadata_table:
#         writer.writerow(row)
    


print 'done'
