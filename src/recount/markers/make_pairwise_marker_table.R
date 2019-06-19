library(dplyr)

marker.list <- readRDS('results/recount/markers/pairwise_leiden_pc3sd_r25e-3_marker_list_filtered_5th_perc.RDS')

unique.marker.list <- readRDS('results/recount/markers/pairwise_leiden_r25e-3_marker_list_filtered.RDS')
## cellmarker.info <- readRDS('data/recount/gene_lists/cell_marker_gene_table.RDS')
## rownames(cellmarker.info) <- cellmarker.info$V3

cellmarker.info <- readRDS('data/recount/gene_lists/cell_marker_gene_table_fixed_ens.RDS')
rownames(cellmarker.info) <- cellmarker.info$V3
## gene.info <- read.table('data/recount/my_gene_ens_row_info.tsv',sep='\t',stringsAsFactors=F)
## gene.info <- distinct(gene.info)
## rownames(gene.info) <- gene.info$V3

all.marker.df <- data.frame()

for(i in 1:length(marker.list)){

    marker.entry <- marker.list[[i]]

    if(nrow(marker.entry) == 0){
        next
    }
    
    colnames(marker.entry) <- c('p-val','unique-fcs','total-fcs')

    marker.entry <- marker.entry <- cbind(marker.entry, cellmarker.info[rownames(marker.entry),4:8])

    marker.entry$annotation <- cellmarker.info[rownames(marker.entry),'V4']
    marker.entry$symbol <- cellmarker.info[rownames(marker.entry),'V1']
    marker.entry$id <- cellmarker.info[rownames(marker.entry),'V2']

    marker.entry$unique <- 'No'
    
    unique.marker.entry <- unique.marker.list[[i]]
    marker.entry[rownames(unique.marker.entry),'unique'] <- 'Yes'

    marker.entry <- marker.entry[,c('symbol','id','annotation','tissueType','cancerType','cellType','cellName','unique','p-val','unique-fcs','total-fcs')]

    ## marker.entry[['p-val']] <- as.numeric(marker.entry[['p-val']])
    marker.entry[['unique-fcs']] <- as.numeric(marker.entry[['unique-fcs']])
    marker.entry[['total-fcs']] <- as.numeric(marker.entry[['total-fcs']])

    ## cellmarker.slice <- 

    marker.list[[i]] <- marker.entry

    marker.entry$cluster <- i-1
    all.marker.df <- rbind(all.marker.df,marker.entry)

}

marker.list[['all']] <- all.marker.df

saveRDS(marker.list,'results/recount/markers/pairwise_leiden_r25e-3_marker_list_filtered_5th_perc_shiny.RDS')

### make new gene choices

gene.choices <- apply(cellmarker.info[,c('V3','V1','V2')],1,function(x) paste(x,collapse=', '))
real.gene.choices <- names(gene.choices)
names(real.gene.choices) <- gene.choices

gene.num.vec <- 1:length(gene.choices)
names(gene.num.vec) <- names(gene.choices)

saveRDS(real.gene.choices,'data/recount/gene_lists/shiny_gene_choice_list.RDS')
saveRDS(gene.num.vec,'data/recount/gene_lists/shiny_gene_num_vec.RDS')
