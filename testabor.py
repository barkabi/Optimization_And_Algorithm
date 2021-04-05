import networkx as nx
from networkx.algorithms.tree import branchings
g = nx.DiGraph()
#g.add_nodes_from([1,2,3,4,5,6])
g.add_edge(1,2,weight=0)
g.add_edge(1,3,weight=-8)
g.add_edge(1,4,weight=0)
g.add_edge(4,3,weight=-9)
g.add_edge(3,2,weight=-6)
g.add_edge(2,5,weight=-8)
g.add_edge(5,4,weight=-8)
g.add_edge(2,6,weight=-6)
g.add_edge(4,6,weight=-2)



print g.edges()
x = branchings.minimum_spanning_arborescence(g)
print x.edges()
for i in x.edges():
	print i
a=list(x.edges_iter(data='weight', default=1))
sum=0
for i in a:
	sum+=i[2]
print sum

