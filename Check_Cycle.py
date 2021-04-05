import networkx as nx
import matplotlib.pyplot as plt

# Create Directed Graph
G=nx.DiGraph()

# Add a list of nodes:
G.add_nodes_from(['1','2','3'])

# Add a list of edges:
G.add_edges_from([(1,2),(2,3), (1,3)])

#Return a list of cycles described as a list o nodes
print list(nx.simple_cycles(G))
