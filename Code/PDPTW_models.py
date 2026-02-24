# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 15:28:30 2025

@author: un_po
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import networkx as nx
import threading


import gurobipy as gp
from gurobipy import Model, GRB, quicksum, tuplelist


filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R5-K3-T3/PDPT-R5-K3-T3-Q100-2.txt"
#filename = "./InstancesLyu23/PDPTWT/3R4K4T/3R-4K-4T-180L-3.txt"

#filename = "./InstancesSartori/n100/bar-n100-1.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R30-K2-T2/PDPT-R30-K2-T2-Q100-1.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R7-K3-T3/PDPT-R7-K3-T3-Q100-6.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-0.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R5-K3-T3/PDPT-R5-K3-T3-Q100-5.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R10-K3-T3/PDPT-R10-K3-T3-Q100-2.txt"
filename = "./InstancesLyu23/PDPT_small/PDPT-R12-K2-T2/PDPT-R12-K2-T2-Q100-4.txt"
filename = "./InstancesLyu23/PDPT_small/PDPT-R5-K2-T2/PDPT-R5-K2-T2-Q100-7.txt"
filename = "./InstancesLyu23/PDPT_small/PDPT-R15-K3-T3/PDPT-R15-K3-T3-Q100-9.txt"
filename = "./InstancesLyu23/PDPT_small/PDPT-R12-K2-T2/PDPT-R12-K2-T2-Q100-4.txt"


filename = "./InstancesFurtado/AA15.txt"
filename = "./Instances-PDPTW-BCP-DataSet1/BB45"
#filename = "./Instances_DARP_BCP_EventBased/a4-32.txt"
#filename = "./Instances_DARP_BCP_EventBased/a3-18.txt"

filename = "./InstancesLiLim/PDPTWT10/PDPTWT_LiLim_R10K25T0C200_lc101.txt"

filename ="./InstancesLyu23/PDPT_small/PDPT-R12-K3-T3/PDPT-R12-K3-T3-Q100-4.txt"

filename = "./Instances-PDPTW-BCP-DataSet1/CC30"

filename = "./InstancesLiLim/PDPTWT10/PDPTWT_LiLim_R10K25T0C50_lr101.txt"
filename = "./Instances-PDPTW-BCP-DataSet1/AA75"


#filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"



global_vehicle_lb = None

global_infos = []

LIFTED=True


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
    if "Furtado" not in filename:
        df = pd.read_csv(filename, skiprows=3, sep='\t')
    if "Lim" in filename:
        df = df.astype({
            'node': str,
            'x': float,
            'y': float,
            'load': int,
            's':int,
            'a': int,
            'b': int
        })
    else:
        df = df.astype({
            'node': str,
            'x': float,
            'y': float,
            'load': int,
            'a': int,
            'b': int
        })
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



# Generate dictionary of (node:load)
def loadDict(df):
    matrix = {}
    for location in df["node"]:
        matrix[location] = df.loc[df["node"]==location, 'load'].values[0]
    return matrix

# Get the list of grouped nodes
def calculateDistance(x1, x2, y1, y2, precision=False):
    if precision==True:
        return float(np.round(math.sqrt((x2 - x1)**2 + (y2-y1)**2),2))
    return math.sqrt((x2 - x1)**2 + (y2-y1)**2)

# one unit of distance can be traveled in one time unit
def distancesMatrix(df, furtado=False):
    matrix = {}
    for location1 in df["node"]:
        for location2 in df["node"]:
            if location1 != location2:
                x1 = df.loc[df["node"]==location1, 'x'].values[0]
                x2 = df.loc[df["node"]==location2, 'x'].values[0]
                y1 = df.loc[df["node"]==location1, 'y'].values[0]
                y2 = df.loc[df["node"]==location2, 'y'].values[0]
                if furtado==True:
                    matrix[location1,location2] = calculateDistance(x1, x2, y1, y2, precision=True)
                else:
                    matrix[location1,location2] = calculateDistance(x1, x2, y1, y2)
    return matrix


def write_furtado_instances(file_path):

    # Parse metadata
    with open(file_path, 'r') as file:
            lines = file.readlines()

    # Parse node data
    for size in range(5,30,5):
        with open(file_path[:-2]+str(size), 'a') as file:
            meta_line = lines[0].strip().split()
            meta_line[1]=str(size)
            meta_line.append("\n")
            file.write('  '.join(meta_line))
            for line in lines[1:2+size]:
                file.write(line)
            n = 1+size
            for line in lines[2+30:30+2+size]:
                line = line.strip().split()
                line[0] = str(n)
                line.append("\n")
                file.write('  '.join(line))
                n+=1
            last_line = lines[1].strip().split()
            last_line[0] = str(n)
            file.write('  '.join(last_line))
    
    
def cb(model, where):
    if where == GRB.Callback.MIPNODE:
        if model._cut == False:
            global global_vehicle_lb 
            if global_vehicle_lb!=None:
                print("vehicle cut = ",global_vehicle_lb)
                model.cbCut(quicksum(model._x["o0", j] for j in [a[1] for a in model._A2.select("o0",'*')]) == global_vehicle_lb)
                model._cut = True


def read_furtado(file_path, furtado=True):

    # Parse metadata
    instance_name= filename.split("/")[-1]
    with open(file_path, 'r') as file:
            lines = file.readlines()
    if furtado==True:
        meta_line = lines[0].strip().split('\t')
        meta = {meta_line[i]: int(meta_line[i + 1]) for i in range(0, len(meta_line), 2)}
        nRequests, Q, nVehicles = meta['n'], meta['Q'], meta['r_mod']
    else:
        meta_line = lines[0].strip().split()
        if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
            nRequests = int(float(meta_line[1])/2)
            nVehicles = int(meta_line[0])
            Lmax = int(meta_line[4])
        else:
            nRequests = int(meta_line[1])
            nVehicles = -1
        Q = int(meta_line[3])
        
    
    metaData = {"nr":nRequests,"capacity":Q,"nv":nVehicles,"nt":0}
    if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
        metaData["lmax"]=Lmax
    
    # Parse node data
    data_lines = lines[1:]
    columns = ['node', 'x', 'y', 's', 'load', 'a', 'b']
    if furtado==True:
        data = [line.split('\t') for line in data_lines]
    else:
        data = [line.split() for line in data_lines]
    df = pd.DataFrame(data, columns=columns)
    
    # Convert columns to correct types
    df = df.astype({
        'node': int,
        'x': float,
        'y': float,
        's': float,
        'load': int,
        'a': int,
        'b': int
    })
    

    
    # Rename node_id column according to your mapping scheme
    def rename_node(node_id):
        if node_id == 0:
            return "o0"  # Origin depot
        elif 1 <= node_id <= nRequests:
            return f"p{node_id-1}"  # Pickup nodes
        elif nRequests+1 <= node_id <= 2*nRequests:
            return f"d{node_id - nRequests - 1}"  # Delivery nodes
        else:
            return f"unknown{node_id}"
    
    df['node'] = df['node'].apply(rename_node)
    if furtado==True:
        depot_row = df.iloc[0].copy()
        depot_row["node"] = "e0"
        df = pd.concat([df, pd.DataFrame([depot_row])], ignore_index=True)
    else:
        df.loc[df.index[-1], 'node'] = "e0"
        
    # Show DataFrame
    #print(df)
    return metaData,df



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


def read_sartori(file_path):    
    # Initialize variables
    capacity = None
    nodes_data = []
    distance_matrix = []
    
    # Read the file and process it
    with open(file_path, 'r') as file:
        lines = file.readlines()
        processing_nodes = False
        processing_edges = False
        
        for line in lines:
            line = line.strip()
            if line.startswith("CAPACITY:"):
                capacity = int(line.split(":")[1].strip())
            elif line == "NODES":
                processing_nodes = True
            elif line == "EDGES":
                processing_nodes = False
                processing_edges = True
            elif processing_nodes and line:
                # Extract nodes data
                nodes_data.append(line.split())
            elif processing_edges and line:
                # Extract edges into a dictionary format
                try:
                    parts = list(map(int, line.split()))
                    distance_matrix.append(parts)
                except ValueError:
                    continue  # Skip invalid lines
    
    distance_matrix = np.array(distance_matrix)
    
    distance_matrix = {(i, j): distance_matrix[i, j] for i in range(distance_matrix.shape[0]) for j in range(distance_matrix.shape[1])}
    # Create a DataFrame for nodes and rename the indices
    columns = ["node", "x", "y", "load", "a", "b", "serviceTime", "Pickup", "Delivery"]
    nodes_df = pd.DataFrame(nodes_data, columns=columns)
    nodes_df["node"] = nodes_df["node"].astype(int)
    nodes_df["x"] = nodes_df["x"].astype(float)
    nodes_df["y"] = nodes_df["y"].astype(float)
    nodes_df["load"] = nodes_df["load"].astype(int)
    nodes_df["a"] = nodes_df["a"].astype(int)
    nodes_df["b"] = nodes_df["b"].astype(int)
    nodes_df["serviceTime"] = nodes_df["serviceTime"].astype(int)
    #nodes_df.set_index("node", inplace=True)
    
    # Rename nodes
    size = len(nodes_df)
    split_index = (size - 1) // 2
    
    new_indices = []
    for idx in nodes_df.node:
        if idx == 0:  # Depot
            new_indices.append("o0")
        elif 1 <= idx <= split_index:  # Pickup nodes
            new_indices.append(f"p{idx-1}")
        else:  # Delivery nodes
            pickup_id = idx - split_index
            new_indices.append(f"d{pickup_id-1}")
    
    nodes_df.node = new_indices
    
    # Rename the distance matrix
    renamed_distance_matrix = {}
    
    for (source, target), distance in distance_matrix.items():
        # Rename source node
        if source == 0:
            renamed_source = "o0"
        elif 1 <= source <= split_index:
            renamed_source = f"p{source-1}"
        else:
            renamed_source = f"d{source - split_index-1}"
    
        if target == 0:
            renamed_target = "o0"
        elif 1 <= target <= split_index:
            renamed_target = f"p{target-1}"
        else:
            renamed_target = f"d{target - split_index-1}"

    
        renamed_distance_matrix[renamed_source,renamed_target] = int(distance)
    
    # Results
    metaData = {"capacity":capacity,
                "nr":(size - 1) // 2,
                "nv": None,
                "nt": 0}
    # Add "e0" to the DataFrame
    node_0_data = nodes_df.loc[0].copy()  # Copy the data of "Node_0"
    node_0_data.node = "e0"
    nodes_df.loc[size+1] = node_0_data  # Add "e0" to the DataFrame

    
    # Add "e0" as a target to other nodes, copying distances from "Node_0"
    new_entries = {}
    for (source, target),distance in list(renamed_distance_matrix.items()):
        source_temp = None
        target_temp = None
        if "o0" in source:
            source_temp = "o0"
            target_temp = target
        if "o0" in target:
            target_temp = "e0"
            if source_temp==None:
                source_temp = source
        if source_temp != None:
            renamed_distance_matrix[source_temp,target_temp] = distance
            

    return metaData, nodes_df, renamed_distance_matrix


    

# Model
def pdptw_model(filename, root=False,rais=True, edges_cut = None, strCap=False,timeFlow=False, dahle=False, letchford=False, solve_RC=False):
    
        print(filename)
        instance_name= filename.split("/")[-1]
        #write_furtado_instances(filename)
        if "Sartori" in filename:
            metaData, df, dist = read_sartori(filename)
            K = [0]
        elif "Furtado" in filename:
            metaData, df = read_furtado(filename)
            K = [0]
            nVehicles = int(metaData['nv'])
        elif "BCP" in filename:
            metaData, df = read_furtado(filename, furtado=False)
            K = [0]
            nVehicles = -1
        else:
            metaData = readMetaData(filename)
            df = readDataframe(filename)
        nodeList = getNodeList(df)

        
        V =  nodeList["V"]
        P = nodeList["P"]
        D = nodeList["D"]
        VO = nodeList["vo"]
        VD = nodeList["vd"]
        if "Sartori" not in filename and "Furtado" not in filename and "BCP" not in filename:
            nVehicles = int(metaData['nv'])
            K = list(range(nVehicles))
        
        if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
            nVehicles = int(metaData['nv'])
            
                
        if "Li" in filename:
            K = [0]
            nVehicles = -1
            
        nRequests = int(metaData['nr'])
        
        nTransports = int(metaData['nt'])
        VC = int(metaData['capacity'])
        
        
        df["points"] = df[["x","y"]].values.tolist()
        
        points = df.set_index("node")["points"].to_dict()
        
        qnode = df.set_index('node')["load"].to_dict()
        q = {int(node.replace("p","")):qnode[node] for node in P}
        
        timeHorizon = df["a"].max()
        
        df["tw"] = df[["a","b"]].values.tolist()
        
        timeWindows = df.set_index('node')["tw"].to_dict()        
        
        if "Sartori" in filename:
            c = dist
            service_time = df.set_index('node')["serviceTime"].to_dict()
            k = [0]
        else:
            if "Furtado" in filename or "BCP" in filename:
                c = distancesMatrix(df,furtado=True)
            else:
                c = distancesMatrix(df)
            k = pd.RangeIndex(nVehicles)
            
        
        
        if VC<0:
            service_time = pd.Series(df.s.values,index=df.node).to_dict()
            node_capacities = pd.Series(df.vcap.values,index=df.node).to_dict()
            vec_capacities = {}
            for node in node_capacities:
                if node_capacities[node]>0:
                    vec_capacities[int(node.replace("o","").replace("e",""))] = node_capacities[node]
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
            if "Furtado" in filename or "BCP" in filename:
                service_time = pd.Series(df.s.values,index=df.node).to_dict()
            else:
                service_time = {s:0 for s in V}
        
        R = list(range(nRequests))
        
        
        def time_window_reduction_rules(l,rule):
            #min arrival time predecessors
            if rule==1:
                twa = timeWindows[l][0]
                if l in P:
                    predset = P|D|VO
                if l in VD:
                    predset = D
                if l in D:
                    predset = P|D
                timeWindows[l][0] = float(np.round(max(timeWindows[l][0], min(timeWindows[l][1],min(timeWindows[i][0]+c[i,l]+service_time[i] for i in predset if l!=i))),2))
                if twa<timeWindows[l][0]:
                    return True
                else:
                    return False
            #min arrival time successors
            if rule==2:
                twa = timeWindows[l][0]
                if l in P:
                    succset = P|D
                if l in VO:
                    succset = P
                if l in D:
                    succset = VD|P|D-set(l.replace("d","p"))
                timeWindows[l][0] = float(np.round(max(timeWindows[l][0], min(timeWindows[l][1],min(timeWindows[i][0]-c[l,i]-service_time[l] for i in succset if l!=i))),2))
                if twa<timeWindows[l][0]:
                    return True
                else:
                    return False
            #max departure from pred
            if rule==3:
                twb = timeWindows[l][1]
                if l in P:
                    predset = P|D
                if l in VD:
                    predset = D
                if l in D:
                    predset = P|D
                timeWindows[l][1] = float(np.round(min(timeWindows[l][1], max(timeWindows[l][0],max(timeWindows[i][1]+c[i,l]+service_time[i] for i in predset if l!=i))),2))
                if twb>timeWindows[l][1]:
                    return True
                else:
                    return False
            #max departure to succ
            if rule==4:
                 twb = timeWindows[l][1]
                 if l in P:
                     succset = P|D
                 if l in VO:
                     succset = P
                 if l in D:
                     succset = VD|P|D-set(l.replace("d","p"))
                 timeWindows[l][1] = float(np.round(min(timeWindows[l][1], max(timeWindows[l][0],max(timeWindows[i][1]-c[l,i]-service_time[i] for i in succset if l!=i))),2))
                 if twb>timeWindows[l][1]:
                     return True
                 else:
                     return False
            raise ValueError(f"Value {rule} is wrong, it must be 1,2,3 or 4")
        
        def time_window_reduction_loop():
            for i in P|D:
                timeWindows[i][0] = min([max(timeWindows[i][0],timeWindows[f"o{k}"][0]+c[f"o{k}",i]+service_time[f"o{k}"]) for k in K])
                timeWindows[i][1] = min(max(timeWindows[f"e{k}"][1]-c[i,f"e{k}"]-service_time[i] for k in K),timeWindows[i][1])
            changed = True
            while changed==True:
                changed = False
                #min arrival time predecessors
                for l in P|D|VD:
                    if time_window_reduction_rules(l,1)==True:
                        changed = True
                    if time_window_reduction_rules(l,3)==True:
                        changed = True
                for l in P|D:
                    if time_window_reduction_rules(l,2)==True:
                        changed = True
                    if time_window_reduction_rules(l,4)==True:
                        changed = True
        
        #time_window_reduction_loop()
        
        
        #change travel times
        t = c.copy()
        n1 = 0
        for i,j in c:
            if c[i,j]+timeWindows[i][1]+service_time[i]<timeWindows[j][0]:
                #t[i,j] = timeWindows[j][0]-timeWindows[i][1]-service_time[i]
                n1+=1
        print("Increased ",n1, " arcs.")
            
        arcs = []
        for i in VO:
            for j in P:
                if timeWindows[i][0]+t[i,j]+service_time[i]<=timeWindows[j][1]:
                    arcs.append((i,j))
            if "Furtado" not in filename and "BCP" not in filename:
                arcs.append((i, i.replace("o","e")))
        
        for i in P:
            for j in D:
                if i != j:
                    if timeWindows[i][0]+t[i,j]+service_time[i]<=timeWindows[j][1]:
                        if i!=j.replace("d","p"):
                            if qnode[i]+abs(qnode[j])<=VC:
                                    arcs.append((i,j))
                        else:
                            arcs.append((i,j))
                            
            for j in P:
                if i != j:
                    if qnode[i]+qnode[j]<=VC:
                        if timeWindows[i][0]+t[i,j]+service_time[i]<=timeWindows[j][1]:
                            arcs.append((i,j))
                        
                        

        
        for i in D:
            for j in P|VD:
                if not (i == j or (j in P and i == j.replace("p","d"))):
                        if timeWindows[i][0]+t[i,j]+service_time[i]<=timeWindows[j][1]:
                            arcs.append((i,j))
            for j in D:
                if not i==j:
                    if abs(qnode[i])+abs(qnode[j])<=VC:
                        if timeWindows[i][0]+t[i,j]+service_time[i]<=timeWindows[j][1]:
                            arcs.append((i,j))
        
        #eleminate arcs by Cordeau 2006 (DARP paper)
        def check_feasibility(path):
            i = path[0]
            z = max(timeWindows[i][0],c["o0",i])
            for j in path[1:]:
                if (i,j) in arcs:
                    z = max(z+service_time[i]+t[i,j],timeWindows[j][0])
                    if z>timeWindows[j][1]:
                        return False
                    i = j
                else:
                    return False
            return True
        
        remove_arcs = set()
        
        for i in P:
            for j in D:
                if i!=j.replace("d","p"):
                    if (i,j) in arcs:
                        path = (j.replace("d","p"),i,j,i.replace("p","d"))
                        if check_feasibility(path)==False:
                            remove_arcs.add((i,j))
                       
        for i in D:
            for j in P:
                if j!=i.replace("d","p"):
                    if (i,j) in arcs:
                        path = (i.replace("d","p"),i,j,j.replace("p","d"))
                        if check_feasibility(path)==False:
                            remove_arcs.add((i,j))
  
        for i in P:
            for j in P:
                if (i,j) in arcs:
                    path1 = (i,j,i.replace("p","d"),j.replace("p","d"))
                    if check_feasibility(path1)==False:
                        path2 = (i,j,j.replace("p","d"),i.replace("p","d"))
                        if check_feasibility(path2)==False:
                            remove_arcs.add((i,j))
        for i in D:
            for j in D:
                if (i,j) in arcs:
                    path1 = (i.replace("d","p"),j.replace("d","p"),i,j)
                    if check_feasibility(path1)==False:
                        path2 = (j.replace("d","p"),i.replace("d","p"),i,j)
                        if check_feasibility(path2)==False:
                            remove_arcs.add((i,j))
                            
        """
        #remove arcs to predecessors
        for l in P|D|VD:
            for i in V:
                if (l,i) in arcs:
                    if timeWindows[i][1]<timeWindows[l][0]:
                        print(l,i)
                        remove_arcs.add((l,i))"""
        
        print("remove ",len(remove_arcs)," arcs")
        #print(remove_arcs)
        #arcs = set(arcs)-remove_arcs
        arcs = list(dict.fromkeys(arcs))
        if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
            Lmax = metaData["lmax"]
        
        #A = [(i,j) for i in V for j in V if i!=j]
        
        A = tuplelist(arcs)
        
        Ayc = [(i,j,r) for r in R for i in P for j in V-(frozenset((i,f"p{r}"))|VO|VD)]
        Ayd = [(i,j,r) for r in R for i in D-frozenset(("d"+str(r),)) for j in (V-frozenset([i,i.replace("d","p"),f"p{r}"])-VO-VD)]
        
        
        Ay = Ayc+Ayd
          
        
        #print(Ay[('d1', 'p1',1)])
        
        Ay = tuplelist(Ay)
        
        #print(Ay)
        
        #print(Ay)
        
        
        
        
        
        
        
        #xc = df.set_index('node').x.to_dict()
        #yc = df.set_index('node').y.to_dict()
        #c = {(i, j): float(np.hypot(xc[i]-xc[j], yc[i]-yc[j]).round(2)) for i, j in A}

        
        #print(c["tf.0.0","ts.1.0"])
        
        
        r = pd.RangeIndex(nRequests)
        
        
        
        
           
        
        
        
        xIndex = [(i, j) for (i,j) in arcs]
        zIndex = [i for i in V]
        
        
        
            
        print(df)
        
        Mij = {(i,j):max(0,timeWindows[i][1]+t[i,j]+service_time[i]-timeWindows[j][0]) for (i,j) in c}
        M = max(Mij.values())

    
    
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
            
     
            
        def solve_pdptw_rais(filename, timelim, cut=None,last_sol=None, strCap=False, timeFlow=False, callback=False, min_vehicle=False, barrier=None):
            
            
            LIFTED=True
            if timeFlow==True:
                LIFTED = False
            
            
            env=gp.Env()
            model = gp.Model(env=env)
            instance_name= filename.split("/")[-1]
            infostr = ""
            if strCap==True:
                infostr += "StrCap"
            if timeFlow==True:
                infostr +="timeFlow"
            if callback==True:
                infostr += "ParallelModel"
            if LIFTED==True:
                infostr+="LiftedMTZ"
            model = Model('PDPTW_Rais'+infostr)
            arcs_keep = set()
            for i in V-VD-VO:
                edges = A.select(i,"*")
                if i in P and (i,i.replace("p","d")) in A:
                    arcs_keep.add((i,i.replace("p","d")))
                costs = {e:c[e] for e in edges}
                #sort by cost
                costs = sorted(costs.items(), key=lambda x: x[1])
                if cut==None:
                    edges_cut  = int(np.ceil(len(edges)/1))
                else:
                    edges_cut = cut
                #cut = 6
                if len(costs)>2:
                    for edge in dict(costs[:edges_cut]):
                            arcs_keep.add(edge)
                else:
                    for edge in dict(costs):
                            arcs_keep.add(edge)
                        
            for ek in VD:            
                for e in A.select("*",ek):
                        arcs_keep.add(e)
            for ok in VO:            
                for e in A.select(ok,"*"):
                        arcs_keep.add(e)
                        
            A2 = tuplelist(arcs_keep) 
            
            Ay_keep = set()
            for arc in Ay:
                if (arc[0],arc[1]) in arcs_keep:
                    Ay_keep.add(arc)
            
            Ay2 = tuplelist(Ay_keep)
            
            if timeFlow==True:
                zIndex = [(i, j) for (i,j) in arcs]
            else:
                zIndex = [i for i in V]
    
            wbTW = {(i,j):min(timeWindows[i][1],timeWindows[j][1]-c[i,j]-service_time[i]) for (i,j) in arcs}
    
            x = model.addVars(A2, vtype=GRB.BINARY, name='x')
            #y = model.addVars(Ay2,lb=0.0,ub=1.0,. vtype=GRB.CONTINUOUS, name='y')
            y = model.addVars(Ay2, vtype=GRB.BINARY, name='y')
            #y = model.addVars(Ay2,lb=0,ub=1.0, vtype=GRB.CONTINUOUS, name='y')

            #Idee wenn zwei vehicle unterschiedliche StartPositionen haben, b trackt vehicle flow
            #bl = model.addVars(kArcs, vtype=GRB.BINARY, name='bl')
            if "Sartori" not in filename and "Furtado" not in filename and "BCP" not in filename:
                bl = model.addVars(V, vtype=GRB.CONTINUOUS, name='bl')
            if VC < 0:
               vl = model.addVars(V, vtype=GRB.CONTINUOUS, name='vl') 
    
            #b = model.addVars(xIndex,lb=0.0, ub=nVehicles ,vtype=GRB.CONTINUOUS, name="b")
            z = model.addVars(zIndex,lb=0.0 ,vtype=GRB.CONTINUOUS, name="z")
            #a = model.addVars([(i,r) for i in TS for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="a")
            if "Furtado" not in filename and "BCP" not in filename: 
                bz = model.addVars(zIndex,lb=0.0 ,vtype=GRB.CONTINUOUS, name="bz")
            #ba = model.addVars([(i,r) for i in TF for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="ba")
            if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
                Li =  model.addVars(P,lb=0.0 ,vtype=GRB.CONTINUOUS, name="Li")
            
            if "Furtado" in filename or "BCP" in filename:
                if min_vehicle==True:
                    model.setObjective(quicksum(x[i, j] for (i,j) in A2.select("o0","*")))
                else:
                    if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
                        #DARP
                        model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in A2))
                    else:
                        #PDPTW
                        model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in A2)+quicksum(pow(10,4) * x[i, j] for (i,j) in A2.select("o0","*")))
            else:
                model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in A2))
            model.update()
            
            
            """
            Restrict flows
            """
            #model.addConstrs(x[e]==0 for e in A2)
            #model.addConstrs(y[e]==0 for e in Ay2)
            #model.addConstrs((quicksum(x[i,j] for j in [a[1] for a in A2.select(i,'*')])==0 for i in TS|TF),name="remove_transfer_arcs")
            #model.addConstrs((quicksum(x[i,j] for i in [a[0] for a in A2.select('*',j)])==0 for j in TS|TF),name="remove_transfer_arcs_j")
    
            #model.addConstrs((quicksum(y[i,j,r] for r in R for j in [a[1] for a in Ay2.select(i,'*',r)])==0 for i in TS|TF),name="remove_transfer_arcs_y")
            #model.addConstrs((quicksum(y[i,j,r] for r in R for i in [a[0] for a in Ay2.select('*',j, r)])==0 for j in TS|TF),name="remove_transfer_arcs_y_j")
    
    
    
            """
            Arc flows
            """
            if "Sartori" in filename or "Furtado" in filename:
                #model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) <= float(np.ceil(sum(qnode[i] for i in P)/VC)) for vo in VO), name = "ct.route_startFirst")
                model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) <= nVehicles for vo in VO), name = "ct.route_startFirst")
                model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) >= 1 for vo in VO), name = "ct.route_startFirstTrivialLB")
                #model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) <= len(P) for vo in VO), name = "ct.route_UB")
                model.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A2.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
            elif "BCP" in filename or "Li" in filename:
                model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) >= 1 for vo in VO), name = "ct.route_startFirstTrivialLB")

                model.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A2.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
            else:
                model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) == 1 for vo in VO), name = "ct.route_startFirst")
                model.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A2.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
            
            
            model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A2.select('*',i)]) == 1 for i in P), name = "ct.PickupJustOnce")
            
            model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A2.select('*',i)]) == 1 for i in D), name = "ct.DeliveryJustOnce")
        
                
            
            model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A2.select('*',i)]) == quicksum(x[i,j] for j in [a[1] for a in A2.select(i,'*')])   for i in P|D), name = "ct.FlowConversion")
            
    
            
            """
            Loads
            """
            
            model.addConstrs((quicksum(y[i, j, r] for j in [a[1] for a in Ay2.select(i,'*',r)])  == 1 for r in R for i in [f"p{r}"]), name = "ct.visit_request_originOut")
        
        
            model.addConstrs((quicksum(y[j,i, r] for j in [a[0] for a in Ay2.select('*',i,r)])  == 1 for r in R for i in [f"d{r}"]), name = "ct.visit_request_destinationIn")
    
        
            model.addConstrs((quicksum(y[i, j,r] for j in [a[1] for a in Ay2.select(i,'*',r)])-quicksum(y[j,i,r] for j in [a[0] for a in Ay2.select('*',i,r)]) == 0 for r in R for i in V-(VD|VO|frozenset((f"p{r}","d{r}"))) if i not in ["p"+str(r),"d"+str(r)]), name = "ct.requestFlowConversion")
        
        
            model.addConstrs((y[i,j,r] <= x[i,j] for r in R for i in V for j in [a[1] for a in Ay2.select(i,'*',r)]), name = "ct.request_flow_link")
        
    
            """
            Capacity constraint
            """
         
            if strCap==True:
                # Strengthened capacity constraints
                model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-abs(qnode[i]+qnode[j]))*x[i,j] for i in P for j in [a[1] for a in A2.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong1")
                model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-abs(qnode[i]+qnode[j]))*x[i,j] for i in D for j in [a[1] for a in A2.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong2")
                model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in P for j in [a[1] for a in A2.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong3")
                model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in D for j in [a[1] for a in A2.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong4")
                
                model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if r!=int(i.replace("p","").replace("d","")) for j in [a[1] for a in Ay2.select(i,'*',r)]) <= (VC-abs(qnode[i])) for i in P|D), name="ct.VehicleCapacityStrong2")
            else:
                # capacity constraint
                model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)]) <= VC*x[i,j] for i in P|D for j in [a[1] for a in Ay2.select(i,'*',r)]), name="ct.VehicleCapacity")
            """
            Vehicle Flow Burger
            """
            if "Sartori" not in filename and "Furtado" not in filename and "BCP" not in filename and "Li" not in filename:
                model.addConstrs((bl[f"o{k}"]  == k+1 for k in K), name = "ct.route_startVehicleLabel")
                
                model.addConstrs((bl[f"e{k}"]  == k+1 for k in K), name = "ct.route_startVehicleLabel")
                    
                
                #model.addConstrs((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j] for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.vehicleLabelFlowA")
                    
                #model.addConstrs((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]  for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.vehicleLabelFlowB")
                for i in V-VD:
                    for j in [a[1] for a in A2.select(i,'*')]:
                        if (j,i) in A2:
                            model.addConstr((bl[i]-(len(K)-1)*(1-x[i,j]-x[j,i])<=bl[j]), name = "ct.vehicleLabelFlowLifted")
                        else:
                            model.addConstr((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j]), name = "ct.vehicleLabelFlowA")
                            model.addConstr((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]), name = "ct.vehicleLabelFlowB")
            
    
        
            if timeFlow==True:
                model.addConstrs(
                   (
                       gp.quicksum(
                           z[i, j] + (t[i,j]+service_time[i]) * x[i, j]
                           for i in V
                           if (i, j) in arcs
                       )
                       <= z.sum(j,"*")
                       for j in P|D 
                   ),
                       name="ct.time_flowA",
                 )
                """
                Time Windows
                """
                model.addConstrs(
                (
                    z[i, j] >= max(timeWindows[i][0],min(t[o,j]+service_time[o] for o in VO)) * x[i, j]
                    for (i, j) in arcs if i not in VO
                ),
                name="timeWindowStart",
                )
                
                model.addConstrs(
                (
                    z[i, j] == timeWindows[i][0]
                    for (i, j) in arcs if i in VO
                ),
                name="timeWindowStart",
                )
                
                model.addConstrs(
                    (
                        z[i, j] <= wbTW[i,j]* x[i, j]
                        for (i, j) in arcs
                    ),
                    name="timeWindowEnd",
                )
                #darp constraints
                if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
                    model.addConstrs((z.sum(i.replace("p","d"),"*")-z.sum(i,"*")-service_time[i]==Li[i]  for i in P), name = "ct.rideTimeConstraintA")
                    model.addConstrs((Li[i]<=Lmax  for i in P), name = "ct.rideTimeConstraintB")
        
                    #model.addConstrs(((service_time[i]+c[i,j])*x[i,j]<=Lmax  for i in P for j in [a[1] for a in A2.select(i,'*')]), name = "ct.rideTimeConstraintB")
                    model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) <= nVehicles for vo in VO), name = "ct.route_startFirstTrivialLB")
        
            else:
                
                if "Furtado" in filename or "BCP" in filename:
                    if LIFTED==True:
                        """
                        Lifted version, benefit unclear. Needs testing!
                        """
                        model.addConstrs((z[i]+service_time[i]+t[i,j]-(Mij[i,j])*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) not in A), name = "ct.time_flowA")
                        
                        model.addConstrs((z[i]-z[j]+Mij[i,j]*x[i,j]+(Mij[i,j]-service_time[i]-t[i,j]+min(-t[j,i]-service_time[j],timeWindows[j][0]-timeWindows[i][1]))*x[j,i]<= Mij[i,j]-t[i,j]-service_time[i]  for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) in A), name = "ct.time_flowLifted")
                    else:
                        model.addConstrs((z[i]+service_time[i]+t[i,j]-Mij[i,j]*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A2.select(i,'*')]), name = "ct.time_flowA")
                    

                
                    """
                    Time Windows
                    """
                    #model.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliest")
                    #model.addConstrs((min(max(timeWindows[f"e{k}"][1]-c[i,f"e{k}"]-service_time[i] for k in K),timeWindows[i][1]) >= z[i] for i in V-VD), name="ct.TimeWindowLatest")
                    model.addConstrs((timeWindows[i][1] >= z[i] for i in V), name="ct.TimeWindowLatest")
                   # model.addConstrs((timeWindows[i][0] <= a[i,r] for r in R for i in TS), name="ct.RtimeWindowEarliest")
                    #model.addConstrs((timeWindows[i][1] >= a[i,r] for r in R for i in TS), name="ct.RTimeWindowLatest")
                    
                    #model.addConstrs((min([max(timeWindows[i][0],c[f"o{k}",i])+service_time[f"o{k}"] for k in K]) <= z[i] for i in V-VO), name="ct.timeWindowEarliestbVO")
                    model.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliest")
                    #darp constraints
                    if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
                        model.addConstrs((z[i.replace("p","d")]-z[i]-service_time[i]==Li[i]  for i in P), name = "ct.rideTimeConstraintA")
                        model.addConstrs((Li[i]<=Lmax  for i in P), name = "ct.rideTimeConstraintB")
            
                        #model.addConstrs(((service_time[i]+c[i,j])*x[i,j]<=Lmax  for i in P for j in [a[1] for a in A2.select(i,'*')]), name = "ct.rideTimeConstraintB")
                        model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) <= nVehicles for vo in VO), name = "ct.route_startFirstTrivialLB")
            

                else:
                    model.addConstrs((bz[i]+t[i,j]-Mij[i,j]*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A2.select(i,'*')]), name = "ct.time_flowA")
                    #model.addConstrs((bz[i]+c[i,j]-Mij[i,j]*(1-x[i,j])+(Mij[i,j]-c[i,j]+min(-c[j,i],timeWindows[j][0]-timeWindows[i][0]))*x[j,i]<= z[j] for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.time_flowLifted")
 
                    model.addConstrs((z[i]+service_time[i] <= bz[i] for i in V), name='ct.DepartureA')

                    """
                    Time Windows
                    """
                    #model.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliest")
                    #model.addConstrs((min(max(timeWindows[f"e{k}"][1]-t[i,f"e{k}"] for k in K),timeWindows[i][1]) >= bz[i] for i in V-VD), name="ct.TimeWindowLatest")
                    model.addConstrs((timeWindows[i][1] >= bz[i] for i in V), name="ct.TimeWindowLatestVD")
                   # model.addConstrs((timeWindows[i][0] <= a[i,r] for r in R for i in TS), name="ct.RtimeWindowEarliest")
                    #model.addConstrs((timeWindows[i][1] >= a[i,r] for r in R for i in TS), name="ct.RTimeWindowLatest")
                    
                    #model.addConstrs((min([max(timeWindows[i][0],t[f"o{k}",i]) for k in K]) <= z[i] for i in V-VO), name="ct.timeWindowEarliestbVO")
                    model.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliestb")
    
            
        
            # Data for callback
            model._obj = None
            model._bd = None
            model._gap = None
            model._data = []
            model._x = x
            model._VO = VO
            model._cut = False
            model._A2 = A2
            model._Ay2 = Ay2
            model._V = V
            model._y = y
            model._z = z
            #model._bz = bz
            if "Sartori" not in filename and "Furtado" not in filename and "BCP" not in filename:
                model._bl = bl
            model._start = time.time()
            if cut!=None:
                model.Params.MIPFocus = 1
                model.Params.PreCrush = 0
            if last_sol!=None:
                try:
                    model.NumStart = 1
                    model.read(f"{filename}_{last_sol}.sol")
                except:
                    model.NumStart = -1
                    print("no initial solution exists")
            else:
                model.NumStart = 0
            if root==True:
                model.Params.NodeLimit = 1
                
            #model.Params.OutputFlag = 0
            #model.Params.LogToConsole=0
            #model.Params.LazyConstraints = 1s
            #model.Params.Symmetry = 0
            model.Params.TimeLimit = timelim*3
            if callback==True or min_vehicle==True:
                model.Params.Threads= 8
            else:
                model.Params.Threads= 16
            if min_vehicle==True:
                model.Params.OutputFlag = 1
                model.Params.LogToConsole=1
            """
            model.NumStart = 1
            model.update()
            
            sol1 = [["o0","p30","p43", "p34", "d30","p15","d15","p31" ,"d31" ,"p18" ,"d34" ,"d43" ,"d18","e0"],['o0', 'p28', 'p20', 'd20', 'p26', 'p46', 'd28', 'p10', 'p21', 'd46', 'd26', 'd21', 'p5', 'd10', 'p24', 'd5', 'd24', 'p0', 'd0', 'e0'], ['o0', 'p39', 'p47', 'p8', 'd8', 'p4', 'd4', 'd39', 'd47', 'p40', 'p7', 'p9', 'd40', 'd9', 'p37', 'p27', 'd27', 'd37', 'd7', 'e0'], ['o0', 'p25', 'd25', 'p29', 'd29', 'p6', 'p38', 'd6', 'p41', 'd41', 'p11', 'd38', 'p17', 'd11', 'd17', 'p36', 'p35', 'd36', 'p49', 'd49', 'd35', 'e0'], ['o0', 'p13', 'p14', 'd13', 'p48', 'p44', 'p42', 'd14', 'p3', 'd48', 'p45', 'd44', 'd45', 'd3', 'd42', 'p22', 'd22', 'e0'], ['o0', 'p32', 'p12', 'd12', 'p19', 'd32', 'p16', 'd16', 'p1', 'p33', 'd1', 'd33', 'p23', 'd19', 'd23', 'p2', 'd2', 'e0']]
            
            # iterate over all MIP starts
            for s in range(model.NumStart):
              
                # set StartNumber
                model.params.StartNumber = s
            
                # now set MIP start values using the Start attribute, e.g.:
                for route in sol1:
                    for i in range(len(route[:-1])):
                            j = i+1
                            model._x[route[i],route[j]].Start = 1.0"""
            model.update()
            if barrier!=None:
                barrier.wait()
            if callback==False:
                model.optimize()
            else:
                model.optimize(callback=cb)
            if min_vehicle==True:
                if model.Status==GRB.OPTIMAL:
                    global global_vehicle_lb 
                    global_vehicle_lb = model.ObjVal
                    return
                else:
                    return
            #model.write("test_reduced.lp")
            #if model.status==3:
             #   model.computeIIS()
              #  model.write("infeasible_model.ilp")
            #model.optimize(callback=checksolution_cb)
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
            
            def get_tour(arcs):
                tours = []
                for a in arcs:
                    if a[0]=="o0":
                        curr_node = a[1]
                        tour = [a]
                        while "e" not in curr_node:
                            for (i,j) in arcs:
                                if i==curr_node:
                                  tour.append((i,j))
                                  curr_node = j
                                  break
                        print(tour)
                        tours.append(tour)
                return tours    
            
            vehicle_number = -1
            if model.Status == GRB.OPTIMAL:
                model.write(f"{filename}_{cut}.sol")
                
                xarcs = plotLocation(df)
                vehicle_number = sum(x[i, j] for (i,j) in A2.select("o0","*")).getValue()
                with open(f"{filename.replace('.txt','')}_sol.txt", "w") as output:
                    output.write(str([a for a in x if x[a].x>0.5]))
                #sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
                infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,0,vehicle_number]  
                #for e in range(nSolutions):
                for iter2 in range(1):
                        model.setParam(GRB.Param.SolutionNumber, iter2)
                        print('%g ' % model.PoolObjVal, end='\n')
                        for v in model.getVars():
                             if v.xn > 1e-5:
                                   #print ('%s %g' % (v.varName, v.xn))
                                   print ('%s %g' % (v.varName, v.xn))
                        print("\n")
                print("\n")
                tours = get_tour([a for a in x if x[a].x>0.5])
                
                
            elif model.Status == GRB.TIME_LIMIT:
                if model.SolCount > 0:
                    vehicle_number = sum(x[i, j] for (i,j) in A2.select("o0","*")).getValue()
                    model.write(f"{filename}_{cut}.sol")
                    xarcs = plotLocation(df)
                    with open(f"{filename.replace('.txt','')}_sol.txt", "w") as output:
                        output.write(str([a for a in x if x[a].x>0.5]))
                    #sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
                    infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,0,vehicle_number]    
            else:
                infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),np.inf, np.inf,model.ObjBound, model.Runtime,0,vehicle_number]  
            env.close()
            if callback==True:
                global global_infos
                global_infos = infos
                return
            return infos
        
        def solve_pdptw_dahle(filename, timelim=60*60, cut=None,last_sol=None, strCap=False, timeFlow=False, callback=False, min_vehicle=False, barrier=None):
            
            
            LIFTED=True
            if timeFlow==True:
                LIFTED = False
            
            
            env=gp.Env()
            model = gp.Model(env=env)
            instance_name= filename.split("/")[-1]
            infostr = ""
            if strCap==True:
                infostr += "StrCap"
            if timeFlow==True:
                infostr +="timeFlow"
            if callback==True:
                infostr += "ParallelModel"
            if LIFTED==True:
                infostr+="LiftedMTZ"
            model = Model('PDPTW_Dahle'+infostr)
            arcs_keep = set()
            for i in V-VD-VO:
                edges = A.select(i,"*")
                if i in P and (i,i.replace("p","d")) in A:
                    arcs_keep.add((i,i.replace("p","d")))
                costs = {e:c[e] for e in edges}
                #sort by cost
                costs = sorted(costs.items(), key=lambda x: x[1])
                if cut==None:
                    edges_cut  = int(np.ceil(len(edges)/1))
                else:
                    edges_cut = cut
                #cut = 6
                if len(costs)>2:
                    for edge in dict(costs[:edges_cut]):
                            arcs_keep.add(edge)
                else:
                    for edge in dict(costs):
                            arcs_keep.add(edge)
                        
            for ek in VD:            
                for e in A.select("*",ek):
                        arcs_keep.add(e)
            for ok in VO:            
                for e in A.select(ok,"*"):
                        arcs_keep.add(e)
                        
            A2 = tuplelist(arcs_keep) 
            
            Ay_keep = set()
            for arc in Ay:
                if (arc[0],arc[1]) in arcs_keep:
                    Ay_keep.add(arc)
            
            Ay2 = tuplelist(Ay_keep)
            
            if timeFlow==True:
                zIndex = [(i, j) for (i,j) in arcs]
            else:
                zIndex = [i for i in V]
    
            wbTW = {(i,j):min(timeWindows[i][1],timeWindows[j][1]-c[i,j]-service_time[i]) for (i,j) in arcs}
    
            x = model.addVars(A2, vtype=GRB.BINARY, name='x')
            #y = model.addVars(Ay2,lb=0.0,ub=1.0,. vtype=GRB.CONTINUOUS, name='y')
            y = model.addVars(Ay2, lb=0.0 ,vtype=GRB.CONTINUOUS, name='y')
            #y = model.addVars(Ay2, vtype=GRB.BINARY, name='y')
            #Idee wenn zwei vehicle unterschiedliche StartPositionen haben, b trackt vehicle flow
            #bl = model.addVars(kArcs, vtype=GRB.BINARY, name='bl')
            if "Sartori" not in filename and "Furtado" not in filename and "BCP" not in filename:
                bl = model.addVars(V, vtype=GRB.CONTINUOUS, name='bl')
            if VC < 0:
               vl = model.addVars(V, vtype=GRB.CONTINUOUS, name='vl') 
    
            #b = model.addVars(xIndex,lb=0.0, ub=nVehicles ,vtype=GRB.CONTINUOUS, name="b")
            z = model.addVars(zIndex,lb=0.0 ,vtype=GRB.CONTINUOUS, name="z")
            #a = model.addVars([(i,r) for i in TS for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="a")
            if "Furtado" not in filename and "BCP" not in filename: 
                bz = model.addVars(zIndex,lb=0.0 ,vtype=GRB.CONTINUOUS, name="bz")
            #ba = model.addVars([(i,r) for i in TF for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="ba")
            if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
                Li =  model.addVars(P,lb=0.0 ,vtype=GRB.CONTINUOUS, name="Li")
            
            if "Furtado" in filename or "BCP" in filename:
                if min_vehicle==True:
                    model.setObjective(quicksum(x[i, j] for (i,j) in A2.select("o0","*")))
                else:
                    if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
                        #DARP
                        model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in A2))
                    else:
                        #PDPTW
                        model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in A2)+quicksum(pow(10,4) * x[i, j] for (i,j) in A2.select("o0","*")))
            else:
                model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in A2))
            model.update()
            
            
            """
            Restrict flows
            """
            #model.addConstrs(x[e]==0 for e in A2)
            #model.addConstrs(y[e]==0 for e in Ay2)
            #model.addConstrs((quicksum(x[i,j] for j in [a[1] for a in A2.select(i,'*')])==0 for i in TS|TF),name="remove_transfer_arcs")
            #model.addConstrs((quicksum(x[i,j] for i in [a[0] for a in A2.select('*',j)])==0 for j in TS|TF),name="remove_transfer_arcs_j")
    
            #model.addConstrs((quicksum(y[i,j,r] for r in R for j in [a[1] for a in Ay2.select(i,'*',r)])==0 for i in TS|TF),name="remove_transfer_arcs_y")
            #model.addConstrs((quicksum(y[i,j,r] for r in R for i in [a[0] for a in Ay2.select('*',j, r)])==0 for j in TS|TF),name="remove_transfer_arcs_y_j")
    
    
    
            """
            Arc flows
            """
            if "Sartori" in filename or "Furtado" in filename:
                #model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) <= float(np.ceil(sum(qnode[i] for i in P)/VC)) for vo in VO), name = "ct.route_startFirst")
                model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) <= nVehicles for vo in VO), name = "ct.route_startFirst")
                model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) >= 1 for vo in VO), name = "ct.route_startFirstTrivialLB")
                #model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) <= len(P) for vo in VO), name = "ct.route_UB")
                model.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A2.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
            elif "BCP" in filename or "Li" in filename:
                model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) >= 1 for vo in VO), name = "ct.route_startFirstTrivialLB")

                model.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A2.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
            else:
                model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) == 1 for vo in VO), name = "ct.route_startFirst")
                model.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A2.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
            
            
            model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A2.select('*',i)]) == 1 for i in P), name = "ct.PickupJustOnce")
            
            model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A2.select('*',i)]) == 1 for i in D), name = "ct.DeliveryJustOnce")
        
                
            
            model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A2.select('*',i)]) == quicksum(x[i,j] for j in [a[1] for a in A2.select(i,'*')])   for i in P|D), name = "ct.FlowConversion")
            
    
            
            """
            Loads
            """
            
            #model.addConstrs((quicksum(y[i, j, r] for j in [a[1] for a in Ay2.select(i,'*',r)])  == 1 for r in R for i in [f"p{r}"]), name = "ct.visit_request_originOut")
        
        
            #model.addConstrs((quicksum(y[j,i, r] for j in [a[0] for a in Ay2.select('*',i,r)])  == 1 for r in R for i in [f"d{r}"]), name = "ct.visit_request_destinationIn")
    
        
            #model.addConstrs((quicksum(y[i, j,r] for j in [a[1] for a in Ay2.select(i,'*',r)])-quicksum(y[j,i,r] for j in [a[0] for a in Ay2.select('*',i,r)]) == 0 for r in R for i in V-(VD|VO|frozenset((f"p{r}","d{r}"))) if i not in ["p"+str(r),"d"+str(r)]), name = "ct.requestFlowConversion")
        
        
            #model.addConstrs((y[i,j,r] <= x[i,j] for r in R for i in V for j in [a[1] for a in Ay2.select(i,'*',r)]), name = "ct.request_flow_link")
        
    
            """
            Capacity constraint
            """
         
            model.addConstrs((quicksum(y[i, j, r] for j in [a[1] for a in Ay2.select(i,'*',r)])  == qnode[i] for r in R for i in [f"p{r}"]), name = "ct.visit_request_originOut")
       
       
            model.addConstrs((quicksum(y[j,i, r] for j in [a[0] for a in Ay2.select('*',i,r)])  == abs(q[r]) for r in R for i in [f"d{r}"]), name = "ct.visit_request_destinationIn")
   
       
            model.addConstrs((quicksum(y[i, j,r] for j in [a[1] for a in Ay2.select(i,'*',r)])-quicksum(y[j,i,r] for j in [a[0] for a in Ay2.select('*',i,r)]) == 0 for r in R for i in V-(VD|VO|frozenset((f"p{r}","d{r}"))) if i not in ["p"+str(r),"d"+str(r)]), name = "ct.requestFlowConversion")
       
       
            model.addConstrs((y[i,j,r] <= q[r]*x[i,j] for r in R for i in V for j in [a[1] for a in Ay2.select(i,'*',r)]), name = "ct.request_flow_link")
           
            model.addConstrs((quicksum(y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)]) <= VC*x[i,j] for i in P|D for j in [a[1] for a in Ay2.select(i,'*',r)]), name="ct.VehicleCapacity")
 
            """
            Vehicle Flow Burger
            """
            if "Sartori" not in filename and "Furtado" not in filename and "BCP" not in filename and "Li" not in filename:
                model.addConstrs((bl[f"o{k}"]  == k+1 for k in K), name = "ct.route_startVehicleLabel")
                
                model.addConstrs((bl[f"e{k}"]  == k+1 for k in K), name = "ct.route_startVehicleLabel")
                    
                
                #model.addConstrs((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j] for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.vehicleLabelFlowA")
                    
                #model.addConstrs((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]  for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.vehicleLabelFlowB")
                for i in V-VD:
                    for j in [a[1] for a in A2.select(i,'*')]:
                        if (j,i) in A2:
                            model.addConstr((bl[i]-(len(K)-1)*(1-x[i,j]-x[j,i])<=bl[j]), name = "ct.vehicleLabelFlowLifted")
                        else:
                            model.addConstr((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j]), name = "ct.vehicleLabelFlowA")
                            model.addConstr((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]), name = "ct.vehicleLabelFlowB")
            
    
        
            if timeFlow==True:
                model.addConstrs(
                   (
                       gp.quicksum(
                           z[i, j] + (t[i,j]+service_time[i]) * x[i, j]
                           for i in V
                           if (i, j) in arcs
                       )
                       <= z.sum(j,"*")
                       for j in P|D 
                   ),
                       name="ct.time_flowA",
                 )
                """
                Time Windows
                """
                model.addConstrs(
                (
                    z[i, j] >= max(timeWindows[i][0],min(t[o,j]+service_time[o] for o in VO)) * x[i, j]
                    for (i, j) in arcs if i not in VO
                ),
                name="timeWindowStart",
                )
                
                model.addConstrs(
                (
                    z[i, j] == timeWindows[i][0]
                    for (i, j) in arcs if i in VO
                ),
                name="timeWindowStart",
                )
                
                model.addConstrs(
                    (
                        z[i, j] <= wbTW[i,j]* x[i, j]
                        for (i, j) in arcs
                    ),
                    name="timeWindowEnd",
                )
                #darp constraints
                if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
                    model.addConstrs((z.sum(i.replace("p","d"),"*")-z.sum(i,"*")-service_time[i]==Li[i]  for i in P), name = "ct.rideTimeConstraintA")
                    model.addConstrs((Li[i]<=Lmax  for i in P), name = "ct.rideTimeConstraintB")
        
                    #model.addConstrs(((service_time[i]+c[i,j])*x[i,j]<=Lmax  for i in P for j in [a[1] for a in A2.select(i,'*')]), name = "ct.rideTimeConstraintB")
                    model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) <= nVehicles for vo in VO), name = "ct.route_startFirstTrivialLB")
        
            else:
                
                if "Furtado" in filename or "BCP" in filename:
                    if LIFTED==True:
                        """
                        Lifted version, benefit unclear. Needs testing!
                        """
                        model.addConstrs((z[i]+service_time[i]+t[i,j]-(Mij[i,j])*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) not in A), name = "ct.time_flowA")
                        
                        model.addConstrs((z[i]-z[j]+Mij[i,j]*x[i,j]+(Mij[i,j]-service_time[i]-t[i,j]+min(-t[j,i]-service_time[j],timeWindows[j][0]-timeWindows[i][1]))*x[j,i]<= Mij[i,j]-t[i,j]-service_time[i]  for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) in A), name = "ct.time_flowLifted")
                    else:
                        model.addConstrs((z[i]+service_time[i]+t[i,j]-Mij[i,j]*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A2.select(i,'*')]), name = "ct.time_flowA")
                    

                
                    """
                    Time Windows
                    """
                    #model.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliest")
                    #model.addConstrs((min(max(timeWindows[f"e{k}"][1]-c[i,f"e{k}"]-service_time[i] for k in K),timeWindows[i][1]) >= z[i] for i in V-VD), name="ct.TimeWindowLatest")
                    model.addConstrs((timeWindows[i][1] >= z[i] for i in V), name="ct.TimeWindowLatest")
                   # model.addConstrs((timeWindows[i][0] <= a[i,r] for r in R for i in TS), name="ct.RtimeWindowEarliest")
                    #model.addConstrs((timeWindows[i][1] >= a[i,r] for r in R for i in TS), name="ct.RTimeWindowLatest")
                    
                    #model.addConstrs((min([max(timeWindows[i][0],c[f"o{k}",i])+service_time[f"o{k}"] for k in K]) <= z[i] for i in V-VO), name="ct.timeWindowEarliestbVO")
                    model.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliest")
                    #darp constraints
                    if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
                        model.addConstrs((z[i.replace("p","d")]-z[i]-service_time[i]==Li[i]  for i in P), name = "ct.rideTimeConstraintA")
                        model.addConstrs((Li[i]<=Lmax  for i in P), name = "ct.rideTimeConstraintB")
            
                        #model.addConstrs(((service_time[i]+c[i,j])*x[i,j]<=Lmax  for i in P for j in [a[1] for a in A2.select(i,'*')]), name = "ct.rideTimeConstraintB")
                        model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) <= nVehicles for vo in VO), name = "ct.route_startFirstTrivialLB")
            

                else:
                    model.addConstrs((bz[i]+t[i,j]-Mij[i,j]*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A2.select(i,'*')]), name = "ct.time_flowA")
                    #model.addConstrs((bz[i]+c[i,j]-Mij[i,j]*(1-x[i,j])+(Mij[i,j]-c[i,j]+min(-c[j,i],timeWindows[j][0]-timeWindows[i][0]))*x[j,i]<= z[j] for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.time_flowLifted")
 
                    model.addConstrs((z[i]+service_time[i] <= bz[i] for i in V), name='ct.DepartureA')

                    """
                    Time Windows
                    """
                    #model.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliest")
                    #model.addConstrs((min(max(timeWindows[f"e{k}"][1]-t[i,f"e{k}"] for k in K),timeWindows[i][1]) >= bz[i] for i in V-VD), name="ct.TimeWindowLatest")
                    model.addConstrs((timeWindows[i][1] >= bz[i] for i in V), name="ct.TimeWindowLatestVD")
                   # model.addConstrs((timeWindows[i][0] <= a[i,r] for r in R for i in TS), name="ct.RtimeWindowEarliest")
                    #model.addConstrs((timeWindows[i][1] >= a[i,r] for r in R for i in TS), name="ct.RTimeWindowLatest")
                    
                    #model.addConstrs((min([max(timeWindows[i][0],t[f"o{k}",i]) for k in K]) <= z[i] for i in V-VO), name="ct.timeWindowEarliestbVO")
                    model.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliestb")
    
            
        
            # Data for callback
            model._obj = None
            model._bd = None
            model._gap = None
            model._data = []
            model._x = x
            model._VO = VO
            model._cut = False
            model._A2 = A2
            model._Ay2 = Ay2
            model._V = V
            model._y = y
            model._z = z
            if root==True:
                model.Params.NodeLimit = 1
            #model._bz = bz
            if "Sartori" not in filename and "Furtado" not in filename and "BCP" not in filename:
                model._bl = bl
            model._start = time.time()
            if cut!=None:
                model.Params.MIPFocus = 1
                model.Params.PreCrush = 0
            if last_sol!=None:
                try:
                    model.NumStart = 1
                    model.read(f"{filename}_{last_sol}.sol")
                except:
                    model.NumStart = -1
                    print("no initial solution exists")
            else:
                model.NumStart = 0
                
            #model.Params.OutputFlag = 0
            #model.Params.LogToConsole=0
            #model.Params.LazyConstraints = 1
            #model.Params.Symmetry = 0
            if root==True:
                model.Params.NodeLimit = 1
            model.Params.TimeLimit = timelim
            if callback==True or min_vehicle==True:
                model.Params.Threads= 8
            else:
                model.Params.Threads= 16
            if min_vehicle==True:
                model.Params.OutputFlag = 1
                model.Params.LogToConsole=1
            """
            model.NumStart = 1
            model.update()
            
            sol1 = [["o0","p30","p43", "p34", "d30","p15","d15","p31" ,"d31" ,"p18" ,"d34" ,"d43" ,"d18","e0"],['o0', 'p28', 'p20', 'd20', 'p26', 'p46', 'd28', 'p10', 'p21', 'd46', 'd26', 'd21', 'p5', 'd10', 'p24', 'd5', 'd24', 'p0', 'd0', 'e0'], ['o0', 'p39', 'p47', 'p8', 'd8', 'p4', 'd4', 'd39', 'd47', 'p40', 'p7', 'p9', 'd40', 'd9', 'p37', 'p27', 'd27', 'd37', 'd7', 'e0'], ['o0', 'p25', 'd25', 'p29', 'd29', 'p6', 'p38', 'd6', 'p41', 'd41', 'p11', 'd38', 'p17', 'd11', 'd17', 'p36', 'p35', 'd36', 'p49', 'd49', 'd35', 'e0'], ['o0', 'p13', 'p14', 'd13', 'p48', 'p44', 'p42', 'd14', 'p3', 'd48', 'p45', 'd44', 'd45', 'd3', 'd42', 'p22', 'd22', 'e0'], ['o0', 'p32', 'p12', 'd12', 'p19', 'd32', 'p16', 'd16', 'p1', 'p33', 'd1', 'd33', 'p23', 'd19', 'd23', 'p2', 'd2', 'e0']]
            
            # iterate over all MIP starts
            for s in range(model.NumStart):
              
                # set StartNumber
                model.params.StartNumber = s
            
                # now set MIP start values using the Start attribute, e.g.:
                for route in sol1:
                    for i in range(len(route[:-1])):
                            j = i+1
                            model._x[route[i],route[j]].Start = 1.0"""
            model.update()
            if barrier!=None:
                barrier.wait()
            if callback==False:
                model.optimize()
            else:
                model.optimize(callback=cb)
            if min_vehicle==True:
                if model.Status==GRB.OPTIMAL:
                    global global_vehicle_lb 
                    global_vehicle_lb = model.ObjVal
                    return
                else:
                    return
            #model.write("test_reduced.lp")
            #if model.status==3:
                #model.computeIIS()
                #model.write("infeasible_model.ilp")
            #model.optimize(callback=checksolution_cb)
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
            
            def get_tour(arcs):
                tours = []
                for a in arcs:
                    if a[0]=="o0":
                        curr_node = a[1]
                        tour = [a]
                        while "e" not in curr_node:
                            for (i,j) in arcs:
                                if i==curr_node:
                                  tour.append((i,j))
                                  curr_node = j
                                  break
                        print(tour)
                        tours.append(tour)
                return tours    
            
            vehicle_number = -1
            if model.Status == GRB.OPTIMAL:
                model.write(f"{filename}_{cut}.sol")
                
                xarcs = plotLocation(df)
                vehicle_number = sum(x[i, j] for (i,j) in A2.select("o0","*")).getValue()
                #with open(f"{filename.replace('.txt','')}_sol.txt", "w") as output:
                    #output.write(str([a for a in x if x[a].x>0.5]))
                #sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
                infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,0,vehicle_number]  
                #for e in range(nSolutions):
                for iter2 in range(1):
                        model.setParam(GRB.Param.SolutionNumber, iter2)
                        print('%g ' % model.PoolObjVal, end='\n')
                        for v in model.getVars():
                             if v.xn > 1e-5:
                                   #print ('%s %g' % (v.varName, v.xn))
                                   print ('%s %g' % (v.varName, v.xn))
                        print("\n")
                print("\n")
                tours = get_tour([a for a in x if x[a].x>0.5])
                
                
            elif model.Status == GRB.TIME_LIMIT:
                if model.SolCount > 0:
                    vehicle_number = sum(x[i, j] for (i,j) in A2.select("o0","*")).getValue()
                    model.write(f"{filename}_{cut}.sol")
                    xarcs = plotLocation(df)
                    #with open(f"{filename.replace('.txt','')}_sol.txt", "w") as output:
                     #   output.write(str([a for a in x if x[a].x>0.5]))
                    #sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
                    infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,0,vehicle_number]    
            else:
                infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),np.inf, np.inf,model.ObjBound, model.Runtime,0,vehicle_number]  
            env.close()
            if callback==True:
                global global_infos
                global_infos = infos
                return
            
            return infos
        
        def solve_pdptw_model_ORLetters_multicommodity(heuristic=True, edges_cut=None):
            
            model = gp.Model()
            model = Model('PDPTW_ORLetters')
            arcs_keep = set()
            for i in V-VD-VO:
                edges = A.select(i,"*")
                if i in P:
                    arcs_keep.add((i,i.replace("p","d")))
                costs = {e:c[e] for e in edges}
                #sort by cost
                costs = sorted(costs.items(), key=lambda x: x[1])
                if edges_cut == None:
                    cut = int(np.ceil(len(edges)/1))
                else:
                    cut = int(np.ceil(len(edges)/edges_cut))
                if len(costs)>2:
                    for edge in dict(costs[:cut]):
                            arcs_keep.add(edge)
                else:
                    for edge in dict(costs):
                            arcs_keep.add(edge)
                        
            Ay2 = tuplelist(arcs_keep)
            
            for ek in VD:            
                for e in A.select("*",ek):
                        arcs_keep.add(e)
            for ok in VO:            
                for e in A.select(ok,"*"):
                        arcs_keep.add(e)
                        
            V1 = V
            A1 = tuplelist(arcs_keep)
        
            x = model.addVars(A1, vtype=GRB.BINARY, name='x')
            #y = model.addVars(A1, vtype=GRB.CONTINUOUS, lb=0.0, name='y')
            y = model.addVars(Ay2, vtype=GRB.CONTINUOUS, name='y')
            #y = model.addVars(Ay1, vtype=GRB.BINARY, name='y')
            bl = model.addVars(V1, vtype=GRB.CONTINUOUS, name='bl')
            z = model.addVars(V1,lb=0.0 ,vtype=GRB.CONTINUOUS, name="z")
            model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in A1))
            model.update()
            """
            Arc flows
            """
            
            model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A1.select(vo,'*')]) == 1 for vo in VO), name = "ct.route_startFirst")
            model.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A1.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A1.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
            model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A1.select('*',i)]) == 1 for i in P|D), name = "ct.PickupDeliveryJustOnce")    
            
            model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A1.select('*',i)]) == quicksum(x[i,j] for j in [a[1] for a in A1.select(i,'*')])   for i in P|D), name = "ct.FlowConversion")
            
            ##########Commodity Flow Formulation#############
            """
            #load-flow-model
            model.addConstrs((quicksum(y[i,j] for j in [a[1] for a in A1.select(i,'*')])-quicksum(y[j,i] for j in [a[0] for a in A1.select('*',i)])  == qnode[i]  for i in P|D), name = "ct.LoadConversion")
            #Capacity constraints
                    
            model.addConstrs((y[i,j] <= x[i,j]*VC  for i,j in A1), name="LoadLB_Link")"""
        
            ##########OR Letters#############
            #Loads
            
            #model.addConstrs((y[j]>= (y[i]+qnode[j])-min(VC,VC+qnode[i])*(1-x[i,j]) for i,j in A1), name="loadContinuation")
        
            
            #Capacity constraints
            
            model.addConstrs((y[i,j]<= (VC+min(0,qnode[i],-qnode[j]))*x[i,j]  for (i,j) in Ay2), name="loadRestUB")
            model.addConstrs((y[i,j]>= (max(0,qnode[i],-qnode[j]))*x[i,j]  for (i,j) in Ay2), name="loadRestLB")
            
        
            model.addConstrs((quicksum(y[i, j] for j in [a[1] for a in Ay2.select(i,'*')])-quicksum(y[j,i] for j in [a[0] for a in Ay2.select('*',i)]) == qnode[i] for i in P|D), name = "ct.requestFlowConversion")
        
            
            """
            model.addConstrs((quicksum(y[i, j, r] for j in [a[1] for a in Ay1.select(i,'*',r)])  == 1 for r in R for i in [f"p{r}"]), name = "ct.visit_request_originOut")
        
        
            model.addConstrs((quicksum(y[j,i, r] for j in [a[0] for a in Ay1.select('*',i,r)])  == 1 for r in R for i in [f"d{r}"]), name = "ct.visit_request_destinationIn")
        
        
            model.addConstrs((quicksum(y[i, j,r] for j in [a[1] for a in Ay1.select(i,'*',r)])-quicksum(y[j,i,r] for j in [a[0] for a in Ay1.select('*',i,r)]) == 0 for r in R for i in V1-(TS|TF|VD|VO|frozenset((f"p{r}","d{r}"))) if i not in ["p"+str(r),"d"+str(r)]), name = "ct.requestFlowConversion")
        
        
            model.addConstrs((y[i,j,r] <= x[i,j] for r in R for i in P|D for j in [a[1] for a in Ay1.select(i,'*',r)]), name = "ct.request_flow_link")
        
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay1.select(i,j,r)]) <= VC for i in P|D for j in [a[1] for a in Ay1.select(i,'*',r)]), name="ct.VehicleCapacity")
            """
            """
            Vehicle Flow Burger
            """
            
            model.addConstrs((bl[f"o{k}"]  == k for k in K), name = "ct.route_startVehicleLabel")
            
            model.addConstrs((bl[f"e{k}"]  == k for k in K), name = "ct.route_startVehicleLabel")
                
            
            model.addConstrs((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j] for i in V1 for j in [a[1] for a in A1.select(i,'*')]), name = "ct.vehicleLabelFlowA")
                
            model.addConstrs((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]  for i in V1 for j in [a[1] for a in A1.select(i,'*')]), name = "ct.vehicleLabelFlowB")
            
            model.addConstrs((bl[i.replace("p","d")]==bl[i] for i in P), name="samepathConstraint")
        
            """
            for i in V1-VD:
                for j in [a[1] for a in A1.select(i,'*')]:
                    if (j,i) in A1:
                        model.addConstr((bl[i]-(len(K)-1)*(1-x[i,j]-x[j,i])<=bl[j]), name = "ct.vehicleLabelFlowLifted")
                    else:
                        model.addConstr((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j]), name = "ct.vehicleLabelFlowA")
                        model.addConstr((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]), name = "ct.vehicleLabelFlowB")"""
            
            
            model.addConstrs((z[i]+service_time[i]+c[i,j]-Mij[i,j]*(1-x[i,j])<= z[j] for i in V1 for j in [a[1] for a in A1.select(i,'*')]), name = "ct.time_flowA")
         
            model.addConstrs((z[i.replace("p","d")]>=z[i]+c[i,i.replace("p","d")] for i in P), name="precedenceConstraint")
            """
            Time Windows
            """
            model.addConstrs((timeWindows[i][1] >= z[i] for i in V1), name="ct.TimeWindowLatest")
        
            
            model.addConstrs((timeWindows[i][0] <= z[i] for i in V1), name="ct.timeWindowEarliestb")
            
        
        
            # Data for callback
            model._obj = None
            model._bd = None
            model._gap = None
            model._data = []
            model._x = x
            model._start = time.time()
            #.Params.LazyConstraints = 1
            #model.Params.Symmetry = 0
            if heuristic==True:
                model.Params.MIPFocus = 1
            model.Params.TimeLimit = 60*60
            model.Params.Threads = 2
            model.update()
            model.optimize()
            #model.optimize(callback=checksolution_cb)
            """
            if model.Status == GRB.OPTIMAL:
                for iter2 in range(1):
                        model.setParam(GRB.Param.SolutionNumber, iter2)
                        print('%g ' % model.PoolObjVal, end='\n')
                        for v in model.getVars():
                             if v.xn > 1e-5:
                                   #print ('%s %g' % (v.varName, v.xn))
                                   print ('%s %g' % (v.varName, v.xn))
                        print("\n")
                print("\n")
            """
        
        def solve_pdptw_model_ORLetters(heuristic=True, edges_cut=None):
            
                    model = gp.Model()
                    instance_name= filename.split("/")[-1]
                    model = Model('PDPTW_ORLetters')
                    arcs_keep = set()
                    for i in V-VD-VO:
                        edges = A.select(i,"*")
                        if i in P:
                            arcs_keep.add((i,i.replace("p","d")))
                        costs = {e:c[e] for e in edges}
                        #sort by cost
                        costs = sorted(costs.items(), key=lambda x: x[1])
                        if edges_cut == None:
                            cut = int(np.ceil(len(edges)/1))
                        else:
                            cut = int(np.ceil(len(edges)/edges_cut))
                        if len(costs)>2:
                            for edge in dict(costs[:cut]):
                                    arcs_keep.add(edge)
                        else:
                            for edge in dict(costs):
                                    arcs_keep.add(edge)
                                
                    for ek in VD:            
                        for e in A.select("*",ek):
                                arcs_keep.add(e)
                    for ok in VO:            
                        for e in A.select(ok,"*"):
                                arcs_keep.add(e)
                                
                    V1 = V
                    A1 = tuplelist(arcs_keep)
                    K = list(range(nVehicles))
            
                    x = model.addVars(A1, vtype=GRB.BINARY, name='x')
                    #y = model.addVars(A1, vtype=GRB.CONTINUOUS, lb=0.0, name='y')
                    y = model.addVars(V1, vtype=GRB.CONTINUOUS, lb=0.0, name='y')
                    #y = model.addVars(Ay1, vtype=GRB.BINARY, name='y')
                    bl = model.addVars(V1, vtype=GRB.CONTINUOUS, name='bl')
                    z = model.addVars(V1,lb=0.0 ,vtype=GRB.CONTINUOUS, name="z")
                    if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
                        Li =  model.addVars(zIndex,lb=0.0 ,vtype=GRB.CONTINUOUS, name="Li")
                    if "Furtado" in filename or "BCP" in filename:
                        #model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in A1))
                        model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in A1)+quicksum(pow(10,4) * x[i, j] for (i,j) in A1.select("o0","*")))
                    else:
                        model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in A1))
                    model.update()
                    """
                    Arc flows
                    """
                    
                    if "Sartori" in filename or "Furtado" in filename:
                        model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A1.select(vo,'*')]) <= nVehicles for vo in VO), name = "ct.route_startFirst")
                        model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A1.select(vo,'*')]) >= 1 for vo in VO), name = "ct.route_startFirstTrivialLB")
                        #model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) <= len(P) for vo in VO), name = "ct.route_UB")
                        model.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A1.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A1.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
                    elif "BCP" in filename:
                        model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A1.select(vo,'*')]) >= 1 for vo in VO), name = "ct.route_startFirstTrivialLB")
                        model.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A1.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A1.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
                    else:
                        model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A1.select(vo,'*')]) == 1 for vo in VO), name = "ct.route_startFirst")
                        model.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A1.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A1.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
                    

                    model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A1.select('*',i)]) == 1 for i in P|D), name = "ct.PickupDeliveryJustOnce")    
                    
                    model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A1.select('*',i)]) == quicksum(x[i,j] for j in [a[1] for a in A1.select(i,'*')])   for i in P|D), name = "ct.FlowConversion")
                    
                    ##########Commodity Flow Formulation#############
                    """
                    #load-flow-model
                    model.addConstrs((quicksum(y[i,j] for j in [a[1] for a in A1.select(i,'*')])-quicksum(y[j,i] for j in [a[0] for a in A1.select('*',i)])  == qnode[i]  for i in P|D), name = "ct.LoadConversion")
                    #Capacity constraints
                            
                    model.addConstrs((y[i,j] <= x[i,j]*VC  for i,j in A1), name="LoadLB_Link")"""
            
                    ##########OR Letters#############
                    #Loads
                    
                    model.addConstrs((y[j]>= (y[i]+qnode[j])-min(VC,VC+qnode[i])*(1-x[i,j]) for i,j in A1), name="loadContinuation")
            
                    
                    #Capacity constraints
                    
                    model.addConstrs((y[i]<= min(VC,VC+qnode[i])  for i in V1), name="loadRestUB")
                    model.addConstrs((y[i]>= max(0,qnode[i])  for i in V1), name="loadRestLB")
                    
                    
                    """
                    model.addConstrs((quicksum(y[i, j, r] for j in [a[1] for a in Ay1.select(i,'*',r)])  == 1 for r in R for i in [f"p{r}"]), name = "ct.visit_request_originOut")
            
            
                    model.addConstrs((quicksum(y[j,i, r] for j in [a[0] for a in Ay1.select('*',i,r)])  == 1 for r in R for i in [f"d{r}"]), name = "ct.visit_request_destinationIn")
            
            
                    model.addConstrs((quicksum(y[i, j,r] for j in [a[1] for a in Ay1.select(i,'*',r)])-quicksum(y[j,i,r] for j in [a[0] for a in Ay1.select('*',i,r)]) == 0 for r in R for i in V1-(TS|TF|VD|VO|frozenset((f"p{r}","d{r}"))) if i not in ["p"+str(r),"d"+str(r)]), name = "ct.requestFlowConversion")
            
            
                    model.addConstrs((y[i,j,r] <= x[i,j] for r in R for i in P|D for j in [a[1] for a in Ay1.select(i,'*',r)]), name = "ct.request_flow_link")
            
                    model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay1.select(i,j,r)]) <= VC for i in P|D for j in [a[1] for a in Ay1.select(i,'*',r)]), name="ct.VehicleCapacity")
                    """
                    """
                    Vehicle Flow Burger
                    """
                    if "Furtado" not in filename and "BCP" not in filename:
                    
                        model.addConstrs((bl[f"o{k}"]  == k for k in K), name = "ct.route_startVehicleLabel")
                        
                        model.addConstrs((bl[f"e{k}"]  == k for k in K), name = "ct.route_startVehicleLabel")
                            
                        
                        model.addConstrs((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j] for i in V1 for j in [a[1] for a in A1.select(i,'*')]), name = "ct.vehicleLabelFlowA")
                            
                        model.addConstrs((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]  for i in V1 for j in [a[1] for a in A1.select(i,'*')]), name = "ct.vehicleLabelFlowB")
                    else:
                        model.addConstrs((bl[i]  >= float(i.replace("p",""))*x["o0",i] for i in P), name = "ct.route_startVehicleLabelA")
                        model.addConstrs((bl[i]  <= float(i.replace("p",""))*x["o0",i]-nRequests*(x["o0",i]-1) for i in P), name = "ct.route_startVehicleLabelB")

                    
                        
                        model.addConstrs((bl[i]-nRequests*(1-x[i,j])<=bl[j] for i in P|D for j in [a[1] for a in A1.select(i,'*')] if j not in VD), name = "ct.vehicleLabelFlowA")
                            
                        model.addConstrs((bl[j]-nRequests*(1-x[i,j])<=bl[i]  for i in P|D for j in [a[1] for a in A1.select(i,'*')] if j not in VD), name = "ct.vehicleLabelFlowB")
                    
                    model.addConstrs((bl[i.replace("p","d")]==bl[i] for i in P), name="samepathConstraint")
            
                    """
                    for i in V1-VD:
                        for j in [a[1] for a in A1.select(i,'*')]:
                            if (j,i) in A1:
                                model.addConstr((bl[i]-(len(K)-1)*(1-x[i,j]-x[j,i])<=bl[j]), name = "ct.vehicleLabelFlowLifted")
                            else:
                                model.addConstr((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j]), name = "ct.vehicleLabelFlowA")
                                model.addConstr((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]), name = "ct.vehicleLabelFlowB")"""
                    
                    
                    model.addConstrs((z[i]+service_time[i]+t[i,j]-Mij[i,j]*(1-x[i,j])<= z[j] for i in V1 for j in [a[1] for a in A1.select(i,'*')]), name = "ct.time_flowA")
             
                    model.addConstrs((z[i.replace("p","d")]>=z[i]+t[i,i.replace("p","d")]+service_time[i] for i in P), name="precedenceConstraint")
                    """
                    Time Windows
                    """
                    model.addConstrs((timeWindows[i][1] >= z[i] for i in V1), name="ct.TimeWindowLatest")
                
                    
                    model.addConstrs((timeWindows[i][0] <= z[i] for i in V1), name="ct.timeWindowEarliestb")
                    
                    #darp constraints
                    if ("a" == instance_name[0] or "b" == instance_name[0]) and len(instance_name)==9:
                        model.addConstrs((z[i.replace("p","d")]-(z[i]+service_time[i])==Li[i]  for i in P), name = "ct.rideTimeConstraintA")
                        model.addConstrs((Li[i]<=Lmax  for i in P), name = "ct.rideTimeConstraintB")

                        #model.addConstrs(((service_time[i]+c[i,j])*x[i,j]<=Lmax  for i in P for j in [a[1] for a in A2.select(i,'*')]), name = "ct.rideTimeConstraintB")
                        model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A1.select(vo,'*')]) <= nVehicles for vo in VO), name = "ct.route_startFirstTrivialLB")

 
                    
            
                
                    # Data for callback
                    model._obj = None
                    model._bd = None
                    model._gap = None
                    model._data = []
                    model._x = x
                    model._start = time.time()
                    #.Params.LazyConstraints = 1
                    #model.Params.Symmetry = 0
                    if heuristic==True:
                        model.Params.MIPFocus = 1
                    if root==True:
                        model.Params.NodeLimit = 1
                    model.Params.TimeLimit = 60*60
                    model.Params.Threads = 16
                    model.update()
                    model.optimize()
                    #model.optimize(callback=checksolution_cb)
                    """
                    if model.Status == GRB.OPTIMAL:
                        for iter2 in range(1):
                                model.setParam(GRB.Param.SolutionNumber, iter2)
                                print('%g ' % model.PoolObjVal, end='\n')
                                for v in model.getVars():
                                     if v.xn > 1e-5:
                                           #print ('%s %g' % (v.varName, v.xn))
                                           print ('%s %g' % (v.varName, v.xn))
                                print("\n")
                        print("\n")
                    """
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
                    
                    vehicle_number = -1
                    if model.Status == GRB.OPTIMAL:
                        vehicle_number = sum(model._x[i, j].x for (i,j) in A1.select("o0","*"))
                        xarcs = plotLocation(df)
                        with open(f"{filename.replace('.txt','')}_sol.txt", "w") as output:
                            output.write(str([a for a in x if x[a].x>0.5]))
                        #sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
                        infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,0,vehicle_number]  
                        #for e in range(nSolutions):
                        for iter2 in range(1):
                                model.setParam(GRB.Param.SolutionNumber, iter2)
                                print('%g ' % model.PoolObjVal, end='\n')
                                for v in model.getVars():
                                     if v.xn > 1e-5:
                                           #print ('%s %g' % (v.varName, v.xn))
                                           print ('%s %g' % (v.varName, v.xn))
                                print("\n")
                        print("\n")
                        
                    elif model.Status == GRB.TIME_LIMIT:
                        if model.SolCount > 0:
                            vehicle_number = sum(model._x[i, j].x for (i,j) in A1.select("o0","*"))
                            xarcs = plotLocation(df)
                            with open(f"{filename.replace('.txt','')}_sol.txt", "w") as output:
                                output.write(str([a for a in x if x[a].x>0.5]))
                            #sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
                            infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,0,vehicle_number]    
                    else:
                        #if model.status==3:
                         #  model.computeIIS()
                          # model.write("infeasible_model.ilp")
                        infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),np.inf, np.inf,model.ObjBound, model.Runtime,0,vehicle_number] 
                    return infos
            
        def solve_iterative(filename):
            start = time.time()
            obj = np.inf
            last_sol = None
            for i in range(5,11):
                infos = solve_pdptw_rais(filename, 300,i,last_sol, True)
                obj = infos[3]
                if obj<np.inf:
                    last_sol=i
            for i in range(11,13):
                infos = solve_pdptw_rais(filename, 600,i,last_sol,True)
                obj = infos[3]
                if obj<np.inf:
                    last_sol=i
            last_time = (60*60 )- (time.time()-start)
            infos = solve_pdptw_rais(filename, last_time ,None,last_sol,True)
            return infos
        
        def solve_RC_instances(filename,edges_cut=None, strCap=True, timeFlow=False):
            global global_vehicle_lb
            global_vehicle_lb = None
            barrier = threading.Barrier(2)
            t1 = threading.Thread(target=solve_pdptw_rais, args=(filename,60*60,edges_cut,None, strCap, timeFlow,True,False, barrier))
            t2 = threading.Thread(target=solve_pdptw_rais, args=(filename,60*60,edges_cut,None, strCap, timeFlow,False,True, barrier))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            global global_infos
            return global_infos
        
        if solve_RC==True:
            return solve_RC_instances(filename,edges_cut=None, strCap=True, timeFlow=False)
        
        if letchford==True:
            solve_pdptw_model_ORLetters_multicommodity()
        elif dahle == True:
                return solve_pdptw_dahle(filename,60*60,cut=edges_cut, strCap=strCap, last_sol=None, timeFlow=timeFlow)
        else:
            if rais == True:
                return solve_pdptw_rais(filename,60*60,cut=edges_cut, strCap=strCap, last_sol=None, timeFlow=timeFlow)
            #return solve_iterative(filename)
            else:
                return solve_pdptw_model_ORLetters(heuristic=False)
        
#print("TF TW reduction")
infos = pdptw_model(filename, rais=True, edges_cut=None, strCap=True, dahle=False, letchford=False,timeFlow=False, solve_RC=False)
#infos = pdptw_model(filename, rais=True, edges_cut=None, strCap=True, dahle=False, letchford=False,timeFlow=True, solve_RC=False)
print(infos)