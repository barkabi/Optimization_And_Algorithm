import cplex
from cplex.exceptions import CplexError

import sys
import numpy as np
import networkx as nx
import time

class MBST_ILP:
   	def __init__(self, Weight,Dest):
		self.my_obj = []
		self.my_ub = []
		self.my_lb = []
		self.my_ctype = ""
		self.my_colnames = []
		self.my_rhs = []
		self.my_rownames = []
		self.my_sense = ""
		self.my_obj = []
		self.my_ub = []
		self.my_lb = []
		self.my_ctype = ""
		self.my_colnames = []
		self.my_rhs = []
		self.my_rownames = []
		self.my_sense = ""
		self.Adj = np.array([[0,1,1,1,1,1,0,0,0,0],[1,0,1,1,0,1,0,1,0,0],[1,1,0,0,0,1,0,0,0,0],[1,1,0,0,1,1,1,1,1,1],[1,0,0,1,0,1,1,0,1,0],[1,1,1,1,1,0,0,0,0,0],[0,0,0,1,1,0,0,1,1,1],[0,1,0,1,0,0,1,0,0,1],[0,0,0,1,1,0,1,0,0,0],[0,0,0,1,0,0,1,1,0,0]])
		self.Weight=Weight

		
		self.DV_Mapping = {}
		self.Dest=Dest
		self.Num_Of_Routers=len(self.Adj)
		self.Decision_Variable_Counter = 0
		self.my_prob = cplex.Cplex()
		self.ConstraintCounter=0
		#self.my_prob.parameters.mip.tolerances.integrality.set(1e-15)
		self.Links=self.Extract_Links()
	def Extract_Links(self):
		Links=[]
		for i in range(len(self.Adj)):
			for j in range(len(self.Adj[0])):
				if self.Adj[i,j]==1:
					Links.append((i,j))

		return Links
	def populatebyrow(self, prob):
		# Our ILP Formulation

		#print "Inside ILP"
		# print self.Demand
		self.setDecisionVariables()
		self.setObjective()
		# print rows
		#FinalConstraints_List = []
		# We should remove Zero Quefficients from Each Row
		#MyConstraints=self.setConstraints()
		FinalConstraints_List = self.setConstraints()
		#print FinalConstraints_List

		#for i in range(len(FinalConstraints_List)):
		#	print "C"+str(i)+" ",
		#	for j in range(len(FinalConstraints_List[i][0])):
		#			print str(FinalConstraints_List[i][1][j])+" "+str(self.DV_Mapping[FinalConstraints_List[i][0][j]]),
		#	print self.my_rhs[i]
		#print "Inja"
		#for r in FinalConstraints_List:
		#	print r
		self.setLB_UB()

		prob.objective.set_sense(prob.objective.sense.minimize)
		prob.variables.add(obj=self.my_obj, lb=self.my_lb, ub=self.my_ub, types=self.my_ctype,names=self.my_colnames)

		prob.linear_constraints.add(lin_expr=FinalConstraints_List, senses=self.my_sense, rhs=self.my_rhs,names=self.my_rownames)

	def Problem_Solve(self):

		try:
			self.my_prob.set_log_stream(None)
			self.my_prob.set_error_stream(None)
			self.my_prob.set_warning_stream(None)
			self.my_prob.set_results_stream(None)
			#self.my_prob.set_results_stream(None)
			handle = self.populatebyrow(self.my_prob)
			#self.my_prob.solve()
			#self.my_prob.set_results_stream(sys.stdout)
			start_time=self.my_prob.get_time()
			self.my_prob.solve()
			end_time=self.my_prob.get_time()
			
		except CplexError, exc:
			#print exc
			#self.CheckPoint()
			print "Error dare"
			return

		# print
		# solution.get_status() returns an integer code
		OutputStatus = self.my_prob.solution.get_status()
		self.my_prob.solution.infeasibility.linear_constraints(self.my_prob.solution.get_values())

	
		#print "Solution status = ", OutputStatus
		if OutputStatus == 101 or OutputStatus == 102:
			
			# the following line prints the corresponding string
			#print self.my_prob.solution.status[self.my_prob.solution.get_status()]
			# print "Solution value  = ", self.my_prob.solution.get_objective_value()
			#print
			# solution.get_status() returns an integer code
			# print "Solution status = ", self.my_prob.solution.get_status(), ":",
			# the following line prints the corresponding string
			# print self.my_prob.solution.status[self.my_prob.solution.get_status()]
			#print "Solution value  = ", self.my_prob.solution.get_objective_value()

			numcols = self.my_prob.variables.get_num()
			#print numcols

			#numrows = self.my_prob.linear_constraints.get_num()
			#print numrows
			#slack = self.my_prob.solution.get_linear_slacks()
			x = self.my_prob.solution.get_values()
			#print x
			BestChoices = []
			BestChoices.append(['u',self.my_prob.solution.get_objective_value()])
			#print "Here"
			for j in range(numcols):
				MyDV = str(self.DV_Mapping[j]).split("_")
				#print "ohoho ",MyDV
				#if MyDV[0]=='Y':
				#	print self.DV_Mapping[j],"  ",x[j]," ",j," ",self.Weight[(int(MyDV[1]),int(MyDV[2]))]
				if MyDV[0]=='Y' and x[j]>0.9:
					#print 'PPPP ',MyDV[1],MyDV[2]

					BestChoices.append([int(MyDV[1]),int(MyDV[2])])

			#print "Injaaaaa",self.Weight
            
			return  self.Final_Result(BestChoices)
		# print "QQ",Results
		# return Results

		elif OutputStatus == 103:
			print "There is No Feasible Solution"
         
		elif OutputStatus==105:
			print "The Error Code", OutputStatus

	def setObjective(self):

		for i in range(len(self.my_colnames) - 1):
			self.my_obj.append(0)
		self.my_obj.append(1)
	
	def setLB_UB(self):
		for i in range(0, len(self.my_colnames)):
			self.my_lb.append(0)

	        self.my_ub = [0 for x in range(len(self.my_colnames) - 1)]

		for i in range(0, len(self.my_colnames) - 1):
			self.my_ub[i] = 1
			self.my_ctype += "B"
		self.my_ub.append(cplex.infinity)
		self.my_ctype += "C"
		#print self.my_lb
		#print self.my_ub
		#print self.my_ctype
	def setDecisionVariables(self):
		#For Y(l)
		for l in self.Links:
			self.DV_Mapping[self.Decision_Variable_Counter] = "Y_" + str(l[0]) + "_" + str(l[1])
			self.DV_Mapping["Y_" + str(l[0]) + "_" + str(l[1])] = self.Decision_Variable_Counter 
			self.my_colnames.append("Y_%d_%d" % (l[0], l[1]))
			self.Decision_Variable_Counter = self.Decision_Variable_Counter + 1
		
	

		#for X(v,l)

		for v in range(self.Num_Of_Routers):#For Source node: v
				for i in range(self.Num_Of_Routers):
					for j in range(self.Num_Of_Routers):
						if self.Adj[i,j]==1:
							self.DV_Mapping[self.Decision_Variable_Counter] = "X_" + str(v)+"_"+ str(i) + "_" + str(j)
							self.DV_Mapping["X_" + str(v)+"_"+str(i) + "_" + str(j)] = self.Decision_Variable_Counter 
							self.my_colnames.append("X_%d_%d_%d" % (v, i, j))
							self.Decision_Variable_Counter = self.Decision_Variable_Counter + 1

		self.my_colnames.append("u")
		self.DV_Mapping[self.Decision_Variable_Counter] = "u"
		self.DV_Mapping["u"] = self.Decision_Variable_Counter
		self.Decision_Variable_Counter = self.Decision_Variable_Counter + 1
		#print self.DV_Mapping
	def setConstraints(self):
		#Constraint Number 1: Sigma(Y(l))=N-1
		rows = []
		VarName = [x for x in range(self.Decision_Variable_Counter)]
		Quefficients = [0 for x in range(self.Decision_Variable_Counter)]
		self.my_rownames.append("C" + str(self.ConstraintCounter))
		for l in self.Links:

			Quefficients[self.DV_Mapping["Y_" + str(l[0]) + "_" + str(l[1])]]=1

		self.my_sense += "E"
		self.my_rhs.append(self.Num_Of_Routers-1)
		tmpList = [VarName, Quefficients]
		self.ConstraintCounter = self.ConstraintCounter + 1
		rows.append(tmpList)


		#Constraint Number 2: Sigma(Y(l) for ln(out))=1
		Quefficients = [0 for x in range(self.Decision_Variable_Counter)]
		for i in range(self.Num_Of_Routers):
			if i!=self.Dest:
				for j in range(self.Num_Of_Routers):
					if self.Adj[i,j]==1:
						Quefficients[self.DV_Mapping["Y_" + str(i) + "_" + str(j)]]=1
				self.my_rownames.append("C" + str(self.ConstraintCounter))
				self.my_sense += "E"
				self.my_rhs.append(1)
				tmpList = [VarName, Quefficients]

				rows.append(tmpList)
				self.ConstraintCounter = self.ConstraintCounter + 1
				Quefficients = [0 for x in range(self.Decision_Variable_Counter)]

		#Constraint Number 3: Sigma(Y(l out)for dest)=0
		Quefficients = [0 for x in range(self.Decision_Variable_Counter)]
		for j in range(self.Num_Of_Routers):
			if self.Adj[self.Dest,j]==1:
				Quefficients[self.DV_Mapping["Y_" + str(self.Dest) + "_" + str(j)]]=1
		self.my_rownames.append("C" + str(self.ConstraintCounter))
		self.my_sense += "E"
		self.my_rhs.append(0)
		tmpList = [VarName, Quefficients]
		self.ConstraintCounter = self.ConstraintCounter + 1

		rows.append(tmpList)




		#Constraint Number 4: y(l)*Weight(l)<=Alpha
		Quefficients = [0 for x in range(self.Decision_Variable_Counter)]
		for l in self.Links:
			self.my_rownames.append("C" + str(self.ConstraintCounter))
			Quefficients[self.DV_Mapping["Y_" + str(l[0]) + "_" + str(l[1])]]=self.Weight[l]
			Quefficients[self.DV_Mapping["u"]]=-1
			self.my_sense += "L"
			self.my_rhs.append(0)
			tmpList = [VarName, Quefficients]
			#print tmpList
			rows.append(tmpList)
			self.ConstraintCounter = self.ConstraintCounter + 1
			Quefficients = [0 for x in range(self.Decision_Variable_Counter)]



		#Constraint Number 5: Path constraint from each node v to the destination 
		for v in range(self.Num_Of_Routers):#For Source node: v
				for i in range(self.Num_Of_Routers):
					for j in range(self.Num_Of_Routers):
						if self.Adj[i,j]==1:
							Quefficients[self.DV_Mapping["X_" + str(v)+ "_"+ str(i) + "_" + str(j)]]=1
					for j in range(self.Num_Of_Routers):
						if self.Adj[j,i]==1:
							Quefficients[self.DV_Mapping["X_" + str(v)+ "_"+ str(j) + "_" + str(i)]]=-1
					if v==i:
						#if self.ConstraintCounter==33:
						#	print "Hey 1",[VarName, Quefficients]
						self.my_rownames.append("C" + str(self.ConstraintCounter))
						self.my_sense += "E"
						self.my_rhs.append(1)
						tmpList = [VarName, Quefficients]
						rows.append(tmpList)
						self.ConstraintCounter = self.ConstraintCounter + 1
						Quefficients = [0 for x in range(self.Decision_Variable_Counter)]
					elif i==self.Dest:
						self.my_rownames.append("C" + str(self.ConstraintCounter))
						#if self.ConstraintCounter==33:
						#	print "Hey 2",[VarName, Quefficients]
						#	for index in range(len(Quefficients)):
						#		if Quefficients[index]==1:
						#			print self.DV_Mapping[VarName[index]]
									
						self.my_sense += "E"
						self.my_rhs.append(-1)
						tmpList = [VarName, Quefficients]

						rows.append(tmpList)
						self.ConstraintCounter = self.ConstraintCounter + 1
						Quefficients = [0 for x in range(self.Decision_Variable_Counter)]

					elif v!=i and v!=self.Dest:
						self.my_rownames.append("C" + str(self.ConstraintCounter))
						#if self.ConstraintCounter==33:
						#	print "Hey 3",[VarName, Quefficients]
						self.my_sense += "E"
						self.my_rhs.append(0)
						tmpList = [VarName, Quefficients]
						rows.append(tmpList)
						self.ConstraintCounter = self.ConstraintCounter + 1
						Quefficients = [0 for x in range(self.Decision_Variable_Counter)]

						

		#Constraint Number 6: X(v,l)<=Y(l)
		Quefficients = [0 for x in range(self.Decision_Variable_Counter)]
		for j in range(self.Num_Of_Routers):
			for l in self.Links:
				if j!=self.Dest:
					self.my_rownames.append("C" + str(self.ConstraintCounter))
					Quefficients[self.DV_Mapping["X_" + str(j)+ "_"+ str(l[0]) + "_" + str(l[1])]]=1
					Quefficients[self.DV_Mapping["Y_" + str(l[0]) + "_" + str(l[1])]]=-1
					self.my_sense += "L"
					self.my_rhs.append(0)
					tmpList = [VarName, Quefficients]
					rows.append(tmpList)
					self.ConstraintCounter = self.ConstraintCounter + 1
					Quefficients = [0 for x in range(self.Decision_Variable_Counter)]
					

		return rows

	def CheckPoint(self):
		print "Objective " + str(self.my_obj) + " " + str(len(self.my_obj))
		print "my_sense " + str(self.my_sense) + " " + str(len(self.my_sense))
		print "my_ctype " + str(self.my_ctype) + " " + str(len(self.my_ctype))
		print "my_lb " + str(self.my_lb) + " " + str(len(self.my_lb))
		print "my_ub " + str(self.my_ub) + " " + str(len(self.my_ub))
		print "my_rhs " + str(self.my_rhs) + " " + str(len(self.my_rhs))
		print "my_colnames " + str(self.my_colnames) + " " + str(len(self.my_colnames))
		print "my_rownames " + str(self.my_rownames) + " " + str(len(self.my_rownames))
		a = cplex.Cplex()
		print a.get_versionnumber()
	def Final_Result(self,OurBestChoices):
		#print OurBestChoices
		g2 = nx.DiGraph(directed=True) 
	
		for l in OurBestChoices:
			if l[0]!='u':
				#print l[0],l[1]
				g2.add_edge(int(l[0]), int(l[1]), weight=self.Weight[int(l[0]),int(l[1])])
	
		MySP=dict(nx.all_pairs_dijkstra_path(g2))
		return MySP

def test():
	start_time = time.time()
	#Adj = np.array([[0,1,1,0,0,0],[1,0,1,0,0,0],[1,0,0,0,1,1],[0,1,0,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0]])
	Adj = np.array([[0,1,1,1,1,1,0,0,0,0],[1,0,1,1,0,1,0,1,0,0],[1,1,0,0,0,1,0,0,0,0],[1,1,0,0,1,1,1,1,1,1],[1,0,0,1,0,1,1,0,1,0],[1,1,1,1,1,0,0,0,0,0],[0,0,0,1,1,0,0,1,1,1],[0,1,0,1,0,0,1,0,0,1],[0,0,0,1,1,0,1,0,0,0],[0,0,0,1,0,0,1,1,0,0]])
	#Weight=np.array([[0.0,4.0,2.0,0.0,0.0,0.0],[0.0,0.0,3.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,6.0,1.0],[0.0,8.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,7.0,0.0,0.0],[0.0,0.0,0.0,0.0,5.0,0.0]])
	Links=[]
	for i in range(len(Adj)):
		for j in range(len(Adj[0])):
			if Adj[i,j]==1:
				Links.append((i,j))

	print Links

	Weight={}
	for l in Links:
		Weight[l]=0.0
	#Weight[(0,1)]=4.0
	#Weight[(0,2)]=2.0
	#Weight[(1,0)]=3.0
	#Weight[(1,2)]=3.0
	#Weight[(2,0)]=4.0	
	#Weight[(2,4)]=4.0
	#Weight[(2,5)]=4.0
	#Weight[(3,1)]=8.0
	#Weight[(4,3)]=7.0
	#Weight[(5,4)]=5.0

	Weight= {(7, 3): 0, (6, 9): 0, (1, 3): 1.3193925826702379e-07, (4, 8): 1.0494871786469067e-07, (3, 0): 1.7359592376631785e-07, (2, 1): 3.9266711845145084e-08, (5, 1): 0, (3, 7): 1.53920810711852e-05, (2, 5): 0, (0, 3): 0, (4, 0): 0, (1, 2): 2.485598150394509e-08, (6, 7): 1.1996578423204694e-07, (7, 6): 0, (6, 3): 0, (1, 5): 0, (3, 6): 1.54584401306317e-05, (0, 4): 0, (8, 6): 1.5041359483502648e-05, (7, 9): 0, (9, 7): 3.345173663177846e-07, (6, 4): 2.7136631120181612e-08, (5, 4): 6.8080855375905906e-09, (4, 6): 1.5283886913950054e-05, (5, 0): 0, (7, 1): 0, (4, 5): 1.842121125532479e-07, (9, 3): 1.2742428820411266e-07, (3, 5): 0, (3, 9): 1.5215228891960108e-05, (0, 5): 3.319800164984861e-08, (1, 0): 0, (9, 6): 9.110320267858704e-08, (5, 3): 9.287217791128158e-08, (0, 1): 0, (8, 3): 0, (6, 8): 7.073049723187273e-09, (3, 4): 8.648610859338344e-08, (3, 1): 2.1680388934908423e-07, (3, 8): 2.310908306284599e-07, (2, 0): 0, (4, 3): 1.5662222010318528e-07, (1, 7): 1.529442204386435e-05, (5, 2): 0, (0, 2): 0, (8, 4): 0}


	
	print Links
	MBST=MBST_ILP(Weight,Dest=7)
	MBST.CheckPoint()
	OurBestChoices=MBST.Problem_Solve()
	print "FFF"
	print OurBestChoices

	#Extracting the paths
	#g2 = nx.DiGraph(directed=True) 

	#for l in OurBestChoices:
	#	if l[0]!='u':
			#print l[0],l[1]
	#		g2.add_edge(l[0], l[1], weight=Weight[(int(l[0]),int(l[1]))])

	#MySP=dict(nx.all_pairs_dijkstra_path(g2))
	#print "SP "
	#print MySP
	print("--- %s seconds ---" % (time.time() - start_time))

#test()
