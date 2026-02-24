# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import time

import gurobipy as gp
from gurobipy import GRB, quicksum, tuplelist

filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-5.txt"
filename = "./InstancesLiLim/PDPTWT10/PDPTWT_LiLim_R10K25T0C200_lr101.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R5-K3-T3/PDPT-R5-K3-T3-Q100-5.txt"
filename = "./InstancesLiLim/PDPTWT10/PDPTWT_LiLim_R10K4T4C50_lrc106.txt"
filename = "./InstancesGhilas/HetPDPT_Instances/Small/R_Ghilas_R6K4T1.txt"
filename  = "./InstancesGhilas/HetPDPT_Instances/NewCapacities/RC_Ghilas_R12K6T1.txt"
filename = "./InstancesGhilas/HetPDPT_Instances/NewCapacities/C_Ghilas_R6K4T1.txt"
filename = "./InstancesGhilas/HetPDPT_Instances/NewCapacities/C_Ghilas_R10K4T1.txt"
filename = "./InstancesGhilas/HetPDPT_Instances/Small/C_Ghilas_R11K4T1.txt"
#filename = "./InstancesGhilas/NewCapInstancesHet/RC_Ghilas_R20K8T1_fixed.txt"
filename = "./InstancesGhilas/NewCapInstancesHet/Ghilas_RC_R11-K4-T2.txt"
#filename = "./InstancesGhilas/NewCapInstancesHet/Ghilas_R_R15-K6-T1.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R5-K3-T3/PDPT-R5-K3-T3-Q100-5.txt"
#filename = "./InstancesGhilas/BigPDPTPWT/MissingBig/Ghilas__R50-K14-T1_1.txt"
#filename = "./InstancesLyu23/PDPT_small/PDPT-R15-K3-T3/PDPT-R15-K3-T3-Q100-9.txt"
filename = "./InstancesLyu23/PDPT_small/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
filename = "./InstancesLyu23/PDPT_small/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-9.txt"
filename = "./InstancesLyu23/PDPT_big/PDPT-R30-K2-T2/PDPT-R30-K2-T2-Q100-0.txt"

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

def readDataframeHet(filename,nrequests,cut=None):
    df = pd.read_csv(filename, skiprows=3, sep='\t')
    R =  list(range(nrequests))
    if cut==None:
        cut = len(R)
    # temp = [df['node'].str.contains("t") == True]
    indices_to_drop = []
    for index, row in df.iterrows():
        if "t" in row['node']:
            indices_to_drop.append(index)
            for r in R[:cut]:
                copy = row.copy()
                copy['node'] = copy['node'].replace('t', f't.{r}.')
                df = df._append(copy, ignore_index = True)
                copy = row.copy()
                
    
    df = df.drop(indices_to_drop)
    df = df.reset_index(drop=True)
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

# Get the list of grouped nodes
def getNodeList(df):
    rOrigins = df.loc[df['node'].str.contains('p'),'node']
    rDestinations = df.loc[df['node'].str.contains('d'),'node']
    vOrigins = df.loc[df['node'].str.contains('o'),'node']
    vDestinations = df.loc[df['node'].str.contains('e'),'node']
    transferNodes = df.loc[df['node'].str.contains('t'),'node']
    return [rOrigins, rDestinations, vOrigins, vDestinations, transferNodes]
def calculateDistance(x1, x2, y1, y2):
    return math.sqrt((x2 - x1)**2 + (y2-y1)**2)

def distancesMatrix(df):
    matrix = {}
    for location1 in df["node"]:
        matrix[location1] = {}
        for location2 in df["node"]:
            if location1 != location2:
                x1 = df.loc[df["node"]==location1, 'x'].values[0]
                x2 = df.loc[df["node"]==location2, 'x'].values[0]
                y1 = df.loc[df["node"]==location1, 'y'].values[0]
                y2 = df.loc[df["node"]==location2, 'y'].values[0]
                matrix[location1,location2] = calculateDistance(int(x1), int(x2), int(y1), int(y2))
    return matrix

def loadMatrix(df):
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
            
            
HET = False

# Model, Parameters, Variables and Objective Function
#trans_copy is not working
def lyuModel(filename, cut=None):
    model = gp.Model("lyuModel_vehickeSymm")
    metaData = readMetaData(filename)
    HET = False
    if "Ghilas" in filename:
        #df = readDataframe(filename)
        HET = True
        df = readDataframeHet(filename, int(metaData["nr"]),cut)
    else:
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
    
    A = [(i,j) for i in V for j in V if j!=i]
    
    A = tuplelist(A)

    
    if "Lim" in filename:
        service_time = pd.Series(df.s.values,index=df.node).to_dict()
    else:
        service_time = {i:0 for i in V}

    arcs = []
    for i in nodeList['vo'].values:
        for j in nodeList['ro'].values:
            arcs.append((i,j))
        for j in nodeList['t'].values:
            arcs.append((i,j))
        for j in nodeList['vd'].values:
            arcs.append((i, i.replace("o", "e")))

    for i in nodeList['ro'].values:
        for j in np.concatenate((nodeList['ro'].values, nodeList['rd'].values, nodeList['t'].values)):
            if i != j:
                arcs.append((i,j))

    for i in nodeList['rd'].values:
        for j in np.concatenate((nodeList['ro'].values, nodeList['rd'].values, nodeList['vd'].values, nodeList['t'].values)):
            if not (i == j or (j in nodeList['ro'].values and i == j.replace("p","d"))):
                arcs.append((i,j))

    for i in nodeList['t'].values:
        for j in np.concatenate((nodeList['ro'].values, nodeList['rd'].values, nodeList['vd'].values, nodeList['t'].values)):
            if  i != j:
                arcs.append((i,j))

    arcs = list(dict.fromkeys(arcs))

    # Testing Symmetries Breaking Constraints
    # df.loc[df['node'].str.contains('o'), 'x'] = 50
    # df.loc[df['node'].str.contains('o'), 'y'] = 50
    # df.loc[df['node'].str.contains('e'), 'x'] = 50
    # df.loc[df['node'].str.contains('e'), 'y'] = 50

    nRequests = int(metaData['nr'])
    nVehicles = int(metaData['nv'])
    nTransports = int(metaData['nt'])
    vCapability = int(metaData['capacity'])

    c = distancesMatrix(df)
    VC = vCapability
    uk = pd.Series(index=K, data=np.full(nVehicles, vCapability))
    #q = pd.Series(index = np.concatenate((nodeList['ro'].values, nodeList['rd'].values)), data=df.loc[0:nRequests*2-1,'load'].values, dtype=int)
    qnode = df.set_index('node')["load"].to_dict()
    q =  {int(node.replace("p","")):qnode[node] for node in P}
    if VC<0:
        service_time = pd.Series(df.s.values,index=df.node).to_dict()
        node_capacities = pd.Series(df.vcap.values,index=df.node).to_dict()
        for node in node_capacities:
            if node_capacities[node]>0:
                uk[int(node.replace("o","").replace("e",""))] = node_capacities[node]
        """
        #seems not to work like intended
        location_capacity_matches = consolidate_vehicle_nodes(VO,points,vec_capacities)
        agg_vec_nodes = {}
        for key in location_capacity_matches:
            agg_vec_nodes[list(location_capacity_matches[key])[0]] = len(location_capacity_matches[key])
            for vecs_to_remove in list(location_capacity_matches[key])[1:]:
                o_node = f"o{vecs_to_remove}"
                e_node = f"e{vecs_to_remove}"
                V = V-frozenset((e_node,o_node))
                VO = VO-frozenset((o_node,))
                VD = VD-frozenset((e_node,))
                K.remove(vecs_to_remove)
        """
    else:
        service_time = {s:0 for s in V}

    print(df)
    
    df["tw"] = df[["a","b"]].values.tolist()
    
    timeWindows = df.set_index('node')["tw"].to_dict()
    
    Mij = {(i,j):max(0,timeWindows[i][1]+c[i,j] -timeWindows[j][0]) for (i,j) in A}
    M = max(Mij.values())
    Mt = {i:timeWindows[i][1]-timeWindows[i][0] for i in T}

    xIndex = [(k, i, j) for k in K for (i,j) in A]
    yIndex = [(k, r, i, j) for k in K for r in R for (i,j) in A]
    sIndex = [(k1, k2, t, r) for k1 in K for k2 in K for t in T for r in R if k1 != k2]
    aIndex = [(k, i) for k in K for i in V]
    bIndex = [(k, i) for k in K for i in V]

    x = model.addVars(xIndex, vtype=GRB.BINARY, name='x')
    y = model.addVars(yIndex, vtype=GRB.BINARY, name='y')
    s = model.addVars(sIndex, vtype=GRB.BINARY, name='s')
    a = model.addVars(aIndex, lb=0.0 ,vtype=GRB.CONTINUOUS, name='a')
    b = model.addVars(bIndex, lb=0.0 ,vtype=GRB.CONTINUOUS, name='b')

    #if "Lim" in filename:
     #   model.setObjective(sum((c[i,j] * x[k, i, j]) for k in K for (i,j) in A)+quicksum(pow(10,4) * x[k,i, j] for k in K for (i,j) in A if i in VO), GRB.MINIMIZE)
   # else:
    model.setObjective(sum((c[i,j] * x[k, i, j]) for k in K for (i,j) in A), GRB.MINIMIZE)
    model.update()
    
    #model.addConstr(x[3,"p2","t3"]==1)
    #model.addConstr(x[3,"t3","t0"]==1)
    #model.addConstr(x[3,"t0","d1"]==1)
    #model.addConstr(x[0,"p1","t3"]==1)
    #model.addConstr(x[0,"t3","e0"]==1)
    #model.addConstr(x[2,"o2","e2"]==1)
    #model.addConstr(x[2,"o2","e2"]==1)
    
            


    # Constraints
    if "Lim" in filename or HET==True:
        model.addConstrs((quicksum(x[k, i, j] for j in [a[1] for a in A.select(i,'*')])==quicksum(x[k,j,i.replace("o","e")] for j in [a[0] for a in A.select('*',i.replace("o","e"))]) for k in K for i in [f"o{k}"]),name="constr25")
        #model.addConstr((quicksum(x[k, i, j] for k in K for i in [f"o{k}"] for j in [a[1] for a in A.select(i,'*')])>=1 ),name="constr25")
    else:
        model.addConstrs((quicksum(x[k,j,i] for j in [a[0] for a in A.select('*',i)])==1 for k in K for i in ["e"+str(k)]),name="constr42")
        model.addConstrs((quicksum(x[k, i, j] for j in [a[1] for a in A.select(i,'*')])==1 for k in K for i in [f"o{k}"]),name="constr25")
 
    #model.addConstrs((quicksum(x[k, i, j] for j in [a[1] for a in A.select(i,'*')])==quicksum(x[k,j,f"e{k}"] for j in [a[0] for a in A.select('*',f"e{k}")]) for k in K for i in [f"o{k}"]),name="constr42")
    model.addConstrs((quicksum(x[k,i, j,] for j in [a[1] for a in A.select(i,'*')]) == quicksum(x[k,j, i] for j in [a[0] for a in A.select('*',i)]) for i in V-VO-VD for k in K), name = "constr3")

    # Constaints (4), (5), (6), (16Lyu) are used to maintain the request flow
    model.addConstrs((quicksum(y[k, r, i, j] for j in [a[1] for a in A.select(i,'*')] for k in K) == 1 for r in R for i in ["p"+str(r)]), name="constr4")
    model.addConstrs((quicksum(y[k, r, j,i ] for j in [a[0] for a in A.select('*',i)] for k in K) == 1 for r in R for i in ["d"+str(r)]), name="constr5")
    
    model.addConstrs((quicksum(y[k, r, i, j] for k in K for j in [a[1] for a in A.select(i,'*')])-quicksum(y[k, r, j,i ] for k in K for j in [a[0] for a in A.select('*',i)]) == 0 for r in R for i in T), name="constr6")


    model.addConstrs((quicksum(y[k, r, i, j] for j in [a[1] for a in A.select(i,'*')])-quicksum(y[k, r,j,i] for j in [a[0] for a in A.select('*',i)] ) == 0 for k in K for r in R for i in V-T-frozenset(["p"+str(r),"d"+str(r)])), name="constr7")

    model.addConstrs((y[k, r, i, j]  <= x[k,i,j] for r in R for k in K for (i,j) in A), name="constr8")
    
   
    
    model.addConstrs((quicksum(q[r]*y[k,r,i, j] for r in R) <= uk[k]*x[k,i, j] for k in K for (i,j) in A), name="constr9")

    
    model.addConstrs((b[k,i]-a[k, j]+c[i,j]<= Mij[i,j]*(1-x[k,i,j]) for k in K for (i,j) in A), name = "constr48")
    
    model.addConstrs((a[k, i]+service_time[i] <= b[k, i] for k in K for i in V), name='constr49')
    
    model.addConstrs((timeWindows[i][0] <= a[k, i] for k in K for i in V), name="constr50")
    #model.addConstrs((timeWindows[i][1] >= a[k, i] for k in K for i in V), name="constr50")
    #model.addConstrs((timeWindows[i][0] <= b[k, i] for k in K for i in V), name="constr51")
    model.addConstrs((timeWindows[i][1] >= b[k, i] for k in K for i in V), name="constr51")
    
    
    model.addConstrs((quicksum(y[k1, r, j, t] for j in [a[0] for a in A.select('*',t)]) + quicksum(y[k2, r, t, j] for j in [a[1] for a in A.select(t,'*')]) <= (s[k1, k2, t, r] + 1) for k1 in K for k2 in K if k2!=k1 for t in T for r in R), name='constr21')

    
    #This constraints are new!
    #model.addConstrs((quicksum(y[k1, r, j, t] for j in [a[0] for a in A.select('*',t)]) >= s[k1, k2, t, r]  for k1 in K for k2 in K if k2!=k1 for t in T for r in R), name='constrOwn1')
    
    #model.addConstrs((quicksum(y[k2, r,t, j] for j in [a[1] for a in A.select(t,'*')]) >= s[k1, k2, t, r]  for k1 in K for k2 in K if k2!=k1 for t in T for r in R), name='constrOwn2')


    model.addConstrs((a[k1, t] - b[k2, t] <= M*(1-s[k1, k2, t, r]) for r in R for k1 in K for k2 in K if k2!=k1 for t in T), name='constr20')

    model.addConstrs((quicksum(x[k,j,i] for j in [a[0] for a in A.select('*',i)])==0 for k in K for i in ["o"+str(k)]),name="constr40")
    
    model.addConstrs((quicksum(x[k,i,j] for j in [a[1] for a in A.select(i,'*')])==0 for k in K for i in VO|VD if i not in ["o"+str(k)]),name="constr41")
  
    

    model.addConstrs((quicksum(x[k,i,j] for j in [a[1] for a in A.select(i,'*')])==0 for k in K for i in ["e"+str(k)]),name="constr43")

    
    model.addConstrs((quicksum(x[k, i, j] for j in [a[1] for a in A.select(i,'*')])<=1 for k in K for i in T),name="constr44")
    
    model.addConstrs((quicksum(x[k,i,j] for k in K  for j in [a[1] for a in A.select(i,'*')])==1 for i in P|D),name="constr45")
    
    model.addConstrs((quicksum(y[k,r,j,i] for k in K  for j in [a[0] for a in A.select('*',i)])==0 for r in R for i in ["p"+str(r)]),name="constr46")

    model.addConstrs((quicksum(y[k,r,j,i] for j in [a[0] for a in A.select('*',i)])==0 for r in R for k in K for i in VD|VO if i not in [f"o{k}",f"e{k}"]),name="constr47")
    
    if HET:
        for t in T:
            r = int(t.split(".")[1])
            tidx = int(t.split(".")[-1])
            if r>0:
                for k in K:
                    t2 = f"t.{r-1}.{tidx}"
                    #waiting at transfer station is not allowed
                    model.addConstr(quicksum(x[k,t,j] for j in [a[1] for a in A.select(t,'*')])<=quicksum(x[k,t2,j] for k in K for j in [a[1] for a in A.select(t2,'*')]))
                    for r2 in range(r):
                        t2 = f"t.{r2}.{tidx}"
                        if (t,t2) in A:
                            model.addConstr(x[k,t,t2]==0)
                    """
                    if r<len(R)-1:
                        for r2 in range(r+1,len(R)):
                            t2 = f"t.{r2}.{tidx}"
                            if (t,t2) in A:
                                model.addConstr(x[k,t,t2]==0)"""
                #:
                    #t0 = f"t.{r-1}.{tidx}"
                    #model.addConstr(quicksum(x[k,t,j] for j in [a[1] for a in A.select(t,'*')])<=quicksum(y[k,r,t,j] for k in K for j in [a[1] for a in A.select(t,'*')]))
                    #model.addConstr(0==quicksum(y[k,r1,t,j] for r1 in R if r1<r for k in K for j in [a[1] for a in A.select(t,'*')]))


    sol = [[(4,'o4', 'p6'), (4,'p6', 'd6'), (4,'d6', 'e4')],
    [(5,'o5', 'p7'), (5,'p7', 'd7'), (5,'d7', 'e5')],
    [(5,'o5', 'p10'), (5,'p10', 'p11'), (5,'d11', 'd2'), (5,'d2', 'e5')],
    [(5,'o5', 'p14'),  (5,'p9', 'd9'), (5,'d9', 'p13'), (5,'p13', 'd13'), (5,'d13', 'e5')],
    [(5,'o5', 'p4'),  (5,'d8', 'e5')],
    [(2,'o2', 'p2'), (2,'p2', 'p0'), (2,'p0', 'd0'), (2,'d0', 'p1'),  (2,'d4', 'e2')],
    [(2,'o2', 'p8'),(2,'p3', 'd3'), (2,'d3', 'd10'), (2,'d10', 'e2')],
    [(2,'o2', 'p5'), (2,'p5', 'd5'), (2,'d14', 'p12'), (2,'p12', 'd12'), (2,'d12', 'e2')],
    ]
    sol = []
    for route in sol:
        for e in route:
            model.addConstr(x[e]==1)

    # Data for callback
    model._obj = None
    model._bd = None
    model._gap = None
    model._x = x
    model._y = y
    model._data = []
    model._start = time.time()
    model.Params.TimeLimit = 60*60
    model.Params.Threads = 16
    model.update()
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
        print(f"LP relax LB: {lp.objVal}")
        return lp.objVal
    lb = compute_LP_relax_bound(model)
    model.optimize()
    opt = model.ObjVal
    ratio = lb#100 * lb / opt
    #model.write("model.lp")
    # model.optimize()
    #model.computeIIS()
    #model.write("model.ilp")
    def get_tour(arcs):
       tours = []
       for a in arcs:
           if a[0] in VO:
               vehicle = a[2]
               curr_node = a[1]
               tour = [(a[0],a[1])]
               start = a[0]
               while "e" not in curr_node:
                   for (i,j,k) in arcs:
                       if i==curr_node and k==vehicle:
                         tour.append((i,j))
                         curr_node = j
                         break
               print(tour)
               tours.append(tour)
       return tours   
   
    def check_tours(model):
        arcsx = [(a[1],a[2],a[0]) for a in model._x if model._x[a].x>0.5]
        arcs_vehicle = {(a[1],a[2]):int(a[0]) for a in model._x if model._x[a].x>0.5}
        arcsy = {(a[2],a[3],a[1],a[0]):1.0 for a in model._y if model._y[a].x>0.5}
        tours = get_tour(arcsx)
        error_msg = ""
        error = False
        for tour in tours:
            q_val = 0
            z_val = 0.0
            for u,v in tour:
                q_val = sum(q[r]*arcsy.get((u,v,r),0) for r in range(nRequests))
                if VC<0:
                    Q_vehicle = uk[arcs_vehicle[u,v]]
                    z_val = max(z_val+c[u,v]+service_time[v],timeWindows[v][0])
                else:
                    Q_vehicle = VC
                    z_val = max(z_val+c[u,v]+service_time[u],timeWindows[v][0])
                if q_val>Q_vehicle:
                    error_msg+=f"capacity violation:{q_val},{Q_vehicle},{v},{tour}"
                    error = True
                if VC>0:
                    if z_val-pow(10,-4)>timeWindows[v][1]:
                        error_msg+=f"violation of time windows: {v},{z_val}>{timeWindows[v][1]}"
                        error = True
                else:
                    if z_val-service_time[v]-pow(10,-4)>timeWindows[v][1]:
                        error_msg+=f"violation of time windows: {v},{z_val}>{timeWindows[v][1]}"
                        error = True
            if q_val>0:
                error_msg+=f"precedence violation: {tour}"
                error = True
        return error, error_msg
    
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
                
    vehicle_number = -1
    error_msg = ""
    sol_transfers = {}
    sol_req_transfers = 0
    sol_transfer_nodes = 0
    cut = ratio
    if model.Status == GRB.OPTIMAL:
        #plotGap(model._data)
        plotLocation(df)
        error_msg = check_tours(model)
        print(error_msg)
        vehicle_number = sum(x[k,o, j] for k in K for o in VO for (o,j) in A.select(o,"*")).getValue()
        sol_transfer_nodes =  sum(x[k,i, j] for k in K for i in T for (i,j) in A.select(i,"*")).getValue()
        #sol_req_transfers = sum(s[k1, k2, t, r] for r in R for k1 in K for k2 in K if k2!=k1 for t in T).getValue()
        for i in T:               
            for r in R:
                if sum(s[k1, k2, i, r] for k1 in K for k2 in K if k2!=k1).getValue()>0.5:
                    for k1 in K:
                        for k2 in K:
                            if k1!=k2:
                                if sum(y[k1, r, j, i] for j in [a[0] for a in A.select('*',i)]).getValue() + sum(y[k2, r, i, j] for j in [a[1] for a in A.select(i,'*')]).getValue()>=1.9:
                                    sol_req_transfers +=1
                                    if i[-1] not in sol_transfers:
                                        sol_transfers[i[-1]] = 1
                    
        infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sum(sol_transfers.values()), sol_req_transfers, sol_transfer_nodes,vehicle_number,cut]   
        for iter2 in range(1):
                model.setParam(GRB.Param.SolutionNumber, iter2)
                print('%g ' % model.PoolObjVal, end='\n')
                for v in model.getVars():
                     if v.xn > 1e-5:
                         if "y" in v.varName and "t" in v.varName:
                           print ('%s %g' % (v.varName, v.xn))
                print("\n")
        print("\n")
    elif model.Status == GRB.TIME_LIMIT:
        if model.SolCount == 0:
            infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sol_transfers, sol_req_transfers, sol_transfer_nodes,vehicle_number,cut]     
        else:
            plotLocation(df)
            error_msg = check_tours(model)
            
            print(error_msg)
            vehicle_number = sum(x[k,o, j] for k in K for o in VO for (o,j) in A.select(o,"*")).getValue()
            sol_transfer_nodes =  sum(x[k,i, j] for k in K for i in T for (i,j) in A.select(i,"*")).getValue()
            #sol_req_transfers = sum(s[k1, k2, t, r] for r in R for k1 in K for k2 in K if k2!=k1 for i in T).getValue()
            for i in T:               
                for r in R:
                    if sum(s[k1, k2, i, r] for k1 in K for k2 in K if k2!=k1).getValue()>0.5:
                        for k1 in K:
                            for k2 in K:
                                if k1!=k2:
                                    if sum(y[k1, r, j, i] for j in [a[0] for a in A.select('*',i)]).getValue() + sum(y[k2, r, i, j] for j in [a[1] for a in A.select(i,'*')]).getValue()>=1.9:
                                        sol_req_transfers +=1
                                        if i[-1] not in sol_transfers:
                                            sol_transfers[i[-1]] = 1
            infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sum(sol_transfers.values()), sol_req_transfers, sol_transfer_nodes,vehicle_number,cut]      
    else:
        infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),"inf", "inf",model.ObjBound, model.Runtime,sol_transfers, sol_req_transfers, sol_transfer_nodes,vehicle_number,cut] 
        #model.computeIIS()
        #model.write("model.ilp")
        
    return infos

infos = lyuModel(filename)



