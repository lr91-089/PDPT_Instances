# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import time

import gurobipy as gp
from gurobipy import GRB, quicksum, tuplelist

filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-5.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R10-K3-T3/PDPT-R10-K3-T3-Q100-9.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-9.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R20-K2-T1/PDPT-R20-K2-T1-Q100-0.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"

#filename = "./InstancesLyu23/PDPT_small/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-9.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R30-K3-T3/PDPT-R30-K3-T3-Q100-4.txt"

gurobi_status_dict = {1: 'LOADED',
  2: 'OPTIMAL',
  3: 'INFEASIBLE',
  4: 'INF_OR_UNBD',
  5: 'UNBOUNDED',
  6: 'CUTOFF',
  7: 'ITERATION_LIMIT',
  8: 'NODE_LIMIT',
  9: 'TIME_LIMIT',
  10: 'SOLUTION_LIMIT',
  11: 'INTERRUPTED',
  12: 'NUMERIC',
  13: 'SUBOPTIMAL',
  14: 'INPROGRESS',
  15: 'USER_OBJ_LIMIT',
  16: 'WORK_LIMIT',
  17: 'MEM_LIMIT'}



# Read the meta-data of problem (number of requests, number of vehicles, number of transport stations, capability of vehicles)
def readMetaData(filename):
    metaData = pd.read_csv(filename, nrows=2, sep= '\t', on_bad_lines='skip')
    return metaData

# Read the instance's data (name of node, location (x, y), time-windows, load of the request)
def readDataframe(filename):
    df = pd.read_csv(filename, skiprows=3, sep='\t')
    return df

# Calculate the Euclid-distance between locations
def calculateDistance(x1, x2, y1, y2):
    return math.sqrt((x2 - x1)**2 + (y2-y1)**2)

# Generate distance-matrix between locations
def distancesMatrix(df):
    matrix = {}
    for location1 in df["node"]:
        for location2 in df["node"]:
            if location1 != location2:
                x1 = df.loc[df["node"]==location1, 'x']
                x2 = df.loc[df["node"]==location2, 'x']
                y1 = df.loc[df["node"]==location1, 'y']
                y2 = df.loc[df["node"]==location2, 'y']
                matrix[location1, location2] = calculateDistance(int(x1), int(x2), int(y1), int(y2))
    return matrix

# Generate dictionary of (node:load)
def loadDict(df):
    matrix = {}
    for location in df["node"]:
        matrix[location] = df.loc[df["node"]==location, 'load'].values[0]
    return matrix



def getNodeList(df):
    allNodes = df['node']
    rOrigins = df.loc[df['node'].str.contains('p'),'node']
    rDestinations = df.loc[df['node'].str.contains('d'),'node']
    vOrigins = df.loc[df['node'].str.contains('o'),'node']
    vDestinations = df.loc[df['node'].str.contains('e'),'node']
    transferNodes = df.loc[df['node'].str.contains('t'),'node']
    return {"a":allNodes, "ro":rOrigins, "rd":rDestinations, "vo":vOrigins, "vd":vDestinations, "t":transferNodes}

# Callback gap vs time
def data_cb(model, where):
    if where == gp.GRB.Callback.MIP:
        cur_obj = model.cbGet(gp.GRB.Callback.MIP_OBJBST)
        cur_bd = model.cbGet(gp.GRB.Callback.MIP_OBJBND)
        gap = (abs(cur_bd - cur_obj)/abs(cur_obj))*100
        
        # Change in obj value or bound?
        if model._obj != cur_obj or model._bd != cur_bd:
            model._obj = cur_obj
            model._bd = cur_bd
            model._gap = gap
            model._data.append([time.time() - model._start, cur_obj, cur_bd, gap])

# Model, Parameters, Variables and Objective Function
def raisModel(filename):
    model = gp.Model("RaisNeuImproved_onlyPreprocessing")
    metaData = readMetaData(filename)
    df = readDataframe(filename)
    nodeList = getNodeList(df)
    
    V =  frozenset(nodeList["a"])
    P = frozenset(nodeList["ro"])
    D = frozenset(nodeList["rd"])
    VO = frozenset(nodeList["vo"])
    VD = frozenset(nodeList["vd"])
    T = frozenset(nodeList["t"])
    
    K = list(range(int(metaData['nv'])))
    R = list(range(int(metaData['nr'])))
    
    #A = [(i,j) for i in V for j in V if j!=i]
    
    #A = tuplelist(A)
    nRequests = int(metaData['nr'])
    nVehicles = int(metaData['nv'])
    nTransports = int(metaData['nt'])
    vCapability = int(metaData['capacity'])
    

    c = distancesMatrix(df)
    u = {k:vCapability for k in K}
    VC = max(u.values())
    qnode = df.set_index('node')["load"].to_dict()
    q = {int(node.replace("p","")):qnode[node] for node in P}


    print(df)
    
    df["tw"] = df[["a","b"]].values.tolist()
    
    timeWindows = df.set_index('node')["tw"].to_dict()
    
    Mij = {(i,j):max(0,timeWindows[i][1]+c[i,j]-timeWindows[j][0]) for (i,j) in c}
    M = max(Mij.values())
    #change travel times
    def check_no_time_window_violation(i,j):
        if timeWindows[i][0]+c[i,j]<=timeWindows[j][1]:
            return True
        return False
    

    Akc= [(k,i, j) for k in K for i in P for j in V-(frozenset((i,))|VO|VD) if j!=i]
    Akd= [(k,i, j) for k in K for i in D for j in V-(frozenset((i,f"p{i}"))|VO|(VD-frozenset([f"e{k}"]))) if j!=i]
    Aks= [(k,i, j) for k in K for i in T for j in V-(frozenset((i,))|VO|(VD-frozenset([f"e{k}"]))) if j!=i]
    AkoOut= [(k,i, j) for k in K for i in [f"o{k}"] for j in V-D-VO-(VD-frozenset([f"e{k}"])) if j!=i]
    arcs_filtered1 = Akc+Akd+Aks+AkoOut
    
    A = set()
    
    for (k,i,j) in arcs_filtered1:
        if check_no_time_window_violation(i,j):
            if i in P and j in P or i in D and j in D:
                if abs(qnode[i])+abs(qnode[j])<=VC:
                    A.add((k,i,j))
            elif  i in P and j in D or i in D and j in P:
                if abs(qnode[i]+qnode[j])<=VC:
                    A.add((k,i,j))
            else:
                A.add((k,i,j))
    
    A = tuplelist(A)

    Ayc = [(k,r,i,j) for r in R for k in K for i in P for j in V-(frozenset((i,f"p{r}"))|VO|VD) if (k,i,j) in A]
    Ayd = [(k,r,i,j) for r in R for k in K for i in D-frozenset([f"d{r}"]) for j in V-(frozenset([i,i.replace("d","p"),f"p{r}"])|VO|VD) if (k,i,j) in A]
    Ays = [(k,r,i,j) for r in R for k in K for i in T for j in V-(frozenset((i,f"p{r}"))|VO|VD) if (k,i,j) in A]

    Ay = Ayc + Ayd + Ays

    Ay = tuplelist(Ay)
    

    # Testing Symmetries Breaking Constraints
    # df.loc[df['node'].str.contains('o'), 'x'] = 50
    # df.loc[df['node'].str.contains('o'), 'y'] = 50
    # df.loc[df['node'].str.contains('e'), 'x'] = 50
    # df.loc[df['node'].str.contains('e'), 'y'] = 50

   


    sIndex = [(k1, k2, t, r) for k1 in K for k2 in K for t in T for r in R if k1 != k2]
    
    aIndex = [(k, i) for k in K for i in V-(VO-frozenset([f"o{k}"]))-(VD-frozenset([f"e{k}"]))]
    bIndex = [(k, i) for k in K for i in V-(VO-frozenset([f"o{k}"]))-(VD-frozenset([f"e{k}"]))]

    x = model.addVars(A, vtype=GRB.BINARY, name='x')
    y = model.addVars(Ay, vtype=GRB.BINARY, name='y')
    s = model.addVars(sIndex, vtype=GRB.BINARY, name='s')
    #at = model.addVars(aIndex, lb=0.0 ,vtype=GRB.CONTINUOUS, name='at')
    #bt = model.addVars(bIndex, lb=0.0 ,vtype=GRB.CONTINUOUS, name='bt')
    a = model.addVars(aIndex, lb=0.0 ,vtype=GRB.CONTINUOUS, name='a')
    b = model.addVars(bIndex, lb=0.0 ,vtype=GRB.CONTINUOUS, name='b')
    f = model.addVars(T, vtype=GRB.BINARY, name='f')

    model.setObjective(sum((c[i,j] * x[k, i, j]) for (k,i,j) in A), GRB.MINIMIZE)
    model.update()
    
    #model.addConstr(x[3,"p2","t3"]==1)
    #model.addConstr(x[3,"t3","t0"]==1)
    #model.addConstr(x[3,"t0","d1"]==1)
    #model.addConstr(x[0,"p1","t3"]==1)
    #model.addConstr(x[0,"t3","e0"]==1)
    #model.addConstr(x[2,"o2","e2"]==1)
    #model.addConstr(x[2,"o2","e2"]==1)


    # Constraints
    model.addConstrs((quicksum(x[k, i, j] for j in [a[2] for a in A.select(k,i,'*')])==1 for k in K for i in [f"o{k}"]),name="constr25")
    model.addConstrs((quicksum(x[k, j,i] for j in [a[1] for a in A.select(k,'*',i)])==1 for k in K for i in [f"e{k}"]),name="constr26")

    #model.addConstrs((quicksum(x[k, i, j] for j in [a[2] for a in A.select(k,i,'*')])==quicksum(x[k,j,f"e{k}"] for j in [a[1] for a in A.select(k,'*',f"e{k}")]) for k in K for i in [f"o{k}"]),name="constr42")
    model.addConstrs((quicksum(x[k,i, j,] for j in [a[2] for a in A.select(k,i,'*')]) == quicksum(x[k,j, i] for j in [a[1] for a in A.select(k,'*',i)]) for i in V-VO-VD for k in K), name = "constr3")

    # Constaints (4), (5), (6), (16Lyu) are used to maintain the request flow
    model.addConstrs((quicksum(y[k, r, i, j] for k in K for j in [a[3] for a in Ay.select(k,r,i,'*')] ) == 1 for r in R for i in ["p"+str(r)]), name="constr4")
    model.addConstrs((quicksum(y[k, r, j,i ] for k in K for j in [a[2] for a in Ay.select(k,r,'*',i)] ) == 1 for r in R for i in ["d"+str(r)]), name="constr5")
    
    model.addConstrs((quicksum(y[k, r, i, j] for k in K for j in [a[3] for a in Ay.select(k,r,i,'*')])-quicksum(y[k, r, j,i ] for k in K for j in [a[2] for a in Ay.select(k,r,'*',i)]) == 0 for r in R for i in T), name="constr6")

    model.addConstrs((quicksum(y[k, r, i, j] for j in [a[3] for a in Ay.select(k,r,i,'*')])-quicksum(y[k, r,j,i] for j in [a[2] for a in Ay.select(k,r,'*',i)] ) == 0 for k in K for r in R for i in V-T-frozenset(["p"+str(r),"d"+str(r)])), name="constr7")

    model.addConstrs((y[k, r, i, j]  <= x[k,i,j] for r in R for k in K for (i,j) in [a[2:] for a in Ay.select(k,r,'*','*')]), name="constr8")
    
    model.addConstrs((quicksum(q[r]*y[k,r,i, j] for r in R if r in [a[1] for a in Ay.select(k,r,i,j)]) <= u[k]*x[k,i, j] for k in K for (i,j) in [a[1:] for a in A.select(k,'*','*')]), name="constr9")
    
    #"""
    #model.addConstrs((quicksum(q[r]*y[k,r,i, j] for r in R) <= u[k]*x[k,i, j] for k in K for (i,j) in A), name="constr9")

    #model.addConstrs((quicksum(q[r]*y[k,r,i, j] for r in R if r in [a[1] for a in Ay.select(k,r,i,j)]) <= u[k]*x[k,i, j] for k in K for i in P|D|T for j in [a[2] for a in A.select(k,i,'*')]), name="cap0")
    #model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R for j in [a[1] for a in Ay.select(i,'*',r)]) <= VC for i in P|D|TF), name="ct.VehicleCapacity")
    # Strengthened capacity constraints
    #model.addConstrs((quicksum(q[r]*y[k,r,i, j] for r in R if r in [a[1] for a in Ay.select(k,r,i,j)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (u[k]-abs(qnode[i]+qnode[j]))*x[k,i,j] for k in K for i in P|D for j in [a[2] for a in A.select(k,i,'*')] if j in P|D), name="cap1")
    #model.addConstrs((quicksum(q[r]*y[k,r,i,j]  for r in R if r!=int(i.replace("p","").replace("d","")) for j in [a[3] for a in Ay.select(k,r,i,'*')]) <= u[k]-abs(qnode[i]) for k in K for i in P|D), name="cap2")
    
    """
    model.addConstrs((quicksum(q[r]*y[k,r,i,j] for r in R if r in [a[1] for a in Ay.select(k,r,i,j)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (u[k]-abs(qnode[i]+qnode[j]))*x[k,i,j] for k in K for i in P for (k_,i_,j) in A.select(k,i,'*') if j in P), name="capStr1")

    model.addConstrs((quicksum(q[r]*y[k,r,i,j] for r in R if r in [a[1] for a in Ay.select(k,r,i,j)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (u[k]-abs(qnode[i]+qnode[j]))*x[k,i,j] for k in K for i in D for (k_,i_,j) in A.select(k,i,'*') if j in D), name="capStr2")

    model.addConstrs((quicksum(q[r]*y[k,r,i,j] for r in R if r in [a[1] for a in Ay.select(k,r,i,j)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (u[k]-max(abs(qnode[i]),abs(qnode[j])))*x[k,i,j] for k in K for i in P for (k_,i_,j) in A.select(k,i,'*') if j in D), name="capStr3")

    model.addConstrs((quicksum(q[r]*y[k,r,i,j] for r in R if r in [a[1] for a in Ay.select(k,r,i,j)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (u[k]-max(abs(qnode[i]),abs(qnode[j])))*x[k,i,j] for k in K for i in D for (k_,i_,j) in A.select(k,i,'*') if j in P), name="capStr4")

    model.addConstrs((quicksum(q[r]*y[k,r,i,j] for r in R if r in [a[1] for a in Ay.select(k,r,i,j)] and r!=int(j.replace("p","").replace("d",""))) <= (u[k]-abs(qnode[j]))*x[k,i,j] for k in K for i in T for (k_,i_,j) in A.select(k,i,'*') if j in P|D), name="capStr5")

    model.addConstrs((quicksum(q[r]*y[k,r,i,j] for r in R if r in [a[1] for a in Ay.select(k,r,i,j)] and r!=int(i.replace("p","").replace("d",""))) <= (u[k]-max(abs(qnode[i]),abs(qnode[j])))*x[k,i,j] for k in K for i in P for (k_,i_,j) in A.select(k,i,'*') if j in T), name="capStr3b")

    model.addConstrs((quicksum(q[r]*y[k,r,i,j] for r in R if r in [a[1] for a in Ay.select(k,r,i,j)] and r!=int(i.replace("p","").replace("d",""))) <= (u[k]-max(abs(qnode[i]),abs(qnode[j])))*x[k,i,j] for k in K for i in D for (k_,i_,j) in A.select(k,i,'*') if j in T), name="capStr4b")

    model.addConstrs((quicksum(q[r]*y[k,r,i,j] for r in R if r!=int(i.replace("p","").replace("d","")) if (k,r,i,j) in Ay) <= (u[k]-abs(qnode[i]))*x[k,i,j] for k in K for i in P|D for j in [a[2] for a in A.select(k,i,'*')]), name="cap2a")

    model.addConstrs((quicksum(q[r]*y[k,r,i,j] for r in R if (k,r,i,j) in Ay) <= (u[k]-abs(qnode[i]))*x[k,i,j] for k in K for i in T for j in [a[2] for a in A.select(k,i,'*')]), name="cap2b")
    
    #"""
    #model.addConstrs((bt[k,i]-a[j]+c[i,j]<= Mij[i,j]*(1-x[k,i,j]) for k in K for i in T for j in [a[2] for a in A.select(k,i,'*')] if j in V-T), name = "constr48a")
    
    #model.addConstrs((bt[k,i]-at[k, j]+c[i,j]<= Mij[i,j]*(1-x[k,i,j]) for k in K for i in T for j in [a[2] for a in A.select(k,i,'*')] if j in T), name = "constr48b")

    model.addConstrs((b[k,i]-a[k,j]+c[i,j]<= Mij[i,j]*(1-x[k,i,j]) 
                          for k in K 
                          for i in V 
                          for (k_,i_,j) in A.select(k,i,'*')),name="ct48c")       
    #model.addConstrs((b[i]-at[k,j]+c[i,j]<= Mij[i,j]*(1-x[k,i,j]) for k in K for i in V-T for j in [a[2] for a in A.select(k,i,'*')] if j in T), name = "constr48d")
    
    #model.addConstrs((at[k, i] <= bt[k, i] for k in K for i in T), name='constr49a')
    
    model.addConstrs((a[k,i] <= b[k,i] for k,i in aIndex), name='constr49b')
    
    #model.addConstrs((timeWindows[i][0] <= at[k, i] for k in K for i in T), name="constr50a")
    #model.addConstrs((timeWindows[i][1] >= at[k, i] for k in K for i in T), name="constr50b")
    #model.addConstrs((timeWindows[i][0] <= bt[k, i] for k in K for i in T), name="constr51a")
    #model.addConstrs((timeWindows[i][1] >= bt[k, i] for k in K for i in T), name="constr51b")
    
    #model.addConstrs((max(timeWindows[i][0],c[f"o{k}",i])*quicksum(x[k,i,j] for (k_,i_,j) in A.select(k,i,'*'))  <= a[k,i] for k,i in aIndex if i not in VO), name="constr50c")
    model.addConstrs((timeWindows[i][0] <= a[k,i] for k,i in aIndex if i in V), name="constr50c")

    #model.addConstrs((timeWindows[i][1] >= a[i] for k in K for i in V-T), name="constr50d")
    #model.addConstrs((timeWindows[i][0] <= b[i] for k in K for i in V-T), name="constr51c")
    #model.addConstrs((min(timeWindows[f"e{k}"][1]-c[i,f"e{k}"],timeWindows[i][1])*quicksum(x[k,i,j] for j in [a[2] for a in A.select(k,i,'*')]) >= b[k,i] for k,i in bIndex if i not in VD), name="constr51d")
    model.addConstrs((timeWindows[i][1] >= b[k,i] for k,i in bIndex if i in V), name="constr51d")
    
    
    
    model.addConstrs((quicksum(y[k1, r, j, t] for j in [a[2] for a in Ay.select(k1,r,'*',t)]) + quicksum(y[k2, r, t, j] for j in [a[3] for a in Ay.select(k2,r,t,'*')]) <= (s[k1, k2, t, r] + 1) for k1 in K for k2 in K if k2!=k1 for t in T for r in R), name='constr21')

    
    #This constraints are new!
    #model.addConstrs((quicksum(y[k1, r, j, t] for j in [a[2] for a in Ay.select(k1,r,'*',t)]) >= s[k1, k2, t, r]  for k1 in K for k2 in K if k2!=k1 for t in T for r in R), name='constrOwn1')
    
    #model.addConstrs((quicksum(y[k2, r,t, j] for j in [a[3] for a in Ay.select(k2,r,t,'*')]) >= s[k1, k2, t, r]  for k1 in K for k2 in K if k2!=k1 for t in T for r in R), name='constrOwn2')


    model.addConstrs((a[k1, t] - b[k2, t] <= M*(1-s[k1, k2, t, r]) for r in R for k1 in K for k2 in K if k2!=k1 for t in T), name='constr20')
    
    model.addConstrs((quicksum(x[k, i, j] for j in [a[2] for a in A.select(k,i,'*')])<=1 for k in K for i in T),name="constrLyuValidInequality")
    
    model.addConstrs((quicksum(x[k,i,j] for k in K  for j in [a[2] for a in A.select(k,i,'*')])==1 for i in P|D),name="constr45")


    #model.addConstrs((quicksum(x[k,j,i] for j in [a[1] for a in A.select(k,'*',i)])==0 for k in K for i in ["o"+str(k)]),name="constr40")
    
    #model.addConstrs((quicksum(x[k,i,j] for j in [a[1] for a in A.select(i,'*')])==0 for k in K for i in VO|VD if i not in ["o"+str(k)]),name="constr41")

    #model.addConstrs((quicksum(x[k,j,i] for j in [a[0] for a in A.select('*',i)])==1 for k in K for i in ["e"+str(k)]),name="constr42")

    #model.addConstrs((quicksum(x[k,i,j] for j in [a[1] for a in A.select(i,'*')])==0 for k in K for i in ["e"+str(k)]),name="constr43")

    
    #model.addConstrs((quicksum(x[k, i, j] for j in [a[1] for a in A.select(i,'*')])<=1 for k in K for i in T),name="constr44")
    
    #model.addConstrs((quicksum(x[k,i,j] for k in K  for j in [a[1] for a in A.select(i,'*')])==1 for i in P|D),name="constr45")
    
    #model.addConstrs((quicksum(y[k,r,j,i] for k in K  for j in [a[0] for a in A.select('*',i)])==0 for r in R for i in ["p"+str(r)]),name="constr46")

    #model.addConstrs((quicksum(y[k,r,j,i] for j in [a[0] for a in A.select('*',i)])==0 for r in R for k in K for i in VD|VO if i not in [f"o{k}",f"e{k}"]),name="constr47")

    model.addConstrs((quicksum(x[k,i,j] for j in [a[2] for a in A.select(k,i,'*')])<=f[i] for k in K for i in T),name="OpeningSateliite")
    
    model.addConstrs((quicksum(x[k,i,j] for k in K for j in [a[2] for a in A.select(k,i,'*')])>=2*f[i] for i in T),name="SatelliteSymmetry")



    # Data for callback
    model._obj = None
    model._bd = None
    model._gap = None
    model._data = []
    model._start = time.time()
    model.Params.TimeLimit = 60*60
    model.Params.Threads = 16
    def compute_LP_relax_bound(model):
        lp = model.copy()
        for v in lp.getVars():
            v.vtype = GRB.CONTINUOUS
        lp.setParam("Presolve", 0)
        lp.setParam("Cuts", 0)
        lp.setParam("Heuristics", 0)
        lp.setParam("Aggregate", 0)
        lp.update()
        lp.optimize()
        print(f"LP relax LB: {lp.ObjVal}")
        return lp.ObjVal
    #model.Params.MIPFocus = 1
    model.update()
    lp = compute_LP_relax_bound(model)
    model.optimize()
    #model.optimize(callback=data_cb)
    #model.write("model.lp")
    # model.optimize()
    #model.computeIIS()
    #model.write("model.ilp")
   

    def plotGap(data):
        dfResult = pd.DataFrame(data, columns=['time', 'cur_obj','cur_bd','gap'])
        dfResult = dfResult.drop(dfResult[dfResult.cur_obj >= 100000000].index)
        
        fig, axes = plt.subplots()
        
        axes.set_xlabel('time')
        axes.set_ylabel('value')
        axes.set_xlim(dfResult['time'].values.min(), dfResult['time'].values.max())
        axes.set_ylim(0, dfResult['cur_obj'].values.max() * 1.1)
        line1, = axes.plot(dfResult['time'].values, dfResult['cur_obj'].values, color = 'navy', label='Current ObjValue')    
        line2, = axes.plot(dfResult['time'].values, dfResult['cur_bd'].values, color = 'blue', label='Current DB')    
        plt.fill_between(dfResult['time'].values, dfResult['cur_obj'].values, dfResult['cur_bd'].values, lw=0, color='lightsteelblue')
        
        axes2 = axes.twinx()
        axes2.set_ylabel('%gap')
        axes2.set_ylim(0, 100)
        line3, = axes2.plot(dfResult['time'].values, dfResult['gap'].values, color = 'red', label='Current Gap')
        axes.legend(handles=[line1, line2, line3], bbox_to_anchor=(0.5, 1.1), frameon=False, loc='upper center', ncol=3)
        
        plt.show()

    def plotLocation(df):
        fig, axes = plt.subplots(figsize=(10, 10))
        
        plt.scatter(df.loc[df['node'].str.contains('p'),'x'].values, df.loc[df['node'].str.contains('p'),'y'].values, s=50, facecolor='red', marker='o')
        plt.scatter(df.loc[df['node'].str.contains('d'),'x'].values, df.loc[df['node'].str.contains('d'),'y'].values, s=50, facecolor='green', marker='o')
        plt.scatter(df.loc[df['node'].str.contains('o'),'x'].values, df.loc[df['node'].str.contains('o'),'y'].values, s=50, facecolor='yellow', marker='s')
        plt.scatter(df.loc[df['node'].str.contains('e'),'x'].values, df.loc[df['node'].str.contains('e'),'y'].values, s=50, facecolor='black', marker='s')
        plt.scatter(df.loc[df['node'].str.contains('t'),'x'].values, df.loc[df['node'].str.contains('t'),'y'].values, s=50, facecolor='blue', marker='D')
        
        for xi, yi, text in zip(df['x'].values, df['y'].values, df['node'].values):
            plt.annotate(text, xy=(xi, yi), xycoords='data', xytext=(5, 5), textcoords='offset points')
        
        xResult = pd.DataFrame(x.keys(), columns=["k","i","j"])
        xResult["value"]=model.getAttr("X", x).values()
        for index, row in xResult.iterrows():
            if row["value"] >= 0.5:
                x1 = df.loc[df['node'] == row["i"], 'x'].values
                y1 = df.loc[df['node'] == row["i"], 'y'].values
                x2 = df.loc[df['node'] == row["j"], 'x'].values
                y2 = df.loc[df['node'] == row["j"], 'y'].values
                plt.plot([x1, x2], [y1, y2], 'gray', linestyle="--")
        plt.show()
        
    sol_transfers = {}
    vehicle_number=0
    sol_req_transfers = 0
    ratio = lp
    if model.Status == GRB.OPTIMAL:
        plotLocation(df)
        vehicle_number = sum(x[k,o, j] for k in K for o in VO for (k,o,j) in A.select(k,o,"*")).getValue()

        for i in T:               
            for r in R:
                if sum(s[k1, k2, i, r] for k1 in K for k2 in K if k2!=k1).getValue()>0.5:
                    for k1 in K:
                        for k2 in K:
                            if k1!=k2:
                                if sum(y[k1, r, j, i] for j in [a[2] for a in Ay.select(k1,r,'*',i)]).getValue() + sum(y[k2, r, i, j] for j in [a[3] for a in Ay.select(k2,r,i,'*')]).getValue()>=1.9:
                                    sol_req_transfers +=1
                                    if i[-1] not in sol_transfers:
                                        sol_transfers[i[-1]] = 1
        infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sum(sol_transfers.values()), sol_req_transfers,vehicle_number,"",ratio]    
        for iter2 in range(1):
                model.setParam(GRB.Param.SolutionNumber, iter2)
                print('%g ' % model.PoolObjVal, end='\n')
                for v in model.getVars():
                     if v.xn > 1e-5:
                           print ('%s %g' % (v.varName, v.xn))
                print("\n")
        print("\n")
    elif model.Status == GRB.TIME_LIMIT:
        if model.SolCount == 0:
            infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sum(sol_transfers.values()), sol_req_transfers,vehicle_number,"",ratio]    
        else:
            plotLocation(df)
            vehicle_number = sum(x[k,o, j] for k in K for o in VO for (k,o,j) in A.select(k,o,"*")).getValue()

            for i in T:               
                for r in R:
                    if sum(s[k1, k2, i, r] for k1 in K for k2 in K if k2!=k1).getValue()>0.5:
                        for k1 in K:
                            for k2 in K:
                                if k1!=k2:
                                    if sum(y[k1, r, j, i] for j in [a[2] for a in Ay.select(k1,r,'*',i)]).getValue() + sum(y[k2, r, i, j] for j in [a[3] for a in Ay.select(k2,r,i,'*')]).getValue()>=1.9:
                                        sol_req_transfers +=1
                                        if i[-1] not in sol_transfers:
                                            sol_transfers[i[-1]] = 1
            infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sum(sol_transfers.values()), sol_req_transfers,vehicle_number,"",ratio]    
    else:
        infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sum(sol_transfers.values()), sol_req_transfers,vehicle_number,"",ratio]
        #model.computeIIS()
        #model.write("model.ilp")
        
    return infos#, model

infos = raisModel(filename)
print("test big instance with symm break ct")



