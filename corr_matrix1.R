#!/usr/bin/Rscript


#makes a correlation matrix from one otu input tables

library(Hmisc)
library(vcd)

args = commandArgs(trailingOnly=TRUE)

x <- read.table(args[1],sep="\t",header=TRUE,check.names=FALSE)

a<-unlist(strsplit(args[1],"\\."))[1]

name1 <- paste(a,"_pearson.tab",sep="")

row.names(x) <- x$gene

x <- x[,-1]

x <- t(x)
row.names(x)
names(x)
#head(x)

c1 <- rcorr(x,type="pearson")

c1.r <- data.frame(c1$r)
c1.p <- data.frame(c1$P) #p values

write.csv(c1.r,name1)
#write.table(c1.r,name1,sep="\t",quote=FALSE,row.names=TRUE)
#write.table("Pearson P-value\n",name1,append=TRUE,sep="\t",quote=FALSE,col.names=TRUE,row.names=TRUE)
#write.table(c1.p,name1,append=TRUE,sep="\t",quote=FALSE,col.names=TRUE,row.names=TRUE)



 



