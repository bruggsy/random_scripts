#!/usr/bin/python

import json
import csv
import sys

csv.field_size_limit(sys.maxsize)

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

with open(WORK_DIR + 'data/tmp/anatomy_mesh_subjtree.txt','r') as in_file:
    reader = csv.reader(in_file,delimiter=',')
    a = reader.next()
    
    anatomy_data = json.loads(a[0])
    
anatomy_table = []

for label in anatomy_data.keys():

    for samp in anatomy_data[label]:
        anatomy_table.append([label,samp])

with open(WORK_DIR + 'data/tmp/anatomy_subjtree_array.csv','w') as out_file:
    writer = csv.writer(out_file,delimiter=',')
    for line in anatomy_table:
        writer.writerow(line)

print 'done'
