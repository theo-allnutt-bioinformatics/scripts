#!/usr/bin/Rscript
#source("https://bioconductor.org/biocLite.R")
#biocLite("Heatplus")
#biocLite("vegan")
#biocLite("ape")
#install.packages("phangorn")

#makes a heatmap that has rows ordered by upgma of variable

library(Heatplus)
library(vegan)
library(RColorBrewer)
library(gplots)
library(ape)
library(phangorn)
library(seqinr)

args = commandArgs(trailingOnly=TRUE)

all.data <- read.table(args[1],sep="\t",header=TRUE,check.names=FALSE)

row.names(all.data) <- all.data$otu
all.data <- all.data[,-1]
group1 = all.data[1,]
all.data <- all.data[-1,]
head(all.data)

#make data proportions, not abundances, normalise by sample total
#log transfrom if required.
data.prop <- (sweep(all.data, 2, colSums(all.data), FUN="/"))

if (args[4]=="10"){data.s <- log10(data.prop+1)}
if (args[4]=="e"){data.s <- log(data.prop+1)}
if (args[4]=="2"){data.s <- log2(data.prop+1)}
if (args[4]=="a"){data.s <- all.data}
if (args[4]=="p"){data.s <- data.prop}
if (args[4]=="a10"){data.s <- log10(all.data+1)}
if (args[4]=="ae"){data.s <- log(all.data+1)}
if (args[4]=="a2"){data.s <- log2(all.data+1)}

#set group data colours
#group1 <- replace(group1,which(group1==1),"red")
#group1 <- replace(group1,which(group1==2),"blue")
#group1 <-t(group1)
#cbind(names(data.prop), group1)

s1=args[3]
colscale <- colorRampPalette(c("chartreuse4","yellow", "red"), space = "rgb")(100)

#simple map
#heatmap(as.matrix(data.prop[1:s1,]), Rowv = NA, Colv = NA, col = scaleyellowred, margins = c(10, 2))

#make trees
x <-data.s[1:s1,]
otu.dist <- vegdist(x, method = "jaccard")
otu.clus <- hclust(otu.dist, "aver")
samples.dist <- vegdist(t(data.prop), method = "jaccard")
samples.clus <- hclust(samples.dist, "aver")

#plot(as.dendrogram(otu.clus), horiz=TRUE)
pdf(file=args[2],width=20,height=20)
xm = as.numeric(args[5])
ym = as.numeric(args[6])
font_size=as.numeric(args[7])
#mode(xm)
#mode(ym)
heatmap.2(as.matrix(x),Rowv = as.dendrogram(otu.clus), Colv = as.dendrogram(samples.clus), col = colscale,margins=c(xm,ym),trace=c("none"),srtCol=90,key=FALSE, cexRow=font_size, cexCol=font_size)
dev.off()

#heatmap.2(as.matrix(x),Rowv = as.dendrogram(otu.clus), Colv = as.dendrogram(samples.clus), col = colscale,margins=c(xm,ym), ColSideColors = group1,trace=c("none"),srtCol=0,key=FALSE)
#hm<-heatmap.2(as.matrix(x),Rowv = as.dendrogram(otu.clus), Colv = as.dendrogram(samples.clus), col = colscale,margins=c(xm,ym), ColSideColors = group1,trace=c("none"),srtCol=0,key=FALSE)

#sorted <- x[match(rev(labels(hm$rowDendrogram)), rownames(x)), ]

#write.table(sorted,"table.txt")