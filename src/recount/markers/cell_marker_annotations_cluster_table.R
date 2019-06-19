marker.list <- readRDS('results/recount/markers/pairwise_leiden_r25e-3_marker_list_filtered_5th_perc_shiny.RDS')

marker.count.list <- list()
for(i in 1:length(marker.list)){

    marker.entry <- marker.list[[i]]

    marker.tissue.type <- marker.entry$tissueType
    tiss.type.split <- unlist(sapply(marker.tissue.type,function(x) strsplit(x,split=', ')[[1]]))
    tiss.type.tab <- table(tiss.type.split)
    tiss.type.tab['unlabelled'] <- sum(marker.entry$tissueType == '')

    marker.cancer.type <- marker.entry$cancerType
    canc.type.split <- unlist(sapply(marker.cancer.type,function(x) strsplit(x,split=', ')[[1]]))
    canc.type.tab <- table(canc.type.split)
    canc.type.tab['unlabelled'] <- sum(marker.entry$cancerType == '')

    marker.cell.type <- marker.entry$cellType
    cell.type.split <- unlist(sapply(marker.cell.type,function(x) strsplit(x,split=', ')[[1]]))
    cell.type.tab <- table(cell.type.split)
    cell.type.tab['unlabelled'] <- sum(marker.entry$cellType == '')
    
    marker.cell.name <- marker.entry$cellName
    cell.name.split <- unlist(sapply(marker.cell.name,function(x) strsplit(x,split=', ')[[1]]))
    cell.name.tab <- table(cell.name.split)
    cell.name.tab['unlabelled'] <- sum(marker.entry$cellName == '')

    
    count.entry <- list()
    count.entry[['no']][['marker_tissue_type']] <- tiss.type.tab
    count.entry[['no']][['marker_cancer_type']] <- canc.type.tab
    count.entry[['no']][['marker_cell_type']] <- cell.type.tab
    count.entry[['no']][['marker_cell_name']] <- cell.name.tab


    if(nrow(marker.entry) > 0){
        marker.entry <- subset(marker.entry,unique=='Yes')
    }

    marker.tissue.type <- marker.entry$tissueType
    tiss.type.split <- unlist(sapply(marker.tissue.type,function(x) strsplit(x,split=', ')[[1]]))
    tiss.type.tab <- table(tiss.type.split)
    tiss.type.tab['unlabelled'] <- sum(marker.entry$tissueType == '')

    marker.cancer.type <- marker.entry$cancerType
    canc.type.split <- unlist(sapply(marker.cancer.type,function(x) strsplit(x,split=', ')[[1]]))
    canc.type.tab <- table(canc.type.split)
    canc.type.tab['unlabelled'] <- sum(marker.entry$cancerType == '')

    marker.cell.type <- marker.entry$cellType
    cell.type.split <- unlist(sapply(marker.cell.type,function(x) strsplit(x,split=', ')[[1]]))
    cell.type.tab <- table(cell.type.split)
    cell.type.tab['unlabelled'] <- sum(marker.entry$cellType == '')
    
    marker.cell.name <- marker.entry$cellName
    cell.name.split <- unlist(sapply(marker.cell.name,function(x) strsplit(x,split=', ')[[1]]))
    cell.name.tab <- table(cell.name.split)
    cell.name.tab['unlabelled'] <- sum(marker.entry$cellName == '')

    count.entry[['yes']][['marker_tissue_type']] <- tiss.type.tab
    count.entry[['yes']][['marker_cancer_type']] <- canc.type.tab
    count.entry[['yes']][['marker_cell_type']] <- cell.type.tab
    count.entry[['yes']][['marker_cell_name']] <- cell.name.tab

    marker.count.list[[i]] <- count.entry

}

saveRDS(marker.count.list,'data/recount/markers/cell_marker_annotations_marker_counts.RDS')



marker.data.frame <- data.frame()

for(i in 1:length(marker.list)){
    marker.entry <- marker.list[[i]]
    if(nrow(marker.entry) == 0){
        next
    }
    marker.entry$cluster <- i
    marker.data.frame <- rbind(marker.data.frame,marker.entry)
}

marker.unique.frame <- subset(marker.data.frame,unique=='Yes')
