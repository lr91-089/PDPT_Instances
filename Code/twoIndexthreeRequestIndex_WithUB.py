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
from itertools import combinations
from collections import defaultdict
import threading
import random
#import igraph as ig
from typing import Dict, Set, List, Tuple, Any, Optional
#import ast
from collections import deque


import gurobipy as gp
from gurobipy import Model, GRB, quicksum, tuplelist

#filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-1.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R15-K3-T3/PDPT-R15-K3-T3-Q100-9.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-0.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R30-K2-T2/PDPT-R30-K2-T2-Q100-1.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R30-K2-T1/PDPT-R30-K2-T1-Q100-0.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R10-K3-T3/PDPT-R10-K3-T3-Q100-9.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R7-K3-T3/PDPT-R7-K3-T3-Q100-6.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R5-K2-T1/PDPT-R5-K2-T1-Q100-6.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R5-K2-T2/PDPT-R5-K2-T2-Q100-6.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R5-K3-T3/PDPT-R5-K3-T3-Q100-2.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R25-K3-T3/PDPT-R25-K3-T3-Q100-8.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R5-K2-T2/PDPT-R5-K2-T2-Q100-6.txt"
#filename = "./InstancesLyu23/Examples/example2.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R5-K3-T3/PDPT-R5-K3-T3-Q100-2.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R7-K3-T3/PDPT-R7-K3-T3-Q100-6.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R20-K2-T2/PDPT-R20-K2-T2-Q100-3.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R5-K3-T3/PDPT-R5-K3-T3-Q100-5.txt"


#filename = "./InstancesGhilas/PDPTW_Rewritten/R40K12T1_Ghilas_13.txt"
#filename = "./InstancesGhilas/PDPTW_Rewritten/R20K8T2_Ghilas_2.txt"
#filename = "./InstancesGhilas/PDPTW_Rewritten/R30K12T1_Ghilas_7.txt"
#filename = "./InstancesGhilas/PDPTW_Rewritten/R40K12T1_Ghilas_14.txt"
#filename = "./InstancesGhilas/PDPTW_Rewritten/R50K16T1_Ghilas_17.txt"

#filename = "./InstancesGhilas/PDPTW_Rewritten/R35K10T1_Ghilas_9.txt"
#filename = "./InstancesGhilas/PDPTW_Rewritten/R50K16T1_Ghilas_17.txt"
#filename = "./InstancesGhilas/PDPTW_Rewritten/R30K12T1_1_Ghilas.txt"

#filename = "./InstancesGhilas/PDPTW_Rewritten/R35K10T1_Ghilas.txt"
#filename = "./InstancesGhilas/PDPTW_Rewritten/R50K14T1_1_Ghilas.txt"
#timelimit instances
#filename = "./InstancesLyu23/PDPTWT/5R4K4T/5R-4K-4T-180M-1.txt"
#filename = "./InstancesLyu23/PDPTWT/5R4K4T/5R-4K-4T-180M-9.txt"
#filename = "./InstancesLyu23/PDPTWT/4R4K4T/4R-4K-4T-300L-4.txt"
#filename = "./InstancesLiLim/PDPTWT10/PDPTWT_LiLim_R10K25T0C200_lc101.txt"
#filename = "./InstancesLiLim/PDPTWT10/PDPTWT_LiLim_R10K25T0C200_lr101.txt"


#filename = "./InstancesLiLim/PDPTWT10/PDPTWT_LiLim_R10K10T4C50_lr101.txt"

#filename = "./InstancesLiLim/PDPTWT10/PDPTWT_LiLim_R10K4T4C50_lc106.txt"

#filename = "./InstancesLyu23/PDPT_big/PDPT-R25-K3-T3/PDPT-R25-K3-T3-Q100-8.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R15-K3-T3/PDPT-R15-K3-T3-Q100-9.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R25-K2-T2/PDPT-R25-K2-T2-Q100-6.txt"
"""
filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-2.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R25-K3-T3/PDPT-R25-K3-T3-Q100-3.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R5-K2-T1/PDPT-R5-K2-T1-Q100-9.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R25-K2-T2/PDPT-R25-K2-T2-Q100-5.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R30-K2-T2/PDPT-R30-K2-T2-Q100-7.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R10-K2-T1/PDPT-R10-K2-T1-Q100-8.txt"

#instances are strange
filename = "./InstancesLyu23/PDPT/PDPT-R25-K2-T1/PDPT-R25-K2-T1-Q100-7.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-4.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R25-K3-T3/PDPT-R25-K3-T3-Q100-3.txt"


filename = "./InstancesLyu23/PDPT/PDPT-R5-K2-T1/PDPT-R5-K2-T1-Q100-9.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R25-K3-T3/PDPT-R25-K3-T3-Q100-3.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R5-K2-T1/PDPT-R5-K2-T1-Q100-9.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R30-K2-T2/PDPT-R30-K2-T2-Q100-2.txt"
filename = "./InstancesLiLim/PDPTWT10/PDPTWT_LiLim_R10K4T4C50_lr107.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R25-K2-T2/PDPT-R25-K2-T2-Q100-6.txt"
filename = "./InstancesLyu23/PDPTWT/5R4K4T/5R-4K-4T-180L-8.txt"""

filename = "./InstancesGhilas/HetPDPT_Instances/Small/R_Ghilas_R9K4T1.txt"
filename = "./InstancesGhilas/HetPDPT_Instances/Small/R_Ghilas_R6K4T1.txt"
filename = "./InstancesGhilas/HetPDPT_Instances/Small/C_Ghilas_R11K4T1.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R30-K2-T1/PDPT-R30-K2-T1-Q100-9.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-6.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-2.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-4.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
filename = "./InstancesGhilas/HetBigPDPTWT_OrginalLoads/Ghilas_TC_R50-K16-T1.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
filename = "./InstancesGhilas/OriginalInstances/R25K10T2_1_Ghilas.txt"

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

class SolverState:
    def __init__(self):
        self.model_ub = np.inf
        self.new_solution = {"x":{},"y":{}, "bl":{}}
        self.master_finished = False
        self.cut_pool = set()
        self.mutex = threading.Lock()
        self.infos_sol = []
        self.time_measure = 0


class CapacityHeuristic:
    """
    Capacity Constraint Heuristic based on Wolfinger paper for the PDPSLT.
    Identifies violated capacity constraints for pickup or delivery locations.
    Uses a simplified flow representation with x[i,j] = flow_value.
    Uses a tabu list to prevent cycling of actions.
    """
    
    def __init__(self, 
                 flow_dict: Dict[Tuple[str, str], float], 
                 locations: List[str], 
                 demand_dict: Dict[str, float], 
                 vehicle_capacity: float, 
                 min_violation: float = 0.1,
                 min_set_size: int = 3,
                 max_iterations: int = 25,
                 num_attempts: int = 3,
                 tabu_tenure: int = 5):
        """
        Initialize the capacity heuristic.
        
        Args:
            flow_dict: Dictionary of flow values where keys are (i,j) tuples
            locations: List of location IDs (either pickup or delivery)
            demand_dict: Dictionary of demands where keys are location IDs
            vehicle_capacity: Maximum vehicle capacity (Q)
            min_violation: Minimum violation threshold
            min_set_size: Minimum size of set S to generate a cut
            max_iterations: Maximum iterations per attempt
            num_attempts: Number of attempts with different starting points
            tabu_tenure: Number of iterations a move remains in the tabu list
        """
        self.flow_dict = flow_dict
        self.locations = locations
        self.demand_dict = demand_dict
        self.vehicle_capacity = vehicle_capacity
        self.min_violation = min_violation
        self.min_set_size = min_set_size
        self.max_iterations = max_iterations
        self.num_attempts = num_attempts
        self.tabu_tenure = tabu_tenure
        
    def run(self) -> List[Dict[str, Any]]:
        """
        Run the capacity heuristic to find violated cuts.
        
        Returns:
            List of violated cuts, each containing location set S and violation amount
        """
        violated_cuts = []
        # Keep track of sets we've already added to avoid duplicates
        added_sets = set()
        
        # Run multiple times with different random starting points
        for attempt in range(self.num_attempts):
            # Start with a random location
            if len(self.locations) == 0:
                continue
            # Determine a random size for the subset (between 1 and m-2)
            subset_size = random.randint(3, len(self.locations)-2)
            
            # Select random elements without replacement
            S = set(random.sample(self.locations, subset_size))
            #random_idx = random.randint(0, len(self.locations) - 1)
            #random_loc = self.locations[random_idx]
            
            # Start with a set of 2 locations to encourage larger sets
            #S = {random_loc}
            
            # Try to add one more random location if possible
            #vailable_locs = [loc for loc in self.locations if loc != random_loc]
            #if available_locs:
             #   second_loc = random.choice(available_locs)
              #  S.add(second_loc)
            
            # Calculate initial demand for set S (use absolute value of demand)
            d_S = sum(abs(self.demand_dict[loc]) for loc in S)
            
            # Initialize tabu list - maps location to iteration when it can be considered again
            # Format: {(location, action): iteration_when_free}
            tabu_list = {}
            
            for iteration in range(self.max_iterations):
                # Get the current flow value δ-(S)
                flow_value = self.calculate_delta_minus(S)
                
                # Check if constraint is violated: x(δ-(S)) < ⌈d(S)/Q⌉
                min_required = math.ceil(d_S / self.vehicle_capacity)
                violation = min_required - flow_value
                
                # Only create a cut if the set S is greater than 2 and violation is significant
                if len(S) >= self.min_set_size and violation > self.min_violation:
                    # Convert set to frozenset to make it hashable
                    location_set_frozenset = frozenset(S)
                    
                    # Check if we already added this set
                    if location_set_frozenset not in added_sets:
                        # Found a new violated cut
                        violated_cuts.append({
                            'location_set': list(S),
                            'violation': violation,
                            'required_flow': min_required,
                            'actual_flow': flow_value,
                            'total_demand': d_S
                        })
                        # Add to our set of already added sets
                        added_sets.add(location_set_frozenset)
                
                # Update tabu list - remove expired entries
                current_tabu_list = {}
                for move, free_iteration in tabu_list.items():
                    if free_iteration > iteration:  # still active
                        current_tabu_list[move] = free_iteration
                tabu_list = current_tabu_list
                
                # Try to modify S to find more violated constraints
                best_location = self.find_best_location_change(S, d_S, tabu_list, iteration)
                
                if best_location is None:
                    break  # No improvement possible
                
                # Update S and d_S based on the best location change
                if best_location['action'] == 'add':
                    loc = best_location['location']
                    S.add(loc)
                    d_S += abs(best_location['demand'])
                    
                    # Add to tabu list - can't remove this location for tabu_tenure iterations
                    tabu_list[(loc, 'remove')] = iteration + self.tabu_tenure
                else:
                    loc = best_location['location']
                    # Only remove if it doesn't make the set too small
                    if len(S) > self.min_set_size:
                        S.remove(loc)
                        d_S -= abs(best_location['demand'])
                        
                        # Add to tabu list - can't add this location for tabu_tenure iterations
                        tabu_list[(loc, 'add')] = iteration + self.tabu_tenure
                    else:
                        break  # Can't improve without making set too small
        
        return violated_cuts
    
    def calculate_delta_minus(self, S: Set[str]) -> float:
        """
        Calculate the flow into set S (δ-(S)) from the current solution.
        
        Args:
            S: Set of locations
            
        Returns:
            Flow value
        """
        flow_value = 0.0
        
        # Examine all arcs in the flow dictionary
        for (from_node, to_node), flow in self.flow_dict.items():
            if from_node not in S and to_node in S:
                flow_value += flow
        
        return flow_value
    
    def find_best_location_change(self, S: Set[str], d_S: float, tabu_list: Dict[Tuple[str, str], int] = None, current_iteration: int = 0) -> Optional[Dict[str, Any]]:
        """
        Find the best location to add to or remove from set S, respecting tabu restrictions.
        
        Args:
            S: Current set of locations
            d_S: Current total demand of set S
            tabu_list: Dictionary of tabu moves with their release iterations
            current_iteration: Current iteration number
            
        Returns:
            Best non-tabu location change or None if no improvement
        """
        if tabu_list is None:
            tabu_list = {}
            
        best_value = 0.0
        best_location = None
        
        # Try adding locations not in S
        for loc in self.locations:
            if loc not in S:
                # Check if this move is in the tabu list
                if (loc, 'add') in tabu_list and tabu_list[(loc, 'add')] > current_iteration:
                    continue
                    
                # Calculate the impact of adding this location (use absolute value of demand)
                demand = abs(self.demand_dict[loc])
                new_demand = d_S + demand
                old_required = math.ceil(d_S / self.vehicle_capacity)
                new_required = math.ceil(new_demand / self.vehicle_capacity)
                
                # Calculate the change in flow for adding this location
                delta_flow = self.calculate_flow_delta_for_addition(S, loc)
                
                # Calculate improvement (higher is better)
                improvement = (new_required - old_required) - delta_flow
                
                if improvement > best_value:
                    best_value = improvement
                    best_location = {
                        'action': 'add',
                        'location': loc,
                        'demand': self.demand_dict[loc]
                    }
        
        # Try removing locations from S (only if it doesn't make the set too small)
        if len(S) > self.min_set_size:
            for loc in list(S):
                # Check if this move is in the tabu list
                if (loc, 'remove') in tabu_list and tabu_list[(loc, 'remove')] > current_iteration:
                    continue
                    
                # Use absolute value of demand
                demand = abs(self.demand_dict[loc])
                
                # Calculate the impact of removing this location
                new_demand = d_S - demand
                
                # Don't allow sets with zero/negative demand
                if new_demand <= 0:
                    continue
                
                old_required = math.ceil(d_S / self.vehicle_capacity)
                new_required = math.ceil(new_demand / self.vehicle_capacity)
                
                # Calculate the change in flow for removing this location
                delta_flow = self.calculate_flow_delta_for_removal(S, loc)
                
                # Calculate improvement (higher is better)
                improvement = (old_required - new_required) + delta_flow
                
                if improvement > best_value:
                    best_value = improvement
                    best_location = {
                        'action': 'remove',
                        'location': loc,
                        'demand': self.demand_dict[loc]
                    }
        
        return best_location
    
    def calculate_flow_delta_for_addition(self, S: Set[str], location: str) -> float:
        """
        Calculate the change in flow value when adding a location to set S.
        
        Args:
            S: Current set
            location: Location to add
            
        Returns:
            Change in flow
        """
        delta = 0.0
        
        # Examine arcs to/from the location
        for (from_node, to_node), flow in self.flow_dict.items():
            if to_node == location and from_node not in S:
                delta += flow  # This arc will become internal to S
            if from_node == location and to_node in S:
                delta -= flow  # This arc will become internal to S
        
        return delta
    
    def calculate_flow_delta_for_removal(self, S: Set[str], location: str) -> float:
        """
        Calculate the change in flow value when removing a location from set S.
        
        Args:
            S: Current set
            location: Location to remove
            
        Returns:
            Change in flow
        """
        delta = 0.0
        
        # Examine arcs to/from the location
        for (from_node, to_node), flow in self.flow_dict.items():
            if to_node == location and from_node in S:
                delta -= flow  # This arc will no longer be internal to S
            if from_node == location and to_node in S:
                delta -= flow  # This arc will no longer be internal to S
        
        return -delta  # Negate because we're removing, not adding


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
    if "Ghilas" in filename:
        last_row = df.shape[0]-1
        #for i in range(1,3):
         #   df.loc[df.shape[0]] = df.loc[last_row]
          #  df.at[df.shape[0]-1,"node"] = f"t{i}"
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
                copy['node'] = copy['node'].replace('t', f'tsr.{r}.')
                df = df._append(copy, ignore_index = True)
                copy['node'] = copy['node'].replace('ts', 'tf')
                copy['s'] = 0
                df = df._append(copy, ignore_index = True)
                copy = row.copy()
                if r <nvehicles:
                    copy['node'] = copy['node'].replace('t', f'tsc.{r}.')
                    df = df._append(copy, ignore_index = True)
                    copy['node'] = copy['node'].replace('ts', 'tf')
                    copy['s'] = 0
                    df = df._append(copy, ignore_index = True)
                
    
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
def calculateDistance(x1, x2, y1, y2, precision=False):
    if precision==True:
        #return math.sqrt((x2 - x1)**2 + (y2-y1)**2)
        return float(np.round(math.sqrt((x2 - x1)**2 + (y2-y1)**2),2))
    return math.sqrt((x2 - x1)**2 + (y2-y1)**2)

# one unit of distance can be traveled in one time unit
def distancesMatrix(df, ghilas=False):
    matrix = {}
    for location1 in df["node"]:
        for location2 in df["node"]:
            if location1 != location2:
                x1 = df.loc[df["node"]==location1, 'x'].values[0]
                x2 = df.loc[df["node"]==location2, 'x'].values[0]
                y1 = df.loc[df["node"]==location1, 'y'].values[0]
                y2 = df.loc[df["node"]==location2, 'y'].values[0]
                if ghilas==True:
                    matrix[location1,location2] = calculateDistance(x1, x2, y1, y2, precision=True)
                else:
                    matrix[location1,location2] = calculateDistance(x1, x2, y1, y2)
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





# Model
def twoIndexModelUB(filename,timeFlow=False, mode="two",symm=False, MULTI_TRANS=False):
    
    print(filename)
    
    metaData = readMetaData(filename)
    HET = False
    if "Ghilas" in filename or MULTI_TRANS:
        df = readDataframeHet(filename,int(metaData["nr"]))
        if MULTI_TRANS==False:
            HET = True
    else:
        df = readDataframe(filename)
    nodeList = getNodeList(df)
    if "Ghilas" in filename:
        ghil = True
    else:
        ghil = False
    
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
        TSC = frozenset(df.loc[df['node'].str.contains('tsc'),'node'])
        TFC = frozenset(df.loc[df['node'].str.contains('tfc'),'node'])
    
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
    #if "Lim" in filename:
     #   K = range(4)
    
    df["points"] = df[["x","y"]].values.tolist()

    points = df.set_index("node")["points"].to_dict()
    
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
    
    if "Lim" in filename:
        service_time = pd.Series(df.s.values,index=df.node).to_dict()
    
    R = list(range(nRequests))
    
    if VC<0:
        c = distancesMatrix(df, ghilas=True)
        #c = distancesMatrix(df)
    else:
        c = distancesMatrix(df)
    
    k = pd.RangeIndex(nVehicles)
    r = pd.RangeIndex(nRequests)
    u = pd.Series(index=k, data=np.full(nVehicles, VC))
    qnode = df.set_index('node')["load"].to_dict()
    q = {int(node.replace("p","")):qnode[node] for node in P}
    
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
            timeWindows[l][0] = float(np.round(max(timeWindows[l][0], min(timeWindows[l][1],min(timeWindows[i][0]-c[l,i]-service_time[l] for i in succset if l!=i))),2))
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
        for i in TS:
            r = int(i.split(".")[1])
            a = min(timeWindows[f"p{r}"][0]+c[f"p{r}",i]+service_time[f"p{r}"],timeWindows[f"d{r}"][1])
            b = max(0+service_time[i],timeWindows[f"d{r}"][1]-c[i.replace("s","f"),f"d{r}"]-service_time[i])
            if a+service_time[i]>b:
                #print(i)
                a = 0
                b = a+service_time[i]
            timeWindows[i][0] = a
            timeWindows[i][1] = b
            timeWindows[i.replace("s","f")][0] = a
            if "tsr" in i and a>0:
                b = max(timeWindows[ed][1]-c[i.replace("s","f"),ed]-service_time[i]-service_time[ed] for ed in VD)
            timeWindows[i.replace("s","f")][1] = b#"""
   
    
   
    #change travel times
    def check_no_time_window_violation(i,j):
        #returns true if no time window violation
        if VC<0:
            if i not in VO:
                if timeWindows[i][0]+service_time[i]+t[i,j]<=timeWindows[j][1]+service_time[j]:
                    return True
            else:
                if timeWindows[i][0]+t[i,j]<=timeWindows[j][1]+service_time[j]:
                    return True
        else:
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
                #t[i,j] = timeWindows[j][0]-timeWindows[i][1]-service_time[i]
                n1+=1
    print("Increased ",n1, " arcs.")
    
    
    min_vec = VC
    if VC<0:
        min_vec = Qmax

    
    arcs = []
    ats = set()
    for i in VO:
        for j in P:
            if check_no_time_window_violation(i,j)==True:
                arcs.append((i,j))
        for j in TS:
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
    

    for i in D:
        for j in P|VD|TS:
            if not (j in P and i == j.replace("p","d")):
                if check_no_time_window_violation(i,j)==True:
                    arcs.append((i,j))
        for j in D:
            if not (i == j or (j in P and i == j.replace("p","d"))):
                if check_no_time_window_violation(i,j)==True:
                    if abs(qnode[i])+abs(qnode[j])<=min_vec:
                        arcs.append((i,j))

    for i in TS:
        for j in TF:
            if i == j.replace("f", "s"):
                arcs.append((i,j))
                ats.add((i,j))

    for i in TF:
        k = int(i.split(".")[-1])
        for j in P|D|VD:
            if check_no_time_window_violation(i,j)==True:
                arcs.append((i,j))
        for j in TS:
            if j.split(".")[2]!=i.split(".")[2]:
                if j.split(".")[1]==i.split(".")[1]:
                    if check_no_time_window_violation(i,j)==True:
                        arcs.append((i,j))    


   
    #eleminate arcs by Cordeau 2006 (DARP paper)
    #only valid for the PDPTW, but not PDPT?
    
    def check_feasibility(path):
        i = path[0]
        if i in VO:
            z = timeWindows[i][0]
        else:
            z = timeWindows[i][0]
        for j in path[1:]:
            if (i,j) in arcs:
                if VC<0:
                    z = max(z+service_time[j]+t[i,j],timeWindows[j][0])
                    if z-service_time[j]>timeWindows[j][1]:
                        #return True
                        return False
                else:
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
                        
    
    print("remove ",len(remove_arcs)," arcs")
    #don't remove infeasible arcs yet
    #arcs = set(arcs)-remove_arcs
    arcs = list(dict.fromkeys(arcs))
    
    #A = [(i,j) for i in V for j in V if i!=j]
    
    A = tuplelist(arcs)
    
    Ayc = [(i,j,r) for r in R for i in P for j in V-(frozenset((i,f"p{r}"))|VO|VD|TF) if (i,j) in A]
    Ayd = [(i,j,r) for r in R for i in D-frozenset(("d"+str(r),)) for j in (V-frozenset([i,i.replace("d","p"),f"p{r}"])-VO-VD-TF) if (i,j) in A]
    if HET==True or MULTI_TRANS:
        Ayts = [(i,j,r) for r in R for i in TSR for j in TF_loc[int(i.split(".")[2])]]
    else:
        Ayts = [(i,j,r) for r in R for i in TS for j in TF_loc[int(i.split(".")[2])]]
    Aytf = [(i,j,r) for r in R for i in TF for j in V-(frozenset((i,f"p{r}"))|VO|VD|TF|frozenset(TS_loc[int(i.split(".")[2])])) if (i,j) in A]

    
    Ay = Ayc+Ayd+Ayts+Aytf
      
    
    #print(Ay[('d1', 'p1',1)])
    
    Ay = tuplelist(Ay)
    TIy = {(i,j) for (i,j,r) in Ayts if i!=j.replace("f","s")}

    #print(Ay)
    
    #print(Ay)

    
    
    

    

    #xc = df.set_index('node').x.to_dict()
    #yc = df.set_index('node').y.to_dict()
    #c = {(i, j): float(np.hypot(xc[i]-xc[j], yc[i]-yc[j]).round(2)) for i, j in A}
    
   
    #print(c["tf.0.0","ts.1.0"])



    

    xIndex = [(i, j) for (i,j) in arcs]
    kIndex = [(i,r) for r in K for i in V]
    if timeFlow==True:
        zIndex = [(i, j) for (i,j) in arcs]
    else:
        zIndex = [i for i in V]
    aIndex = [(i,r) for i in TS|TF for r in pd.RangeIndex(nRequests) ]
    
    
    
        
    print(df)
    
    Mij = {(i,j):max(0,timeWindows[i][1]+t[i,j]+service_time[i]-timeWindows[j][0]) for (i,j) in c}
    wbTW = {(i,j):min(timeWindows[i][1],timeWindows[j][1]-t[i,j]-service_time[i]) for (i,j) in arcs}
    M = max(Mij.values())
    #Mt = {(i,j):(timeWindows[i][1]-t[i.replace("s","f"),"e"+i.split(".")[1]])-max(t["o"+j.split(".")[1].replace("f","s"),i],timeWindows[j][0]) for i in TS for j in TF}
    #Mtr = {(i,j,r):min(timeWindows[f"d{r}"][1]-t[j,f"d{r}"],timeWindows[j][1]) for (i,j) in TIy for r in R}


    kArcs = tuplelist([(i,j,k) for (i,j) in arcs for k in K])
    
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
    

    def checksolution_cb(model, where):
         ###MIPSOL callback
         if where == GRB.Callback.MIPSOL:
             eliminate_precedence(model)
             
    def usercut_cb(model, where):
        if where == GRB.Callback.MIPNODE:
          status = model.cbGet(GRB.Callback.MIPNODE_STATUS)
          if status == GRB.OPTIMAL:
            xrel = model.cbGetNodeRel(model._x)
            for i in TS:
                if quicksum(xrel[j,i] for j in [a[0] for a in A.select("*",i)]).getValue()>1.0:
                   model.cbCut(quicksum(xrel[j,i] for j in [a[0] for a in A.select("*",i)]) <= 1)
            frel = model.cbGetNodeRel(model._f)
            #yrel = model.cbGetNodeRel([model._y])
            
            for n in TS_loc:
                if frel[f"ts{n}"]>1.0:
                    #model.cbCut(frel[f"ts{n}"] <= quicksum(yrel[i,j,r] for r in R for i in TS_loc[n] for j in [a[1] for a in Ay.select(i,'*',r) if a[1].replace("f","s")!=i]))
                    model.cbCut((2*frel[f"ts{n}"] <= quicksum(xrel[j,i] for i in TS_loc[n] for j in [a[0] for a in A.select('*',i)]))) 
 
                
    def pdp_cb(model, where):
        if where == gp.GRB.Callback.MIPSOL:
            cur_obj = model.cbGet(gp.GRB.Callback.MIPSOL_OBJ)
            if cur_obj < model._solver_state.model_ub:
                model._solver_state.model_ub = cur_obj
                #print("update best sol", model_ub)
                start = time.time()
                with model._solver_state.mutex:
                    model._solver_state.new_solution = {"x":{},"y":{}}
                    all_x_vars = model.cbGetSolution(model._x)
                    all_y_vars = model.cbGetSolution(model._y)
                    for a in model._A2:
                            model._solver_state.new_solution["x"][a] = all_x_vars[a]
                    for a in model._Ay2:
                            model._solver_state.new_solution["y"][a] = all_y_vars[a]

                model._solver_state.time_measure += time.time()-start
        if where == gp.GRB.Callback.MIP:
            if model._solver_state.master_finished==True:
                model.terminate()
                
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
            q_val = 0
            z_val = 0.0
            for u,v in tour:
                q_val = sum(q[r]*arcsy.get((u,v,r),0) for r in range(nRequests))
                if VC<0:
                    Q_vehicle = Qmax-model._vl[v].x
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
             
    def create_pdptw_model(filename, cut=None, strCap=True,timeFlow=False, env=None, state=None):
             #if barrier!=None:
              #   barrier.wait()    
             if env==None:
                 model1 = gp.Model()
             else:
                 model1 = gp.Model(env=env)
             infostr = ""
             if strCap==True:
                 infostr += "StrCap"
             if timeFlow==True:
                 infostr += "timeFlow"
             model1 = Model('PDPTW_Rais'+infostr)
             model1._solver_state = state
             arcs_keep = set()
             arcs = []


             for i in VO:
                for j in P:
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
            
            
             for i in D:
                for j in P|VD:
                    if not (j in P and i == j.replace("p","d")):
                        if check_no_time_window_violation(i,j)==True:
                            arcs.append((i,j))
                for j in D:
                    if not (i == j or (j in P and i == j.replace("p","d"))):
                        if check_no_time_window_violation(i,j)==True:
                            if abs(qnode[i])+abs(qnode[j])<=min_vec:
                                arcs.append((i,j))
             
             #eleminate arcs by Cordeau 2006 (DARP paper)
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
              

             
             print("remove ",len(remove_arcs)," arcs")
             #arcs = set(arcs)-remove_arcs
             arcs = list(dict.fromkeys(arcs))
             
             #A = [(i,j) for i in V for j in V if i!=j]
             
             A = tuplelist(arcs)
             for i in V-VD-VO:
                 edges = A.select(i,"*")
                 if i in P:
                     arcs_keep.add((i,i.replace("p","d")))
                 costs = {e:c[e] for e in edges}
                 #sort by cost
                 costs = sorted(costs.items(), key=lambda x: x[1])
                 if cut==None:
                     edges_cut  = len(edges)
                 else:
                     if cut >0:
                         edges_cut = cut
                     else:
                         edges_cut  = int(np.ceil(len(edges)/(cut*(-1))))
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
              
              
             x = model1.addVars(A2, vtype=GRB.BINARY, name='x')
             y = model1.addVars(Ay2, vtype=GRB.BINARY, name='y')
             #Idee wenn zwei vehicle unterschiedliche StartPositionen haben, b trackt vehicle flow
             #bl = model1.addVars(kArcs, vtype=GRB.BINARY, name='bl')
             if "Sartori" not in filename:
                 bl = model1.addVars(V, vtype=GRB.CONTINUOUS, name='bl')
             if VC < 0:
                vl = model1.addVars(V,lb=0.0,ub=Qmax, vtype=GRB.CONTINUOUS, name='vl') 
              
             #b = model1.addVars(xIndex,lb=0.0, ub=nVehicles ,vtype=GRB.CONTINUOUS, name="b")

             if timeFlow==True:
                 z = model1.addVars(A2,lb=0.0 ,vtype=GRB.CONTINUOUS, name="z")
             else:
                 z = model1.addVars(zIndex,lb=0.0 ,vtype=GRB.CONTINUOUS, name="z")
             #a = model1.addVars([(i,r) for i in TS for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="a")
             bz = model1.addVars(zIndex,lb=0.0 ,vtype=GRB.CONTINUOUS, name="bz")
             #ba = model1.addVars([(i,r) for i in TF for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="ba")
             if VC<0:
                 model1.setObjective(quicksum(c[i,j]* x[i, j] for (i,j) in A2))
             else:
                 #if "Lim" in filename:
                    # model1.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in A2)+quicksum(pow(10,4) * x[i, j] for (i,j) in A2 if i in VO))
                # else:
                     model1.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in A2))
             model1.update()
             
             
             """
             Restrict flows
             """
             #model1.addConstrs(x[e]==0 for e in A2)
             #model1.addConstrs(y[e]==0 for e in Ay2)
             #model1.addConstrs((quicksum(x[i,j] for j in [a[1] for a in A2.select(i,'*')])==0 for i in TS|TF),name="remove_transfer_arcs")
             #model1.addConstrs((quicksum(x[i,j] for i in [a[0] for a in A2.select('*',j)])==0 for j in TS|TF),name="remove_transfer_arcs_j")
              
             #model1.addConstrs((quicksum(y[i,j,r] for r in R for j in [a[1] for a in Ay2.select(i,'*',r)])==0 for i in TS|TF),name="remove_transfer_arcs_y")
             #model1.addConstrs((quicksum(y[i,j,r] for r in R for i in [a[0] for a in Ay2.select('*',j, r)])==0 for j in TS|TF),name="remove_transfer_arcs_y_j")
              
              
              
             """
             Arc flows
             """
             if "Sartori" in filename:
                 model1.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) <= float(np.ceil(sum(qnode[i] for i in P)/VC)) for vo in VO), name = "ct.route_startFirst")
                 #model1.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) <= len(P) for vo in VO), name = "ct.route_UB")
                 model1.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A2.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
                 
             else:
                 if "Lim" not in filename:
                     model1.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) == 1 for vo in VO), name = "ct.route_startFirst")
                 model1.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A2.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A2.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
                 
             
             
             model1.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A2.select('*',i)]) == 1 for i in P), name = "ct.PickupJustOnce")
             
             model1.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A2.select('*',i)]) == 1 for i in D), name = "ct.DeliveryJustOnce")
             
                 
             
             model1.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A2.select('*',i)]) == quicksum(x[i,j] for j in [a[1] for a in A2.select(i,'*')])   for i in P|D), name = "ct.FlowConversion")
             
              
             
             """
             Loads
             """
             
             model1.addConstrs((quicksum(y[i, j, r] for j in [a[1] for a in Ay2.select(i,'*',r)])  == 1 for r in R for i in [f"p{r}"]), name = "ct.visit_request_originOut")
             
             
             model1.addConstrs((quicksum(y[j,i, r] for j in [a[0] for a in Ay2.select('*',i,r)])  == 1 for r in R for i in [f"d{r}"]), name = "ct.visit_request_destinationIn")
              
             
             model1.addConstrs((quicksum(y[i, j,r] for j in [a[1] for a in Ay2.select(i,'*',r)])-quicksum(y[j,i,r] for j in [a[0] for a in Ay2.select('*',i,r)]) == 0 for r in R for i in V-(VD|VO|frozenset((f"p{r}","d{r}"))) if i not in ["p"+str(r),"d"+str(r)]), name = "ct.requestFlowConversion")
             
             
             model1.addConstrs((y[i,j,r] <= x[i,j] for r in R for i in V for j in [a[1] for a in Ay2.select(i,'*',r)]), name = "ct.request_flow_link")
             
              
                
             """
             Capacity constraint
             """
             # capacity constraint
             if VC>0:
                 if strCap==True:
                     # Strengthened capacity constraints
                     model1.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-abs(qnode[i]+qnode[j]))*x[i,j] for i in P for j in [a[1] for a in A2.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong1")
                     model1.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-abs(qnode[i]+qnode[j]))*x[i,j] for i in D for j in [a[1] for a in A2.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong2")
                     model1.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in P for j in [a[1] for a in A2.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong3")
                     model1.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in D for j in [a[1] for a in A2.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong4")
                     model1.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if r!=int(i.replace("p","").replace("d","")) and j in [a[1] for a in Ay2.select(i,'*',r)]) <= (VC-abs(qnode[i]))*x[i,j] for i in P|D  for j in [a[1] for a in A2.select(i,'*')]), name="ct.VehicleCapacityStrong2")
                 else:
                     # capacity constraint
                     model1.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)]) <= VC*x[i,j] for i in P|D for j in [a[1] for a in Ay2.select(i,'*',r)]), name="ct.VehicleCapacity")
             else:
                 model1.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (Qmax-abs(qnode[i]+qnode[j]))*x[i,j] for i in P for j in [a[1] for a in A2.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong1")
                 model1.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (Qmax-abs(qnode[i]+qnode[j]))*x[i,j] for i in D for j in [a[1] for a in A2.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong2")
                 model1.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (Qmax-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in P for j in [a[1] for a in A2.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong3")
                 model1.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay2.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (Qmax-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in D for j in [a[1] for a in A2.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong4")
                
                 model1.addConstrs((vl[f"o{k}"]  == vec_capacities[k] for k in K), name = "ct.route_startVehicleCapLabelStart")
                 
                 model1.addConstrs((vl[f"e{k}"]  == vec_capacities[k] for k in K), name = "ct.route_startVehicleCapLabelEnd")
                 
                
                 
                 model1.addConstrs((vl[i]-(max(vec_capacities[k]-vec_capacities[l] for k in K for l in K if k!=l))*(1-x[i,j])<=vl[j] for i in V for j in [a[1] for a in A2.select(i,'*')] if (j,i) not in A2), name = "ct.vehicleCapLabelFlowA")
                 
                 model1.addConstrs((vl[i]-vl[j]<=(max(vec_capacities[k]-vec_capacities[l] for k in K for l in K if k!=l))*(1-x[i,j]-x[j,i]) for i in V for j in [a[1] for a in A2.select(i,'*')] if (j,i) in A2), name = "ct.vehicleCapLabelFlowA")

               
                 model1.addConstrs((vl[j]-(max(vec_capacities[k]-vec_capacities[l] for k in K for l in K if k!=l))<=vl[i]  for i in V for j in [a[1] for a in A2.select(i,'*')] if (j,i) not in A2), name = "ct.vehicleCapLabelFlowB")
                
                 model1.addConstrs((quicksum(q[r]*y[i, j,r] for r in R for j in [a[1] for a in Ay2.select(i,'*',r)]) <= Qmax-vl[i] for i in P|D), name="ct.VehicleCapacity")
                
         
                
             
             """
             Vehicle Flow Burger
             """
             if "Sartori" not in filename:
                 model1.addConstrs((bl[f"o{k}"]  == k+1 for k in K), name = "ct.route_startVehicleLabel")
                 
                 model1.addConstrs((bl[f"e{k}"]  == k+1 for k in K), name = "ct.route_startVehicleLabel")
                     
                 
                 #model1.addConstrs((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j] for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.vehicleLabelFlowA")
                     
                 #model1.addConstrs((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]  for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.vehicleLabelFlowB")
                 for i in V-VD:
                     for j in [a[1] for a in A2.select(i,'*')]:
                         if (j,i) in A2:
                             model1.addConstr((bl[i]-(len(K)-1)*(1-x[i,j]-x[j,i])<=bl[j]), name = "ct.vehicleLabelFlowLifted")
                         else:
                             model1.addConstr((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j]), name = "ct.vehicleLabelFlowA")
                             model1.addConstr((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]), name = "ct.vehicleLabelFlowB")
             
              
             
                         
             if timeFlow==True:
                        model1.addConstrs(
                           (
                               gp.quicksum(
                                   z[i, j] + (t[i,j]+service_time[i]) * x[i, j]
                                   for i in P|D|VO
                                   if (i, j) in A2
                               )
                               <= z.sum(j,"*")
                               for j in P|D
                           ),
                               name="ct.time_flowA",
                         )
                        """
                        Time Windows
                        """
                        model1.addConstrs(
                        (
                            z[i, j] >= timeWindows[i][0] * x[i, j]
                            for (i, j) in A2
                        ),
                        name="timeWindowStart",
                        )
                        
                        model1.addConstrs(
                            (
                                z[i, j] <= wbTW[i,j]* x[i, j]
                                for (i, j) in A2
                            ),
                            name="timeWindowEnd",
                        )
   
             else:
                 model1.addConstrs((bz[i]+t[i,j]-(Mij[i,j])*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A2.select(i,'*')] if (j,i) not in A2), name = "ct.time_flowA")
                 #lifted
                 model1.addConstrs((bz[i]-z[j]+Mij[i,j]*x[i,j]+(Mij[i,j]-t[i,j]+min(-t[j,i],timeWindows[j][0]-timeWindows[i][1]))*x[j,i]<= Mij[i,j]-t[i,j]  for i in V for j in [a[1] for a in A2.select(i,'*')] if (j,i) in A2), name = "ct.time_flowLifted")
                 
                 #model1.addConstrs((bz[i]+service_time[i]+c[i,j]-Mij[i,j]*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A2.select(i,'*')]), name = "ct.time_flowA")
                 
                 #model1.addConstrs((bz[i]+c[i,j]-Mij[i,j]*(1-x[i,j])+(Mij[i,j]-c[i,j]+min(-c[j,i],timeWindows[j][0]-timeWindows[i][0]))*x[j,i]<= z[j] for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.time_flowLifted")
                 
                  
                 model1.addConstrs((z[i]+service_time[i] <= bz[i] for i in V), name='ct.DepartureA')
                     
                 
                 """
                 Time Windows
                 """
                 #model1.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliest")
                 #model1.addConstrs((min(max(timeWindows[f"e{k}"][1]-c[i,f"e{k}"] for k in K),timeWindows[i][1]) >= bz[i]-service_time[i] for i in V-VD), name="ct.TimeWindowLatest")
                 model1.addConstrs((timeWindows[i][1] >= bz[i] for i in V), name="ct.TimeWindowLatestVD")
                # model1.addConstrs((timeWindows[i][0] <= a[i,r] for r in R for i in TS), name="ct.RtimeWindowEarliest")
                 #model1.addConstrs((timeWindows[i][1] >= a[i,r] for r in R for i in TS), name="ct.RTimeWindowLatest")
                 
                 #model1.addConstrs((min([max(timeWindows[i][0],c[f"o{k}",i]) for k in K]) <= z[i] for i in V-VO), name="ct.timeWindowEarliestbVO")
                 model1.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliestb")
 
             
             # Data for callback
             model1._obj = None
             model1._bd = None
             model1._gap = None
             model1._data = []
             model1._x = x
             model1._A2 = A2
             model1._Ay2 = Ay2
             model1._VO = VO
             model1._V = V
             model1._y = y
             model1._z = z
             model1._bz = bz
             model1._timeFlow = timeFlow
             if VC<0:
                 model1._vl = vl
             model1._vars = model1.getVars()
             if "Sartori" not in filename:
                 model1._bl = bl
             model1._start = time.time()
             model1.Params.MIPFocus = 1
             model1.Params.OutputFlag = 0
             model1.Params.LogToConsole=0
             return model1
    
    def solve_pdptw(model1,timelim, barrier=None,cut=None,last_sol=None, sollim=None, timeFlow=False):
        if last_sol!=None:
            try:
                model1.NumStart = 1
                model1.read(f"{filename}_{last_sol}.sol")
            except:
                model1.NumStart = -1
                print("no initial solution exists")
            
        #model1.Params.OutputFlag = 0
        #model1.Params.LogToConsole=0
        #model1.Params.LazyConstraints = 1
        #model1.Params.Symmetry = 0
        if sollim!=None:
            model1.Params.SolutionLimit = sollim
        model1.Params.TimeLimit = timelim
        model1.Params.Threads= 4
        """
        model1.NumStart = 1
        model1.update()
        
        sol1 = [["o0","p30","p43", "p34", "d30","p15","d15","p31" ,"d31" ,"p18" ,"d34" ,"d43" ,"d18","e0"],['o0', 'p28', 'p20', 'd20', 'p26', 'p46', 'd28', 'p10', 'p21', 'd46', 'd26', 'd21', 'p5', 'd10', 'p24', 'd5', 'd24', 'p0', 'd0', 'e0'], ['o0', 'p39', 'p47', 'p8', 'd8', 'p4', 'd4', 'd39', 'd47', 'p40', 'p7', 'p9', 'd40', 'd9', 'p37', 'p27', 'd27', 'd37', 'd7', 'e0'], ['o0', 'p25', 'd25', 'p29', 'd29', 'p6', 'p38', 'd6', 'p41', 'd41', 'p11', 'd38', 'p17', 'd11', 'd17', 'p36', 'p35', 'd36', 'p49', 'd49', 'd35', 'e0'], ['o0', 'p13', 'p14', 'd13', 'p48', 'p44', 'p42', 'd14', 'p3', 'd48', 'p45', 'd44', 'd45', 'd3', 'd42', 'p22', 'd22', 'e0'], ['o0', 'p32', 'p12', 'd12', 'p19', 'd32', 'p16', 'd16', 'p1', 'p33', 'd1', 'd33', 'p23', 'd19', 'd23', 'p2', 'd2', 'e0']]
        
        # iterate over all MIP starts
        for s in range(model1.NumStart):
          
            # set StartNumber
            model1.params.StartNumber = s
        
            # now set MIP start values using the Start attribute, e.g.:
            for route in sol1:
                for i in range(len(route[:-1])):
                        j = i+1
                        model1._x[route[i],route[j]].Start = 1.0"""
                        
 
            
        model1.update()
        if barrier!=None:
            barrier.wait()
        model1.optimize(callback=pdp_cb)
        #print("solved PDPTW", cut)
        error_msg = ""
        vehicle_number = -1
        if model1.Status == GRB.OPTIMAL:
            model1.write(f"{filename}_{cut}.sol")
            #sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
            sol_check, error_msg = check_tours(model1)
            vehicle_number = sum(model1._x[i, j].x for o in model1._VO for (i,j) in model1._A2.select(o,"*"))
            infos = [filename, model1.ModelName ,gurobi_status_dict.get(model1.Status),model1.ObjVal, model1.MIPGap,model1.ObjBound, model1.Runtime,0, vehicle_number,error_msg]  
            for iter2 in range(0):
                    model1.setParam(GRB.Param.SolutionNumber, iter2)
                    print('%g ' % model1.PoolObjVal, end='\n')
                    for v in model1.getVars():
                         if "z" in v.varName:
                             if v.xn > 1e-5:
                                   #print ('%s %g' % (v.varName, v.xn))
                                   print ('%s %g' % (v.varName, v.xn))
                    print("\n")
            print("\n")
            
        elif model1.Status == GRB.TIME_LIMIT:
            if model1.SolCount == 0:
                sol_transfers = None
                infos = [filename, model1.ModelName ,gurobi_status_dict.get(model1.Status),model1.ObjVal, model1.MIPGap,model1.ObjBound, model1.Runtime,0,vehicle_number,error_msg]    
            else:
                model1.write(f"{filename}_{cut}.sol")
                sol_check, error_msg = check_tours(model1)
                vehicle_number = sum(model1._x[i, j].x for o in model1._VO for (i,j) in model1._A2.select(o,"*"))
                infos = [filename, model1.ModelName ,gurobi_status_dict.get(model1.Status),model1.ObjVal, model1.MIPGap,model1.ObjBound, model1.Runtime,0,vehicle_number,error_msg]   
        else:
            #if model1.status==3:
             #  model1.computeIIS()
              # model1.write("infeasible_model.ilp")
            infos = [filename, model1.ModelName ,gurobi_status_dict.get(model1.Status),np.inf, np.inf,np.inf, model1.Runtime,0,vehicle_number,error_msg] 
        return infos
    
    
    def build_igraph_graph(edges, VD, VO):
        g = ig.Graph(directed=True)
        nodes = set([u for e in edges for u in e] + list(VD) + list(VO) + ["source", "target"])
        node_map = {v: i for i, v in enumerate(nodes)}
        g.add_vertices(len(nodes))
    
        capacity = []
        edge_list = []
    
        for u, v in edges:
            edge_list.append((node_map[u], node_map[v]))
            capacity.append(edges[(u, v)])
    
        for o in VD:
            edge_list.append((node_map[o], node_map["target"]))
            capacity.append(1.0)
    
        for o in VO:
            edge_list.append((node_map["source"], node_map[o]))
            capacity.append(1.0)
    
        g.add_edges(edge_list)
        g.es['capacity'] = capacity
        return g, node_map
    
    def exact_subtour_elemination(model,edges,f, mipsol=False):
        return False
        added_st_cut = False
        g, node_map = build_igraph_graph(edges, VD, VO)
        for u in model._D | model._P:
            result = g.st_mincut(node_map[u], node_map["target"], capacity='capacity')
            cut_value = result.value
            partition = result.partition
            if cut_value < 1 - 1e-1:
                rev_node_map = {idx: name for name, idx in node_map.items()}
                print("ST user cut",cut_value, u)
                for part in partition:
                    if node_map["target"] in part:
                        S_comp = part
                    else:
                        S = part
                S = {rev_node_map[i] for i in S}
                S_comp = V-S
                model.cbCut(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A)>=1)
                #cut_pool.append((S,S_comp))
                model._user_cuts["ST2"] +=1
                #return True
                return True
        """
        for u in TF:
            if u in edges:
                mincut, partition = nx.minimum_cut(G,u,"target")
                if mincut<f["ts"+u[-1]]-pow(10,-3):
                    print("ST user cut", mincut, u)
                    for part in partition:
                        if "target" in part:
                            S_comp = part
                        else:
                            S = part
                    model.cbCut(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A)>=f["ts"+u[-1]])
                    model._user_cuts["ST2"] +=1
                    #return True
                    added_st_cut = True
            
            if u in P:
                mincut, partition = nx.minimum_cut(G,"source",u)
                if mincut<1-pow(10,-1):
                    print("ST user cut", mincut, u)
                    for part in partition:
                        if "source" in part:
                            S = part
                        else:
                            S_comp = part
                    model.cbCut(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A)>=1)
                    model._user_cuts["ST2"] +=1
                    #return True
                    added_st_cut = True
                #print(U,V)"""
        return added_st_cut
    
    def exact_subtour_elemination_nx(model,edges,f, mipsol=False):
        added_st_cut = False
        G = nx.DiGraph()
        for e in edges:
            G.add_edge(e[0],e[1],capacity=edges[e])
        for o in VD:
            G.add_edge(o,"target",capacity=1.0)
        for o in VO:
            G.add_edge("source",o,capacity=1.0)
        for u in model._D|model._P:
            mincut, partition = nx.minimum_cut(G,u,"target")
            if mincut<1-pow(10,-1):
                print("ST user cut", mincut, u)
                for part in partition:
                    if "target" in part:
                        S_comp = part
                    else:
                        S = part
                model.cbCut(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A)>=1)
                #model._user_cuts["ST2"] +=1
                #return True
                return True
        """
        for u in TF:
            if u in edges:
                mincut, partition = nx.minimum_cut(G,u,"target")
                if mincut<f["ts"+u[-1]]-pow(10,-3):
                    print("ST user cut", mincut, u)
                    for part in partition:
                        if "target" in part:
                            S_comp = part
                        else:
                            S = part
                    model.cbCut(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A)>=f["ts"+u[-1]])
                    model._user_cuts["ST2"] +=1
                    #return True
                    added_st_cut = True
            
            if u in P:
                mincut, partition = nx.minimum_cut(G,"source",u)
                if mincut<1-pow(10,-1):
                    print("ST user cut", mincut, u)
                    for part in partition:
                        if "source" in part:
                            S = part
                        else:
                            S_comp = part
                    model.cbCut(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A)>=1)
                    model._user_cuts["ST2"] +=1
                    #return True
                    added_st_cut = True
                #print(U,V)"""
        return added_st_cut
    
    def build_pi_sigma_graph(x, exclude_nodes, add_edges):
        g = ig.Graph(directed=True)
        all_nodes = set(u for e in x for u in e).union(*[set(edge) for edge in add_edges])
        all_nodes -= set(exclude_nodes)
    
        node_map = {node: idx for idx, node in enumerate(all_nodes)}
        rev_node_map = {idx: node for node, idx in node_map.items()}
        
        g.add_vertices(len(node_map))
        edge_list = []
        capacities = []
    
        for (u, v), cap in x.items():
            if u in node_map and v in node_map:
                edge_list.append((node_map[u], node_map[v]))
                capacities.append(cap)
    
        for u, v, cap in add_edges:
            if u in node_map and v in node_map:
                edge_list.append((node_map[u], node_map[v]))
                capacities.append(cap)
    
        g.add_edges(edge_list)
        g.es['capacity'] = capacities
        return g, node_map, rev_node_map
    
    def separate_weak_pi_and_sigma_cuts(model, x, y, mipsol=True):
        R1 = list(R)
        random.shuffle(R1)
        
        for r in R1:
            pr = f"p{r}"
            dr = f"d{r}"
            """
            ### --- π-Cut --- ###
            exclude_nodes = frozenset([pr]) | VO
            add_edges = [(d, "target", 1.0) for d in VD]
    
            g, node_map, rev_node_map = build_pi_sigma_graph(x, exclude_nodes, add_edges)
            if dr not in node_map or "target" not in node_map:
                continue
    
            result = g.st_mincut(node_map[dr], node_map["target"], capacity='capacity')
            if result.value < 1 - 1e-1:
                print("weak pi cut", result.value, dr)
                for part in result.partition:
                    if node_map["target"] in part:
                        S_comp = part
                    else:
                        S = part
                S = {rev_node_map[i] for i in S}
                S_comp = V-(frozenset([pr]) | VO|S)
                #cut_pool.append((S,S_comp,dr))
                if mipsol:
                    model.cbLazy(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A) >= 1)
                else:
                    model.cbCut(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A) >= 1)
                    model._user_cuts["pi"] +=1
                return True
            """
            ### --- σ-Cut --- ###
            exclude_nodes = frozenset([dr]) | VD
            add_edges = [("source", o, 1.0) for o in VO]
    
            g, node_map, rev_node_map = build_pi_sigma_graph(x, exclude_nodes, add_edges)
            if pr not in node_map or "source" not in node_map:
                continue
    
            result = g.st_mincut(node_map["source"], node_map[pr], capacity='capacity')
            if result.value < 1 - 1e-1:
                print("weak sigma cut", result.value, pr)
                for part in result.partition:
                    if node_map["source"] in part:
                        S = part
                    else:
                        S_comp = part
                S = {rev_node_map[i] for i in S}
                S_comp = V-(frozenset([dr]) | VD|S)
                #cut_pool.append((S,S_comp,pr))
                if mipsol:
                    model.cbLazy(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A) >= 1)
                else:
                    model.cbCut(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A) >= 1)
                    model._user_cuts["sig"] +=1
                if len(S_comp.intersection(VO)) > 0:
                    model._error_msgs += f"wrong S_comp set! {S_comp}"
                return True
    
        return False
        
    def separate_weak_pi_and_sigma_cuts_nx(model,x,y,mipsol=True):
        #return False
        R1 = R
        random.shuffle(R1)
        for r in R1:
            pr = f"p{r}"
            dr = f"d{r}"
            #separate pi-sigma
            #"""
            G = nx.DiGraph()
            for e in x:
                G.add_edge(e[0],e[1],capacity=x[e])
            #separate_pi
            
            G.remove_node(pr)
            for j in VO:
                G.remove_node(j)
            for d in VD:
                G.add_edge(d,"target",capacity=1.0)
            mincut, partition = nx.minimum_cut(G,dr,"target")
            if mincut<1-pow(10,-1):
                print("weak pi cut", mincut, dr)
                for part in partition:
                    if "target" in part:
                        S_comp = part
                    else:
                        S = part
                if mipsol==True:
                    model.cbLazy(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A)>=1)
                else:
                    model.cbCut(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A)>=1)
                    #model._user_cuts["pi"] +=1
                    #model._test_cuts.append((S,S_comp,(dr,)))
                return True
            #separate sigma
            G = nx.DiGraph()
            for e in x:
                G.add_edge(e[0],e[1],capacity=x[e])
            G.remove_node(dr)
            for j in VD:
                G.remove_node(j)
            for o in VO:
                G.add_edge("source",o,capacity=1.0)
            mincut, partition = nx.minimum_cut(G,"source",pr)
            if mincut<1-pow(10,-1):
                print("weak sigma cut", mincut,pr)
                for part in partition:
                    if "source" in part:
                        S = part
                    else:
                        S_comp = part
                if mipsol==True:
                    model.cbLazy(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A)>=1)
                else:
                    model.cbCut(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A)>=1)
                    #model._user_cuts["sig"] +=1
                    #model._test_cuts.append((S,S_comp,(pr,)))
                if len(S_comp.intersection(VO))>0:
                    model._error_msgs += f"wrong S_comp set! {S_comp}"
                return True
            #"""
        return False
    
    def separate_capacity_constraint(model,x, nodeset):
        #return False
        heuristic = CapacityHeuristic(
            x,
            list(nodeset),
            qnode,
            VC,
            0.01,
            2
        )
        
        cuts = heuristic.run()
        cut_added = False
        for cut in cuts:
            S = set(cut['location_set'])
            RHS = cut['required_flow']
            LHS = quicksum(model._x[j,i]for i in S for j in V-S if (j,i) in A)
            model.cbCut(LHS>=RHS)
            print("capacity cut", S,RHS,cut['actual_flow'])
            cut_added = True
            model._user_cuts["CapC"] +=1
        return cut_added
    


    def analyze_growth_rate(model):
        """
        Analyze the growth rate of unexplored nodes based on collected data.
        
        Args:
            model: Gurobi model with tracking data
        """
        # Get the samples
        node_counts = list(model._cb_node_counts)
        timestamps = list(model._cb_timestamps)
        
        # Calculate time differences
        time_diffs = np.diff(timestamps)
        
        # Calculate node count differences
        node_diffs = np.diff(node_counts)
        
        # Calculate growth rates (nodes per second)
        growth_rates = node_diffs / time_diffs
        
        # Only analyze if we have enough data points
        if len(growth_rates) >= 2:
            avg_growth_rate = np.mean(growth_rates)
            
            # Calculate trend over the available data (up to 100 seconds)
            # Linear regression on data points
            relative_times = np.array(timestamps) - timestamps[0]
            
            # Simple linear regression to get trend
            slope, intercept = np.polyfit(relative_times, node_counts, 1)
            
            # Determine if increasing or decreasing
            trend = "increasing" if slope > 0 else "decreasing"
            elapsed_seconds = relative_times[-1]
            if slope<=0:
                if model._cb_mipnode_stop == False:
                    print(f"Stop separation of VIs: Slope: {slope:.2f}")
                model._cb_mipnode_stop = True
            else:
                if model._cb_mipnode_stop == True:
                    print(f"Continue separation of VIs: Slope: {slope:.2f}")
                model._cb_mipnode_stop = False
            
            """
            print(f"Unexplored nodes: {node_counts[-1]}")
            print(f"Growth rate: {avg_growth_rate:.2f} nodes/second")
            print(f"Trend over last {elapsed_seconds:.1f} seconds: {trend}")
            print(f"Slope: {slope:.2f}")
            print("-" * 40)"""
    
    def setup_mip_node_tracker(model):
        """
        Set up the MIP node tracker on a Gurobi model.
        
        Args:
            model: Gurobi model to track
            
        Returns:
            model: The same model with tracking parameters added
        """
        # Initialize tracking parameters on the model
        model._cb_node_counts = deque(maxlen=5)
        model._cb_timestamps = deque(maxlen=5)
        model._cb_last_sample_time = 0
        model._cb_mipnode_stop = False

        
        return model
    
    def check_illegal_transfer(model, x, y):
            #returns true if cut was added

            G = nx.DiGraph()
            #for e in z:
             #  G.add_edge(e[0],e[1],arrival_time=z[e])
            
            G.add_edges_from(x)
            trans_edges = [(e[0],e[1]) for e in y if (e[0],e[1]) in TIy]
            for o in VO:
                if o in G.nodes:
                    tours = list(nx.all_simple_paths(G, o, o.replace("o","e")))
                    for tour in tours:
                        # Get edges in the tour
                        #tour_edges = [(tour[i], tour[i+1]) for i in range(len(tour)-1)]
                        
                        # Create subgraph with these edges
                        #subgraph = G.edge_subgraph(tour_edges).copy()
                        for e in trans_edges:
                            if e[0] in tour and e[1] in tour:
                                LHS = quicksum(model._x[e] for e in model._A if e not in x) 
                                LHS_check = sum(x.get(e,0) for e in model._A if e not in x)
                                RHS = 1.0
                                model.cbLazy(
                                    LHS#for (i,j) in edges)#
                                    >= RHS
                                    )
                                model._stats["lazy_self_transfer"] += 1
                                print(f"added double Trans visit cut {LHS_check}<={RHS}")
                                return True
                            
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
                        #model._cuts.append((S1,do,de_cut,(None,None,None)))
                        model._lazy_cuts += 1
                        if RHS_check>=1:
                            #breakpoint()
                            print("Stop")
                        return
    
    def ub_callback(model, where):
        """
        if where == GRB.Callback.MIP:
            # Get current time
            current_time = time.time()
            
            # Check if it's time for a new sample (every 10 seconds)
            if current_time - model._cb_last_sample_time >= 10:
                # Get the count of unexplored nodes
                unexplored_nodes  = model.cbGet(GRB.Callback.MIP_NODLFT)
                
                # Store the data
                model._cb_node_counts.append(unexplored_nodes)
                model._cb_timestamps.append(current_time)
                model._cb_last_sample_time = current_time
                
                # If we have enough data, calculate and report growth rate
                if len(model._cb_node_counts) >= 2:
                    analyze_growth_rate(model)"""
        if where == GRB.Callback.MIPSOL:
            model._stats["lazy_calls"] += 1
            start = time.time()
            cur_obj = model.cbGet(gp.GRB.Callback.MIPSOL_OBJ)
            cur_bnd =    model.cbGet(gp.GRB.Callback.MIPSOL_OBJBND)  
            sol_cnt =  model.cbGet(gp.GRB.Callback.MIPSOL_SOLCNT)
            if model._HET:
                all_x_vars = model.cbGetSolution(model._x)
                all_y_vars = model.cbGetSolution(model._y)
                x_arcs = {a:all_x_vars[a] for a in A if all_x_vars[a] > 0.5}
                y_arcs = tuplelist({a for a in Ay if all_y_vars[a] > 0.5})
                added_cut = check_illegal_transfer(model, x_arcs, y_arcs)
                if added_cut == True:
                    return
            if model._symm or model._multi_trans:
                all_x_vars = model.cbGetSolution(model._x)
                all_x_vars = model.cbGetSolution(model._x)
                x_arcs = {a:1 for a in A if all_x_vars[a] > 0.5}
                check_multiple_transfer_stations(model,x_arcs)
            if sol_cnt>0:
                if cur_obj < model._solver_state.model_ub:
                   model._solver_state.model_ub = cur_obj
            
            else:
                if model._solver_state.model_ub<np.inf:
                    model._sols.add(np.round(model._solver_state.model_ub,4))
                    temp_sol = model._solver_state.new_solution
                    new_vars = [model._x[var] for var in temp_sol["x"]] + [model._y[var] for var in temp_sol["y"]]#+[model._z[var] for var in temp_sol["z"]]+[model._bz[var] for var in temp_sol["bz"]]+[model._bl[var] for var in temp_sol["bl"]]
                    new_vals = list(temp_sol["x"].values()) + list(temp_sol["y"].values())#+ list(temp_sol["z"].values())+ list(temp_sol["bz"].values())+ list(temp_sol["bl"].values())
                    print("new solution:", model._solver_state.model_ub, cur_obj)
                    #model.cbSetSolution(model._vars,[0.0]*len(model._vars))
                    model.cbSetSolution(new_vars, new_vals)
            model._stats["lazy_t"] += time.time()-start
        if where == GRB.Callback.MIPNODE:
            model._stats["user_calls"] += 1
            start = time.time()
            cur_obj = model.cbGet(gp.GRB.Callback.MIPNODE_OBJBST)
            sol_cnt =  model.cbGet(gp.GRB.Callback.MIPNODE_SOLCNT)
            #print("check new solution",model_ub)
            """
            status = model.cbGet(GRB.Callback.MIPNODE_STATUS)
            if status == GRB.OPTIMAL:
                nodecnt = model.cbGet(GRB.Callback.MIPNODE_NODCNT)
                #if nodecnt<200 :#or nodecnt - model._cb_lastnode >= 400:
                all_x_vars = model.cbGetNodeRel(model._x)
                x_arcs = {a:all_x_vars[a] for a in A if all_x_vars[a] > 0.00001 }
                #separate_strengthened_capacity_constraint(model, x_arcs)
                all_y_vars = model.cbGetNodeRel(model._y)
                y_arcs = {a:all_y_vars[a] for a in Ay if all_y_vars[a] > 0.001 }
                #all_f_vars = model.cbGetNodeRel(model._f)
                #f_arcs = {a:all_f_vars[a] for a in all_f_vars if all_f_vars[a] > 0.00001 }
                if nodecnt<1 or (nodecnt - model._cb_lastnode >= 200 and model._cb_mipnode_stop ==False):
                    print(f"{int(nodecnt)} - MIPNODE separation -")
                    model._cb_lastnode= nodecnt
                    if exact_subtour_elemination(model, x_arcs, [])==False:
                        if separate_weak_pi_and_sigma_cuts(model, x_arcs,y_arcs, mipsol=False)==False:
                            no = 2
                            #if np.random.rand()>0.5:
                             #   separate_capacity_constraint(model, x_arcs, P)
                            #else:
                             #   separate_capacity_constraint(model, x_arcs, D)
            """           
            if sol_cnt>0:
                if np.round(cur_obj,4) > np.round(model._solver_state.model_ub,4)+pow(10,-4):
                    if np.round(model._solver_state.model_ub,4) not in model._sols:
                        model._sols.add(np.round(model._solver_state.model_ub,4))
                        temp_sol = model._solver_state.new_solution
                        new_vars = [model._x[var] for var in temp_sol["x"]] + [model._y[var] for var in temp_sol["y"]]#+[model._z[var] for var in temp_sol["z"]]+[model._bz[var] for var in temp_sol["bz"]]+[model._bl[var] for var in temp_sol["bl"]]
                        new_vals = list(temp_sol["x"].values()) + list(temp_sol["y"].values())#+ list(temp_sol["z"].values())+ list(temp_sol["bz"].values())+ list(temp_sol["bl"].values())
                        print("new solution:", model._solver_state.model_ub, cur_obj)
                        #model.cbSetSolution(model._vars,[0.0]*len(model._vars))
                        model.cbSetSolution(new_vars, new_vals)
                        model.cbUseSolution()
            else:
                if model._solver_state.model_ub<np.inf:
                    model._sols.add(np.round(model._solver_state.model_ub,4))
                    temp_sol = model._solver_state.new_solution
                    new_vars = [model._x[var] for var in temp_sol["x"]] + [model._y[var] for var in temp_sol["y"]]#+[model._z[var] for var in temp_sol["z"]]+[model._bz[var] for var in temp_sol["bz"]]+[model._bl[var] for var in temp_sol["bl"]]
                    new_vals = list(temp_sol["x"].values()) + list(temp_sol["y"].values())#+ list(temp_sol["z"].values())+ list(temp_sol["bz"].values())+ list(temp_sol["bl"].values())
                    print("new solution:", model._solver_state.model_ub, cur_obj)
                    #model.cbSetSolution(model._vars,[0.0]*len(model._vars))
                    model.cbSetSolution(new_vars, new_vals)
            model._stats["usercut_t"] += time.time()-start


            
             
    
    def solve_compact(barrier=None, env=gp.Model(), timeFlow=False, mode="two", state=None, symm=False):
     

        model_str =""
        if timeFlow==True:
            model_str += "_tf"
        model = Model(f'myTwoIndexModel_withUBPDPTW_StrCap_UB_{mode}Phase'+model_str,env=env )
        model._solver_state = state
        model._lazy_cuts = 0
        x = model.addVars(xIndex, vtype=GRB.BINARY, name='x')
        y = model.addVars(Ay, vtype=GRB.BINARY, name='y')
        #Idee wenn zwei vehicle unterschiedliche StartPositionen haben, b trackt vehicle flow
        b = model.addVars(arcs,lb=0.0,ub=len(K)-1, vtype=GRB.CONTINUOUS, name='b')
        #bl = model.addVars(kArcs, vtype=GRB.BINARY, name='bl')
        bl = model.addVars(V,ub=len(K), vtype=GRB.CONTINUOUS, name='bl')
        if VC < 0:
           vl = model.addVars(V,lb=0.0,ub=Qmax, vtype=GRB.CONTINUOUS, name='vl') 
        ti = model.addVars(TIy, vtype=GRB.BINARY, name='ti')
        #b = model.addVars(xIndex,lb=0.0, ub=nVehicles ,vtype=GRB.CONTINUOUS, name="b")
        z = model.addVars(zIndex,lb=0.0 ,vtype=GRB.CONTINUOUS, name="z")
        #a = model.addVars([(i,r) for i in TS for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="a")
        if timeFlow==False:
            bz = model.addVars(V,lb=0.0 ,vtype=GRB.CONTINUOUS, name="bz")
        else:
            zr = model.addVars(Ayts,lb=0.0 ,vtype=GRB.CONTINUOUS, name="zr")
        #ba = model.addVars([(i,r) for i in TF for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="ba")
        f = model.addVars([i for i in TS_pure], vtype=GRB.BINARY, name='f')
        
        model.modelSense = GRB.MINIMIZE
        if VC<0:
            model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in arcs))
        #else:
            #if "Lim" in filename:
               # model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in arcs)+quicksum(pow(10,4) * x[i, j] for (i,j) in arcs if i in VO))
            #else:
        model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in arcs))
        model.update()
        
        
       
        """
        Arc flows
        """
    
        
        if "Lim" not in filename:
            model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A.select(vo,'*')]) == 1 for vo in VO), name = "ct.route_startFirst")
            #else:
                #model.addConstr((quicksum(x[vo, j] for vo in VO for j in [a[1] for a in A.select(vo,'*')]) >= 1), name = "ct.route_startFirst")
        model.addConstrs(( quicksum(x[vo, j] for j in [a[1] for a in A.select(vo,'*')]) == quicksum(x[j, vo.replace("o","e")] for j in [a[0] for a in A.select('*',vo.replace("o","e"))]) for vo in VO), name = "ct.StartArcEqEndArc")
        
    
        
        model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A.select('*',i)]) == 1 for i in P), name = "ct.PickupJustOnce")
        
        model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A.select('*',i)]) == 1 for i in D), name = "ct.DeliveryJustOnce")
    
        
        model.addConstrs((quicksum(x[j,i] for j in [a[0] for a in A.select('*',i)]) == quicksum(x[i,j] for j in [a[1] for a in A.select(i,'*')])   for i in P|D|TS|TF), name = "ct.FlowConversion")
        
        
        """
        Loads
        """
        
        model.addConstrs((quicksum(y[i, j, r] for j in [a[1] for a in Ay.select(i,'*',r)])  == 1 for r in R for i in [f"p{r}"]), name = "ct.visit_request_originOut")
    
    
        model.addConstrs((quicksum(y[j,i, r] for j in [a[0] for a in Ay.select('*',i,r)])  == 1 for r in R for i in [f"d{r}"]), name = "ct.visit_request_destinationIn")
    
    
    
        model.addConstrs((quicksum(y[i, j,r] for j in [a[1] for a in Ay.select(i,'*',r)])-quicksum(y[j,i,r] for j in [a[0] for a in Ay.select('*',i,r)]) == 0 for r in R for i in V-(VD|VO|frozenset((f"p{r}","d{r}"))) if i not in ["p"+str(r),"d"+str(r)]), name = "ct.requestFlowConversion")
    
    
        model.addConstrs((y[i,j,r] <= x[i,j] for r in R for i in V-TS for j in [a[1] for a in Ay.select(i,'*',r)]), name = "ct.request_flow_link")
    
    
    
        """
        Capacity constraint
        """
        # capacity constraint
        if VC>0:
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-abs(qnode[i]+qnode[j]))*x[i,j] for i in P for j in [a[1] for a in A.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong1")
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-abs(qnode[i]+qnode[j]))*x[i,j] for i in D for j in [a[1] for a in A.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong2")
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in P for j in [a[1] for a in A.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong3")
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (VC-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in D for j in [a[1] for a in A.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong4")
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(j.replace("p","").replace("d",""))) <= (VC-abs(qnode[j]))*x[i,j] for i in TF for j in [a[1] for a in A.select(i,'*')] if j in P|D), name="ct.VehicleCapacityStrong5")
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d",""))) <= (VC-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in P for j in [a[1] for a in A.select(i,'*')] if j in TS), name="ct.VehicleCapacityStrong3b")
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d",""))) <= (VC-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in D for j in [a[1] for a in A.select(i,'*')] if j in TS), name="ct.VehicleCapacityStrong4b")
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)]) <= (VC-abs(qnode[j]))*x[i,j] for i in TF for j in [a[1] for a in A.select(i,'*')] if j in TS), name="ct.VehicleCapacityStrong5b")
            model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if r!=int(i.replace("p","").replace("d","")) and j in [a[1] for a in Ay.select(i,'*',r)]) <= (VC-abs(qnode[i]))*x[i,j] for i in P|D  for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacityStrong2")
            model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if j in [a[1] for a in Ay.select(i,'*',r)]) <= (VC)*x[i,j] for i in TS|TF  for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacityStrong2")

        else:
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (Qmax-abs(qnode[i]+qnode[j]))*x[i,j] for i in P for j in [a[1] for a in A.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong1")
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (Qmax-abs(qnode[i]+qnode[j]))*x[i,j] for i in D for j in [a[1] for a in A.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong2")
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (Qmax-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in P for j in [a[1] for a in A.select(i,'*')] if j in D), name="ct.VehicleCapacityStrong3")
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d","")) and r!=int(j.replace("p","").replace("d",""))) <= (Qmax-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in D for j in [a[1] for a in A.select(i,'*')] if j in P), name="ct.VehicleCapacityStrong4")
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d",""))) <= (Qmax-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in P for j in [a[1] for a in A.select(i,'*')] if j in TS), name="ct.VehicleCapacityStrong3b")
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)] and r!=int(i.replace("p","").replace("d",""))) <= (Qmax-max(abs(qnode[i]),abs(qnode[j])))*x[i,j] for i in D for j in [a[1] for a in A.select(i,'*')] if j in TS), name="ct.VehicleCapacityStrong4b")
           
            model.addConstrs((vl[f"o{k}"]  == vec_capacities[k] for k in K), name = "ct.route_startVehicleCapLabelStart")
            
            model.addConstrs((vl[f"e{k}"]  == vec_capacities[k] for k in K), name = "ct.route_startVehicleCapLabelEnd")
            
           
            
            model.addConstrs((vl[i]-(max(vec_capacities[k]-vec_capacities[l] for k in K for l in K if k!=l))*(1-x[i,j])<=vl[j] for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) not in A), name = "ct.vehicleCapLabelFlowA")
            
            model.addConstrs((vl[i]-vl[j]<=(max(vec_capacities[k]-vec_capacities[l] for k in K for l in K if k!=l))*(1-x[i,j]-x[j,i]) for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) in A), name = "ct.vehicleCapLabelFlowA")

          
            model.addConstrs((vl[j]-(max(vec_capacities[k]-vec_capacities[l] for k in K for l in K if k!=l))<=vl[i]  for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) not in A), name = "ct.vehicleCapLabelFlowB")
           
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R for j in [a[1] for a in Ay.select(i,'*',r)]) <= Qmax-vl[i] for i in P|D|TF), name="ct.VehicleCapacity")
           
    
    
        
        """
        Vehicle Flow Burger
        """
        
        
        model.addConstrs((bl[f"o{k}"]  == k+1 for k in K), name = "ct.route_startVehicleLabel")
        
        model.addConstrs((bl[f"e{k}"]  == k+1 for k in K), name = "ct.route_startVehicleLabel")
        
        if HET==False and symm==False and MULTI_TRANS==False:
        
            model.addConstrs((bl[i]  == int(i.split(".")[1])+1 for n in TS_loc for i in TS_loc[n]), name = "ct.route_transferVehicleLabel")
    
        
        covered = set()
        for i in V:
            for j in [a[1] for a in A.select(i,'*')]:
                if (j,i) in arcs:
                    #if (i,j) not in covered:
                     #   covered.add((i,j))
                      #  covered.add((j,i))
                        model.addConstr(( bl[i]-bl[j] <= ((len(K)-1)*(1-x[i,j]-x[j,i]))), name = "ct.vehicleLabelFlowLifted")
                else:
                    model.addConstr((bl[i]-(len(K)-1)*(1-x[i,j])<=bl[j]), name = "ct.vehicleLabelFlowA")
                    model.addConstr((bl[j]-(len(K)-1)*(1-x[i,j])<=bl[i]), name = "ct.vehicleLabelFlowB")
        
    
                    
        
        
        
        #for (i,j) in A:
         #   model.addConstr((bz[i]+service_time[i]+c[i,j]-Mij[i,j]*(1-x[i,j])<= z[j]), name = "ct.time_flow")

    
        
        if timeFlow==True:
                model.addConstrs(
                   (
                       gp.quicksum(
                           z[i, j] + (t[i,j]+service_time[i]) * x[i, j]
                           for i in V-VD
                           if (i, j) in A
                       )
                       <= z.sum(j,"*")
                       for j in V-VD
                   ),
                       name="ct.time_flowA",
                 )
                
                if HET==False and symm==False:
                   model.addConstrs((z.sum(i,"*")+service_time[i] -Mij[i,j]*(1-ti[i,j])<= z.sum(j,"*") for (i,j) in TIy), name = "ct.transferTimeWait")
                else:
                    if MULTI_TRANS==False:
                        model.addConstrs((z.sum(i,"*")+service_time[i] -Mij[i,j]*(1-y[i,j,r])<= z.sum(j,"*") for r in R for i in TS for j in [a[1] for a in Ay.select(i,'*',r) if (a[0],a[1]) in TIy]), name = "ct.transferTimeWait")
                    else:
                        #model.addConstrs(z.sum(f"p{r}","*")+t[f"p{r}",f"d{r}"]<=z.sum(f"d{r}","*") for r in R)
                        model.addConstrs(
                            (gp.quicksum(
                                z[i, j] + (t[i,j]+service_time[i]) * x[i, j]
                                for i in V-VD
                                if (i, j) in A
                            )
                            <= zr.sum(j,"*",r) for r in R for j in TS
                            )
                            , name="ct.timeTransSched1"
                            )
                        model.addConstrs(
                            (gp.quicksum(
                                zr[i, j,r] 
                                for i in TS
                                if (i,j,r) in Ay
                            )
                            <= z.sum(j,"*") for j in TF for r in R
                            )
                            , name="ct.timeTransSched2"
                            )
                        model.addConstrs(
                            (
                            zr[i, j,r] 
                            <=  y[i,j,r]*df.b.max() for (i,j,r) in Ayts
                            )
                            , name="ct.timeTransSched2"
                            )
                #model.addConstrs((z.sum(i,"*")+service_time[i] -Mtr[i,j,r]*(1-y[i,j,r])<= z.sum(j,"*") for (i,j) in TIy for r in R), name = "ct.transferTimeWait")

                """
                Time Windows
                """
                model.addConstrs(
                (
                    z[i, j] >= timeWindows[i][0] * x[i, j]
                    for (i, j) in A
                ),
                name="timeWindowStart",
                )

                model.addConstrs(
                    (
                        z[i, j] <= wbTW[i,j]* x[i, j]
                        for (i, j) in A
                    ),
                    name="timeWindowEnd",
                )
      
    
        else:
            """
            Lifted version, benefit unclear. Needs testing!
            """
            
            #model.addConstrs((bz[i]+service_time[i]+t[i,j]-(Mij[i,j])*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.time_flowA")

            #super valid inequality
            model.addConstrs((bz[i]+t[i,j]-(Mij[i,j])*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) not in A), name = "ct.time_flowA")
            
            model.addConstrs((bz[i]-z[j]+Mij[i,j]*x[i,j]+(Mij[i,j]-t[i,j]+min(-t[j,i],timeWindows[j][0]-timeWindows[i][1]+service_time[i]+service_time[j]))*x[j,i]<= Mij[i,j]-t[i,j]  for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) in A), name = "ct.time_flowLifted")
            
            model.addConstrs((z[i]+service_time[i] <= bz[i] for i in V-(TS|TF)), name='ct.DepartureA')
            
            model.addConstrs((z[i]+service_time[i]+0.01  <= bz[i] for i in TS|TF), name='ct.DepartureA')
            if HET==False:
                model.addConstrs((z[i] -Mij[i,j]*(1-ti[i,j])<= bz[j] for i in TS for j in [a[1] for a in Ay.select(i,'*',0) if (a[0],a[1]) in TIy]), name = "ct.transferTimeWait")
            else:
                model.addConstrs((z[i]-Mij[i,j]*(1-y[i,j,r])<= bz[j] for r in R for i in TS for j in [a[1] for a in Ay.select(i,'*',r) if (a[0],a[1]) in TIy]), name = "ct.transferTimeWait")
                for tf in TFC:
                    r = int(tf.split(".")[1])
                    model.addConstr((z[tf.replace("fc","sr")] +service_time[tf.replace("fc","sr")]<= bz[tf]), name = "ct.transferTimeWait")
            """
            Time Windows
            """
            #model.addConstrs((min(max(timeWindows[f"e{k}"][1]-c[i,f"e{k}"] for k in K),timeWindows[i][1]) >= bz[i]-service_time[i] for i in V-VD), name="ct.TimeWindowLatest")
            model.addConstrs((timeWindows[i][1] >= bz[i] for i in V), name="ct.TimeWindowLatestVD")
        
            #model.addConstrs((min([max(timeWindows[i][0],c[f"o{k}",i]) for k in K]) <= z[i] for i in V-VO), name="ct.timeWindowEarliestbVO")
            model.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliestb")
                


            
        
        """
        Request Transfer Time
        """
     
        #model.addConstrs((ti[i,j]+1>=(quicksum(y[j,i,r] for j in [a[0] for a in Ay.select('*',i,r)])-quicksum(y[i,j,r] for j in [a[1] for a in Ay.select(i,'*',r)]))+(quicksum(y[j,i,r] for i in [a[1] for a in Ay.select(j,'*',r)])-quicksum(y[i,j,r] for i in [a[0] for a in Ay.select('*',j,r)])) for r in R for i in TS for j in [a[1] for a in Ay.select(i,'*',r) if (a[0],a[1]) in TIy] ), name="transfer_indicator")
        
        if HET==False and symm==False:
            model.addConstrs((ti[i,j]>= y[i,j,r] for r in R for i in TS for j in [a[1] for a in Ay.select(i,'*',r) if (a[0],a[1]) in TIy] ), name="transfer_indicator")
    
        
    
        """
        Transfer location open
        """
        model.addConstrs((1 >= x[i,j] for j in TS for i in [a[0] for a in A.select('*',j)]), name = "ct.TransferVITS")
    
        model.addConstrs((1 >= x[i,j] for i in TF for j in [a[1] for a in A.select(i,'*')]), name = "ct.TransferVITF")
    
    
        model.addConstrs((f[f"ts{n}"] >= quicksum(x[i,j] for j in [a[1] for a in A.select(i,'*')]) for n in TS_loc for i in TS_loc[n]), name = "ct.TransferFlowLink")
        model.addConstrs((f[f"ts{n}"] <= quicksum(y[i,j,r] for r in R for i in TS_loc[n] for j in [a[1] for a in Ay.select(i,'*',r) if a[1].replace("f","s")!=i]) for n in TS_loc), name = "ct.TransferRequestFlowLink")
        
        #model.addConstrs((f[f"ts{n}"] <= quicksum(y[i,j,r] for r in R for i in TS_loc[n] for j in [a[1] for a in Ay.select(i,'*',r) if a[1].replace("f","s")!=i]) for n in TS_loc), name = "ct.TransferRequestFlowLink")
        model.addConstrs((2*f[f"ts{n}"] <= quicksum(x[j,i] for i in TS_loc[n] for j in [a[0] for a in A.select('*',i)]) for n in TS_loc), name = "ct.AtLeastTwoVehicles")
        
        
        """
        HET Constraints
        """
        if symm==True:
            for n in TS_loc:
                for k in K:
                    t1 = f"ts.{k}.{n}"
                    if k== 0:
                        model.addConstr(quicksum(y[t1,j,r] for r in R for j in [a[1] for a in Ay.select(t1,'*',r)])>=quicksum(x[t1,j] for j in [a[1] for a in A.select(t1,'*')]))
                    if k>0:
                        t2 = f"ts.{k-1}.{n}"
                        model.addConstr(quicksum(y[t1,j,r]*r for r in R for j in [a[1] for a in Ay.select(t1,'*',r)])<=quicksum(y[t2,j,r]*r for r in R for j in [a[1] for a in Ay.select(t2,'*',r)]))
                
        if HET==True or MULTI_TRANS:
            for ts in TSR:
                r = int(ts.split(".")[1])
                model.addConstr(x[ts,ts.replace("s","f")]<=quicksum(y[ts,j,r] for j in [a[1] for a in Ay.select(ts,'*',r)]))
                if r>0:
                    model.addConstr(quicksum(y[ts,j,r1] for r1 in R if r1<r for j in [a[1] for a in Ay.select(ts,'*',r1)])==0)
            for ts in TSC:
                model.addConstr(0==quicksum(y[ts,j,r] for r in R for j in [a[1] for a in Ay.select(ts,'*',r)]))
            for tf in TFC:
                r = int(tf.split(".")[1])
                model.addConstr(x[tf.replace("f","s"),tf]<=quicksum(y[j,tf,r] for j in [a[0] for a in Ay.select('*',tf,r)]))
                if r>0:
                    model.addConstr(quicksum(y[j,tf,r1] for r1 in R if r1<r for j in [a[0] for a in Ay.select('*',tf,r1)])==0)
        
        """
        # Open and read the file
        with open('cut_lst.txt', 'r') as file:
            content = file.read()
        
        # Convert the string representation to a Python object
        cut_lst = ast.literal_eval(content)
        
        for idx,cut in enumerate(cut_lst):
            S = cut[0]
            Sp = cut[1]
            model.addConstr((quicksum(x[i,j] for i in S for j in Sp if (i,j) in A)>=1), name=f"user_cut_{idx}")
                
          
        for route in  [[('o2', 'p7'), ('p7', 'tsr.7.0'), ('tsr.7.0', 'tfr.7.0'), ('tfr.7.0', 'd0'), ('d0', 'e2')],
         [('o2', 'e2')],
         [('o0', 'e0')],
         [('o1', 'p5'), ('p5', 'd5'), ('d5', 'p8'), ('p8', 'd8'), ('d8', 'e1')],
         [('o1', 'p3'), ('p3', 'p1'), ('p1', 'd1'), ('d1', 'p2'), ('p2', 'd3'), ('d3', 'd2'), ('d2', 'e1')],
         [('o1', 'p0'), ('p0', 'tsr.0.0'), ('tsr.0.0', 'tfr.0.0'), ('tfr.0.0', 'p6'), ('p6', 'd7'), ('d7', 'd6'), ('d6', 'e1')],
         [('o1', 'p4'), ('p4', 'd4'), ('d4', 'e1')],
         [('o1', 'e1')],
         [('o3', 'e3')]]:
             for e in route:
                 model.addConstr(x[e]==1) """
        
        #for e in [('o0', 'p29'), ('o1', 'p17'), ('p0', 'p4'), ('p17', 'd17'), ('p10', 'd15'), ('p23', 'd21'), ('p6', 'd6'), ('p4', 'p14'), ('p3', 'd9'), ('p19', 'p0'), ('p20', 'p27'), ('p9', 'p3'), ('p22', 'ts.1.0'), ('p25', 'd27'), ('p16', 'd16'), ('p15', 'p10'), ('p8', 'ts.0.0'), ('p21', 'd2'), ('p12', 'd12'), ('p26', 'd26'), ('p7', 'd7'), ('p1', 'd13'), ('p5', 'd5'), ('p13', 'p1'), ('p11', 'd11'), ('p18', 'd25'), ('p2', 'p21'), ('p14', 'd0'), ('p29', 'd29'), ('p27', 'p25'), ('p24', 'd10'), ('p28', 'p24'), ('d26', 'p16'), ('d23', 'd1'), ('d28', 'p11'), ('d29', 'p7'), ('d9', 'p8'), ('d7', 'p12'), ('d15', 'd18'), ('d12', 'p6'), ('d3', 'd22'), ('d2', 'p5'), ('d17', 'p26'), ('d20', 'p18'), ('d13', 'p23'), ('d8', 'e0'), ('d18', 'p28'), ('d10', 'd24'), ('d22', 'p2'), ('d16', 'p20'), ('d6', 'p19'), ('d25', 'p15'), ('d0', 'd19'), ('d11', 'p22'), ('d21', 'd23'), ('d19', 'd4'), ('d24', 'd28'), ('d1', 'e1'), ('d14', 'p9'), ('d27', 'd20'), ('d5', 'p13'), ('d4', 'd14'), ('ts.0.0', 'tf.0.0'), ('ts.1.0', 'tf.1.0'), ('tf.1.0', 'd3'), ('tf.0.0', 'd8')]:
            #model.addConstr(x[e]==1) 

        """
        for route in [[('o0', 'e0')],
        [('o3', 'tsc.4.0'), ('tsc.4.0', 'tfc.4.0'), ('tfc.4.0', 'd4'), ('d4', 'd5'), ('d5', 'e3')],
        [('o3', 'e3')],
        [('o1', 'p2'), ('p2', 'p4'), ('p4', 'p1'), ('p1', 'p5'), ('p5', 'tsr.1.0'), ('tsr.1.0', 'tfr.1.0'), ('tfr.1.0', 'p7'), ('p7', 'p0'), ('p0', 'p6'), ('p6', 'tsr.0.0'), ('tsr.0.0', 'tfr.0.0'), ('tfr.0.0', 'd7'), ('d7', 'p10'), ('p10', 'd8'), ('d8', 'd10'), ('d10', 'd9'), ('d9', 'd3'), ('d3', 'd2'), ('d2', 'e1')],
        [('o1', 'e1')],
        [('o2', 'p9'), ('p9', 'p8'), ('p8', 'p3'), ('p3', 'tsr.3.0'), ('tsr.3.0', 'tfr.3.0'), ('tfr.3.0', 'd1'), ('d1', 'd0'), ('d0', 'd6'), ('d6', 'e2')],
        [('o2', 'e2')]]:
            for e in route:
                model.addConstr(x[e]==1)"""
        
        # Data for callback
        model._obj = None
        model._bd = None
        model._gap = None
        model._data = []
        model._x = x
        model._y = y
        model._z = z
        model._TS = TS
        model._HET = HET
        model._symm= symm
        model._multi_trans = MULTI_TRANS
        if VC>0:
            if timeFlow==False:
                model._bz = bz
        else:
            model._vl = vl
        model._bl = bl
        model._f = f
        model._ti = ti
        model._A = A
        model._VO = VO
        model._VD = VD
        model._P = P
        model._D =D
        model._Ay = Ay
        model._timeFlow=timeFlow
        model._sols = set()
        model._vars = model.getVars()
        model._start = time.time()
        model._cb_lastnode= 0
        if model._symm or HET or MULTI_TRANS:
            model.Params.LazyConstraints = 1
        #model.Params.Symmetry = 0
        #if timeFlow==True:
         #   model.Params.NumericFocus =3
            #model.Params.FeasibilityTol = 10e-4
        
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
        #model.Params.PreCrush = 1
        model._cb_lastnode = 0
        model._error_msgs = ""
        model._stats  = {"usercut_t":0.0, "lazy_t":0.0, "user_calls":0, "lazy_calls":0,"lazy_self_transfer":0}
        model._user_cuts = {"ST2":0,"CapC":0,"pi":0,"sig":0}
        #model = setup_mip_node_tracker(model)
        model.update()
        if barrier!=None:
            barrier.wait()
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
        #model.optimize()
        lp = compute_LP_relax_bound(model)
        
        model.optimize(callback=ub_callback)
        
        #model.optimize(callback=usercut_cb)
        #model.write("model.lp")
        # model.optimize()
        # model.computeIIS()
        #
        #if model.status==3:
           #model.computeIIS()
           #model.write("infeasible_model.ilp")
        
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
            
            
        #plotGap(model._data)
        # plotArcs(arcs)
        
        vehicle_number = -1
        error_msg = ""
        sol_transfers = 0
        sol_req_trans = 0
        if model.Status == GRB.OPTIMAL:
            ratio = lp/model.ObjVal*100
            xarcs = plotLocation(df)
            sol_check, error_msg = check_tours(model)
            vehicle_number = sum(model._x[i, j].x for o in model._VO for (i,j) in model._A.select(o,"*"))
            with open(f"{filename.replace('.txt','')}_sol.txt", "w") as output:
                output.write(str([a for a in x if x[a].x>0.5]))
            sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
            sol_req_trans = quicksum(y[i,j,r] for (i,j) in TIy for r in R if (i,j,r) in Ay).getValue()
            infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sol_transfers,sol_req_trans,vehicle_number,error_msg,model._lazy_cuts,ratio]  
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
            if model.SolCount == 0:
                sol_transfers = None
                infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sol_transfers,sol_req_trans,vehicle_number,error_msg, model._lazy_cuts,lp]      
            else:
                ratio = lp/model.ObjVal*100
                xarcs = plotLocation(df)
                sol_check, error_msg = check_tours(model)
                vehicle_number = sum(model._x[i, j].x for o in model._VO for (i,j) in model._A.select(o,"*"))
                with open(f"{filename.replace('.txt','')}_sol.txt", "w") as output:
                    output.write(str([a for a in x if x[a].x>0.5]))
                sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
                sol_req_trans = quicksum(y[i,j,r] for (i,j) in TIy for r in R if (i,j,r) in Ay).getValue()
                infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sol_transfers,sol_req_trans,vehicle_number,error_msg, model._lazy_cuts,ratio]      
        else:
            infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),"inf","inf" ,model.ObjBound, model.Runtime,sol_transfers,0,vehicle_number,error_msg,model._lazy_cuts,lp]    
        """for key in model._user_cuts:
            infos.append(model._user_cuts[key])"""
        for key in model._stats:
            infos.append(model._stats[key])
        #global infos_sol
        #infos_sol = infos
        #global master_finished
        model._solver_state.master_finished=True
        model._solver_state.infos_sol = infos
        #master_finished=True
        #with open("cut_lst.txt", 'w') as file:
         #   file.write(str(cut_pool))
        #print(np.array(stats_RCCP[1]).mean(),np.array(stats_RCCP[2]).mean())
        return infos#.append(stats_RCCP)
    
    def solve_iterative(barrier,env):
        #barrier.wait()
        start = time.time()
        obj = np.inf
        last_sol = None
        global master_finished
        models = {}
        for i in range(5,20):
            models[i] = create_pdptw_model(filename, cut=1, strCap=True, env=env)
        models[21] = create_pdptw_model(filename, cut=None, strCap=True, env=env)
        barrier.wait()
        for i in range(5,20):
            if master_finished==True:
                print("finished first loop")
                break
            infos = solve_pdptw(models[i],20, None,cut=i,last_sol=last_sol)
            #infos = solve_pdptw(filename, 200,i,last_sol, True)
            obj = infos[3]
            if obj<np.inf:
                last_sol=i
        for i in range(12,15):
            if master_finished==True:
                break
            infos = solve_pdptw(models[i],600, None,cut=i,last_sol=last_sol)
            obj = infos[3]
            if obj<np.inf:
                last_sol=i
        if master_finished==True:
            print("finished")
            env.close()
            return []
        last_time = (60*60 )- (time.time()-start)
        infos = solve_pdptw(models[14],last_time, None,cut=i,last_sol=last_sol)
        env.close()
        #print("end run", infos)
        return infos
    
    def solve_two_phase(barrier,timeFlow,env,state):
        #barrier.wait()
        #Ghilas is only one phase
        start = time.time()
        obj = np.inf
        last_sol = None
        if VC>0:
            model_run_1 = create_pdptw_model(filename, cut=-3, strCap=True,timeFlow=timeFlow, env=env, state=state)
            model_run_2 = create_pdptw_model(filename, cut=-2, strCap=True,timeFlow=timeFlow, env=env, state=state)
            infos = solve_pdptw(model_run_1,1500, barrier,cut=-3,timeFlow=timeFlow,last_sol=last_sol, sollim=None)
        else:
            model_run_1 = create_pdptw_model(filename, cut=None, strCap=True,timeFlow=timeFlow, env=env, state=state)
            infos = solve_pdptw(model_run_1,3600, barrier,cut=-1.5,timeFlow=timeFlow,last_sol=last_sol, sollim=None)
        obj = infos[3]
        if obj<np.inf:
            last_sol=-1
        
        if state.master_finished==True:
            env.close()
            return []
        
        last_time = (60*60 )- (time.time()-start)
        if VC>0:
            infos = solve_pdptw(model_run_2,last_time, barrier=None,cut=-2,last_sol=last_sol)


        #infos = solve_pdptw(filename, last_time,None,-2,last_sol, True, env=env)
        #infos = solve_pdptw(filename, last_time ,None,last_sol,True)
        env.close()
        return infos
    
    def solve_one_phase(barrier, timeFlow,env):
        if "Ghilas" in filename:
            model = create_pdptw_model(filename, cut=None, timeFlow=timeFlow,strCap=True, env=env)
            infos = solve_pdptw(model,3600*3, barrier=barrier,timeFlow=timeFlow,cut=None,last_sol=None)
        else:
            model = create_pdptw_model(filename, cut=None, timeFlow=timeFlow,strCap=True, env=env)
            infos = solve_pdptw(model,3600, barrier=barrier,timeFlow=timeFlow,cut=None,last_sol=None)

        return infos

    def solve_parallel(mode="two",timeFlow=False,symm=False):
        state = SolverState()
        master_finished=False
        model_ub = np.inf
        env2 = gp.Env()
        env1 = gp.Env()
        new_solution = {"x":{},"y":{}}
        barrier = threading.Barrier(2) 
        #t1 = threading.Thread(target=solve_iterative,args=(barrier,env1))
        #t1 = threading.Thread(target=solve_pdptw)
        if mode=="two":
            t1 = threading.Thread(target=solve_two_phase, args=(barrier,timeFlow,env1,state))
        else:
            t1 = threading.Thread(target=solve_one_phase, args=(barrier,timeFlow, env1,state))
        t2 = threading.Thread(target=solve_compact, args=(barrier, env2,timeFlow, mode,state, symm))
        t1.start()
        t2.start()
    
        t1.join()
        t2.join()
        env2.close()
        env1.close()
        
        return state.infos_sol
    
    #barrier = threading.Barrier(1) 
    infos_sol = solve_parallel(mode, timeFlow=timeFlow, symm=symm)
    #state = SolverState()
    #infos_sol = solve_compact(None,gp.Env(),timeFlow=timeFlow,mode=mode, state=state)
    #check PDPTW
    """
    env = gp.Env()
    barrier = threading.Barrier(1) 
    model_run_1 = create_pdptw_model(filename, cut=None, strCap=True, timeFlow=timeFlow, env=env)
    infos_sol = solve_pdptw(model_run_1,3600, barrier,timeFlow=timeFlow,cut=None, sollim=None)
    env.close()"""
    
    return infos_sol

info = twoIndexModelUB(filename, timeFlow=False, mode="two",symm=False,MULTI_TRANS=False)
#print("only sig")
#csvIndex = ['Instace name','model','Status', 'Obj.Value','MIPGap','Obj. Bound', 't(s)','used_transfer_stations']
#resultDf = pd.DataFrame([info])
#resultDf.to_csv("result_VehicleFlow.csv",mode='a', encoding='utf-8', index=False)

#print(time_measure1, time_measure2, time_measure3)