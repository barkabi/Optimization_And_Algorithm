import networkx as nx
import matplotlib.pyplot as plt
edges = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 0], [1, 2], [1,5], [1, 7], [2, 0], [2, 1], [2, 3], [3, 0], [3, 2], [3, 4],[3, 6], [3, 7], [3, 8], [3, 9], [4, 0], [4, 3], [4, 5], [4, 6], [4, 8], [5, 0], [5, 1], [5, 4], [6, 3], [6, 4], [6, 8], [6, 9], [7, 1], [7, 3], [7, 9], [8, 3], [8, 4], [8, 6], [9, 3], [9, 6],[9, 7]]
NumOfNodes=10
adjMatrix = [[0 for i in range(NumOfNodes)] for k in range(NumOfNodes)]
for tmp1 in edges:
		adjMatrix[tmp1[0]][tmp1[1]]=1
print adjMatrix

g = nx.DiGraph(edges)

nx.draw_networkx(g)
plt.show()
