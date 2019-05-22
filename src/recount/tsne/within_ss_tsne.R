library(reshape2)

setwd('~/Documents/Projects/Mercator/')

tsne.tmp <- readRDS('results/recount/tsne/recount_tsne.RDS')
tsne.rownames <- rownames(tsne.tmp$Y)

## tsne.list <- readRDS('results/recount/tsne/recount_tsne_pca_list_noNAs.RDS')
tsne.list <- readRDS('results/recount/tsne/recount_tsne_pca_list_noNAs_over50_noSingle_protein_coding.RDS')

## recount.metadata <- read.table('data/recount/metadata/tsv_friendly_recount_meta.tsv',sep='\t',header=T)
recount.metadata <- read.table('data/recount/metadata/all_recount_metadata_ordered.tsv',sep='\t',header=T,stringsAsFactors=F)

ss.table <- NULL

for(tsne.entry in tsne.list){

    ## rownames(tsne.entry) <- tsne.rownames
    tsne.entry <- data.frame(tsne.entry)    

    ## tsne.entry <- tsne.entry[recount.metadata$run_id,]
    rownames(recount.metadata) <- recount.metadata$run_id
    recount.metadata <- recount.metadata[rownames(tsne.entry),]

    ## tsne.entry <- data.frame(tsne.entry)

    tsne.entry$proj_id <- recount.metadata$proj_id
    tsne.entry$samp_id <- recount.metadata$samp_id
    tsne.entry$run_id <- recount.metadata$run_id

    proj.table <- table(tsne.entry$proj_id)
    samp.table <- table(tsne.entry$samp_id)

    samp.table <- samp.table[samp.table > 2]

    tsne.entry <- tsne.entry[tsne.entry$samp_id %in% names(samp.table),]

    tsne.melt <- melt(tsne.entry)

    tsne.centers.byproj <- dcast(tsne.melt,proj_id ~ variable,mean)
    rownames(tsne.centers.byproj) <- tsne.centers.byproj$proj_id

    tsne.centers.bysamp <- dcast(tsne.melt,samp_id ~ variable,mean)
    rownames(tsne.centers.bysamp) <- tsne.centers.bysamp$samp_id

    tsne.center <- c(mean(tsne.entry$X1),mean(tsne.entry$X2))

    tsne.center.dists <- apply(tsne.entry[,c('X1','X2')],1,function(x) {
        ## return(x[1] + x[2])}
        return((x[1] - tsne.center[1])^2 + (x[2] - tsne.center[2])^2)}
        )

    tsne.total.ss <- sum(tsne.center.dists)

    within.proj.ss <- apply(tsne.entry[,c('X1','X2','proj_id'),drop=F],1,function(x) {
        (as.numeric(x[1]) - tsne.centers.byproj[x[3],2])^2 + (as.numeric(x[2]) - tsne.centers.byproj[x[3],3])^2
    })

    within.samp.ss <- apply(tsne.entry[,c('X1','X2','samp_id'),drop=F],1,function(x) {
        (as.numeric(x[1]) - tsne.centers.bysamp[x[3],2])^2 + (as.numeric(x[2]) - tsne.centers.bysamp[x[3],3])^2
    })


    between.proj.ss <- apply(tsne.centers.byproj[,c('X1','X2','proj_id'),drop=F],1,function(x) {
        proj.table[x[3]] * ((as.numeric(x[1]) - tsne.center[1])^2 + (as.numeric(x[2]) - tsne.center[2])^2)
    })
                        

    between.samp.ss <- apply(tsne.centers.bysamp[,c('X1','X2','samp_id'),drop=F],1,function(x) {
        samp.table[x[3]] * ((as.numeric(x[1]) - tsne.center[1])^2 + (as.numeric(x[2]) - tsne.center[2])^2)
    })

    total.dof <- nrow(tsne.entry) - 1

    within.proj.dof <- nrow(tsne.entry) - length(proj.table)
    within.samp.dof <- nrow(tsne.entry) - length(samp.table)

    between.proj.dof <- length(proj.table) - 1
    between.samp.dof <- length(samp.table) - 1

    if(typeof(ss.table) == 'NULL'){

        ss.table <- data.frame(total.ss = tsne.total.ss,
                               within.proj.ss = sum(within.proj.ss),
                               within.samp.ss = sum(within.samp.ss),
                               between.proj.ss = sum(between.proj.ss),
                               between.samp.ss = sum(between.samp.ss),
                               total.dof = total.dof,
                               within.proj.dof = within.proj.dof,
                               within.samp.dof = within.samp.dof,
                               between.proj.dof = between.proj.dof,
                               between.samp.dof = between.samp.dof,
                               total.var = tsne.total.ss / total.dof,
                               within.proj.var = sum(within.proj.ss) / within.proj.dof,
                               within.samp.var = sum(within.samp.ss) / within.samp.dof,
                               between.proj.var = sum(between.proj.ss) / between.proj.dof,
                               between.samp.var = sum(between.samp.ss) / between.samp.dof)
    }
    else{
        ss.table <- rbind(ss.table,c(tsne.total.ss,
                                     sum(within.proj.ss),
                                     sum(within.samp.ss),
                                     sum(between.proj.ss),
                                     sum(between.samp.ss),
                                     total.dof,
                                     within.proj.dof,
                                     within.samp.dof,
                                     between.proj.dof,
                                     between.samp.dof,
                                     tsne.total.ss / total.dof,
                                     sum(within.proj.ss) / within.proj.dof,
                                     sum(within.samp.ss) / within.samp.dof,
                                     sum(between.proj.ss) / between.proj.dof,
                                     sum(between.samp.ss) / between.samp.dof))
    }



    ## within.proj.ss <- apply(tsne.entry[1,c('X1','X2','proj_id'),drop=F],1,function(x) {
    ##     return((as.numeric(x[1]) - tsne.centers.byproj[x[3],2])^2 + (as.numeric(x[2]) - tsne.centers.byproj[x[3],3])^2)
    ##     }

    saveRDS(ss.table,'results/recount/tsne/tsne_noProj_noScale_noNAs_protein_codinganalysis.RDS')
   
    ## break

}

rownames(ss.table) <- names(tsne.list)
saveRDS(ss.table,'results/recount/tsne/tsne_noProj_noScale_noNAs_protein_codinganalysis.RDS')



## within ss by:
##    project
##    samples
##    metadata
