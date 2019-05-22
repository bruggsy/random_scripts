#!/usr/bin/python

import csv

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

gtex_tissue_general_mapping = {
    'Lung': 'D008168',
    'Brain': 'D001921',
    'Heart': 'D006321',
    'Skin': 'D012867',
    'Adipose Tissue': 'D000273',
    'Uterus': 'D014599',
    'Nerve': 'D009474',
    'Muscle': 'D009132',
    'Ovary': 'D010053',
    'Blood': 'D001769',
    'Colon': 'D003106',
    'Adrenal Gland': 'D000311',
    'Thyroid': 'D013961',
    'Esophagus': 'D004947',
    'Blood Vessel': 'D001808',
    'Liver': 'D008099',
    'Prostate': 'D011467',
    'Testis': 'D013737',
    'Kidney': 'D007668',
    'Pancreas': 'D010179',
    'Stomach': 'D013270',
    'Small Intestine': 'D007421',
    'Breast': 'D001940',
    'Pituitary': 'D010902',
    'Cervix Uteri': 'D002584',
    'Vagina': 'D014621',
    'Bone Marrow': 'D001853',
    'Spleen': 'D013154',
    'Salivary Gland': 'D012469',
    'Bladder': 'D001743',
    'Fallopian Tube': 'D005187'}

gtex_tissue_detail_mapping = {
    'Lung': 'D008168',
    'Brain - Cerebellar Hemisphere': 'D002531',
    'Heart - Left Ventricle': 'D006352',
    'Skin - Sun Exposed (Lower leg)': 'D012867',
    'Brain - Amygdala': 'D000679',
    'Adipose - Subcutaneous': 'D050151',
    'Brain - Cortex': 'D002540',
    'Uterus': 'D014599',
    'Nerve - Tibial': 'D013979',
    'Muscle - Skeletal': 'D018482',
    'Ovary': 'D010053',
    'Whole Blood': 'D001769',
    'Brain - Nucleus accumbens (basal ganglia)': 'D003342',
    'Colon - Transverse': 'D044684',
    'Adipose - Visceral (Omentum)': 'D009852',
    'Adrenal Gland': 'D000311',
    'Brain - Anterior cingulate cortex (BA24)': 'D006179',
    'Brain - Substantia nigra': 'D013378',
    'Thyroid': 'D013961',
    'Esophagus - Mucosa': 'D000071041',
    'Artery - Coronary': 'D003331',
    'Esophagus - Muscularis': 'D004947',
    'Brain - Caudate (basal ganglia)': 'D003342',
    'Heart - Atrial Appendage': 'D020517',
    'Esophagus - Gastroesophageal Junction': 'D004943',
    'Colon - Sigmoid': 'D012809',
    'Artery - Tibial': 'D016909',
    'Liver': 'D008099',
    'Prostate': 'D011467',
    'Testis': 'D013737',
    'Cells - Transformed fibroblasts': 'D005347',
    'Brain - Putamen (basal ganglia)': 'D011699',
    'Kidney - Cortex': 'D007672',
    'Pancreas': 'D010179',
    'Stomach': 'D013270',
    'Small Intestine - Terminal Ileum': 'D007082',
    'Breast - Mammary Tissue': 'D042361',
    'Brain - Hippocampus': 'D006624',
    'Brain - Cerebellum': 'D002531',
    'Pituitary': 'D010902',
    'Skin - Not Sun Exposed (Suprapubic)': 'D012867',
    'Brain - Frontal Cortex (BA9)': 'D005625',
    'Artery - Aorta': 'D001011',
    'Cervix - Ectocervix': 'D002584',
    'Vagina': 'D014621',
    'Cells - Leukemia cell line (CML)': 'D001853',
    'Brain - Hypothalamus': 'D007031',
    'Spleen': 'D013154',
    'Cells - EBV-transformed lymphocytes': 'D008214',
    'Brain - Spinal cord (cervical c-1)': 'D066193',
    'Minor Salivary Gland': 'D012470',
    'Bladder': 'D001743',
    'Cervix - Endocervix': 'D002584',
    'Fallopian Tube': 'D005187'}    


gtex_mesh_tissue_mapping = {
    'Lung': 'D004848', # epithelium
    'Brain - Cerebellar Hemisphere': 'D009417', # nerve tissue ##########
    'Heart - Left Ventricle': 'D009206', # myocardium
    'Skin - Sun Exposed (Lower leg)': 'D004817', # epidermis
    'Brain - Amygdala': 'D009417', # nerve tissue
    'Adipose - Subcutaneous': 'D000273', # adipose tissue
    'Brain - Cortex': 'D009417', # nerve tissue
    'Uterus': 'D004847', #epithelial cells
    'Nerve - Tibial': 'D009417', # nerve tissue
    'Muscle - Skeletal': 'D018482', # skeletal muscle
    'Ovary': 'D004848', # epithelium
    'Whole Blood': 'D003238', # connective tissue ############
    'Brain - Nucleus accumbens (basal ganglia)':  'D009417', # nerve tissue
    'Colon - Transverse': 'D007413', # intestinal mucosa
    'Adipose - Visceral (Omentum)': 'D000273', # adipose tissue
    'Adrenal Gland': 'D055098', # ##################
    'Brain - Anterior cingulate cortex (BA24)': 'D009474', # 
    'Brain - Substantia nigra': 'D009474', #
    'Thyroid': 'D000072637', #  #############
    'Esophagus - Mucosa': 'D004847', # 
    'Artery - Coronary': 'D042783', # #######
    'Esophagus - Muscularis': 'D004947',
    'Brain - Caudate (basal ganglia)': 'D003342',
    'Heart - Atrial Appendage': 'D020517',
    'Esophagus - Gastroesophageal Junction': 'D004943',
    'Colon - Sigmoid': 'D012809',
    'Artery - Tibial': 'D016909',
    'Liver': 'D008099',
    'Prostate': 'D011467',
    'Testis': 'D013737',
    'Cells - Transformed fibroblasts': 'D005347',
    'Brain - Putamen (basal ganglia)': 'D011699',
    'Kidney - Cortex': 'D007672',
    'Pancreas': 'D010179',
    'Stomach': 'D013270',
    'Small Intestine - Terminal Ileum': 'D007082',
    'Breast - Mammary Tissue': 'D042361',
    'Brain - Hippocampus': 'D006624',
    'Brain - Cerebellum': 'D002531',
    'Pituitary': 'D010902',
    'Skin - Not Sun Exposed (Suprapubic)': 'D012867',
    'Brain - Frontal Cortex (BA9)': 'D005625',
    'Artery - Aorta': 'D001011',
    'Cervix - Ectocervix': 'D002584',
    'Vagina': 'D014621',
    'Cells - Leukemia cell line (CML)': 'D001853',
    'Brain - Hypothalamus': 'D007031',
    'Spleen': 'D013154',
    'Cells - EBV-transformed lymphocytes': 'D008214',
    'Brain - Spinal cord (cervical c-1)': 'D066193',
    'Minor Salivary Gland': 'D012470',
    'Bladder': 'D001743',
    'Cervix - Endocervix': 'D002584',
    'Fallopian Tube': 'D005187'} 


tcga_gtex_df = []

with open(WORK_DIR + 'data/recount/gtex/pheno_r_friendly.tsv','r') as in_file:
    
    reader = csv.reader(in_file,delimiter='\t')
    reader.next()

    for line in reader:
        
        tcga_gtex_df.append([line[0],gtex_tissue_general_mapping[line[3]],gtex_tissue_detail_mapping[line[4]]])
        

tcga_tissue_general_mapping = {
    'Lung': 'D008168',
    'Brain': 'D001921',
    'Heart': 'D006321',
    'Skin': 'D012867',
    'Adipose Tissue': 'D000273',
    'Uterus': 'D014599',
    'Nerve': 'D009474',
    'Muscle': 'D009132',
    'Ovary': 'D010053',
    'Blood': 'D001769',
    'Colon': 'D003106',
    'Adrenal Gland': 'D000311',
    'Thyroid': 'D013961',
    'Esophagus': 'D004947',
    'Blood Vessel': 'D001808',
    'Liver': 'D008099',
    'Prostate': 'D011467',
    'Testis': 'D013737',
    'Kidney': 'D007668',
    'Pancreas': 'D010179',
    'Stomach': 'D013270',
    'Small Intestine': 'D007421',
    'Breast': 'D001940',
    'Pituitary': 'D010902',
    'Cervix Uteri': 'D002584',
    'Cervix': 'D002584',
    'Vagina': 'D014621',
    'Bone Marrow': 'D001853',
    'Spleen': 'D013154',
    'Salivary Gland': 'D012469',
    'Bladder': 'D001743',
    'Fallopian Tube': 'D005187',
    'Colorectal': 'D007420',
    'Lymph Nodes': 'D008198',
    'Pleura': 'D010994',
    'Thymus': 'D013950',
    'Eye': 'D005123',
    'Bile Duct': 'D001652',
    'Head and Neck': 'D009333',
    'Soft Tissue': 'D003238'}

tcga_tissue_detail_mapping = {
    'Liver Hepatocellular Carcinoma': 'D008099',
    'Prostate Adenocarcinoma': 'D011467',
    'Rectum Adenocarcinoma': 'D012007',
    'Bladder Urothelial Carcinoma': 'D001743',
    'Brain Lower Grade Glioma': 'D009417',                           
    'Breast Invasive Carcinoma': 'D042361',                                       
    'Uterine Corpus Endometrial Carcinoma': 'D004717',
    'Sarcoma': 'D003238',                           
    'Kidney Renal Clear Cell Carcinoma': 'D007672',
    'Pheochromocytoma and Paraganglioma': 'D000311',                              
    'Lymphoid Neoplasm Diffuse Large B-cell Lymphoma': 'D007962',                 
    'Mesothelioma': 'D010994',                                                    
    'Thymoma': 'D013950',                                                         
    'Lung Squamous Cell Carcinoma': 'D008168',
    'Ovarian Serous Cystadenocarcinoma': 'D005347',
    'Lung Adenocarcinoma': 'D008168',                                             
    'Stomach Adenocarcinoma': 'D013270',                                          
    'Glioblastoma Multiforme': 'D009417',                                         
    'Acute Myeloid Leukemia': 'D001853',                                          
    'Thyroid Carcinoma': 'D013961',                                               
    'Thyroid': 'D013961',                                                         
    'Cervical Squamous Cell Carcinoma and Endocervical Adenocarcinoma': 'D004717',
    'Prostate': 'D011467',                                                        
    'Colon Adenocarcinoma': 'D003106',                                            
    'Head and Neck Squamous Cell Carcinoma': 'D009333',                           
    'Uveal Melanoma': 'D014602',                                                  
    'Skin Cutaneous Melanoma': 'D008544',                                         
    'Pancreatic Adenocarcinoma': 'D010179',                                       
    'Liver': 'D008099',
    'Testicular Germ Cell Tumors': 'D013094',                                     
    'Lung': 'D008168',
    'Kidney Chromophobe': 'D007684',                                              
    'Breast': 'D001940',
    'Esophageal Carcinoma': 'D004947',
    'Kidney Renal Papillary Cell Carcinoma': 'D007684',                           
    'Adrenocortical Carcinoma': 'D000302',                                        
    'Cholangiocarcinoma': 'D001652',                                              
    'Uterine Carcinosarcoma': 'D014599',                                          
    'Lung': 'D008168',
    'Brain': 'D001921',
    'Heart': 'D006321',
    'Skin': 'D012867',
    'Adipose Tissue': 'D000273',
    'Uterus': 'D014599',
    'Nerve': 'D009474',
    'Muscle': 'D009132',
    'Ovary': 'D010053',
    'Blood': 'D001769',
    'Colon': 'D003106',
    'Adrenal Gland': 'D000311',
    'Thyroid': 'D013961',
    'Esophagus': 'D004947',
    'Blood Vessel': 'D001808',
    'Liver': 'D008099',
    'Prostate': 'D011467',
    'Testis': 'D013737',
    'Kidney': 'D007668',
    'Pancreas': 'D010179',
    'Stomach': 'D013270',
    'Small Intestine': 'D007421',
    'Breast': 'D001940',
    'Pituitary': 'D010902',
    'Cervix Uteri': 'D002584',
    'Vagina': 'D014621',
    'Bone Marrow': 'D001853',
    'Spleen': 'D013154',
    'Salivary Gland': 'D012469',
    'Bladder': 'D001743',
    'Fallopian Tube': 'D005187',
    'Colorectal': 'D007420',
    'Lymph Nodes': 'D008198',
    'Pleura': 'D010994',
    'Thymus': 'D013950',
    'Eye': 'D005123',
    'Bile Duct': 'D001652',
    'Head and Neck': 'D009333',
    'Soft Tissue': 'D003238',
    'Cervix': 'D002584',    
}



with open(WORK_DIR + 'data/recount/tcga/pheno_r_friendly.tsv','r') as in_file:
    
    reader = csv.reader(in_file,delimiter='\t')
    reader.next()

    for line in reader:
        
        try:
            tcga_gtex_df.append([line[0],tcga_tissue_general_mapping[line[3]],tcga_tissue_detail_mapping[line[4]]])
        except KeyError:
            print line

with open(WORK_DIR + 'data/recount/metadata/mesh_tcga_gtex_mapped.tsv','w') as out_file:
    writer = csv.writer(out_file,delimiter='\t')
    writer.writerow(['samp_id','tissue_general','tissue_detail'])

    for line in tcga_gtex_df:
        writer.writerow(line)

print 'done'
