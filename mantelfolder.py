#!/usr/bin/python
import numpy as np
from itertools import permutations
from scipy import spatial, stats
import sys
import re
import glob
import subprocess


digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))


infolder = sys.argv[1] 

g=open(sys.argv[2]+".list",'w')
h=open(sys.argv[2]+".dist",'w')

infiles=glob.glob(infolder+"/*")

infiles.sort(key=tokenize)

#thresh=float(sys.argv[3])

#for 57.17
#from https://github.com/jwcarr/MantelTest/blob/master/Mantel.py

def mantel_test(X, Y, perms=10000, method='pearson', tail='two-tail'):


	# Ensure that X and Y are formatted as Numpy arrays.
	X, Y = np.asarray(X, dtype=float), np.asarray(Y, dtype=float)

	# Check that X and Y are valid distance matrices.
	if spatial.distance.is_valid_dm(X) == False and spatial.distance.is_valid_y(X) == False:
		raise ValueError('X is not a valid condensed or redundant distance matrix')
	if spatial.distance.is_valid_dm(Y) == False and spatial.distance.is_valid_y(Y) == False:
		raise ValueError('Y is not a valid condensed or redundant distance matrix')

	# If X or Y is a redundant distance matrix, reduce it to a condensed distance matrix.
	if len(X.shape) == 2:
		X = spatial.distance.squareform(X, force='tovector', checks=False)
	if len(Y.shape) == 2:
		Y = spatial.distance.squareform(Y, force='tovector', checks=False)

	# Check for size equality.
	if X.shape[0] != Y.shape[0]:
		raise ValueError('X and Y are not of equal size')

	# Check for minimum size.
	if X.shape[0] < 3:
		raise ValueError('X and Y should represent at least 3 objects')

	# If Spearman correlation is requested, convert X and Y to ranks.
	if method == 'spearman':
		X, Y = stats.rankdata(X), stats.rankdata(Y)

	# Check for valid method parameter.
	elif method != 'pearson':
		raise ValueError('The method should be set to "pearson" or "spearman"')

	# Check for valid tail parameter.
	if tail != 'upper' and tail != 'lower' and tail != 'two-tail':
		raise ValueError('The tail should be set to "upper", "lower", or "two-tail"')

	X_residuals, Y_residuals = X - X.mean(), Y - Y.mean()

	# Expand the Y residuals to a redundant matrix.
	Y_residuals_as_matrix = spatial.distance.squareform(Y_residuals, force='tomatrix', checks=False)

	# Get the number of objects.
	m = Y_residuals_as_matrix.shape[0]

	# Calculate the number of possible matrix permutations.
	n = np.math.factorial(m)

	# Initialize an empty array to store temporary permutations of Y_residuals.
	Y_residuals_permuted = np.zeros(Y_residuals.shape[0], dtype=float)

	# If the number of requested permutations is greater than the number of
	# possible permutations (m!) or the perms parameter is set to 0, then run a
	# deterministic Mantel test ...
	if perms >= n or perms == 0:

		# Initialize an empty array to store the covariances.
		covariances = np.zeros(n, dtype=float)

		# Enumerate all permutations of row/column orders and iterate over them.
		for i, order in enumerate(permutations(range(m))):

			# Take a permutation of the matrix.
			Y_residuals_as_matrix_permuted = Y_residuals_as_matrix[order, :][:, order]

			# Condense the permuted version of the matrix. Rather than use
			# distance.squareform(), we call directly into the C wrapper for speed.
			spatial.distance._distance_wrap.to_vector_from_squareform_wrap(Y_residuals_as_matrix_permuted, Y_residuals_permuted)

			# Compute and store the covariance.
			covariances[i] = (X_residuals * Y_residuals_permuted).sum()

	# ... otherwise run a stochastic Mantel test.
	else:

		# Initialize an empty array to store the covariances.
		covariances = np.zeros(perms, dtype=float)

		# Initialize an array to store the permutation order.
		order = np.arange(m)

		# Store the veridical covariance in 0th position...
		covariances[0] = (X_residuals * Y_residuals).sum()

		# ...and then run the random permutations.
		for i in range(1, perms):

			# Choose a random order in which to permute the rows and columns.
			np.random.shuffle(order)

			# Take a permutation of the matrix.
			Y_residuals_as_matrix_permuted = Y_residuals_as_matrix[order, :][:, order]

			# Condense the permuted version of the matrix. Rather than use
			# distance.squareform(), we call directly into the C wrapper for speed.
			spatial.distance._distance_wrap.to_vector_from_squareform_wrap(Y_residuals_as_matrix_permuted, Y_residuals_permuted)

			# Compute and store the covariance.
			covariances[i] = (X_residuals * Y_residuals_permuted).sum()

	# Calculate the veridical correlation coefficient from the veridical covariance.
	r = covariances[0] / np.sqrt((X_residuals ** 2).sum() * (Y_residuals ** 2).sum())

	# Calculate the empirical p-value for the upper or lower tail.
	if tail == 'upper':
		p = (covariances >= covariances[0]).sum() / float(covariances.shape[0])
	elif tail == 'lower':
		p = (covariances <= covariances[0]).sum() / float(covariances.shape[0])
	elif tail == 'two-tail':
		p = (abs(covariances) >= abs(covariances[0])).sum() / float(covariances.shape[0])

	# Calculate the standard score.
	z = (covariances[0] - covariances.mean()) / covariances.std()

	return r, p, z
	
print infiles

g.write("source\ttarget\tR\tP\tZ\n")

tot=len(infiles)
h.write(str(tot)+"\n")

c=-1
for i in infiles:
	c=c+1
	a=np.loadtxt(i,dtype=float)
	a=np.asmatrix(a,dtype=float)
	
	#print a
	iname=i.split("/")[-1].split(".")[0]
	
	if len(iname)<10:
		h.write(iname+" "*(9-len(iname))+" "*c)
	else:
		h.write(iname[:8]+" "+" "*c)
	
	for j in infiles[c:]:
		
		jname=j.split("/")[-1].split(".")[0]
		
		b=np.loadtxt(j,dtype=float)
		b=np.asmatrix(b,dtype=float)
		
		#print b
		x=mantel_test(a,b)
		
		#if float(x[0])>=thresh:
		g.write(iname+"\t"+jname+"\t"+str(x[0])+"\t"+str(x[1])+"\t"+str(x[2])+"\n")
		print iname,jname,x
		
		dist=1-x[0]
		h.write(" "+str(dist))
		
		
		
	h.write("\n")
		
		
		
		
		
		
		
		
