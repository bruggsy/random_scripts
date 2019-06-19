clus.dist.info <- readRDS('data/recount/markers/leiden_pca_over50_pc3sd_k40_r25e-3_markers_dist_info.RDS')

dist.info <- list()

i <- 0

for(gene in names(clus.dist.info[[1]]$means)){
    
    if(i %% 100){print(i)}

    gene.vec <- sapply(clus.dist.info,function(x) x$means[gene])
    clus.order <- order(gene.vec,decreasing=T)
    dist.info[[gene]] <- clus.order[1:10]

}

saveRDS(dist.info,'data/recount/markers/leiden_pc3sd_r25e-3_markers_top_clus.RDS')
