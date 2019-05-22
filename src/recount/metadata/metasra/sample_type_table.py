#!/usr/bin/python

import csv
import json
import requests
import urllib

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

if not 'metasra' in locals():
    with open(WORK_DIR + 'downloads/metaSRA/metasra.v1-4.json','r') as in_file:
        metasra = json.load(in_file)


samples = set([])

samples_2_runs = {}

label_table = []



with open(WORK_DIR + 'data/recount/gtex/tsv_friendly_gtex_meta.tsv','r') as in_file:
    reader = csv.reader(in_file,delimiter='\t')
    reader.next()

    for line in reader:
        
        sample = line[2]
        run = line[4]

        meta_entry = metasra.get(sample,None)

        if not meta_entry:

            label = 'NA'

        else:
            
            label = meta_entry['sample type']

        # if run 

        # line.append(label)

        label_table.append([sample,label])

        # samples.add(sample)

        # sample_entry = samples_2_runs.get(sample,[])
        # sample_entry.append(run)
        # samples_2_runs[sample] = sample_entry

with open(WORK_DIR + 'data/recount/metadata/tsv_friendly_recount_meta.tsv','r') as in_file:
    reader = csv.reader(in_file,delimiter='\t')
    reader.next()

    for line in reader:

        sample = line[2]
        run = line[4]

        meta_entry = metasra.get(sample,None)

        if not meta_entry:
            label='NA'
        else:
            label = meta_entry['sample type']

        # line.append(label)
        label_table.append([sample,label])

        # samples.add(sample)

        # sample_entry = samples_2_runs.get(sample,[])
        # sample_entry.append(run)
        # samples_2_runs[sample] = sample_entry



        
with open(WORK_DIR + 'data/recount/metadata/tcga_sra_pheno.tsv','r') as in_file:
    reader = csv.reader(in_file,delimiter='\t')
    reader.next()

    for line in reader:

        samp = line[1].strip('.bw')

        label_table.append([samp,'tissue'])

with open(WORK_DIR + 'data/recount/metadata/metasra_sample_type_table.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')

    for line in label_table:
        writer.writerow(line)


print 'done'
