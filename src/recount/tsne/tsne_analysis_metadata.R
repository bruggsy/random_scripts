library(reshape2)
library(jsonlite)

setwd('~/Documents/Projects/Mercator/')

tsne.tmp <- readRDS('results/recount/tsne/recount_tsne.RDS')
tsne.rownames <- rownames(tsne.tmp$Y)

## tsne.list <- readRDS('results/recount/tsne/recount_tsne_pca_list_noNAs_narrow_perp.RDS')

## tsne.list <- readRDS('results/recount/tsne/recount_tsne_pca_list_noNAs_over100_noSingle.RDS') 

tsne.list <- readRDS('results/recount/tsne/recount_tsne_pca_list_noNAs_over50_noSingle_protein_coding.RDS') 

## recount.metadata <- read.table('data/recount/metadata/tsv_friendly_recount_meta.tsv',sep='\t',header=T)
recount.metadata <- read.table('data/recount/metadata/all_recount_metadata_ordered.tsv',sep='\t',header=T,stringsAsFactors=F)
rownames(recount.metadata) <- recount.metadata$run_id

gtex.meta <- read.table('data/recount/gtex/pheno_r_friendly.tsv',sep='\t',header=T,stringsAsFactors=F)
tcga.meta <- read.table('data/recount/tcga/pheno_r_friendly.tsv',sep='\t',header=T,stringsAsFactors=F)

recount.metadata$tissue <- 'unlabelled'

gtex.tcga.meta <- rbind(gtex.meta,tcga.meta)
gtex.tcga.meta <- subset(gtex.tcga.meta,data_id != '')

tissue.metadata<- fromJSON('http://localhost:3000/ontology_info/A')

for(tissue in names(tissue.metadata)){
    
    tissue.entry <- tissue.metadata[[tissue]]

    recount.metadata[tissue.entry,]$tissue <- tissue

}

recount.metadata <- subset(recount.metadata,tissue != 'unlabelled')

ss.table <- NULL

for(tsne.entry in tsne.list){

    ## rownames(tsne.entry) <- tsne.rownames
    tsne.entry <- data.frame(tsne.entry)    

    tsne.entry <- tsne.entry[gtex.tcga.meta$data_id,]

    ## tsne.entry <- tsne.entry[recount.metadata$run_id,]
    tsne.entry <- subset(tsne.entry,!(is.na(X1) | is.na(X2)))

    rownames(gtex.tcga.meta) <- gtex.tcga.meta$data_id
    gtex.tcga.meta <- gtex.tcga.meta[rownames(tsne.entry),]

    ## rownames(recount.metadata) <- recount.metadata$run_id
    ## recount.metadata <- recount.metadata[rownames(tsne.entry),]

    ## tsne.entry <- data.frame(tsne.entry)

    ## tsne.entry$proj_id <- recount.metadata$proj_id
    ## tsne.entry$samp_id <- recount.metadata$samp_id
    ## tsne.entry$run_id <- recount.metadata$run_id
    ## tsne.entry$tissue <- recount.metadata$tissue
    tsne.entry$tissue_general <- gtex.tcga.meta$tissue_general
    tsne.entry$tissue_detail <- gtex.tcga.meta$tissue_detail
    tsne.melt <- melt(tsne.entry)

    tsne.centers.tissue.detail <- dcast(tsne.melt,tissue_detail ~ variable,mean)
    rownames(tsne.centers.tissue.detail) <- tsne.centers.tissue.detail$tissue_detail

    tsne.centers.tissue.general <- dcast(tsne.melt,tissue_general~ variable,mean)
    rownames(tsne.centers.tissue.general) <- tsne.centers.tissue.general$tissue_general

    tsne.center <- c(mean(tsne.entry$X1),mean(tsne.entry$X2))

    tsne.center.dists <- apply(tsne.entry[,c('X1','X2')],1,function(x) {
        ## return(x[1] + x[2])}
        return((x[1] - tsne.center[1])^2 + (x[2] - tsne.center[2])^2)}
        )

    tsne.total.ss <- sum(tsne.center.dists)

    within.tissue.general.ss <- apply(tsne.entry[,c('X1','X2','tissue_general'),drop=F],1,function(x) {
        (as.numeric(x[1]) - tsne.centers.tissue.general[x[3],2])^2 + (as.numeric(x[2]) - tsne.centers.tissue.general[x[3],3])^2
    })
    
    within.tissue.detail.ss <- apply(tsne.entry[,c('X1','X2','tissue_detail'),drop=F],1,function(x) {
        (as.numeric(x[1]) - tsne.centers.tissue.detail[x[3],2])^2 + (as.numeric(x[2]) - tsne.centers.tissue.detail[x[3],3])^2
    })

    tissue.general.table <- table(tsne.entry$tissue_general)
    tissue.detail.table <- table(tsne.entry$tissue_detail)

    between.tissue.general.ss <- apply(tsne.centers.tissue.general[,c('X1','X2','tissue_general'),drop=F],1,function(x) {
        tissue.general.table[x[3]] * ((as.numeric(x[1]) - tsne.center[1])^2 + (as.numeric(x[2]) - tsne.center[2])^2)
    })

    between.tissue.detail.ss <- apply(tsne.centers.tissue.detail[,c('X1','X2','tissue_detail'),drop=F],1,function(x) {
        tissue.detail.table[x[3]] * ((as.numeric(x[1]) - tsne.center[1])^2 + (as.numeric(x[2]) - tsne.center[2])^2)
    })
                        
    total.dof <- nrow(tsne.entry) - 1

    within.tissue.general.dof <- nrow(tsne.entry) - length(tissue.general.table)
    within.tissue.detail.dof <- nrow(tsne.entry) - length(tissue.detail.table)

    between.tissue.general.dof <- length(tissue.general.table) - 1
    between.tissue.detail.dof <- length(tissue.detail.table) - 1

    if(typeof(ss.table) == 'NULL'){

        ss.table <- data.frame(total.ss = tsne.total.ss,
                               within.tissue.general.ss = sum(within.tissue.general.ss),
                               within.tissue.detail.ss = sum(within.tissue.detail.ss),
                               between.tissue.general.ss = sum(between.tissue.general.ss),
                               between.tissue.detail.ss = sum(between.tissue.detail.ss),
                               total.dof = total.dof,
                               within.tissue.general.dof = within.tissue.general.dof,
                               within.tissue.detail.dof = within.tissue.detail.dof,
                               between.tissue.general.dof = between.tissue.general.dof,
                               between.tissue.detail.dof = between.tissue.detail.dof,
                               total.var = tsne.total.ss / total.dof,
                               within.tissue.general.var = sum(within.tissue.general.ss) / within.tissue.general.dof,
                               between.tissue.general.var = sum(between.tissue.general.ss) / between.tissue.general.dof,
                               within.tissue.detail.var = sum(within.tissue.detail.ss) / within.tissue.detail.dof,
                               between.tissue.detail.var = sum(between.tissue.detail.ss) / between.tissue.detail.dof)

    }
    else{

        ss.table <- rbind(ss.table,c(tsne.total.ss,
                               sum(within.tissue.general.ss),
                               sum(within.tissue.detail.ss),
                               sum(between.tissue.general.ss),
                               sum(between.tissue.detail.ss),
                               total.dof,
                               within.tissue.general.dof,
                               within.tissue.detail.dof,
                               between.tissue.general.dof,
                               between.tissue.detail.dof,
                               total.var = tsne.total.ss / total.dof,
                               sum(within.tissue.general.ss) / within.tissue.general.dof,
                               sum(between.tissue.general.ss) / between.tissue.general.dof,
                               sum(within.tissue.detail.ss) / within.tissue.detail.dof,
                               sum(between.tissue.detail.ss) / between.tissue.detail.dof))
        
        ## ss.table <- rbind(ss.table,c(tsne.total.ss,
        ##                              sum(within.tissue.ss),
        ##                              sum(between.tissue.ss),
        ##                              total.dof,
        ##                              within.tissue.dof,
        ##                              between.tissue.dof,
        ##                              tsne.total.ss / total.dof,
        ##                              sum(within.tissue.ss) / within.tissue.dof,
        ##                              sum(between.tissue.ss) / between.tissue.dof))
    }



    ## within.proj.ss <- apply(tsne.entry[1,c('X1','X2','proj_id'),drop=F],1,function(x) {
    ##     return((as.numeric(x[1]) - tsne.centers.byproj[x[3],2])^2 + (as.numeric(x[2]) - tsne.centers.byproj[x[3],3])^2)
    ##     }
   
    ## saveRDS(ss.table,'results/recount/tsne/tsne_noProj_noScale_noNAs_tissue_analysis.RDS')

    ## break

}

rownames(ss.table) <- names(tsne.list)
saveRDS(ss.table,'results/recount/tsne/tsne_noProj_noScale_noNAs_tissue_analysis_noSingle_over50_protein_coding.RDS')
