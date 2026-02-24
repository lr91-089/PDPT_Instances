#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 22:11:54 2024

@author: rocha01
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import networkx as nx
from collections import defaultdict
from itertools import combinations

import gurobipy as gp
from gurobipy import Model, GRB, quicksum, tuplelist

#filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-1.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R15-K3-T3/PDPT-R15-K3-T3-Q100-9.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-0.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R10-K3-T3/PDPT-R10-K3-T3-Q100-9.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R7-K3-T3/PDPT-R7-K3-T3-Q100-6.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R5-K2-T1/PDPT-R5-K2-T1-Q100-6.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R5-K2-T2/PDPT-R5-K2-T2-Q100-6.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R5-K3-T3/PDPT-R5-K3-T3-Q100-2.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R5-K2-T2/PDPT-R5-K2-T2-Q100-6.txt"
#filename = "./InstancesLyu23/Examples/example2.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R5-K3-T3/PDPT-R5-K3-T3-Q100-2.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R7-K3-T3/PDPT-R7-K3-T3-Q100-6.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R7-K3-T3/PDPT-R7-K3-T3-Q100-5.txt"
#filename = "./InstancesLyu23/PDPT_small/PDPT-R10-K3-T3/PDPT-R10-K3-T3-Q100-5.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R5-K3-T3/PDPT-R5-K3-T3-Q100-5.txt"



#filename = "./InstancesGhilas/PDPTW_Rewritten/R40K12T1_Ghilas_13.txt"
#filename = "./InstancesGhilas/PDPTW_Rewritten/R20K8T2_Ghilas_2.txt"

filename = "./InstancesGhilas/HetPDPT_Instances/NewCapacities/C_Ghilas_R6K4T1.txt"
#filename  = "./InstancesGhilas/HetPDPT_Instances/NewCapacities/RC_Ghilas_R12K6T1.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R25-K3-T3/PDPT-R25-K3-T3-Q100-8.txt"
filename = "./InstancesGhilas/HetPDPT_Instances/Small/R_Ghilas_R7K4T1.txt"
#filename = "./InstancesGhilas/HetPDPT_Instances/NewCapacities/C_Ghilas_R6K4T1.txt"
filename = "./InstancesGhilas/HetPDPT_Instances/NewCapacities/C_Ghilas_R10K4T1.txt"
#filename = "./InstancesGhilas/HetPDPT_Instances/NewCapInstancesHet/C_Ghilas_R10K4T1.txt"

#filename = "./InstancesGhilas/HetPDPT_Instances/NewCapacities/C_Ghilas_R8K4T1.txt"

#filename = "./InstancesGhilas/HetPDPT_Instances/NewCapacities/RC_Ghilas_R20K8T1.txt"
filename = "./InstancesGhilas/HetPDPT_Instances/Small/C_Ghilas_R11K4T1.txt"
filename = "./InstancesGhilas/HetPDPT_Instances/Small/R_Ghilas_R6K4T1.txt"
filename = "./InstancesGhilas/HetPDPT_Instances/Small/C_Ghilas_R11K4T1.txt"
filename = "./InstancesGhilas/HetPDPT_Instances/NewCapacities/C_Ghilas_R10K4T1.txt"
filename = "./InstancesGhilas/HetPDPT_Instances/NewCapacities/RC_Ghilas_R15K6T1.txt"

filename = "./InstancesLyu23/PDPTWT/4R4K4T/4R-4K-4T-240L-5.txt"
filename = "./InstancesLyu23/PDPTWT/4R4K4T/4R-4K-4T-300L-9.txt"
filename = "./InstancesLyu23/PDPTWT/3R4K4T/3R-4K-4T-240M-1.txt"

#filename = "./InstancesLyu23/PDPTWT/3R4K4T/3R-4K-4T-300L-3.txt"
#filename = "./InstancesGhilas/NewCapInstancesHet/RC_Ghilas_R20K8T1_fixed.txt"
filename = "./InstancesGhilas/NewCapInstancesHet/Ghilas_R_R15-K6-T1.txt"
filename = "./InstancesGhilas/NewCapInstancesHet/Ghilas_RC_R11-K4-T2.txt"

#filename = "./InstancesGhilas/NewCapInstancesHet/Ghilas_R_R15-K6-T1.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
filename = "./InstancesGhilas/NewCapInstancesHet/Ghilas_R_R25-K8-T2.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-6.txt"
filename = "./InstancesGhilas/NewCapInstancesHet/Ghilas_RC_R11-K4-T2.txt"
filename = "./InstancesGhilas/BigPDPTPWT/Ghilas__R40-K12-T1_1.txt"
filename = "./InstancesGhilas/HetBigPDPTWT_OrginalLoads/Ghilas_TC_R50-K16-T1.txt"
filename = "./InstancesGhilas/HetBigPDPTWT_OrginalLoads/Ghilas_TC_R20-K8-T2.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
filename = "./InstancesLyu23/PDPT_small/PDPT-R10-K3-T3/PDPT-R10-K3-T3-Q100-1.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
filename = "./InstancesATH/ath_25_3_3_1_L_converted.txt"
filename = "./InstancesGhilas/HetBigPDPTWT_OrginalLoads/Ghilas_TC_R20-K8-T2.txt"
filename = "./InstancesGhilas/BigPDPTPWT/Ghilas__R35-K12-T1.txt"
filename = "./InstancesGhilas/BigPDPTPWT/Ghilas__R50-K14-T1_1.txt"
filename = "./InstancesGhilas/HetBigPDPTWT_OrginalLoads/Ghilas_TC_R20-K8-T2.txt"
#filename = "./InstancesGhilas/HetBigPDPTWT_OrginalLoads/Ghilas_TC_R35-K12-T1_1.txt"

filename = "./InstancesGhilas/OriginalInstances/R40K12T1_1_Ghilas.txt"
filename = "./InstancesGhilas/OriginalInstances/R50-K14-T1_GhilasOriginal.txt"
filename = "./InstancesGhilas/OriginalInstances/R35-K10-T1_GhilasOriginal.txt"
#filename = "./InstancesGhilas/OriginalInstances/R50K14T1_1_Ghilas.txt"
filename = "./InstancesGhilas/OriginalInstances/R40K12T1_1_Ghilas.txt"
filename = "./InstancesGhilas/OriginalInstances/R25-K10-T2_GhilasOriginal.txt"
filename = "./InstancesGhilas/PDPTW-T_rewritten_OriginalTopo/R20-K8-T2_GhilasOriginalTop.txt"
filename = "./InstancesGhilas/PDPTW-T_rewritten_OriginalTopo/R6-K4-T1_GhilasOriginalTopTest.txt"


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
    K =  list(range(df.loc[df['node'].str.contains('o'),'node'].shape[0]))
    # temp = [df['node'].str.contains("t") == True]
    indices_to_drop = []
    for index, row in df.iterrows():
        if "t" in row['node']:
            indices_to_drop.append(index)
            for k in K:
                copy = row.copy()
                copy['node'] = copy['node'].replace('t', f'ts.{k}.')
                df = df._append(copy, ignore_index = True)
                copy['node'] = copy['node'].replace('ts', 'tf')
                df = df._append(copy, ignore_index = True)
                
    
    df = df.drop(indices_to_drop)
    df = df.reset_index(drop=True)
    return df

# Read the instance's data (name of node, location (x, y), time-windows, load of the request)
def readDataframeHet(filename,nrequests, nvehicles=None):
    df = pd.read_csv(filename, skiprows=3, sep='\t')
    R =  list(range(nrequests))
    # temp = [df['node'].str.contains("t") == True]
    indices_to_drop = []
    if nvehicles==None:
        nvehicles=len(R)
    for index, row in df.iterrows():
        if "t" in row['node']:
            indices_to_drop.append(index)
            for r in R:
                copy = row.copy()
                copy['node'] = copy['node'].split(".")[0]+"."+str(r)+"."+copy['node'].split(".")[1]
                df = df._append(copy, ignore_index = True)
                
    
    df = df.drop(indices_to_drop)
    df = df.reset_index(drop=True)
    return df


# Generate dictionary of (node:load)
def loadDict(df):
    matrix = {}
    for location in df["node"]:
        matrix[location] = df.loc[df["node"]==location, 'load'].values[0]
    return matrix

# Get the list of grouped nodes
def calculateDistance(x1, x2, y1, y2):
    return math.sqrt((x2 - x1)**2 + (y2-y1)**2)

# one unit of distance can be traveled in one time unit
def distancesMatrix(df):
    matrix = {}
    for location1 in df["node"]:
        for location2 in df["node"]:
            if location1 != location2:
                x1 = df.loc[df["node"]==location1, 'x'].values[0]
                x2 = df.loc[df["node"]==location2, 'x'].values[0]
                y1 = df.loc[df["node"]==location1, 'y'].values[0]
                y2 = df.loc[df["node"]==location2, 'y'].values[0]
                matrix[location1,location2] = calculateDistance(int(x1), int(x2), int(y1), int(y2))
    return matrix


def getNodeList(df):
    allNodes = df['node']
    rOrigins = df.loc[df['node'].str.contains('p'),'node']
    rDestinations = df.loc[df['node'].str.contains('d'),'node']
    vOrigins = df.loc[df['node'].str.contains('o'),'node']
    vDestinations = df.loc[df['node'].str.contains('e'),'node']
    # transferNodes = df.loc[df['node'].str.contains('t') and not df.loc['node'].str.contains("s") and not df.loc['node'].str.contains("f") , 'node']
    transferStart = df.loc[df['node'].str.contains('ts'),'node']
    transferFinish = df.loc[df['node'].str.contains('tf'), 'node']
    return {"V":frozenset(allNodes), "P":frozenset(rOrigins), "D":frozenset(rDestinations), "vo":frozenset(vOrigins), "vd":frozenset(vDestinations), "ts":frozenset(transferStart), "tf":frozenset(transferFinish)}

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
            
def consolidate_vehicle_nodes(VO,points,vec_capacities):
    origin_vehicles = {}
    for o in VO:
        if tuple(points[o]) in origin_vehicles:
            origin_vehicles[tuple(points[o])].add(int(o.replace("o","")))
        else:
            origin_vehicles[tuple(points[o])] = set([int(o.replace("o",""))])
            
    location_capacity_matches = {}

    # Iterate over each location and its vehicles
    for location, vehicles in origin_vehicles.items():
        # Group vehicles by their capacities
        capacity_groups = {}
        for vehicle in vehicles:
            capacity = vec_capacities[vehicle]
            if capacity not in capacity_groups:
                capacity_groups[capacity] = set()
            capacity_groups[capacity].add(vehicle)

        # Filter out groups where there are more than one vehicle with the same capacity
        for capacity, vehicles_set in capacity_groups.items():
            if len(vehicles_set) > 1:
                location_capacity_matches[(location, capacity)] = vehicles_set
    return location_capacity_matches


def add_cuts(model):
    cuts = [(frozenset({'d2'}), 'tsr.3.0', 'tfr.3.0', ('tsr.3.0', 'tfc.3.0', 3)), (frozenset({'d2', 'tsr.10.0', 'p10', 'tfr.10.0'}), 'tsr.3.0', 'tfr.3.0', ('tsr.3.0', 'tfc.3.0', 3))]
    cuts = []
    #path = 'tfr.1.0', 'd1', 'tsc.0.0'
    for idx, (S1, do, de,(i,j,r)) in enumerate(cuts):
        if i == None:
            node_id = int(do.split(".")[-1])
            TS_comp = model._TS-frozenset([do,de])
            S2 = (model._P|model._D|model._VD|TS_comp)-S1
            RHS =  quicksum(model._x[i, do] for i in S1 if (i,do) in model._A)+quicksum(model._x[de,i] for i in S2 if (de,i) in model._A)
            RHS+=quicksum(model._x[i, j] for i in S1 for j in S2 if (i,j) in model._A)
            LHS = model._f[f"ts{node_id}"]
            model.addConstr((RHS>=LHS), name=f"cut{idx}")
        else:
            node_id = int(do.split(".")[-1])
            S2 = (model._P|model._D|model._VD|(model._TS-frozenset((i,j.replace("f","s"),))))-S1
            RHS =  quicksum(model._x[i, do] for i in S1 if (i,do) in model._A)+quicksum(model._x[de,i] for i in S2 if (de,i) in model._A)
            RHS+=quicksum(model._x[i, j] for i in S1 for j in S2 if (i,j) in model._A)
            LHS = model._y[i,j,r]
            model.addConstr((RHS>=LHS), name=f"cut{idx}")
    
    sol = [
     [('o0', 'p14'), ('p14', 'd14'), ('d14', 'e0')],
    [('o2', 'p4'), ('p4', 'p3'), ('p3', 'd4'), ('d4', 'p18'), ('p18', 'd3'), ('d3', 'p11'), ('p11', 'd11'), ('d11', 'p5'), ('p5', 'd18'), ('d18', 'p15'), ('p15', 'd5'), ('d5', 'p8'), ('p8', 'p17'), ('p17', 'ts.0.1'), ('ts.0.1', 'tf.0.1'), ('tf.0.1', 'd9'), ('d9', 'd2'), ('d2', 'd15'), ('d15', 'p7'), ('p7', 'd7'), ('d7', 'p12'), ('p12', 'p0'), ('p0', 'd12'), ('d12', 'p10'), ('p10', 'd10'), ('d10', 'p1'), ('p1', 'd0'), ('d0', 'ts.0.0'), ('ts.0.0', 'tf.0.0'), ('tf.0.0', 'e2')],
    [('o1', 'ts.2.0'), ('ts.2.0', 'tf.2.0'), ('tf.2.0', 'p13'), ('p13', 'p9'), ('p9', 'd1'), ('d1', 'p2'), ('p2', 'ts.1.1'), ('ts.1.1', 'tf.1.1'), ('tf.1.1', 'p19'), ('p19', 'd17'), ('d17', 'd19'), ('d19', 'd13'), ('d13', 'd8'), ('d8', 'p6'), ('p6', 'p16'), ('p16', 'd16'), ('d16', 'd6'), ('d6', 'e1')],
    ]
    sol = []
    for route in sol:
        for e in route:
            model.addConstr(model._x[e]==1)
    return model
        

# Model
def twoIndexModel(filename, seed=None, symm=False):
    
    def check_precedence(edges):
        G = nx.DiGraph()
        G.add_edges_from(edges, capacity=1.0)
        partitions = []
        #for o in VO:
        for r in R:
            flow_value, flow_dict = nx.maximum_flow(G, f"p{r}" , f"d{r}")
            if flow_value<1.0:
                cut_val, partition = nx.minimum_cut(G,  f"p{r}" , f"d{r}", capacity='capacity')
                #partition = nx.minimum_node_cut(G, o , o.replace("o","e"))
                #if len(partition[0])<len(partition[1]):
                if f"d{r}" in partition[0]:
                    partitions.append(partition[0])
                else:
                    partitions.append(partition[1])
        return partitions
    
    def eliminate_precedence(model):
        """Extract the current solution, check for subtours, and formulate lazy
        constraints to cut off the current solution if subtours are found.
        Assumes we are at MIPSOL."""
        all_x_vars = model.cbGetSolution(model._x)
        edges = [a for a in A if all_x_vars[a] >= 0.5]
        illegal_subsets = check_precedence(edges)
        if illegal_subsets !=None:
            for illegal_subset in illegal_subsets:
                if len(illegal_subset) < len(V):
                    # add subtour elimination constraint for every pair of cities in tour
                    #pos_edges = list(combinations(illegal_subset,2))
                    #pos_edges += [(j,i) for i,j in pos_edges]
                    incoming_edges = set()
                    for i in illegal_subset:
                        incoming_edges.update([a for a in A.select("*",i) if a[0] not in illegal_subset])
                    model.cbLazy(
                        gp.quicksum(model._x[i, j] for i, j in incoming_edges)
                        >= 1
                    )
    

    def check_illegal_transfer(model, x, y):
            #returns true if cut was added

            G = nx.DiGraph()
            #for e in z:
             #  G.add_edge(e[0],e[1],arrival_time=z[e])
            
            G.add_edges_from(x)
            trans_edges = [e for e in y if (e[0],e[1]) in TIy]
            for o in VO:
                if o in G.nodes:
                    tours = list(nx.all_simple_paths(G, o, o.replace("o","e")))
                    for tour in tours:
                        # Get edges in the tour
                        #tour_edges = [(tour[i], tour[i+1]) for i in range(len(tour)-1)]
                        
                        # Create subgraph with these edges
                        #subgraph = G.edge_subgraph(tour_edges).copy()
                        for do,de,r in trans_edges:
                            if do in tour and de in tour:
                                path = nx.shortest_path(G, do,de)
                                i,j = do,de
                                do = do.replace("f","s")
                                de = do.replace("s","f")
                                S1 = frozenset(path[2:-2])
                                S2 = (model._P|model._D|model._VD|model._VO|(TS-frozenset((i,j.replace("f","s"),))))-S1
                                RHS =  quicksum(model._x[i, do] for i in S1 if (i,do) in model._A)+quicksum(model._x[de,i] for i in S2 if (de,i) in model._A)
                                RHS+=quicksum(model._x[i, j] for i in S1 for j in S2 if (i,j) in model._A)
                                RHS_check= sum(x[i, do] for i in S1 if (i,do) in x)+sum(x[de,i] for i in S2 if (de,i) in x)+sum(x[i, j] for i in S1 for j in S2 if (i,j) in x)
                                LHS = model._y[i,j,r]
                                print(f"Self transfer cut for set {S1}, {path}, RHS: {RHS_check}")
                                model.cbLazy(RHS>=LHS)
                                model._lazy_cuts += 1
                                model._cuts.append((S1,do,de,(i,j,r)))
                                return True
                                #Naive approach
                                """
                                LHS = quicksum(model._x[e] for e in model._A if e not in x) 
                                LHS_check = sum(x.get(e,0) for e in model._A if e not in x)
                                RHS = 1.0
                                model.cbLazy(
                                    LHS#for (i,j) in edges)#
                                    >= RHS
                                    )
                                model._lazy_cuts += 1
                                print(f"added double Trans visit cut {LHS_check}<={RHS}")
                                return True#"""
                            
            return False
        
        
    def has_duplicate_node_ids(nodes):
        node_ids = [node.split('.')[-1] for node in nodes]
        return len(node_ids) != len(set(node_ids))
    
    def get_nodes_with_duplicate_ids(nodes):
        # Group nodes by their node ID
        id_to_nodes = defaultdict(list)
        for node in nodes:
            node_id = int(node.split('.')[-1])
            id_to_nodes[node_id].append(node)
        
        # Return only groups with duplicates
        return {node_id: nodes_list for node_id, nodes_list in id_to_nodes.items() 
                if len(nodes_list) > 1}
    
    def check_multiple_transfer_stations(model,x):
        G = nx.Graph()
        G.add_edges_from(x)
        scc = [
            c
            for c in sorted(nx.connected_components(G), key=len) if len(c)>1
        ]
        for comp in scc:
            T_nodes = frozenset(comp) & model._TS
            if has_duplicate_node_ids(T_nodes):
                duplicates = get_nodes_with_duplicate_ids(T_nodes)
                # For each group of duplicate node IDs, find shortest paths
                for node_id, duplicate_nodes in duplicates.items():
                    min_path = None
                    min_length = float('inf')
                    nodes = None
                    #print("has duplicates")
                    G = nx.DiGraph()
                    G.add_edges_from(x)
                    # Check all pairs of nodes with the same ID
                    for i, node1 in enumerate(duplicate_nodes):
                        for node2 in duplicate_nodes:
                            if node2!=node1:
                                try:
                                    node1 = node1.replace("s","f")
                                    # Find shortest path (by number of nodes)
                                    path = nx.shortest_path(G, node1, node2)
                                    path_length = len(path)
                                    
                                    if path_length < min_length:
                                        min_length = path_length
                                        min_path = path
                                        nodes = (node1,node2)
                                except nx.NetworkXNoPath:
                                    # No path exists between these nodes
                                    pass
                    
                    if min_path:
                        do_cut ,de_cut = nodes
                        do = do_cut.replace("f","s")
                        de = do_cut
                        node_id = int(do.split(".")[-1])
                        S1 = frozenset(min_path[1:-1])
                        TS_comp = model._TS-frozenset([do,de_cut])
                        S2 = (model._P|model._D|model._VD|TS_comp)-S1
                        RHS =  quicksum(model._x[i, do] for i in S1 if (i,do) in model._A)+quicksum(model._x[de,i] for i in S2 if (de,i) in model._A)
                        RHS+=quicksum(model._x[i, j] for i in S1 for j in S2 if (i,j) in model._A)
                        RHS_check= sum(x[i, do] for i in S1 if (i,do) in x)+sum(x[de,i] for i in S2 if (de,i) in x)+sum(x[i, j] for i in S1 for j in S2 if (i,j) in x)
                        LHS = model._f[f"ts{node_id}"]
                        print(f"Shortest path for node_id {node_id}: {min_path},(length: {min_length}), RHS: {RHS_check}")
                        model.cbLazy(RHS>=LHS)
                        model._cuts.append((S1,do,de_cut,(None,None,None)))
                        model._lazy_cuts += 1
                        if RHS_check>=1:
                            #breakpoint()
                            print("Stop")
                        return
        
    def callback_het(model, where):
        if where == GRB.Callback.MIPSOL:
            model._lazy_calls += 1
            start = time.time()
            cur_obj = model.cbGet(gp.GRB.Callback.MIPSOL_OBJ)
            cur_bnd =    model.cbGet(gp.GRB.Callback.MIPSOL_OBJBND)
            sol_cnt =  model.cbGet(gp.GRB.Callback.MIPSOL_SOLCNT)
            if sol_cnt>0:
                best_obj = model.cbGet(gp.GRB.Callback.MIPSOL_OBJBST)
                cur_gap =  abs(best_obj -cur_bnd)/cur_obj
            else:
                cur_gap = 1.0
            all_x_vars = model.cbGetSolution(model._x)
            all_y_vars = model.cbGetSolution(model._y)
            #all_f_vars = model.cbGetSolution(model._f)
            #f_arcs = {a:all_f_vars[a] for a in TS_pure if all_f_vars[a] > 0.5}
            #if len(f_arcs)>0:
            #if cur_obj<=503.236 and cur_obj>=503.23:
             #   print("violation", cur_obj)
                #breakpoint()
            x_arcs = {a:1 for a in A if all_x_vars[a] > 0.5}
            y_arcs = tuplelist({a for a in Ay if all_y_vars[a] > 0.5})
            added_cut = check_illegal_transfer(model, x_arcs, y_arcs)
            if added_cut == True:
                return
            if MULTI_TRANS:
                check_multiple_transfer_stations(model,x_arcs)
                
    def callback_symm(model, where):
        if where == GRB.Callback.MIPSOL:
            model._lazy_calls += 1
            start = time.time()
            cur_obj = model.cbGet(gp.GRB.Callback.MIPSOL_OBJ)
            cur_bnd =    model.cbGet(gp.GRB.Callback.MIPSOL_OBJBND)
            sol_cnt =  model.cbGet(gp.GRB.Callback.MIPSOL_SOLCNT)
            if sol_cnt>0:
                best_obj = model.cbGet(gp.GRB.Callback.MIPSOL_OBJBST)
                cur_gap =  abs(best_obj -cur_bnd)/cur_obj
            else:
                cur_gap = 1.0
            all_x_vars = model.cbGetSolution(model._x)
            x_arcs = {a:1 for a in A if all_x_vars[a] > 0.5}
            check_multiple_transfer_stations(model,x_arcs)
             
    model = gp.Model()
    print(filename)
    metaData = readMetaData(filename)
    HET = False
    MULTI_TRANS = False
    if "Ghilas" in filename:
        df = readDataframeHet(filename,int(metaData["nr"]))
        HET = True
        MULTI_TRANS=False
    elif MULTI_TRANS:
        df = readDataframeHet(filename,int(metaData["nr"]), int(metaData["nv"]))
    else:
        df = readDataframe(filename)
    nodeList = getNodeList(df)
    
    V =  nodeList["V"]
    P = nodeList["P"]
    D = nodeList["D"]
    VO = nodeList["vo"]
    VD = nodeList["vd"]
    TS = nodeList["ts"]
    TF = nodeList["tf"]
    if HET or MULTI_TRANS:
        TSR = frozenset(df.loc[df['node'].str.contains('tsr'),'node'])
        TFR = frozenset(df.loc[df['node'].str.contains('tfr'),'node'])
    
    TS_loc = {}
    
    TF_loc = {}
    
    TS_pure = []
    TF_pure = []
    
    for node in TS:
        prefix,k_idx,node_idx = node.split(".")
        node_idx = int(node_idx)
        k_idx = int(k_idx)
        if node_idx in TS_loc:
            TS_loc[node_idx].append(node)
            TF_loc[node_idx].append(node.replace("s","f"))
        else:
            TS_loc[node_idx] = [node]
            TF_loc[node_idx]= [node.replace("s","f")]
    
    for n in TS_loc:
        node = TS_loc[n][0]
        node = node.split(".")[0]+node.split(".")[2]
        TS_pure.append(node.replace("r","").replace("c",""))
        TF_pure.append(node.replace("s","f"))
        
    nRequests = int(metaData['nr'])
    nVehicles = int(metaData['nv'])
    nTransports = int(metaData['nt'])
    VC = int(metaData['capacity'])
    K = list(range(nVehicles))
    
    df["points"] = df[["x","y"]].values.tolist()

    points = df.set_index("node")["points"].to_dict()
    VCmax = VC
    
    if VC<0:
        service_time = pd.Series(df.s.values,index=df.node).to_dict()
        node_capacities = pd.Series(df.vcap.values,index=df.node).to_dict()
        vec_capacities = {}
        Qk = {int(i.replace("o","")):node_capacities[i] for i in VO}
        Qmin = min(Qk.values())
        Qmax = max(Qk.values())
        for node in node_capacities:
            if node_capacities[node]>0:
                vec_capacities[int(node.replace("o","").replace("e",""))] = abs(Qmin-node_capacities[node])
                vec_capacities[int(node.replace("o","").replace("e",""))] = abs(Qmax-node_capacities[node])
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
    
    c = distancesMatrix(df)
    timeHorizon = df["a"].max()
    
    df["tw"] = df[["a","b"]].values.tolist()
    
    timeWindows = df.set_index('node')["tw"].to_dict()
    def time_window_reduction_rules(l,rule):
        #min arrival time predecessors
        if rule==1:
            twa = timeWindows[l][0]
            if l in P:
                predset = P|D|VO|TF
            if l in VD:
                predset = D|TF
            if l in D:
                predset = P|D|TF
            if l in TS:
                predset = P|D|TF|VO
            if l in TF:
                predset = TS
            timeWindows[l][0] = float(np.round(max(timeWindows[l][0], min(timeWindows[l][1],min(timeWindows[i][0]+c[i,l]+service_time[i] for i in predset if l!=i))),2))
            if twa<timeWindows[l][0]:
                return True
            else:
                return False
        #min arrival time successors
        if rule==2:
            twa = timeWindows[l][0]
            if l in P:
                succset = P|D|TS
            if l in VO:
                succset = P|TS
            if l in D:
                succset = (VD|P|D|TS)-set(l.replace("d","p"))
            if l in TS:
                succset = TF
            if l in TF:
                succset = P|D|VD|TS
            timeWindows[l][0] = float(np.round(max(timeWindows[l][0], min(timeWindows[l][1],min(timeWindows[i][0]-c[l,i] for i in succset if l!=i))),2))
            if twa<timeWindows[l][0]:
                return True
            else:
                return False
        #max departure from pred
        if rule==3:
            twb = timeWindows[l][1]
            if l in P:
                predset = P|D|VO|TF
            if l in VD:
                predset = D|TF
            if l in D:
                predset = P|D|TF
            if l in TS:
                predset = P|D|TF|VO
            if l in TF:
                predset = TS
            timeWindows[l][1] = float(np.round(min(timeWindows[l][1], max(timeWindows[l][0],max(timeWindows[i][1]+c[i,l]+service_time[i] for i in predset if l!=i))),2))
            if twb>timeWindows[l][1]:
                return True
            else:
                return False
        #max departure to succ
        if rule==4:
             twb = timeWindows[l][1]
             if l in P:
                 succset = P|D|TS
             if l in VO:
                 succset = P|TS
             if l in D:
                 succset = (VD|P|D|TS)-set(l.replace("d","p"))
             if l in TS:
                 succset = TF
             if l in TF:
                 succset = P|D|VD|TS
             timeWindows[l][1] = float(np.round(min(timeWindows[l][1], max(timeWindows[l][0],max(timeWindows[i][1]-c[l,i] for i in succset if l!=i))),2))
             if twb>timeWindows[l][1]:
                 return True
             else:
                 return False
        raise ValueError(f"Value {rule} is wrong, it must be 1,2,3 or 4")
    def time_window_reduction_loop():
        for i in P|D:
            timeWindows[i][0] = min([max(timeWindows[i][0],timeWindows[f"o{k}"][0]+c[f"o{k}",i]) for k in K])
            timeWindows[i][1] = min(max(timeWindows[f"e{k}"][1]-c[i,f"e{k}"]-service_time[i] for k in K),timeWindows[i][1])
        changed = True
        loops = 0
        while changed==True:
            changed = False
            loops+=1
            #min arrival time predecessors
            for l in P|D|VD:
                if time_window_reduction_rules(l,1)==True:
                    changed = True
                if time_window_reduction_rules(l,3)==True:
                    changed = True
            for l in P|D|TS|TF|VO:
                if time_window_reduction_rules(l,2)==True:
                    changed = True
                if time_window_reduction_rules(l,4)==True:
                    changed = True
        print(f"{loops} times changed TWs loop")
    time_window_reduction_loop()
    if HET or MULTI_TRANS:
        for i in TS|TF:
            r = int(i.split(".")[1])
            a = min(timeWindows[f"p{r}"][0]+c[f"p{r}",i]+service_time[f"p{r}"],timeWindows[f"d{r}"][1])
            b = max(0+service_time[i],timeWindows[f"d{r}"][1]-c[i.replace("s","f"),f"d{r}"]-service_time[i])
            if a+service_time[i]>b:
                #print(i)
                a = 0
                b = a+service_time[i]
            #else:
                #b = max(timeWindows[ed][1]-c[i.replace("s","f"),ed]-service_time[i] for ed in VD)
            timeWindows[i][0] = a
            timeWindows[i][1] = b
   
    qnode = df.set_index('node')["load"].to_dict()
    q = {int(node.replace("p","")):qnode[node] for node in P}
        
    #change travel times
    def check_no_time_window_violation(i,j):
        #returns true if no time window violation
        if timeWindows[i][0]+t[i,j]+service_time[i]<=timeWindows[j][1]:
            return True
        return False
    
    
    t = c.copy()
    n1 = 0
    for i,j in c:
        if VC<0:
            if c[i,j]+timeWindows[i][1]+service_time[i]<timeWindows[j][0]:
                t[i,j] = timeWindows[j][0]-timeWindows[i][1]-service_time[i]
                n1+=1
        else:
            if c[i,j]+timeWindows[i][1]+service_time[i]<timeWindows[j][0]:
                t[i,j] = timeWindows[j][0]-timeWindows[i][1]-service_time[i]
                n1+=1
    R = list(range(nRequests))
    
    min_vec = VC
    if VC<0:
        min_vec = Qmax
        
    arcs = []
    ats = set()
    for i in VO:
        for j in P:
            if check_no_time_window_violation(i,j)==True:
                arcs.append((i,j))
        for j in TS|TF:
            if check_no_time_window_violation(i,j)==True:
                arcs.append((i,j))
        arcs.append((i, i.replace("o","e")))

    for i in P:
        for j in P:
            if i != j:
                if check_no_time_window_violation(i,j)==True:
                    if qnode[i]+qnode[j]<=min_vec:
                        arcs.append((i,j))
        for j in D:
            if i != j:
                if check_no_time_window_violation(i,j)==True:
                    if i!=j.replace("d","p"):
                        if abs(qnode[i])+abs(qnode[j])<=min_vec:
                            arcs.append((i,j))
                    else:
                        arcs.append((i,j))
        for j in TS:
            if i != j:
                if check_no_time_window_violation(i,j)==True:
                    arcs.append((i,j))
                    
        for j in TF:
            if i != j:
                if check_no_time_window_violation(i,j)==True:
                    arcs.append((i,j))
    

    for i in D:
        for j in P|VD|TS|TF:
            if not (j in P and i == j.replace("p","d")):
                if check_no_time_window_violation(i,j)==True:
                    arcs.append((i,j))
        for j in D:
            if not (i == j or (j in P and i == j.replace("p","d"))):
                if check_no_time_window_violation(i,j)==True:
                    if abs(qnode[i])+abs(qnode[j])<=min_vec:
                        arcs.append((i,j))

    for i in TS:
        for j in TS|P|D|VD:
            if i != j:
                if check_no_time_window_violation(i,j)==True:
                    arcs.append((i,j))
        for j in TF:
            prefix,k_idx,node_idx = j.split(".")
            node_idx = int(node_idx)
            if j not in TF_loc[node_idx]:
                if check_no_time_window_violation(i,j)==True:
                    arcs.append((i,j))
                    
    for i in TF:
        for j in TF|P|D|VD:
            if i != j:
                if check_no_time_window_violation(i,j)==True:
                    arcs.append((i,j))
        for j in TS:
            prefix,k_idx,node_idx = j.split(".")
            node_idx = int(node_idx)
            if j not in TS_loc[node_idx]:
                if check_no_time_window_violation(i,j)==True:
                    arcs.append((i,j))




    arcs = list(dict.fromkeys(arcs))
    
    #A = [(i,j) for i in V for j in V if i!=j]
    
    A = tuplelist(arcs)
    
    Ayc = [(i,j,r) for r in R for i in P for j in V-(frozenset((i,f"p{r}"))|VO|VD) if (i,j) in A]
    Ayd = [(i,j,r) for r in R for i in D-frozenset(("d"+str(r),)) for j in (V-frozenset([i,i.replace("d","p"),f"p{r}"])-VO-VD) if (i,j) in A]
    Ayts1 = [(i,i.replace("s","f"),int(i.split(".")[1])) for i in TS]
    Ayts2 = [(i.replace("s","f"),i,int(i.split(".")[1])) for i in TS]

    Aytf1 = [(i,j,r) for r in R for i in TF for j in V-(frozenset((i,f"p{r}"))|VO|VD) if (i,j) in A]
    Aytf2 = [(i,j,r) for r in R for i in TS for j in V-(frozenset((i,f"p{r}"))|VO|VD) if (i,j) in A]

    
    Ay = Ayc+Ayd+Ayts1+Ayts2+Aytf1+Aytf2
      
    
    #print(Ay[('d1', 'p1',1)])
    
    Ay = tuplelist(Ay)
    TIy = [(i,j) for i in TS for j in TF_loc[int(i.split(".")[2])] if i!=j.replace("f","s")]

    #print(Ay)
    
    #print(Ay)

    
    
    

    

    #xc = df.set_index('node').x.to_dict()
    #yc = df.set_index('node').y.to_dict()
    #c = {(i, j): float(np.hypot(xc[i]-xc[j], yc[i]-yc[j]).round(2)) for i, j in A}
    
    
    
    
    #print(c["tf.0.0","ts.1.0"])

    k = pd.RangeIndex(nVehicles)
    r = pd.RangeIndex(nRequests)
    u = pd.Series(index=k, data=np.full(nVehicles, VC))
   
   

    

    xIndex = [(i, j) for (i,j) in arcs]
    kIndex = [(i,r) for r in K for i in V]
    zIndex = [i for i in V]
    aIndex = [(i,r) for i in TS|TF for r in pd.RangeIndex(nRequests) ]
    
    
        
    print(df)
    
    Mij = {(i,j):max(0,timeWindows[i][1]+service_time[i]+t[i,j]-timeWindows[j][0]) for (i,j) in c}
    #Mij = {(i,j):600+service_time[j] for (i,j) in c}

    M = max(Mij.values())
    #Mt = {(i,j):(timeWindows[i][1]-c[i.replace("s","f"),"e"+i.split(".")[1]])-max(c["o"+j.split(".")[1].replace("f","s"),i],timeWindows[j][0]) for i in TS for j in TF}


    Akc= [(i, j,k) for k in K for i in P for j in V-(frozenset((i,))|VO|VD) if (i,j) in A]
    Akd= [(i, j,k) for k in K for i in D for j in V-(frozenset((i,))|VO) if (i,j) in A]
    Aks= [(i, j,k) for k in K for i in TS|TF for j in V-(frozenset((i,))|VO) if (i,j) in A]
    AkoOut= [(i, j,k) for k in K for i in [f"o{k}"] for j in V-VO-(VD-frozenset([f"e{k}"])) if (i,j) in A]
    Ak = Akc+Akd+Aks+AkoOut
    Ak = tuplelist(Ak)


    model = Model('myTwoIndexModel_TGhilasTWs')
    
    x = model.addVars(xIndex, vtype=GRB.BINARY, name='x')
    y = model.addVars(Ay, vtype=GRB.BINARY, name='y')
    #alph = model.addVars(TS|TF,lb=0,ub=1.0, vtype=GRB.CONTINUOUS, name='alph')
    #Idee wenn zwei vehicle unterschiedliche StartPositionen haben, b trackt vehicle flow
    b = model.addVars(arcs,lb=0.0,ub=len(K)-1, vtype=GRB.CONTINUOUS, name='b')
    #bl = model.addVars(kArcs, vtype=GRB.BINARY, name='bl')
    bl = model.addVars(V,ub=len(K), vtype=GRB.CONTINUOUS, name='bl')
    if VC < 0:
       vl = model.addVars(V,lb=0.0,ub=max(vec_capacities[k]-vec_capacities[l] for k in K for l in K if l!=k ), vtype=GRB.CONTINUOUS, name='vl')
       #vl = model.addVars(Ak, vtype=GRB.BINARY, name='vl') 
       model._vl = vl
    #ti = model.addVars(TIy, vtype=GRB.BINARY, name='ti')

    #b = model.addVars(xIndex,lb=0.0, ub=nVehicles ,vtype=GRB.CONTINUOUS, name="b")
    z = model.addVars(zIndex,lb=0.0 ,vtype=GRB.CONTINUOUS, name="z")
    #a = model.addVars([(i,r) for i in TS for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="a")
    #ba = model.addVars([(i,r) for i in TF for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="ba")
    f = model.addVars([i for i in TS_pure], vtype=GRB.BINARY, name='f')
    
    model.modelSense = GRB.MINIMIZE
    model.setObjective(quicksum(0.5*c[i,j] * x[i, j] for (i,j) in arcs))
    model.update()
    
    
    """
    Arc flows
    """
    

    
    #model.addConstr(x["p1","ts.1.0"]==1)
    #model.addConstr(x["tf.1.0","d1"]==1)
    #model.addConstr(x["o2","e2"]==1)
    #model.addConstr(x["o0","e0"]==1)
    #model.addConstr(f["ts1"]==0)
    
    #model.addConstr(x["p0","d0"]==1)
    
    #model.addConstr(x["d0","e0"]==1)
    #model.addConstrs(x[i,i.replace("s","f")]==0 for i in TS)
    model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A.select(vo,'*')]) == 1 for vo in VO), name = "ct.route_startFirst")
    model.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
    

    
    model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A.select('*',i)]) == 1 for i in P), name = "ct.PickupJustOnce")
    
    model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A.select('*',i)]) == 1 for i in D), name = "ct.DeliveryJustOnce")

    
    #model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A.select('*',i)]) <= 1 for i in V), name = "ct.PickupAndDeliveryJustOnce")

    
    model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A.select('*',i)]) == quicksum(x[i,j] for j in [a[1] for a in A.select(i,'*')])   for i in P|D|TS|TF), name = "ct.FlowConversion")
    
    """
    for i in V:
        for j in V:
            if (i,j) in arcs:
                if (j,i) in arcs:
                    model.addConstr((x[j,i]+x[i,j] <= 1), name = "ct.SubtourElimCT")
    
    
    for i in P|D:
        for j in TS:
            if (i,j) in arcs:
                if (j.replace("s","f"),i) in arcs:
                    model.addConstr((x[j.replace("s","f"),i]+x[i,j] <= 1), name = "ct.SubtourElimCTTransfer")
    """
    
    """
    Loads
    """
    
    model.addConstrs((quicksum(y[i, j, r] for j in [a[1] for a in Ay.select(i,'*',r)])  == 1 for r in R for i in [f"p{r}"]), name = "ct.visit_request_originOut")


    model.addConstrs((quicksum(y[j,i, r] for j in [a[0] for a in Ay.select('*',i,r)])  == 1 for r in R for i in [f"d{r}"]), name = "ct.visit_request_destinationIn")

    #model.addConstrs((quicksum(y[i, j,r]  for i in TS_loc[n] for j in [a[1] for a in Ay.select(i,'*',r)])-quicksum(y[j,i,r]  for i in TF_loc[n] for j in [a[0] for a in Ay.select('*',i,r)]) == 0 for r in R for n in TS_loc), name = "ct.requestTransferFlow")

    #model.addConstrs((quicksum(y[i, j,r]  for j in [a[1] for a in Ay.select(i,'*',r)])== 0 for r in R for i in TS), name = "ct.requestTransferFlow")


    model.addConstrs((quicksum(y[i, j,r] for j in [a[1] for a in Ay.select(i,'*',r)])-quicksum(y[j,i,r] for j in [a[0] for a in Ay.select('*',i,r)]) == 0 for r in R for i in V-(VD|VO|frozenset((f"p{r}","d{r}"))) if i not in ["p"+str(r),"d"+str(r)]), name = "ct.requestFlowConversion")

    for (i,j,r) in Ay:
        if (i,j,r) not in Ayts1+Ayts2:
            model.addConstr((y[i,j,r] <= x[i,j]), name = "ct.request_flow_link")
    for i in TS:
        r = int(i.split(".")[1])
        j = i.replace("s","f")
        model.addConstr((y[i,j,r]+y[j,i,r] <= 1), name = "ct.request_transfer_balance")


    #model.addConstrs((y[i,j,r] <= x[i,j] for r in R for i in V-TS for j in [a[1] for a in Ay.select(i,'*',r)]), name = "ct.request_flow_link")


    #model.addConstrs((y[i,j,r] <= quicksum(x[j,i] for j in [a[0] for a in A.select('*',i)]) for r in R for i in TS for j in [a[1] for a in Ay.select(i,'*',r)]), name = "ct.request_flow_linkTS")

    #model.addConstrs((y[j,i,r] <= quicksum(x[i,j] for j in [a[1] for a in A.select(i,'*')]) for r in R for i in TF for j in [a[0] for a in Ay.select('*',i,r)]), name = "ct.request_flow_linkTF")

    """
    Capacity constraint
    """
    # capacity constraint
    if VC>0:
        #model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)]) <= VC*x[i,j] for i in P|D|TF for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacity")
        #model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R for j in [a[1] for a in Ay.select(i,'*',r)]) <= VC for i in P|D|TF), name="ct.VehicleCapacity")
        # Strengthened capacity constraints
        #"""
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-abs(qnode[i]+qnode[j]))*x[i,j] for i in P for j in [a[1] for a in A.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong1")
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-abs(qnode[i]+qnode[j]))*x[i,j] for i in D for j in [a[1] for a in A.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong2")
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in P for j in [a[1] for a in A.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong3")
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in D for j in [a[1] for a in A.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong4")
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(j.replace("p","").replace("d",""))) <= (VC-abs(qnode[j]))*x[i,j] for i in TF for j in [a[1] for a in A.select(i,'*')] if j in P|D), name="ct.VehicleCapacityStrong5")
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d",""))) <= (VC-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in P for j in [a[1] for a in A.select(i,'*')] if j in TS), name="ct.VehicleCapacityStrong3b")
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d",""))) <= (VC-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in D for j in [a[1] for a in A.select(i,'*')] if j in TS), name="ct.VehicleCapacityStrong4b")
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)]) <= (VC-abs(qnode[j]))*x[i,j] for i in TF for j in [a[1] for a in A.select(i,'*')] if j in TS), name="ct.VehicleCapacityStrong5b")
        
        #model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= VC*x[i,j] for i in TF for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacityStrong5")

        #model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(j.replace("p","").replace("d",""))) <= (VC-abs(qnode[i]+qnode[j]))*x[i,j] for i in TF for j in [a[1] for a in A.select(i,'*')] if j in P|D), name="ct.VehicleCapacityStrongTF")
        
        #tested cts
        #model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if r!=int(i.replace("p","").replace("d","")) for j in [a[1] for a in Ay.select(i,'*',r)]) <= VC-abs(qnode[i]) for i in P|D), name="ct.VehicleCapacityStrong2")
        #model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R for j in [a[1] for a in Ay.select(i,'*',r)]) <= VC for i in TS|TF), name="ct.VehicleCapacityStrong2")
        #"""
        #test original one
        #model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if r!=int(i.replace("p","").replace("d","")) and j in [a[1] for a in Ay.select(i,'*',r)]) <= (VC-abs(qnode[i]))*x[i,j] for i in P|D  for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacityStrong2")
        #model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if j in [a[1] for a in Ay.select(i,'*',r)]) <= (VC)*x[i,j] for i in P|D  for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacityStrong2")
        
        #best performing one
        model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if r!=int(i.replace("p","").replace("d","")) and j in [a[1] for a in Ay.select(i,'*',r)]) <= (VC-abs(qnode[i]))*x[i,j] for i in P|D  for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacityStrong2")
        model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if j in [a[1] for a in Ay.select(i,'*',r)]) <= (VC)*x[i,j] for i in TS|TF  for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacityStrong2")

        #naive redudant
        #model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if j in [a[1] for a in Ay.select(i,'*',r)]) <= (VC)*x[i,j] for i in P|D|TS|TF  for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacityStrong2")


        #model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R for j in [a[1] for a in Ay.select(i,'*',r)]) <= quicksum((VC-abs(qnode[i]))*x[i,j] for j in [a[1] for a in A.select(i,'*')]) for i in TF), name="ct.VehicleCapacityStrong2")
        #model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if r!=int(i.replace("p","").replace("d","")) for j in [a[1] for a in Ay.select(i,'*',r)]) <= quicksum((VC-abs(qnode[i]))*x[i,j] for j in [a[1] for a in A.select(i,'*')]) for i in P|D), name="ct.VehicleCapacityStrong2")

        #model.addConstrs((quicksum(q[r]*y[i, j,r] for j in [a[1] for a in A.select(i,'*')] for r in R if r in [a[2] for a in Ay.select(i,j,r)]) <= VC for i in TF|TS), name="ct.VehicleCapacity")
        #model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if r!=int(i.replace("p","").replace("d","")) for j in [a[1] for a in Ay.select(i,'*',r)]) <= quicksum((VC-abs(qnode[i]))*x[i,j] for j in [a[1] for a in A.select(i,'*')]) for i in P|D), name="ct.VehicleCapacityStrong2")
        
        
    else:
        """
        model.addConstrs((vl[i, j, k]   >= x[i,j] for k in K for i in VO for j in [a[1] for a in Ak.select(i,'*',k)]), name = "ct.visit_request_originOut")

        model.addConstrs((quicksum(vl[i, j, k] for j in [a[1] for a in Ak.select(i,'*',k)])   == quicksum(vl[j,i.replace("o","e"), k] for j in [a[0] for a in Ak.select('*',i.replace("o","e"),k)])  for k in K for i in VO), name = "ct.visit_request_originOut")

        #model.addConstrs((quicksum(y[i, j,r]  for i in TS_loc[n] for j in [a[1] for a in Ay.select(i,'*',r)])-quicksum(y[j,i,r]  for i in TF_loc[n] for j in [a[0] for a in Ay.select('*',i,r)]) == 0 for r in R for n in TS_loc), name = "ct.requestTransferFlow")

        #model.addConstrs((quicksum(y[i, j,r]  for j in [a[1] for a in Ay.select(i,'*',r)])== 0 for r in R for i in TS), name = "ct.requestTransferFlow")


        model.addConstrs((quicksum(vl[i, j,k] for j in [a[1] for a in Ak.select(i,'*',k)])-quicksum(vl[j,i,k] for j in [a[0] for a in Ak.select('*',i,k)]) == 0 for k in K for i in V-(VD|VO|TS|TF)), name = "ct.requestFlowConversion")


        model.addConstrs((vl[i,j,k] <= x[i,j] for k in K for i in V for j in [a[1] for a in Ak.select(i,'*',k)]), name = "ct.request_flow_link")

        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)]) <= quicksum(Qk[k]*vl[i,j,k] for k in K) for i in P|D|TF for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacity")
        
        """
        #model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R for j in [a[1] for a in Ay.select(i,'*',r)]) <= VC for i in P|D|TF), name="ct.VehicleCapacity")
        # Strengthened capacity constraints
        #"""
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (Qmax-abs(qnode[i]+qnode[j]))*x[i,j] for i in P for j in [a[1] for a in A.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong1")
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (Qmax-abs(qnode[i]+qnode[j]))*x[i,j] for i in D for j in [a[1] for a in A.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong2")
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (Qmax-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in P for j in [a[1] for a in A.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong3")
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (Qmax-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in D for j in [a[1] for a in A.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong4")
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d",""))) <= (Qmax-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in P for j in [a[1] for a in A.select(i,'*')] if j in TS|TF), name="ct.VehicleCapacityStrong3b")
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d",""))) <= (Qmax-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in D for j in [a[1] for a in A.select(i,'*')] if j in TS|TF), name="ct.VehicleCapacityStrong4b")
       
        model.addConstrs((vl[f"o{k}"]  == vec_capacities[k] for k in K), name = "ct.route_startVehicleCapLabelStart")
        
        model.addConstrs((vl[f"e{k}"]  == vec_capacities[k] for k in K), name = "ct.route_startVehicleCapLabelEnd")
        
       
        
        model.addConstrs((vl[i]-(max(vec_capacities[k]-vec_capacities[l] for k in K for l in K if k!=l))*(1-x[i,j])<=vl[j] for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) not in A), name = "ct.vehicleCapLabelFlowA")
        
        model.addConstrs((vl[i]-vl[j]<=(max(vec_capacities[k]-vec_capacities[l] for k in K for l in K if k!=l))*(1-x[i,j]-x[j,i]) for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) in A), name = "ct.vehicleCapLabelFlowA")

      
        model.addConstrs((vl[j]-(max(vec_capacities[k]-vec_capacities[l] for k in K for l in K if k!=l))<=vl[i]  for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) not in A), name = "ct.vehicleCapLabelFlowB")
       
        model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R for j in [a[1] for a in Ay.select(i,'*',r)]) <= Qmax-vl[i] for i in P|D|TF|TS), name="ct.VehicleCapacity")#"""
     

    """
    Vehicle Flow Bektas 2018
    """
    """
    model.addConstrs((bl[i]+(len(K)-1-int(od.replace("o","")))*x[od,i]  <= (len(K)-1) for od in VO for i in [a[1] for a in A.select(od,'*')]), name = "ct.route_startVehicleLabel")
    
    model.addConstrs((bl[i]+(len(K)-1-int(ed.replace("e","")))*x[i,ed]  <= (len(K)-1) for ed in VD for i in [a[0] for a in A.select('*',ed)]), name = "ct.route_endVehicleLabel")
    
    model.addConstrs(((int(od.replace("o","")))*x[od,i]  <= bl[i] for od in VO for i in [a[1] for a in A.select(od,'*')]), name = "ct.route_startVehicleLabelB")
    
    model.addConstrs(((int(ed.replace("e","")))*x[i,ed]  <= bl[i] for ed in VD for i in [a[0] for a in A.select('*',ed)]), name = "ct.route_endVehicleLabelB")
    
    model.addConstrs((bl[i]  == int(i.split(".")[1]) for n in TS_loc for i in TS_loc[n]), name = "ct.route_transferVehicleLabel")


    
    covered = set()
    for i in V-VD-VO:
        for j in [a[1] for a in A.select(i,'*') if a[1] not in VD|VO]:
            if (j,i) in arcs:
                if (i,j) not in covered:
                    covered.add((i,j))
                    covered.add((j,i))
                    model.addConstr((bl[i]-(len(K)-2)*(1-x[i,j]-x[j,i])<=bl[j]), name = "ct.vehicleLabelFlowLifted")
            else:
                model.addConstr((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j]), name = "ct.vehicleLabelFlowA")
                model.addConstr((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]), name = "ct.vehicleLabelFlowB")
    """
    
    """
    Vehicle Flow Burger
    """
    
    
    model.addConstrs((bl[f"o{k}"]  == k+1 for k in K), name = "ct.route_startVehicleLabel")
    
    model.addConstrs((bl[f"e{k}"]  == k+1 for k in K), name = "ct.route_endVehicleLabel")
    
    if HET==False and  MULTI_TRANS==False and symm==False and "Ghilas" not in filename:
    
        model.addConstrs((bl[i]  == int(i.split(".")[1])+1 for n in TS_loc for i in TS_loc[n]), name = "ct.route_transferVehicleLabel")

    
    #model.addConstrs((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j] for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.vehicleLabelFlowA")
        
    #model.addConstrs((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]  for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.vehicleLabelFlowB")
    #"""
    covered = set()
    for i in V:
        for j in [a[1] for a in A.select(i,'*')]:
            if (j,i) in arcs:
               # if (i,j) not in covered:
                    #covered.add((i,j))
                    #covered.add((j,i))
                    model.addConstr(( bl[i]-bl[j] <= ((len(K)-1)*(1-x[i,j]-x[j,i]))), name = "ct.vehicleLabelFlowLifted")
            else:
                model.addConstr((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j]), name = "ct.vehicleLabelFlowA")
                model.addConstr((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]), name = "ct.vehicleLabelFlowB")#"""
    
    """
    Vehicle flow, for each vehicle one
    """
    #model.addConstrs((b[f"o{k}", k]  == 1 for k in K), name = "ct.route_startVehicleFlow")
    #model.addConstrs((b[i,k] <= quicksum(x[i,j] for j in [a[1] for a in A.select(i,'*')]) for k in K for i in V-VD), name = "ct.GoodsFlowLink")
    #model.addConstrs((b[i,k] <= quicksum(x[j,i] for j in [a[0] for a in A.select('*',i)]) for k in K for i in VD), name = "ct.GoodsFlowLink")
    #model.addConstrs((b[i,k] <= b[j,k]+(1- x[i,j]) for k in K for i in V-VD for j in [a[1] for a in A.select(i,'*')]), name = "ct.GoodsFlowConversion")
    #model.addConstrs((b[j,k] <= 0 for k in K for j in VD if int(j[1])!=k), name = "ct.NoGoodsInFinalDepot")

    
    ###
    ###
    #BinaryFLow Variant
    ###
    """
    model.addConstrs((quicksum(bl[f"o{k}", j,k] for j in [a[1] for a in A.select(f"o{k}",'*')]) == 1 for k in K), name = "ct.route_startVehicleFlow")

    model.addConstrs((quicksum(bl[vo, j,k] for j in [a[1] for a in A.select(vo,'*')]) == quicksum(bl[j, vo.replace("o","e"),k] for j in [a[0] for a in A.select('*',vo.replace("o","e"))]) for vo in VO for k in K), name = "ct.VehicleStartArcEqEndFlow")

    model.addConstrs((bl[i,j,k] <= x[i,j] for i in V-VD for j in [a[1] for a in A.select(i,'*')] for k in K), name = "ct.VehicleFlowArcLink")

    model.addConstrs((quicksum(bl[j,i,k] for j in [a[0] for a in A.select('*',i)]) == quicksum(bl[i,j,k] for j in [a[1] for a in A.select(i,'*')]) for k in K for i in P|D|TS|TF), name = "ct.VehicleFlowConversion")
    model.addConstrs((quicksum(bl[j,i,k] for j in [a[0] for a in A.select('*',i)] if k !=int(i.split(".")[1]) )  == 0 for n in TS_loc for i in TS_loc[n] for k in K), name = "ct.route_transferVehicleLabel")
    """

    ###
    #FLow Variant
    ###
    """
    model.addConstrs((quicksum(b[f"o{k}", j] for j in [a[1] for a in A.select(f"o{k}",'*')]) == k for k in K), name = "ct.route_startVehicleFlow")
    model.addConstrs((quicksum(b[j,f"e{k}"] for j in [a[0] for a in A.select('*',f"e{k}")]) == k for k in K), name = "ct.route_endVehicleFlow")
    model.addConstrs((quicksum(b[j,i] for j in [a[0] for a in A.select('*',i)])  <= int(i.split(".")[1])*quicksum(x[j,i] for j in [a[0] for a in A.select('*',i)]) for n in TS_loc for i in TS_loc[n]), name = "ct.route_transferVehicleLabel")
    model.addConstrs((quicksum(b[j,i] for j in [a[0] for a in A.select('*',i)])  >= int(i.split(".")[1])*quicksum(x[j,i] for j in [a[0] for a in A.select('*',i)]) for n in TS_loc for i in TS_loc[n]), name = "ct.route_transferVehicleLabel")


    #model.addConstrs((quicksum(b[vo, j] for j in [a[1] for a in A.select(vo,'*')]) == quicksum(b[j, vo.replace("o","e")] for j in [a[0] for a in A.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.VehicleStartArcEqEndFlow")

    model.addConstrs((b[i,j] <= x[i,j]*(len(K)-1) for i,j in A if j not in TS), name = "ct.VehicleFlowArcLink")

    model.addConstrs((quicksum(b[j,i] for j in [a[0] for a in A.select('*',i)]) == quicksum(b[i,j] for j in [a[1] for a in A.select(i,'*')])   for i in P|D|TS|TF), name = "ct.VehicleFlowConversion")
    """

    """
    Time continuation
    """
    #model.addConstrs(z[i]==0 for i in VO)
    
 
    for (i,j) in A:
        if j not in TS|TF:
            model.addConstr((z[i]+t[i,j]+service_time[j]-Mij[i,j]*(1-x[i,j])<= z[j]), name = "ct.time_flow")
        else:
            _, r, _temp = j.split(".")
            r = int(r)
            if "s" in j:
                l = j.replace("s","f")
            else:
                l = j.replace("f","s")
            model.addConstr((z[i]+t[i,j]+service_time[j]*y[j,l,r]+service_time[l]*y[l,j,r]-Mij[i,j]*(1-x[i,j])<= z[j]), name = "ct.time_flow")

    #for i in TS:
     #   model.addConstr(alph[i]>=y[i,i.replace("s","f"),int(i.split(".")[1])])
    #for i in TF:
     #   model.addConstr(alph[i]>=y[i,i.replace("f","s"),int(i.split(".")[1])])
    
    for n in TS_loc:
        model.addConstr(quicksum(y[i,i.replace("s","f"),r] for i in TS_loc[n] for r in [int(i.split(".")[1])])>=quicksum(y[i.replace("s","f"),i,r] for i in TS_loc[n] for r in [int(i.split(".")[1])]))
    for i in TS:
        _, req, node_idx = i.split(".")
        req = int(req)
        node_idx = int(node_idx)
        model.addConstr(quicksum(x[i,j] for j in [a[1] for a in A.select(i,'*')]) <=y[i,i.replace("s","f"),req]+y[i.replace("s","f"),i,req])

        for j in TS_loc[node_idx]:
            if (i,j) in A:
                _, req2, node_idx2 = j.split(".")
                req2 = int(req2)
                if req2<req:
                    model.addConstr(x[i,j] <= y[i,i.replace("s","f"),req]+y[j,j.replace("s","f"),req2] )#alph[i]+alph[j])
                    model.addConstr(x[i,j] <= 2-y[i,i.replace("s","f"),req]-y[j,j.replace("s","f"),req2] )
    for i in TF:
        _, req, node_idx = i.split(".")
        req = int(req)
        node_idx = int(node_idx)
        model.addConstr(quicksum(x[i,j] for j in [a[1] for a in A.select(i,'*')]) <=y[i,i.replace("f","s"),req]+y[i.replace("f","s"),i,req])
        for j in TF_loc[node_idx]:
            if (i,j) in A:
                _, req2, node_idx2 = j.split(".")
                req2 = int(req2)
                if req2<req:
                    model.addConstr(x[i,j] <= y[i,i.replace("f","s"),req]+y[j,j.replace("f","s"),req2])#alph[i]+alph[j])
                    model.addConstr(x[i,j] <= 2-y[i,i.replace("f","s"),req]-y[j,j.replace("f","s"),req2])#2-alph[i]-alph[j])
    #"""
    #model.addConstr(y["ts.3.0","tf.3.0",3]==1)
    #model.addConstrs((bz[i]+c[i,j]-(Mij[i,j])*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A.select(i,'*')] ), name = "ct.time_flow")
    #"""
    #for e in [('o3', 'p18'), ('o5', 'p11'), ('o1', 'p5'), ('o2', 'p12'), ('o4', 'p3'), ('o6', 'p17'), ('o0', 'p1'), ('o7', 'e7'), ('p18', 'p2'), ('p14', 'd4'), ('p8', 'd8'), ('p0', 'd0'), ('p13', 'd13'), ('p16', 'd16'), ('p15', 'd6'), ('p12', 'p9'), ('p4', 'p8'), ('p5', 'p10'), ('p9', 'p19'), ('p10', 'd5'), ('p19', 'd19'), ('p3', 'p4'), ('p2', 'd2'), ('p6', 'd9'), ('p1', 'd1'), ('p7', 'ts.7.1'), ('p17', 'd17'), ('p11', 'd11'), ('d14', 'e1'), ('d12', 'p6'), ('d19', 'd12'), ('d13', 'p16'), ('d11', 'e5'), ('d0', 'e6'), ('d2', 'd18'), ('d7', 'e4'), ('d6', 'd15'), ('d4', 'tf.3.1'), ('d3', 'd14'), ('d18', 'e3'), ('d1', 'p13'), ('d9', 'p15'), ('d5', 'd10'), ('d10', 'p7'), ('d15', 'e2'), ('d16', 'e0'), ('d17', 'p0'), ('d8', 'p14'), ('ts.7.1', 'ts.3.1'), ('ts.3.1', 'ts.14.1'), ('ts.14.1', 'd3'), ('tf.7.1', 'd7'), ('tf.14.1', 'tf.7.1'), ('tf.3.1', 'tf.14.1')]:
            #model.addConstr(x[e]==1)#"""
    """
    Lifted version, benefit unclear. Needs testing!
    """
    #model.addConstrs((bz[i]+t[i,j]-(Mij[i,j])*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) not in A), name = "ct.time_flowA")
    
    #model.addConstrs((bz[i]-z[j]+Mij[i,j]*x[i,j]+(Mij[i,j]-service_time[i]-t[i,j]+min(-t[j,i]-service_time[j],timeWindows[j][0]-timeWindows[i][1]))*x[j,i]<= Mij[i,j]-t[i,j]-service_time[i]  for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) in A), name = "ct.time_flowLifted")
    
    
    #model.addConstrs((z[i]+service_time[i] <= bz[i] for i in V-(VO|TS|TF)), name='ct.DepartureA')
    


    
    
    """
    Request Transfer Time
    """
    model.addConstrs((z[i] -(Mij[i,j]+service_time[i])*(1-y[i,j,r])<= z[j] for i in TS for j in [i.replace("s","f")] for r in [int(i.split(".")[1])]), name = "ct.transferTimeWait")

    model.addConstrs((z[i] -(Mij[i,j]+service_time[i])*(1-y[i,j,r])<= z[j] for i in TF for j in [i.replace("f","s")] for r in [int(i.split(".")[1])]), name = "ct.transferTimeWait")
        
   

    """
    Transfer location open
    """
    model.addConstrs((1 >= x[i,j] for i in TS for j in [a[1] for a in A.select(i,'*')]), name = "ct.TransferVITS")

    model.addConstrs((1 >= x[i,j] for i in TF for j in [a[1] for a in A.select(i,'*')]), name = "ct.TransferVITF")

    model.addConstrs((f[f"ts{n}"] >= quicksum(x[i,j] for j in [a[1] for a in A.select(i,'*')]) for n in TS_loc for i in TS_loc[n]), name = "ct.TransferFlowLink")
    model.addConstrs((f[f"ts{n}"] <= quicksum(y[i,j,r] for r in R for i in TS_loc[n] for j in [a[1] for a in Ay.select(i,'*',r) if a[1].replace("f","s")!=i]) for n in TS_loc), name = "ct.TransferRequestFlowLink")
    
    model.addConstrs((2*f[f"ts{n}"] <= quicksum(x[j,i] for i in TS_loc[n] for j in [a[0] for a in A.select('*',i)]) for n in TS_loc), name = "ct.AtLeastTwoVehicles")


    """
    Time Windows
    """
    model.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliest")
    #model.addConstrs((x[o,i]*c[o,i] <= z[i] for i in V-VO for o in VO if (o,i) in A), name="ct.timeWindowEarliest")
    #model.addConstrs((min(max(timeWindows[f"e{k}"][1]-c[i,f"e{k}"] for k in K),timeWindows[i][1]) >= bz[i] for i in V-VD), name="ct.TimeWindowLatest")
    model.addConstrs((timeWindows[i][1] >= z[i]-service_time[i] for i in V), name="ct.TimeWindowLatestVD")
    #model.addConstrs((timeWindows[i][0] <= a[i,r] for r in R for i in TS), name="ct.RtimeWindowEarliest")
    #model.addConstrs((timeWindows[i][1] >= a[i,r] for r in R for i in TS), name="ct.RTimeWindowLatest")
    
    #model.addConstrs((min([max(timeWindows[i][0],c[f"o{k}",i]) for k in K]) <= z[i] for i in V-VO), name="ct.timeWindowEarliestbVO")
    #model.addConstrs((timeWindows[i][0] <= z[i] for i in VO), name="ct.timeWindowEarliestb")

    #model.addConstrs((timeWindows[i][1] >= bz[i] for i in V), name="ct.TimeWindowLatestb")
    #model.addConstrs((timeWindows[i][0] <= ba[i,r] for r in R for i in TF), name="ct.RtimeWindowEarliestb")
    #model.addConstrs((timeWindows[i][1] >= ba[i,r] for r in R for i in TF), name="ct.RTimeWindowLatestb")
    
    

            
    
    # Data for callback
    model._obj = None
    model._bd = None
    model._gap = None
    model._data = []
    model._x = x
    model._y = y
    
    model._f = f
    model._VO = VO
    model._A = A
    model._TS = TS
    model._TS_pure = TS_pure
    model._TS_loc = TS_loc
    model._P = P
    model._VD = VD
    model._D = D
    model._start = time.time()
    model._cuts = []
    model = add_cuts(model)
    #model.Params.LazyConstraints = 1
    #model.Params.Symmetry = 0
    
    """
    sol_start, pdpm = solve_pdptw()
    x = model._x
    model.NumStart = 1
    model.update()
    
    # iterate over all MIP starts
    for s in range(model.NumStart):
      
      # set StartNumber
      model.params.StartNumber = s
    
      # now set MIP start values using the Start attribute, e.g.:
      for idx in sol_start:
          model._x[idx].Start = 1.0
          """
    model.Params.TimeLimit = 60*60
    model.Params.Threads = 16
    #model.Params.NodeLimit = 0
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
    #model.Params.Presolve = 0
    model._lazy_calls = 0
    model._lazy_cuts = 0
    if seed!=None:
        model.Params.Seed=seed
    model.update()
    #model.write("correct_model.lp")
    
    if HET or MULTI_TRANS:
        model.optimize()
        #model.Params.LazyConstraints = 1
        
        #model.optimize(callback=callback_het)
    elif symm==True:
        model.Params.LazyConstraints = 1
        
        model.optimize(callback=callback_symm)
    else:
        
        model.optimize()
    #model.optimize(callback=usercut_cb)
    # model.optimize()
    # model.computeIIS()
    #
    #"""
    
    
    #if model.status==3:
        #model.computeIIS()
        #model.write("infeasible_model.ilp")#"""
    #lb = compute_LP_relax_bound(model)
    #opt = model.ObjVal
    #ratio = 100 * lb / opt
    
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
        plt.scatter(df.loc[df['node'].str.contains('ts'),'x'].values, df.loc[df['node'].str.contains('ts'),'y'].values, s=50, facecolor='blue', marker='D')
        # plt.scatter(df.loc[df['node'].str.contains('tf'),'x'].values, df.loc[df['node'].str.contains('tf'),'y'].values, s=50, facecolor='blue', marker='D')
        
        for xi, yi, text in zip(df['x'].values, df['y'].values, df['node'].values):
            if "t" in text:
                text = text.split(".")[0]+text.split(".")[2]
            if "tf" in text:
                continue
            plt.annotate(text, xy=(xi, yi), xycoords='data', xytext=(5, 5), textcoords='offset points')
        xResult = pd.DataFrame(x.keys(), columns=["i","j"])
        xResult["value"]=model.getAttr("X", x).values()
        plt.xlabel("x-Koordinaten")
        plt.ylabel("y-Koordinaten")
        
        for index, row in xResult.iterrows():
            if row["value"] > 1e-5:
                x1 = df.loc[df['node'] == row["i"], 'x'].values
                y1 = df.loc[df['node'] == row["i"], 'y'].values
                x2 = df.loc[df['node'] == row["j"], 'x'].values
                y2 = df.loc[df['node'] == row["j"], 'y'].values
                plt.plot([x1, x2], [y1, y2], 'gray', linestyle="--")
        plt.show()
        return xResult
    
    def plotArcs(arcs):
        fig, axes = plt.subplots()
        
        plt.scatter(df.loc[df['node'].str.contains('p'),'x'].values, df.loc[df['node'].str.contains('p'),'y'].values, s=50, facecolor='red', marker='o')
        plt.scatter(df.loc[df['node'].str.contains('d'),'x'].values, df.loc[df['node'].str.contains('d'),'y'].values, s=50, facecolor='green', marker='o')
        plt.scatter(df.loc[df['node'].str.contains('o'),'x'].values, df.loc[df['node'].str.contains('o'),'y'].values, s=50, facecolor='red', marker='s')
        plt.scatter(df.loc[df['node'].str.contains('e'),'x'].values, df.loc[df['node'].str.contains('e'),'y'].values, s=50, facecolor='green', marker='s')
        plt.scatter(df.loc[df['node'].str.contains('ts'),'x'].values, df.loc[df['node'].str.contains('ts'),'y'].values, s=50, facecolor='blue', marker='D')
        
        for (i,j) in arcs:
            x1 = df.loc[df['node'] == i, 'x'].values
            y1 = df.loc[df['node'] == i, 'y'].values
            x2 = df.loc[df['node'] == j, 'x'].values
            y2 = df.loc[df['node'] == j, 'y'].values
            plt.plot([x1, x2], [y1, y2], 'gray', linestyle="--")
            

        plt.show()
        
    def get_tour(arcs):
        tours = []
        for a in arcs:
            if a[0] in VO:
                curr_node = a[1]
                tour = [a]
                start = a[0]
                while "e" not in curr_node:
                    for (i,j) in arcs:
                        if i==curr_node:
                          tour.append((i,j))
                          curr_node = j
                          break
                print(tour)
                tours.append(tour)
        return tours    
    
        
    def check_tours(model):
        arcsx = [a for a in model._x if model._x[a].x>0.5]
        arcsy = {a:1.0 for a in model._y if model._y[a].x>0.5}
        tours = get_tour(arcsx)
        error_msg = ""
        error = False
        
        for tour in tours:
            q_list = []
            q_val = 0
            z_val = 0.0
            for u,v in tour:
                q_val = sum(q[r]*arcsy.get((u,v,r),0) for r in range(nRequests))
                q_list.append(q_val)
                if VC<0:
                    Q_vehicle = Qmax-model._vl[v].x
                    z_val = max(z_val+c[u,v]+service_time[u],timeWindows[v][0])
                else:
                    Q_vehicle = VC
                    z_val = max(z_val+c[u,v]+service_time[u],timeWindows[v][0])
                if q_val>Q_vehicle:
                    error_msg+=f"capacity violation:{q_val},{Q_vehicle},{v},{tour}"
                    print(error_msg)
                    error = True
                if VC>0:
                    if z_val+service_time[v]-pow(10,-4)>timeWindows[v][1]:
                        error_msg+=f"violation of time windows: {v},{z_val}>{timeWindows[v][1]}"
                        error = True
                else:
                    if z_val-pow(10,-4)>timeWindows[v][1]:
                        error_msg+=f"violation of time windows: {v},{z_val}>{timeWindows[v][1]}"
                        error = True
            if q_val>0:
                error_msg+=f"precedence violation: {tour}"
                error = True
            print(tour)
            print(Q_vehicle,q_list)
        return error, error_msg
             
        
    #plotGap(model._data)
    # plotArcs(arcs)
    
    vehicle_number = -1
    
    sol_transfers = 0
    sol_req_trans = 0
    vehicle_empty = 0
    if model.Status == GRB.OPTIMAL:
        
        xarcs = plotLocation(df)
        sol_check, error_msg = check_tours(model)
        #error_msg = ratio
        vehicle_number = sum(model._x[i, j].x for o in model._VO for (i,j) in model._A.select(o,"*") if j not in model._VD)
        with open(f"{filename.replace('.txt','')}_sol.txt", "w") as output:
            output.write(str([a for a in x if x[a].x>0.5]))
        sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
        sol_req_trans = quicksum(y[i,j,r] for i in TS|TF for j in TF|TS if (i,j) in Ay).getValue()

        infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sol_transfers,sol_req_trans,vehicle_number,error_msg,vehicle_empty ]  
        #for e in range(nSolutions):
        for iter2 in range(1):
                model.setParam(GRB.Param.SolutionNumber, iter2)
                print('%g ' % model.PoolObjVal, end='\n')
                for v in model.getVars():
                     if v.xn > 1e-5:
                         #if "d16" in v.varName or "d10" in v.varName:
                           #print ('%s %g' % (v.varName, v.xn))
                           print ('%s %g' % (v.varName, v.xn))
                print("\n")
        print("\n")
        """
        print(Mij["d10","d16"])
        print(Mij["d16","d10"])
        print(t["d10","d16"])
        print(t["d16","d10"])
        print(timeWindows["d16"])
        print(timeWindows["d10"])"""
        
    elif model.Status == GRB.TIME_LIMIT or model.Status==8:
        if model.SolCount == 0:
            sol_transfers = None
            error_msg = ""#ratio
            infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sol_transfers,sol_req_trans,vehicle_number,error_msg,vehicle_empty ]      
        else:
            xarcs = plotLocation(df)
            sol_check, error_msg = check_tours(model)
            #error_msg = ratio
            vehicle_number = sum(model._x[i, j].x for o in model._VO for (i,j) in model._A.select(o,"*") if j not in model._VD)
            with open(f"{filename.replace('.txt','')}_sol.txt", "w") as output:
                output.write(str([a for a in x if x[a].x>0.5]))
            sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
            sol_req_trans = quicksum(y[i,j,r] for i in TS|TF for j in TF|TS if (i,j) in Ay).getValue()
            infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sol_transfers,sol_req_trans,vehicle_number,error_msg,vehicle_empty ]      
    else:
        infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),"inf","inf" ,model.ObjBound, model.Runtime,sol_transfers,sol_req_trans,vehicle_number,error_msg,vehicle_empty]
    #infos.append(model._lazy_cuts)
    print(model._cuts)
    return infos#, model._cuts

info = twoIndexModel(filename)
#print(info)
"""
for i in range(100):
    info, cuts = twoIndexModel(filename,seed=i)
    if len(cuts)>0 and info[3]>310:
        print(f"cut was added! seed: {i}")
        break"""
#csvIndex = ['Instace name','model','Status', 'Obj.Value','MIPGap','Obj. Bound', 't(s)','used_transfer_stations']
#resultDf = pd.DataFrame([info])
#resultDf.to_csv("result_VehicleFlow.csv",mode='a', encoding='utf-8', index=False)