import edmonds
import networkx as nx
from networkx.algorithms.tree import branchings
from collections import defaultdict, namedtuple

g={'1': {'0': -0.0007305538062814656, '3': -2.041137931431335e-12, '2': -1.7569974227104004e-13, '4': -7.269939802367565e-05}, '0': {'1': -4.736154985519917e-09, '4': -9.189194457704936e-13}, '3': {'1': -9.412545052149416e-05, '2': -1.3140157797176135e-12, '4': -9.41207070433786e-05}, '2': {'1': -9.411708902129708e-05, '3': -3.6025707472478062e-12}, '4': {'1': -9.412545012439288e-05, '0': -0.0006079236559595177, '3': -7.103038166264593e-13}}



print 
h = edmonds.mst('0',g)
for s in h:
        for t in h[s]:
            print  (s,t),h[s][t]
print

cost=1
m = nx.DiGraph() 
m.add_edge(1, 0, weight=-0.0007305538062814656+cost)
m.add_edge(1, 3, weight=-2.041137931431335e-12+cost)
m.add_edge(1, 2, weight=-1.7569974227104004e-13+cost)
m.add_edge(1, 4, weight=-7.269939802367565e-05+cost)
m.add_edge(0, 1, weight=-4.736154985519917e-09+cost)
m.add_edge(0, 4, weight=-9.189194457704936e-13+cost)
m.add_edge(3, 1, weight=-9.412545052149416e-05+cost)
m.add_edge(3, 2, weight=-1.3140157797176135e-12+cost)
m.add_edge(3, 4, weight=-9.41207070433786e-05+cost)
m.add_edge(2, 1, weight=-9.411708902129708e-05+cost)
m.add_edge(2, 3, weight=-3.6025707472478062e-12+cost)
m.add_edge(4, 1, weight=-9.412545012439288e-05+cost)
m.add_edge(4, 0, weight=-0.0006079236559595177+cost)
m.add_edge(4, 3, weight=-7.103038166264593e-13+cost)
print len(m.edges())
#b=nx.minimum_spanning_arborescence(m,attr='weight', default=1,preserve_attrs=False)
b=branchings.minimum_spanning_arborescence(m)
print "Here"
edges=b.edges()
for a in edges():
	print a[0],a[1],b[a[0]][a[1]]['weight']	


Arc = namedtuple('Arc', ('tail', 'weight', 'head'))


newG=[]
for node1,adj in g.items():
		for node2,cost in adj.items():
			newG.append(Arc(int(node1),cost,int(node2)))
print 

def min_spanning_arborescence(arcs, sink):
    good_arcs = []
    quotient_map = {arc.tail: arc.tail for arc in arcs}
    quotient_map[sink] = sink
    while True:
        min_arc_by_tail_rep = {}
        successor_rep = {}
        for arc in arcs:
            if arc.tail == sink:
                continue
            tail_rep = quotient_map[arc.tail]
            head_rep = quotient_map[arc.head]
            if tail_rep == head_rep:
                continue
            if tail_rep not in min_arc_by_tail_rep or min_arc_by_tail_rep[tail_rep].weight > arc.weight:
                min_arc_by_tail_rep[tail_rep] = arc
                successor_rep[tail_rep] = head_rep
        cycle_reps = find_cycle(successor_rep, sink)
        if cycle_reps is None:
            good_arcs.extend(min_arc_by_tail_rep.values())
            return spanning_arborescence(good_arcs, sink)
        good_arcs.extend(min_arc_by_tail_rep[cycle_rep] for cycle_rep in cycle_reps)
        cycle_rep_set = set(cycle_reps)
        cycle_rep = cycle_rep_set.pop()
        quotient_map = {node: cycle_rep if node_rep in cycle_rep_set else node_rep for node, node_rep in quotient_map.items()}


def find_cycle(successor, sink):
    visited = {sink}
    for node in successor:
        cycle = []
        while node not in visited:
            visited.add(node)
            cycle.append(node)
            node = successor[node]
        if node in cycle:
            return cycle[cycle.index(node):]
    return None


def spanning_arborescence(arcs, sink):
    arcs_by_head = defaultdict(list)
    for arc in arcs:
        if arc.tail == sink:
            continue
        arcs_by_head[arc.head].append(arc)
    solution_arc_by_tail = {}
    stack = arcs_by_head[sink]
    while stack:
        arc = stack.pop()
        if arc.tail in solution_arc_by_tail:
            continue
        solution_arc_by_tail[arc.tail] = arc
        stack.extend(arcs_by_head[arc.tail])
    return solution_arc_by_tail

try:
	MSA=(min_spanning_arborescence(newG,0))
	for key,val in MSA.items():
		print key,val,val[0],val[1],val[2]
except:
	print "Error"


