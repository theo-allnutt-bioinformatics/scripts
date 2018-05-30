
from ete3 import Tree, TreeStyle, NodeStyle, faces, AttrFace, CircleFace, TextFace
import sys

tree1 = Tree(sys.argv[1])
datafile=open(sys.argv[2])

global scale1

scale1=float(sys.argv[3])

def get_tree(tree1,abundance):
	
	
	for n in tree1.iter_leaves():
		
		
		face1= CircleFace(abundance[n.name][0],abundance[n.name][1],style='sphere')
		face2=TextFace(n.name,ftype='Verdana', fsize=10, fgcolor='black', penwidth=0, fstyle='normal', tight_text=False, bold=False)
		face1.opacity=0.9
		
		n.add_face(face1,column=0)
		n.add_face(face2,column=0,position="branch-right") #branch-top branch-bottom branch-right
		
	tree1.ladderize()
	
	ts = TreeStyle()
	ts.mode= 'r'
	ts.scale=scale1
	ts.show_leaf_name = False

	return tree1,ts

abundance={}
ab1=[]
for i in datafile:
	print i.rstrip("\n")
	ab1.append(float(i.split("\t")[1]))
ab2=[]#normalise bubble sizes to scale
for x in ab1:
	ab2.append(float(x/max(ab1))*(scale1/10))
	
datafile.seek(0)
c=-1
for i in datafile:
	c=c+1
	a=ab2[c]
	col=i.split("\t")[2].rstrip("\n")
	leaf_name=i.split("\t")[0]
	d=[a,col]
	abundance[leaf_name]=d
	
	
t,ts= get_tree(tree1,abundance)
t.render("bubble.png", w=1200, dpi=600)
#t.render("bubble.svg", w=1200, dpi=1200)
t.show(tree_style=ts)


