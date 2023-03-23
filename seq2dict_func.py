def seq2dict(seqfile):

	print("seq2dict")

	data={}

	i=seqfile.readline()
	while i!="":
		
		id1=i[1:].split(" ")[0]
		
		suffix=id1[-2:]
		if suffix == ".1" or suffix == ".2" or suffix == "/1" or suffix == "/2" or suffix == "_1" or suffix == "_2":
			id1=id1[:-2]
		
		s1=seqfile.readline()#seq
		i=seqfile.readline() #+
		q1=seqfile.readline() #qual
		i=seqfile.readline() #next id
	
		data[id1]=(s1,q1)
	
	return data
	