#!/usr/bin/python

import csv
import json

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

gtex_tissue_detail_mapping = {
    'Lung': 'T0717', # alveolar epithelium --------- respiratory mucosa
    'Brain - Cerebellar Hemisphere': 'T0611', # Brain ##########
    'Heart - Left Ventricle': 'T0521', # myocardium
    'Skin - Sun Exposed (Lower leg)': 'T023', # epidermis
    'Brain - Amygdala': 'T0611', # nerve tissue
    'Adipose - Subcutaneous': 'T0121', # adipose tissue
    'Brain - Cortex': 'T0611', # Brain
    'Uterus': 'T0712', #endometrium
    'Nerve - Tibial': 'T0621', # nerve tissue
    'Muscle - Skeletal': 'T0522', # skeletal muscle
    'Ovary': 'T083', # parenchymal tissue
    'Whole Blood': 'T011', # connective tissue ############
    'Brain - Nucleus accumbens (basal ganglia)':  'T0611', # nerve tissue
    'Colon - Transverse': 'T0711', # intestinal mucosa
    'Adipose - Visceral (Omentum)': 'T0122', # adipose tissue
    'Adrenal Gland': 'T0323', # ##################
    'Brain - Anterior cingulate cortex (BA24)': 'T0611', # 
    'Brain - Substantia nigra': 'T0611', #
    'Thyroid': 'T0324', #  #############
    'Esophagus - Mucosa': 'T0713', # 
    'Artery - Coronary': 'T0241', # #######
    'Esophagus - Muscularis': 'T0511', #muscularis mucosae
    'Brain - Caudate (basal ganglia)': 'T0611',
    'Heart - Atrial Appendage': 'T0521', #myocardium
    'Esophagus - Gastroesophageal Junction': 'T052211',
    'Colon - Sigmoid': 'T0711', # intestinal mucosa
    'Artery - Tibial': 'T0241', # endothelium vascular
    'Liver': 'T081', # liver parenchyme
    'Prostate': 'T0311', # exocrine
    'Testis': 'T084', # parenchymal tissue
    'Cells - Transformed fibroblasts': 'T0',  # no clue where to put these yet, maybe not a tissue?
    'Brain - Putamen (basal ganglia)': 'T0611',
    'Kidney - Cortex': 'T0821', # under parenchymal tissue
    'Pancreas': 'T0321',
    'Stomach': 'T0714', # gastric mucosa
    'Small Intestine - Terminal Ileum': 'T0711', # intestinal mucosa
    'Breast - Mammary Tissue': 'T0312', # mammary gland (exocrine)
    'Brain - Hippocampus': 'T0611',
    'Brain - Cerebellum': 'T0611',
    'Pituitary': 'T0322',
    'Skin - Not Sun Exposed (Suprapubic)': 'T023',
    'Brain - Frontal Cortex (BA9)': 'T0611',
    'Artery - Aorta': 'T0241', # endothelium, vascular
    'Cervix - Ectocervix': 'T0715', # vaginal mucosa
    'Vagina': 'T0715', # vaginal mucosa
    'Cells - Leukemia cell line (CML)': 'T0', # leaving alone for now
    'Brain - Hypothalamus': 'T0611',
    'Spleen': 'T041', # spleen
    'Cells - EBV-transformed lymphocytes': 'T0', # leaving cell types alone
    'Brain - Spinal cord (cervical c-1)': 'T0612', # spinal cord
    'Minor Salivary Gland': 'T0313',
    'Bladder': 'T021', # bladder epithelium
    'Cervix - Endocervix': 'T0715', # vaginal mucosa
    'Fallopian Tube': 'T0716'}  # fallopian tube mucosa

tcga_tissue_detail_mapping = {
    'Liver Hepatocellular Carcinoma': 'T081', # liver parenchyme
    'Prostate Adenocarcinoma': 'T0311', # exocrine
    'Rectum Adenocarcinoma': 'T0711',  # intestinal mucosa
    'Bladder Urothelial Carcinoma': 'T021', # bladder epithelium
    'Brain Lower Grade Glioma': 'T0611', # brain
    'Breast Invasive Carcinoma': 'T0312', # mammry gland
    'Uterine Corpus Endometrial Carcinoma': 'T0712', # endometrium
    'Sarcoma': 'T01',                           # connective tissue
    'Kidney Renal Clear Cell Carcinoma': 'T082', # kidney parenchyme
    'Pheochromocytoma and Paraganglioma': 'T0323',  # adrenal tissue
    'Lymphoid Neoplasm Diffuse Large B-cell Lymphoma': 'T011',  # blood
    'Mesothelioma': 'T0251',  # pleura
    'Thymoma': 'T042',  # thymus
    'Lung Squamous Cell Carcinoma': 'T0717', # respiratory mucosa (bronchi?)
    'Ovarian Serous Cystadenocarcinoma': 'T083', # ovary parenchyme
    'Lung Adenocarcinoma': 'T0717',  # respiratory mucosa
    'Stomach Adenocarcinoma': 'T0714', # gastric mucosa
    'Glioblastoma Multiforme': 'T0611', # brain
    'Acute Myeloid Leukemia': 'T044',  # bone marrow
    'Thyroid Carcinoma': 'T0324', # thyroid gland
    'Thyroid': 'T0324', #thyroid
    'Cervical Squamous Cell Carcinoma and Endocervical Adenocarcinoma': 'T0715', # vaginal mucosa
    'Prostate': 'T0311', # prostate
    'Colon Adenocarcinoma': 'T0711',  # intestinal mucosa
    'Head and Neck Squamous Cell Carcinoma': 'T0',   ########### sinus mucosa... repiratory???
    'Uveal Melanoma': 'T0', ############## uvea?
    'Skin Cutaneous Melanoma': 'T023',  # epidermis
    'Pancreatic Adenocarcinoma': 'T0321',    # pancreas
    'Liver': 'T081', # liver parenchyme
    'Testicular Germ Cell Tumors': 'T084',  # testis parenchyme
    'Lung': 'T0717', # respiratory mucosa
    'Kidney Chromophobe': 'T082', # kidney parenchyme ------- should be changed to epithelium?
    'Breast': 'T0312', # mammary gland
    'Esophageal Carcinoma': 'T0713', # espophageal mucosa
    'Kidney Renal Papillary Cell Carcinoma': 'T082',  # kidney parenchyme
    'Adrenocortical Carcinoma': 'T0323', # adrenal tissue
    'Cholangiocarcinoma': 'T0818', # bile duct mucosa -------- should have parent of duct mucosa?
    # 'Uterine Carcinosarcoma': ['T0712','T01'],  # endometrium & connective tissue ## doesn't include connective tissue component 
    'Uterine Carcinosarcoma': 'T0712',  # temporary
    'Brain':  'T0611', # nerve tissue
    'Heart': 'T0521', # myocardium
    'Skin': 'T023', # epidermis
    'Adipose Tissue': 'T012', # adipose tissue
    'Uterus': 'T0712', # endometrium
    'Nerve': 'T06', # nerve tissue
    'Muscle': 'T05', # Muscles
    'Ovary': 'T083', # ovary parenchyme
    'Blood': 'T011', # connective tissue - blood
    'Colon': 'T0711', # intestinal mucosa
    'Adrenal Gland': 'T0323', # adrenal tissue
    'Thyroid': 'T0324', # thyroid
    'Esophagus': 'T0713', # esophageal mucosa
    'Blood Vessel': 'T0241', # vascular endothelium
    'Liver': 'T081', # liver parenchyme
    'Prostate': 'T0311', # prostate
    'Testis': 'T084', # testis parenchyme
    'Kidney': 'T082', # kidney parenchyme
    'Pancreas': 'T0321', # pancreas
    'Stomach': 'T0714', # gastric mucosa
    'Small Intestine': 'T0711', # intestinal mucosa
    'Breast': 'T0312', # mammary gland
    'Pituitary': 'T0322', # pituitary gland
    'Cervix Uteri': 'T0712', # endometrium
    'Vagina': 'T0715', # vaginal mucosa
    'Bone Marrow': 'T044', # bone marrow
    'Spleen': 'T041', # spleen
    'Salivary Gland': 'T0313',  # salivary gland
    'Bladder': 'T021', # bladder epithelium
    'Fallopian Tube': 'T0716', # fallopian tube mucosa
    'Colorectal': 'T0711', # intestinal mucosa
    'Lymph Nodes': 'T043', # lymph noces
    'Pleura': 'T0251', # pleura
    'Thymus': 'T042', # thymus
    'Eye': 'D005123', ######## ???????????????????????????
    'Bile Duct': 'T0818', # bile duct mucosa
    'Head and Neck': 'T0', ###### same issue as cancer
    'Soft Tissue': 'T01', # connective tissue
    'Cervix': 'T0712'     # endometrium
}

tcga_gtex_df = []

with open(WORK_DIR + 'data/recount/gtex/pheno_r_friendly.tsv','r') as in_file:
    
    reader = csv.reader(in_file,delimiter='\t')
    reader.next()

    for line in reader:
        tcga_gtex_df.append([line[0],line[4],gtex_tissue_detail_mapping[line[4]]])


with open(WORK_DIR + 'data/recount/tcga/pheno_r_friendly.tsv','r') as in_file:
    
    reader = csv.reader(in_file,delimiter='\t')
    reader.next()

    for line in reader:
        tcga_gtex_df.append([line[0],line[4],tcga_tissue_detail_mapping[line[4]]])


with open(WORK_DIR + 'data/recount/metadata/tissue/tissue_tcga_gtex_mapped.tsv','w') as out_file:
    writer = csv.writer(out_file,delimiter='\t')
    writer.writerow(['samp_id','tissue_detail','tissue_detail_mapped'])

    for line in tcga_gtex_df:
        writer.writerow(line)

############### mapping complete ####################

with open(WORK_DIR + 'data/recount/metadata/tissue/tissue_children.json','r') as in_file:
    tissue_children = json.load(in_file)

with open(WORK_DIR + 'data/recount/metadata/tissue/tissue_rparents.json','r') as in_file:
    tissue_rparents = json.load(in_file)

mapped_metadata = {}

for line in tcga_gtex_df:

    samp = line[0]
    tissue_term = line[2]

    term_entry = mapped_metadata.get(tissue_term,None)

    if not term_entry:

        term_entry = {}
        term_entry['name'] = tissue_rparents[tissue_term]['name']

        term_entry['runs'] = set([samp])
    else:
        term_entry['runs'] |= set([samp])

    mapped_metadata[tissue_term] = term_entry

    parents = tissue_rparents[tissue_term]['rparents']

    for parent in parents:

        term_entry = mapped_metadata.get(parent,None)

        if not term_entry:
            term_entry = {}
            
            parent_dat = tissue_rparents[parent]

            term_entry['name'] = parent_dat['name']

            term_entry['runs'] = set([samp])
        else:
            term_entry['runs'] |= set([samp])

        mapped_metadata[parent] = term_entry

for term in mapped_metadata.keys():
    mapped_metadata[term]['runs'] = list(mapped_metadata[term]['runs'])

term_2_subjtree = {}

for key in mapped_metadata.keys():
    
    meta_entry = mapped_metadata[key]
    term_runs = meta_entry['runs']

    children = tissue_children.get(key,{'children':[]})
    children_ids = list(set(children['children']))

    term_tree = {}
    root_terms = term_runs

    child_terms = []

    for run in root_terms:
        
        run_children_ids = filter(lambda x: run in mapped_metadata.get(x,{}).get('runs',[]),children_ids)
        run_children_names = map(lambda x: tissue_rparents[x]['name'],run_children_ids)

        if len(run_children_ids) > 0:
            run_label = ' + '.join(run_children_names)

            tree_entry = term_tree.get(run_label,[])
            tree_entry.append(run)
            term_tree[run_label] = tree_entry
        else:

            run_label = tissue_rparents[key]['name']
            tree_entry = term_tree.get(run_label,[])
            tree_entry.append(run)
            term_tree[run_label] = tree_entry

    term_2_subjtree[key] = term_tree
    if len(term_2_subjtree) % 10 == 0: print len(term_2_subjtree)

metadata_table = []

for key in term_2_subjtree.keys():

    if key == 'T0':
        row = [key,'Tissue']
    else:
        row = [key,tissue_rparents[key]['name']]

    row.append(json.dumps(term_2_subjtree[key]))

    metadata_table.append(row)

with open(WORK_DIR + 'data/recount/metadata/tissue/tissue_subjtree_table.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')
    writer.writerow(['id','name','children'])

    for row in metadata_table:
        writer.writerow(row)

print 'done'
