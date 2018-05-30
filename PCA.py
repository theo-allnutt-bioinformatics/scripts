#!/usr/bin/python
import sys
import mdp
import numpy

#Calcualtes principal components and reports first three components.
#Input file is data only with no sample or variable titles. 
#Usage:
#PCA.py infile outfile

infile=sys.argv[1]
outfile=sys.argv[2]

f=open(infile,"r")

array2d = [[float(digit) for digit in line.split("\t")] for line in f]

print array2d

#change below depending on how data organised

#data = numpy.asarray(array2d) #vairables in columns, samples in rows
#tdata = numpy.transpose(array2d)
tdata = numpy.asarray(array2d) #variables in rows, sample in columns
data = numpy.transpose(array2d)

tdata = numpy.corrcoef(tdata) #use correlation (-1 to +1) isntead of raw values.. use this if variables are on different scales
data = numpy.corrcoef(data)


pca = mdp.nodes.PCANode(output_dim=3)

results = pca(data)

sumv=pca.d[0]+pca.d[1]+pca.d[2]

var1 =str(pca.d[0]/sumv * pca.explained_variance*100)
var2=str(pca.d[1]/sumv * pca.explained_variance*100)
var3=str(pca.d[2]/sumv * pca.explained_variance*100)

print "components of samples"
print results
#print dir(pca)
print "Explained % variance = ",pca.explained_variance*100

pca2 = mdp.nodes.PCANode(output_dim=3)

results2 = pca2(tdata)

print "components of variables"
print results2
print "variance"
print var1,var2,var3

g=open(outfile,"w")

g.write("principal components\n")

for i in results:
	g.write(str(i[0])+"\t"+str(i[1])+"\t"+str(i[2])+"\n")
g.write("\ncomponents of variables\n")

for i in results2:
	g.write(str(i[0])+"\t"+str(i[1])+"\t"+str(i[2])+"\n")

g.write("\nvariance\tpc1\tpc2\tpc3\n\t"+var1+"\t"+var2+"\t"+var3)

g.close()
f.close()
