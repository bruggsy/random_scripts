#!/usr/bin/python

import csv
import re

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

cellmarker_mat = []

with open(WORK_DIR + 'downloads/CellMarker/cell_markers_fixed.tsv','r') as in_file:

    reader = csv.reader(in_file,delimiter='\t')
    reader.next()
    
    for line in reader:

        # gene_ids = re.sub('\w\[\w'
        gene_ids = re.sub('\[','',line[9])
        gene_ids = re.sub('\]','',gene_ids)
        gene_ids = gene_ids.split(', ')
        gene_ids = filter(lambda x: x != 'NA',gene_ids)
        
        gene_sym = re.sub('\[','',line[8])
        gene_sym = re.sub('\]','',gene_sym)
        gene_sym = gene_sym.split(', ')
        gene_sym = filter(lambda x: x != 'NA',gene_sym)

        for i in range(len(gene_ids)):

            cellmarker_mat.append([gene_sym[i],
                                   gene_ids[i],
                                   line[1],
                                   line[3],
                                   line[4],
                                   line[5]])

with open(WORK_DIR + 'data/recount/gene_lists/cell_markers_by_gene.tsv','w') as out_file:
    writer = csv.writer(out_file,delimiter='\t',quoting=csv.QUOTE_ALL)

    for line in cellmarker_mat:
        writer.writerow(line)


print 'done'
