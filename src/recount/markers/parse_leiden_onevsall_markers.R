marker.dat <- readRDS('results/recount/markers/leiden_onevsall_markers_r25e-3.RDS')

cluster.num <- length(marker.dat)

parsed.marker.dat <- list()

for(i in 1:cluster.num){

    marker.entry <- marker.dat[[i]]

    marker.entry$pvalue <- p.adjust(marker.entry$pvalue,method='bonferroni')
    marker.entry$pvalue <- marker.entry$pvalue * 149
    
    marker.entry <- subset(marker.entry,pvalue <= 0.01)
    marker.entry <- marker.entry[order(marker.entry$fold.change),]
    
    parsed.marker.dat[[i]] <- marker.entry

}

all.genes <- unlist(sapply(parsed.marker.dat,rownames))
gene.table <- table(all.genes)

unique.genes <- gene.table[which(gene.table == 1)]
