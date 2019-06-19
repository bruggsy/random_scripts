import csv
import re

WORK_DIR = '/Users/Jake/Documents/Projects/Mercator/'

natural_killer = []
bcells = []
tcells = []
helper_cells = []
other_cells = []

with open(WORK_DIR + 'downloads/CellMarker/cell_markers_fixed.tsv','r') as in_file:

    cellmarker_dat = []
    
    reader = csv.reader(in_file,delimiter='\t')
    header = reader.next()

    for line in reader:
        if re.search('killer',line[5],re.IGNORECASE):
            natural_killer.append(line)
        elif re.search('b cell',line[5],re.IGNORECASE):
            bcells.append(line)
        elif re.search('t cell',line[5],re.IGNORECASE) or re.search('treg',line[5],re.IGNORECASE):
            tcells.append(line)
        elif re.search('helper',line[5],re.IGNORECASE):
            helper_cells.append(line)
        else:
            other_cells.append(line)

with open(WORK_DIR + 'downloads/CellMarker/cell_markers_removed_lymphocytes.tsv','w') as out_file:
    writer = csv.writer(out_file,delimiter='\t')
    writer.writerow(header)
    for line in other_cells:
        writer.writerow(line)


remaining_cell_types = set(map(lambda x: x[5],other_cells))


print 'done'        
