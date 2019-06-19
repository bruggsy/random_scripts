library(dplyr)
library(reshape2)

marker.list <- readRDS('results/recount/markers/pairwise_leiden_pc3sd_r25e-3_marker_list_filtered_5th_perc.RDS')

unique.marker.list <- readRDS('results/recount/markers/pairwise_leiden_r25e-3_marker_list_filtered.RDS')

orig.gene.info <- read.table('data/recount/my_gene_ens_row_info.tsv',sep='\t',stringsAsFactors=F)

orig.gene.info$tissueType <- ''
orig.gene.info$cancerType <- ''
orig.gene.info$cellType <- ''
orig.gene.info$cellName <- ''

gene.info <- distinct(orig.gene.info)
gene.info <- gene.info[!is.na(gene.info$V2),]

cellmarker.info <- read.table('data/recount/gene_lists/cell_markers_by_gene.tsv',sep='\t',stringsAsFactors=F)
colnames(cellmarker.info) <- c('symbol','id','tissueType','cancerType','cellType','cellName')
## cellmarker.info <- subset(cellmarker.info,!is.na(geneID))

## cellmarker.info <- read.table('data/tmp/cell_marker_test.txt',sep='\t',stringsAsFactors=F)

cellmarker.minfo <- melt(cellmarker.info,id=c('symbol','id'))
cellmarker.minfo <- subset(cellmarker.minfo,value != 'Undefined')
cellmarker.cinfo <- cast(cellmarker.minfo[,c('symbol','variable','value')],symbol~variable, function(x) paste(unique(x),collapse=', '))

rownames(cellmarker.cinfo) <- cellmarker.cinfo$symbol

for(i in 1:nrow(orig.gene.info)){

    entry <- orig.gene.info[i,]
    cellmarker.entry <- cellmarker.cinfo[entry$V1,]

    if(all(is.na(cellmarker.entry))){
        next
    }

    entry$tissueType <- as.character(cellmarker.entry$tissueType)
    entry$cancerType <- as.character(cellmarker.entry$cancerType)
    entry$cellType <- as.character(cellmarker.entry$cellType)
    entry$cellName <- as.character(cellmarker.entry$cellName)

    orig.gene.info[i,] <- entry

}

saveRDS(orig.gene.info,'data/recount/gene_lists/cell_marker_gene_table.RDS')    

all.genes <- read.table('data/recount/gene_names_all.txt',stringsAsFactors=F)

fixed.ens.gene.info <- data.frame()

for(i in 1:nrow(all.genes)){

    if(i %% 1000 == 0){
        print(i)
    }

    gene <- all.genes$V1[i]
    gene.stripped <- gsub('[.].*$','',gene)

    cellmarker.entry <- distinct(subset(orig.gene.info,V3==gene.stripped))

    if(nrow(cellmarker.entry) == 0){

        cellmarker.entry <- c(V1=NA, V2=NA, V3=gene, V4='', tissueType='', cancerType='', cellType='', cellName='')

    } else{
        cellmarker.entry$V3 <- gene
    }

    fixed.ens.gene.info <- rbind(fixed.ens.gene.info,cellmarker.entry)

}

## write.table(orig.gene.info,'data/recount/gene_lists/cell_marker_gene_table.tsv',sep='\t')

saveRDS(fixed.ens.gene.info,'data/recount/gene_lists/cell_marker_gene_table_fixed_ens.RDS')

gene.tables <- list()

tissue.table <- list()

for(tissue in unique(cellmarker.info$tissueType)){

    cellmarker.tissue <- subset(cellmarker.info,tissueType==tissue)
    ## gene.info.inds <- (gene.info$V2 %in% cellmarker.tissue$id)
    ## gene.info.slice <- gene.info[gene.info.inds,]
    
    ## tissue.table[[tissue]] <- subset(gene.info,V2 %in% cellmarker.tissue$id)[,c('V1','V2','V3','V4')]
    tissue.table[[tissue]] <- which(orig.gene.info$V2 %in% cellmarker.tissue$id)

    ## tissue.table[[tissue]] <- subset(cellmarker.info,tissueType==tissue)[,c('V1','V2','V3','V4')]

}

gene.tables[['tissue']] <- tissue.table

cancer.table <- list()

for(cancer in unique(cellmarker.info$cancerType)){
    cellmarker.cancer <- subset(cellmarker.info,cancerType==cancer)

    cancer.table[[cancer]] <- which(orig.gene.info$V2 %in% cellmarker.cancer$id)
}

gene.tables[['cancer']] <- cancer.table

cell.type.table <- list()

for(cell.type in unique(cellmarker.info$cellType)){
    cellmarker.cell.type <- subset(cellmarker.info,cellType==cell.type)

    ## cell.type.table[[cell.type]] <- subset(gene.info,V2 %in% cellmarker.cell.type$id)[,c('V1','V2','V3','V4')]
    cell.type.table[[cell.type]] <- which(orig.gene.info$V2 %in% cellmarker.cell.type$id)
}

gene.tables[['cellType']] <- cell.type.table

cell.name.table <- list()

for(cell.name in unique(cellmarker.info$cellName)){
    cellmarker.cell.name <- subset(cellmarker.info,cellName==cell.name)

    cell.name.table[[cell.name]] <- which(orig.gene.info$V2 %in% cellmarker.cell.name$id)
}

gene.tables[['cellName']] <- cell.name.table

marker.table <- list()

for(clus in 1:length(marker.list)){

    marker.ens <- gsub('[.].*$','',rownames(marker.list[[clus]]))

    marker.table[[clus]] <- which(orig.gene.info$V3 %in% marker.ens)

}

gene.tables[['markers']] <- marker.table

saveRDS(gene.tables,'data/recount/gene_lists/gene_groups_tiscellcancer_tables.RDS')



## for(i in 1:nrow(cellmarker.info)){

##     row <- cellmarker.info[i,]

##     gene.ids <- strsplit(row$geneID,', ')[[1]]
##     ## gene.ids <- strsplit(row$V10,', ')[[1]]
##     gene.ids <- gene.ids[!is.na(gene.ids)]
##     gene.ids <- gsub('\\[','',gene.ids)
##     gene.ids <- gsub('\\]','',gene.ids)
##     ## gene.ids <- sapply(gene.ids,as.numeric)

##     ## gene.sym <- strsplit(row$V9,', ')[[1]]
##     gene.sym <- strsplit(row$geneSymbol,', ')[[1]]
##     gene.sym <- gene.sym[!is.na(gene.sym)]
##     gene.sym <- gsub('\\[','',gene.sym)
##     gene.sym <- gsub('\\]','',gene.sym)
##     ## gene.sym <- sapply(gene.ids,as.numeric)

##     for(j in 1:length(gene.ids)){

        

##         cellmarker.df <- rbind(cellmarker.df,
##                                data.frame(
##                                    geneSymbol=gene.sym[j],
##                                    geneID=gene.ids[j],
##                                    tissueType=row$tissueType,
##                                    cancerType=row$cancerType,
##                                    cellType=row$cellType,
##                                    cellName=row$cellName))
##         ## cellmarker.df <- rbind(cellmarker.df,
##         ##                        data.frame(
##         ##                            geneSymbol=gene.sym[j],
##         ##                            geneID=gene.ids[j],
##         ##                            tissueType=row$V2,
##         ##                            cancerType=row$V4,
##         ##                            cellType=row$V5,
##         ##                            cellName=row$V6))

##     }

##     if(nrow(cellmarker.df)>1519){
##         break
##     }
## }
