sample.tab <- read.table('data/recount/metadata/metasra_sample_type_table.csv',sep=',',stringsAsFactors=F)
sample.vec <- sample.tab$V2
names(sample.vec) <- sample.tab$V1

tsne.meta <- readRDS('data/recount/metadata/app_tables/recount_meta.RDS')
rownames(tsne.meta) <- tsne.meta$run_id

sample.vec.slice <- sample.vec[tsne.meta$samp_id]
tsne.meta$sample_type <- sample.vec.slice
tsne.meta$sample_type[tsne.meta$proj_id == 'TCGA'] <- 'tissue'


saveRDS(tsne.meta,'data/recount/metadata/app_tables/recount_meta_sampletype.RDS')
