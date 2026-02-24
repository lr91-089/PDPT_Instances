#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 22:11:54 2024

@author: rocha01
"""



import math
import time
import threading
import os
import re
import copy
import random
import networkx as nx
from networkx.algorithms import flow
from itertools import combinations
from typing import Dict, Set, List, Tuple, Any, Optional
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import igraph as ig
from collections import defaultdict, deque
import heapq

import ast

import gurobipy as gp
from gurobipy import Model, GRB, quicksum, tuplelist
from cap_sep_mip import separate_rounded_capacity_inequalities

#filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-1.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R5-K3-T3/PDPT-R5-K3-T3-Q100-2.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R5-K2-T1/PDPT-R5-K2-T1-Q100-9.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R5-K3-T3/PDPT-R5-K3-T3-Q100-5.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R25-K3-T3/PDPT-R25-K3-T3-Q100-3.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R25-K2-T2/PDPT-R25-K2-T2-Q100-6.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R15-K3-T3/PDPT-R15-K3-T3-Q100-9.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R25-K2-T2/PDPT-R25-K2-T2-Q100-6.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R30-K2-T1/PDPT-R30-K2-T1-Q100-7.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-6.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-2.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-6.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R25-K2-T2/PDPT-R25-K2-T2-Q100-6.txt"
#filename = "./InstancesLiLim/PDPTWT10/PDPTWT_LiLim_R10K4T4C50_lc206.txt"
#filename = "./InstancesLiLim/PDPTWT10/PDPTWT_LiLim_R10K4T4C50_lr107.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R25-K2-T2/PDPT-R25-K2-T2-Q100-6.txt"
#filename = "./InstancesLyu23/PDPTWT/5R4K4T/5R-4K-4T-240L-5.txt"
#filename = "./InstancesLyu23/PDPTWT/5R4K4T/5R-4K-4T-180M-1.txt"
#filename = "./InstancesLyu23/PDPTWT/4R4K4T/4R-4K-4T-180L-4.txt"
#filename = "./InstancesLyu23/PDPTWT/4R4K4T/4R-4K-4T-300L-2.txt"
#filename = "./InstancesLyu23/PDPTWT/4R4K4T/4R-4K-4T-300S-6.txt"
#filename = "./InstancesLyu23/PDPTWT/4R4K4T/4R-4K-4T-180M-1.txt"

#filename = "./InstancesLyu23/PDPT/PDPT-R25-K2-T2/PDPT-R25-K2-T2-Q100-6.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R30-K2-T1/PDPT-R30-K2-T1-Q100-7.txt"
#filename = "./InstancesLyu23/PDPTWT/3R4K4T/3R-4K-4T-180L-8.txt"
#filename = "./InstancesLyu23/PDPTWT/5R4K4T/5R-4K-4T-180L-8.txt"
#filename = "./InstancesLyu23/PDPTWT/4R4K4T/4R-4K-4T-180M-8.txt"
filename = "./InstancesLyu23/PDPTWT/4R4K4T/4R-4K-4T-300L-4.txt"
#time.sleep(3600)
filename = "./InstancesGhilas/HetPDPT_Instances/Small/R_Ghilas_R7K4T1.txt"

filename = "./InstancesGhilas/HetPDPT_Instances/NewCapacities/C_Ghilas_R8K4T1.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-4.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R25-K3-T3/PDPT-R25-K3-T3-Q100-1.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R20-K3-T3/PDPT-R20-K3-T3-Q100-2.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R25-K3-T3/PDPT-R25-K3-T3-Q100-3.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R30-K2-T2/PDPT-R30-K2-T2-Q100-1.txt"
filename = "./InstancesLyu23/PDPT/PDPT-R12-K2-T1/PDPT-R12-K2-T1-Q100-1.txt"

filename = "./InstancesLyu23/PDPT/PDPT-R30-K2-T2/PDPT-R30-K2-T2-Q100-0.txt"
#filename = "./InstancesLyu23/PDPT/PDPT-R30-K2-T2/PDPT-R30-K2-T2-Q100-1.txt"

l_cuts = {}
l_cuts["multTrans"] = []
l_cuts["cycle"] = []
l_cuts["infp"] = []

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
def readDataframeHet(filename,nrequests):
    df = pd.read_csv(filename, skiprows=3, sep='\t')
    R =  list(range(nrequests))
    # temp = [df['node'].str.contains("t") == True]
    indices_to_drop = []
    for index, row in df.iterrows():
        if "t" in row['node']:
            indices_to_drop.append(index)
            for r in R:
                copy = row.copy()
                copy['node'] = copy['node'].replace('t', f'tsr.{r}.')
                df = df._append(copy, ignore_index = True)
                copy['node'] = copy['node'].replace('ts', 'tf')
                df = df._append(copy, ignore_index = True)
                copy = row.copy()
                copy['node'] = copy['node'].replace('t', f'tsc.{r}.')
                df = df._append(copy, ignore_index = True)
                copy['node'] = copy['node'].replace('ts', 'tf')
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

class StrengthenedCapacitySeparation:
    """
    Class for implementing the strengthened capacity constraint separation heuristic.
    Identifies violated cuts and returns them with S, S_prime, and U information.
    Uses a randomized heuristic approach for efficiency.
    """
    
    def __init__(self, P, D, Q, d):
        """
        Initialize the separation heuristic.
        
        Args:
            P: Set of pickup nodes
            D: Set of delivery nodes
            Q: Vehicle capacity
            d: Dictionary mapping nodes to their demand values
        """
        self.P = set(P)
        self.D = set(D)
        self.Q = Q
        self.d = d
        self.pickup_to_delivery = self._create_pickup_to_delivery_map()
        
    def _create_pickup_to_delivery_map(self):
        """Create a mapping from pickup nodes to delivery nodes"""
        pickup_to_delivery = {}
        
        for p in self.P:
            # Extract index from node name
            p_idx = p[1:] if isinstance(p, str) else p
            
            # Find corresponding delivery node
            for d_node in self.D:
                d_idx = d_node[1:] if isinstance(d_node, str) else d_node
                if d_idx == p_idx:
                    pickup_to_delivery[p] = d_node
                    break
        
        return pickup_to_delivery
    
    def _calculate_pi_S(self, S):
        """Calculate π(S) - the set of pickup vertices whose delivery vertex is in S"""
        pi_S = set()
        for p, d in self.pickup_to_delivery.items():
            if d in S and p not in S:
                pi_S.add(p)
        
        return pi_S
    
    def _calculate_U(self, S, S_prime):
        """Calculate U = π(S) \ (S ∪ S')"""
        pi_S = self._calculate_pi_S(S)
        return pi_S - (S | S_prime)
    
    def _calculate_cut_components(self, S, S_prime, x_val):
        """Calculate the components needed to check if a cut is violated"""
        nodes = set()
        for (i, j) in x_val.keys():
            nodes.add(i)
            nodes.add(j)
        
        # Calculate d(S)
        d_S = sum(self.d.get(node, 0) for node in S)
        
        # Calculate U = π(S) \ (S ∪ S')
        U = self._calculate_U(S, S_prime)
        
        # Calculate d(U)
        d_U = sum(self.d.get(node, 0) for node in U)
        
        # Calculate the right-hand side
        rhs = (d_S + d_U) / self.Q
        
        # Calculate the left-hand side
        
        # Calculate x(δ+(S)) - flow out of S
        x_delta_plus_S = sum(x_val.get((i, j), 0) for i in S for j in nodes if j not in S)
        
        # Calculate x(δ-(S')) - flow into S_prime
        x_delta_minus_S_prime = sum(x_val.get((i, j), 0) for i in nodes if i not in S_prime for j in S_prime)
        
        # Calculate x(S:S') - flow from S to S_prime
        x_S_to_S_prime = sum(x_val.get((i, j), 0) for i in S for j in S_prime)
        
        # Calculate left-hand side
        lhs = x_delta_plus_S + x_delta_minus_S_prime - x_S_to_S_prime
        
        # Calculate violation
        violation = rhs - lhs
        
        return lhs, rhs, U, violation
    
    def separate(self, x_val, max_cuts=10, min_violation=1e-6, max_iterations=100):
        """
        Find violated cuts using a randomized strengthened capacity constraint heuristic
        
        Args:
            x_val: Dictionary mapping (i,j) to current variable values
            max_cuts: Maximum number of cuts to return
            min_violation: Minimum violation threshold for cuts
            max_iterations: Maximum number of random subset pairs to try
            
        Returns:
            List of dictionaries with cut information
        """
        
        # Create graph from x_val
        G = nx.DiGraph()
        for (i, j), flow in x_val.items():
            if flow > 0:
                G.add_edge(i, j, flow=flow)
        
        # Get all nodes involved in the solution
        nodes = list(set(i for (i, j) in x_val.keys()) | set(j for (i, j) in x_val.keys()))
        
        # List to store the cuts found
        cuts = []
        
        # Set to track already tried combinations to avoid duplicates
        tried_combinations = set()
        
        # Tabu search parameters
        tabu_list = []
        tabu_size = 10
        
        # Try different random subsets
        for iteration in range(max_iterations):
            # Decide sizes of S and S_prime
            size_S = random.randint(2, min(5, len(nodes) - 1))
            size_S_prime = random.randint(1, min(3, len(nodes) - size_S))
            
            # Select random nodes for S
            S = set(random.sample(nodes, size_S))
            
            # Make sure S has a positive demand
            attempts = 0
            while sum(self.d.get(node, 0) for node in S) <= 0 and attempts < 10:
                S = set(random.sample(nodes, size_S))
                attempts += 1
            
            if attempts == 10:
                continue  # Skip this iteration if can't find S with positive demand
            
            # Select random nodes for S_prime from remaining nodes
            remaining_nodes = [n for n in nodes if n not in S]
            S_prime = set(random.sample(remaining_nodes, size_S_prime))
            
            # Create a hash of the combination to check if we've tried it
            combo_hash = (frozenset(S), frozenset(S_prime))
            if combo_hash in tried_combinations:
                continue
            
            tried_combinations.add(combo_hash)
            
            # Calculate components and check violation
            lhs, rhs, U, violation = self._calculate_cut_components(S, S_prime, x_val)
            
            # Add to cuts if violated
            if violation > min_violation and rhs > 0:
                cut = {
                    'S': S,
                    'S_prime': S_prime,
                    'U': U,
                    'rhs': rhs,
                    'violation': violation
                }
                cuts.append(cut)
                
                # Try to improve the cut with local search
                self._improve_cut(cut, nodes, x_val)
                
                # Update tabu list with this combination
                tabu_list.append(combo_hash)
                if len(tabu_list) > tabu_size:
                    tabu_list.pop(0)
                    
            # If we found enough cuts, stop
            if len(cuts) >= max_cuts:
                break
                
        # Sort cuts by violation (most violated first)
        cuts.sort(key=lambda x: x['violation'], reverse=True)
        
        # Return the most violated cuts
        return cuts[:max_cuts]
    
    def _improve_cut(self, cut, nodes, x_val, max_iterations=10):
        """
        Try to improve a cut using local search
        
        Args:
            cut: The cut to improve
            nodes: List of all nodes
            x_val: Dictionary of variable values
            max_iterations: Maximum improvement iterations
        """
        S = cut['S'].copy()
        S_prime = cut['S_prime'].copy()
        best_violation = cut['violation']
        
        for _ in range(max_iterations):
            improved = False
            
            # Try adding a node to S
            for node in nodes:
                if node not in S and node not in S_prime:
                    S_new = S.copy()
                    S_new.add(node)
                    
                    _, rhs, U, violation = self._calculate_cut_components(S_new, S_prime, x_val)
                    
                    if violation > best_violation and rhs > 0:
                        S = S_new
                        best_violation = violation
                        improved = True
                        break
            
            # Try adding a node to S_prime
            if not improved:
                for node in nodes:
                    if node not in S and node not in S_prime:
                        S_prime_new = S_prime.copy()
                        S_prime_new.add(node)
                        
                        _, rhs, U, violation = self._calculate_cut_components(S, S_prime_new, x_val)
                        
                        if violation > best_violation and rhs > 0:
                            S_prime = S_prime_new
                            best_violation = violation
                            improved = True
                            break
            
            # Try removing a node from S
            if not improved and len(S) > 2:
                for node in list(S):
                    S_new = S.copy()
                    S_new.remove(node)
                    
                    d_S = sum(self.d.get(n, 0) for n in S_new)
                    if d_S <= 0:
                        continue  # Skip if removing this node makes d(S) non-positive
                    
                    _, rhs, U, violation = self._calculate_cut_components(S_new, S_prime, x_val)
                    
                    if violation > best_violation and rhs > 0:
                        S = S_new
                        best_violation = violation
                        improved = True
                        break
            
            # Try removing a node from S_prime
            if not improved and len(S_prime) > 1:
                for node in list(S_prime):
                    S_prime_new = S_prime.copy()
                    S_prime_new.remove(node)
                    
                    _, rhs, U, violation = self._calculate_cut_components(S, S_prime_new, x_val)
                    
                    if violation > best_violation and rhs > 0:
                        S_prime = S_prime_new
                        best_violation = violation
                        improved = True
                        break
            
            # If no improvement was made in this iteration, stop
            if not improved:
                break
        
        # Update the cut with the improved sets
        if best_violation > cut['violation']:
            _, rhs, U, _ = self._calculate_cut_components(S, S_prime, x_val)
            cut['S'] = S
            cut['S_prime'] = S_prime
            cut['U'] = U
            cut['rhs'] = rhs
            cut['violation'] = best_violation
    
    def get_cut_expr(self, model_vars, cut):
        """Create a Gurobi linear expression for the cut"""
        
        S = cut['S']
        S_prime = cut['S_prime']
        rhs = cut['rhs']
        
        # Get all nodes from model_vars
        nodes = set()
        for (i, j) in model_vars.keys():
            nodes.add(i)
            nodes.add(j)
        
        # Create linear expression
        expr = gp.LinExpr()
        
        # Add x(δ+(S)) terms - flow out of S
        for i in S:
            for j in nodes:
                if j not in S and (i, j) in model_vars:
                    expr += model_vars[(i, j)]
        
        # Add x(δ-(S')) terms - flow into S_prime
        for i in nodes:
            for j in S_prime:
                if i not in S_prime and (i, j) in model_vars:
                    expr += model_vars[(i, j)]
        
        # Subtract x(S:S') terms - flow from S to S_prime
        for i in S:
            for j in S_prime:
                if (i, j) in model_vars:
                    expr -= model_vars[(i, j)]
        
        return expr, rhs

def create_precedence_graph_layout(G):
    """
    Create a layout for vehicle precedence graph where each vehicle 
    is on a separate horizontal line with nodes in order.
    """
    
    # Categorize nodes by type and vehicle
    vehicle_nodes = defaultdict(list)  # vehicle_id -> [nodes in order]
    node_types = {}
    
    for node in G.nodes():
        node_str = str(node)
        
        # Vehicle start nodes (o0, o1, o2)
        if node_str.startswith('o'):
            vehicle_id = int(node_str[1:])
            node_types[node] = 'start'
            
        # Vehicle end nodes (e0, e1, e2)
        elif node_str.startswith('e'):
            vehicle_id = int(node_str[1:])
            node_types[node] = 'end'
            
        # Transfer start nodes (ts.vehicle.station)
        elif node_str.startswith('ts.'):
            parts = node_str.split('.')
            vehicle_id = int(parts[1])
            node_types[node] = 'transfer_start'
            
        # Transfer finish nodes (tf.vehicle.station)
        elif node_str.startswith('tf.'):
            parts = node_str.split('.')
            vehicle_id = int(parts[1])
            node_types[node] = 'transfer_end'
            
        # Pickup nodes (p1, p2, etc.)
        elif node_str.startswith('p'):
            # For pickup/delivery, we need to determine which vehicle serves them
            # This requires analyzing the graph structure
            vehicle_id = None
            node_types[node] = 'pickup'
            
        # Delivery nodes (d1, d2, etc.)
        elif node_str.startswith('d'):
            vehicle_id = None
            node_types[node] = 'delivery'
        else:
            vehicle_id = None
            node_types[node] = 'other'
        
        # Add to vehicle_nodes if we identified a vehicle
        if vehicle_id is not None:
            vehicle_nodes[vehicle_id].append(node)
    
    # For pickup/delivery nodes, assign them to vehicles based on graph connectivity
    unassigned_nodes = [node for node in G.nodes() 
                       if node_types[node] in ['pickup', 'delivery', 'other']]
    
    # Try to assign pickup/delivery nodes to vehicles based on paths
    for node in unassigned_nodes:
        for vehicle_id in vehicle_nodes.keys():
            vehicle_start = f'o{vehicle_id}'
            vehicle_end = f'e{vehicle_id}'
            
            # Check if there's a path from vehicle start through this node to vehicle end
            if (vehicle_start in G.nodes() and vehicle_end in G.nodes() and
                node in G.nodes()):
                try:
                    if (nx.has_path(G, vehicle_start, node) and 
                        nx.has_path(G, node, vehicle_end)):
                        vehicle_nodes[vehicle_id].append(node)
                        break
                except:
                    continue
    
    return vehicle_nodes, node_types

def order_nodes_in_vehicle(G, nodes, vehicle_id):
    """
    Order nodes for a vehicle based on the precedence relationships.
    """
    if not nodes:
        return []
    
    # Create subgraph with only these nodes
    subgraph = G.subgraph(nodes)
    
    # Try topological sort if the subgraph is a DAG
    try:
        if nx.is_directed_acyclic_graph(subgraph):
            return list(nx.topological_sort(subgraph))
    except:
        pass
    
    # Fallback: order by node type priority
    start_nodes = [n for n in nodes if str(n).startswith(f'o{vehicle_id}')]
    transfer_start = [n for n in nodes if str(n).startswith('ts.') and f'.{vehicle_id}.' in str(n)]
    pickup_nodes = [n for n in nodes if str(n).startswith('p')]
    delivery_nodes = [n for n in nodes if str(n).startswith('d')]
    transfer_end = [n for n in nodes if str(n).startswith('tf.') and f'.{vehicle_id}.' in str(n)]
    end_nodes = [n for n in nodes if str(n).startswith(f'e{vehicle_id}')]
    
    # Sort within each category
    pickup_nodes.sort(key=lambda x: int(str(x)[1:]) if str(x)[1:].isdigit() else 0)
    delivery_nodes.sort(key=lambda x: int(str(x)[1:]) if str(x)[1:].isdigit() else 0)
    
    ordered = start_nodes + transfer_start + pickup_nodes + delivery_nodes + transfer_end + end_nodes
    
    # Add any remaining nodes
    remaining = [n for n in nodes if n not in ordered]
    ordered.extend(remaining)
    
    return ordered

def draw_precedence_graph(G, figsize=(15, 8)):
    """
    Draw the precedence graph with vehicles in separate horizontal lines.
    """
    vehicle_nodes, node_types = create_precedence_graph_layout(G)
    
    # Create positions
    pos = {}
    vehicle_colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    node_colors = []
    
    # Set up the plot
    plt.figure(figsize=figsize)
    
    # Position nodes for each vehicle
    y_spacing = 2.0
    x_spacing = 2.0
    
    max_nodes = max(len(nodes) for nodes in vehicle_nodes.values()) if vehicle_nodes else 1
    
    for i, (vehicle_id, nodes) in enumerate(sorted(vehicle_nodes.items())):
        y_pos = -i * y_spacing
        
        # Order nodes for this vehicle
        ordered_nodes = order_nodes_in_vehicle(G, nodes, vehicle_id)
        
        # Position nodes horizontally
        for j, node in enumerate(ordered_nodes):
            pos[node] = (j * x_spacing, y_pos)
            
    # Draw the graph
    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.6, arrows=True, 
                          arrowsize=20, edge_color='gray')
    
    # Draw nodes with different colors based on type
    type_colors = {
        'start': 'lightgreen',
        'end': 'lightcoral', 
        'pickup': 'lightblue',
        'delivery': 'lightyellow',
        'transfer_start': 'lightpink',
        'transfer_end': 'lightcyan',
        'other': 'lightgray'
    }
    
    for node_type, color in type_colors.items():
        nodes_of_type = [node for node in G.nodes() 
                        if node in node_types and node_types[node] == node_type]
        if nodes_of_type:
            nx.draw_networkx_nodes(G, pos, nodelist=nodes_of_type, 
                                 node_color=color, node_size=800, alpha=0.8)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # Add vehicle labels on the left
    for i, vehicle_id in enumerate(sorted(vehicle_nodes.keys())):
        plt.text(-1, -i * y_spacing, f'Vehicle {vehicle_id}', 
                fontsize=12, fontweight='bold', ha='right', va='center')
    
    # Add legend
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.8, label=node_type.replace('_', ' ').title()) 
                      for node_type, color in type_colors.items()]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.title('Vehicle Precedence Graph', fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Model
def twoIndexModelUB(filename, mode="two",timeFlow=True,cutTrans=False):
    
    print(filename)
    metaData = readMetaData(filename)
    HET = False
    if "Ghilas" in filename:
        df = readDataframeHet(filename,int(metaData["nr"]))
        HET = True
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
    if HET:
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
        
    nRequests = int(metaData['nr'].iloc[0])
    nVehicles = int(metaData['nv'].iloc[0])
    nTransports = int(metaData['nt'].iloc[0])
    VC = int(metaData['capacity'].iloc[0])
    K = list(range(nVehicles))
    
    df["points"] = df[["x","y"]].values.tolist()

    points = df.set_index("node")["points"].to_dict()
    
    qnode = df.set_index('node')["load"].to_dict()
    q = {int(i.replace("p","")):qnode[i] for i in P}
    
    timeHorizon = df["a"].max()
    
    df["tw"] = df[["a","b"]].values.tolist()
    
    timeWindows = df.set_index('node')["tw"].to_dict()
    if HET:
        for i in TSR:
            r = int(i.split(".")[1])
            a = timeWindows[f"p{r}"][0]
            b = timeWindows[f"d{r}"][1]
            timeWindows[i][0] = a
            timeWindows[i][1] = b 
    
    c = distancesMatrix(df)
    
    
    pd_dict = {i:i.replace("p","d") for i in P}
    
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
        
    def check_no_time_window_violation(i,j):
        #returns true if no time window violation
        if VC<0:
            if i not in VO:
                if timeWindows[i][0]+service_time[i]+c[i,j]<=timeWindows[j][1]+service_time[j]:
                    return True
            else:
                if timeWindows[i][0]+c[i,j]<=timeWindows[j][1]+service_time[j]:
                    return True
        else:
            if timeWindows[i][0]+c[i,j]+service_time[i]<=timeWindows[j][1]:
                return True
        return False
    
    def check_feasibility(path):
        i = path[0]
        if i in VO:
            z = timeWindows[i][0]
        else:
            z = timeWindows[i][0]
        for j in path[1:]:
            if (i,j) in arcs:
                if VC<0:
                    z = max(z+service_time[j]+c[i,j],timeWindows[j][0])
                    if z-service_time[j]>timeWindows[j][1]:
                        #return True
                        return False
                else:
                    z = max(z+service_time[i]+c[i,j],timeWindows[j][0])
                    if z>timeWindows[j][1]:
                        return False
                i = j
            else:
                return False
        return True
    
    R = list(range(nRequests))
        
    arcs = []
    ats = set()
    min_vec = VC
    if HET:
        min_vec = Qmax
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
                if cutTrans ==True:
                    if check_no_time_window_violation(i,j)==True:
                        arcs.append((i,j))   
                else:
                    if j.split(".")[1]==i.split(".")[1]:
                      if check_no_time_window_violation(i,j)==True:
                        arcs.append((i,j))   


    arcs = list(dict.fromkeys(arcs))
    
    #A = [(i,j) for i in V for j in V if i!=j]
    
    A = tuplelist(arcs)
    
    Ayc = [(i,j,r) for r in R for i in P for j in V-(frozenset((i,f"p{r}"))|VO|VD|TF) if (i,j) in A]
    Ayd = [(i,j,r) for r in R for i in D-frozenset(("d"+str(r),)) for j in (V-frozenset([i,i.replace("d","p"),f"p{r}"])-VO-VD-TF) if (i,j) in A]
    if HET==True:
        Ayts = [(i,j,r) for r in R for i in TSR for j in TF_loc[int(i.split(".")[2])]]
    else:
        Ayts = [(i,j,r) for r in R for i in TS for j in TF_loc[int(i.split(".")[2])]]
    Aytf = [(i,j,r) for r in R for i in TF for j in V-(frozenset((i,f"p{r}"))|VO|VD|TF|frozenset(TS_loc[int(i.split(".")[2])])) if (i,j) in A]

    
    Ay = Ayc+Ayd+Ayts+Aytf
      
    
    #print(Ay[('d1', 'p1',1)])
    
    Ay = tuplelist(Ay)
    TIy = tuplelist([(i,j) for i in TS for j in TF_loc[int(i.split(".")[2])] if i!=j.replace("f","s")])

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
    
    Mij = {(i,j):max(0,timeWindows[i][1]+c[i,j]+service_time[i]-timeWindows[j][0]) for (i,j) in c}
    M = max(Mij.values())
    #Mt = {i: max(0,timeWindows[i][1]-min(c[i.replace("s","f"),j]+c[j,de] for j in D for de in VD)) for i in TS|TF}
    #Mt = {(i,j):(timeWindows[i][1]-c[i.replace("s","f"),"e"+i.split(".")[1]])-max(c["o"+j.split(".")[1].replace("f","s"),i],timeWindows[j][0]) for i in TS for j in TF}

    wbTW = {(i,j):min(timeWindows[i][1],timeWindows[j][1]-c[i,j]-service_time[i]) for (i,j) in arcs}

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
                
    #change travel times
    
             
    def create_pdptw_model(filename, cut=None, strCap=True, env=None,solver_state=None):
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
             model1._solver_state = solver_state
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
                vl = model1.addVars(V, vtype=GRB.CONTINUOUS, name='vl') 
              
             #b = model1.addVars(xIndex,lb=0.0, ub=nVehicles ,vtype=GRB.CONTINUOUS, name="b")
             #z = model1.addVars(zIndex,lb=0.0 ,vtype=GRB.CONTINUOUS, name="z")
             z = model1.addVars(A2,vtype=GRB.CONTINUOUS, name="z")
             #a = model1.addVars([(i,r) for i in TS for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="a")
             #bz = model1.addVars(zIndex,lb=0.0 ,vtype=GRB.CONTINUOUS, name="bz")
             #ba = model1.addVars([(i,r) for i in TF for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="ba")
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
                 if "Lim" not in filename and "Ghilas" not in filename:
                     model1.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A.select(vo,'*')]) == 1 for vo in VO), name = "ct.route_startFirst")
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
                
                 model1.addConstrs((quicksum(q[r]*y[i, j,r] for r in R for j in [a[1] for a in Ay2.select(i,'*',r)]) <= Qmin+vl[i] for i in P|D), name="ct.VehicleCapacity")
                
         
                
             
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
             
              
             
             
             """
             Time Windows
             """
             """
             model1.addConstrs((z[i]+service_time[i]+c[i,j]-(Mij[i,j])*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A2.select(i,'*')] if (j,i) not in A2), name = "ct.time_flowA")
             
             model1.addConstrs((z[i]-z[j]+Mij[i,j]*x[i,j]+(Mij[i,j]-service_time[i]-c[i,j]+min(-c[j,i]-service_time[j],timeWindows[j][0]-timeWindows[i][1]))*x[j,i]<= Mij[i,j]-c[i,j]-service_time[i]  for i in V for j in [a[1] for a in A2.select(i,'*')] if (j,i) in A2), name = "ct.time_flowLifted")
             model1.addConstrs((timeWindows[i][1] >= z[i] for i in V), name="ct.TimeWindowLatest")
             model1.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliest")
             """
      
             #model1.addConstrs((quicksum(z[i,j] for j in [a[1] for a in A2.select(i,'*')])-quicksum(z[j,i] for j in [a[0] for a in A2.select('*',i)])== quicksum((c[i,j]+service_time[i])*x[i,j] for j in [a[1] for a in A2.select(i,'*')])  for i in P|D|VO), name = "ct.time_flowA")
             
             
             #model1.addConstrs((z[i,j] >= (c[i,j]+service_time[i])*x[i,j] for (i,j) in A2), name='ct.TimeLB')
             
             #model1.addConstrs((z[i,j] <= (timeWindows[j][1])*x[i,j] for (i,j) in A2), name='ct.TimeUB')
             
             #model1.addConstr((quicksum((c[i,j]+service_time[i])*x[i,j] for (i,j) in A2)<= int(df.b.max())*len(K)), name='ct.GlobalUB')
            
            
             model1.addConstrs(
                (
                    gp.quicksum(
                        z[i, j] + (c[i,j]+service_time[i]) * x[i, j]
                        for i in P|D|VO
                        if (i, j) in A2
                    )
                    <= z.sum(j,"*")
                    for j in P|D
                ),
                    name="ct.time_flowA",
              )

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
             
            
             
             
         
              
             
             # Data for callback
             model1._obj = None
             model1._bd = None
             model1._gap = None
             model1._data = []
             model1._x = x
             model1._A2 = A2
             model1._Ay2 = Ay2
             model1._V = V
             model1._y = y
             model1._z = z
             model1._vars = model1.getVars()
             if "Sartori" not in filename:
                 model1._bl = bl
             model1._start = time.time()
             model1.Params.MIPFocus = 1
             #model1.Params.PreCrush = 0
             model1.Params.OutputFlag = 0
             model1.Params.LogToConsole=0
             return model1
    
    def solve_pdptw(model1,timelim, barrier=None,cut=None,last_sol=None, sollim=None):
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
        if model1.Status == GRB.OPTIMAL:
            #os.remove(f"{filename}_{cut}.sol") 
            model1.write(f"{filename}_{cut}.sol")
            #sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
            infos = [filename, model1.ModelName ,gurobi_status_dict.get(model1.Status),model1.ObjVal, model1.MIPGap,model1.ObjBound, model1.Runtime,0]  

            
        elif model1.Status == GRB.TIME_LIMIT:
            if model1.SolCount == 0:
                sol_transfers = None
                infos = [filename, model1.ModelName ,gurobi_status_dict.get(model1.Status),model1.ObjVal, model1.MIPGap,model1.ObjBound, model1.Runtime,0]    
            else:
                #os.remove(f"{filename}_{cut}.sol") 
                model1.write(f"{filename}_{cut}.sol")
                print("time limit solution")
                infos = [filename, model1.ModelName ,gurobi_status_dict.get(model1.Status),model1.ObjVal, model1.MIPGap,model1.ObjBound, model1.Runtime,0]    
        else:
            #if model.status==3:
             #  model.computeIIS()
              # model.write("infeasible_model.ilp")
            infos = [filename, model1.ModelName ,gurobi_status_dict.get(model1.Status),np.inf, np.inf,np.inf, model1.Runtime,0] 
        return infos
    
    def fork_constraint(model,x,path,mipsol=True):
        outfork_set = set((path[-1],))
        last_leg = path[-2]
        pathf = path [:-1]
        edgesl = [(pathf[i], pathf[i + 1]) for i in range(len(pathf) - 1)]
        edges = [(i,j) for i in pathf for j in pathf if (i,j) in A]
        plength =sum(c[e] for e in edgesl)
        LHS = quicksum(model._x[i, j] for (i,j) in edges if (i,j) in A)
        for i in V-set(pathf):
            if (last_leg,i) in A:
                if plength + c[last_leg,i]>df.b.max():
                    outfork_set.add(i)

        LHS += quicksum(model._x[last_leg, j] for j in outfork_set )
        if mipsol==True:
            model.cbLazy(
                LHS#for (i,j) in edges)#
                <= len(path)-2
                )
            model._lazy_cuts["IP"] +=1
            print("added fork constraint ", len(path), path)
            #l_cuts["ipath"].append((path,outfork_set))
        else:
            model.cbCut(
                LHS#for (i,j) in edges)#
                <= len(path)-2
                )
            #model._lazy_cuts["IP"] +=1
            print("added fork constraint ", len(path), path)
    
    def illegal_path_cut(model,x,G,path, mipsol=True):
        fork_constraint(model,x,path,mipsol=True)
        return
        edges = [(path[i], [i + 1]) for i in range(len(path) - 1)]

        """
        S = set()
        Tset   = set()
        T_locs = set()
        for i in path:
            if "t" not in S:
                S.add(i)
            else:
                Tset.add(int(i[-1]))
                T_locs.add(i)
        #+edges = list(zip(path, path[1:]))
        if len(find_duplicate_location_indices(T_locs-TF))==0:
            #breakpoint()
            LHS = quicksum(model._x[i, j] for i in S for j in path if (i,j) in A)
            LHS += quicksum(model._f[f"ts{idx}"] for idx in Tset)
            LHS += quicksum(model._x[i,j] for i in S for idx in Tset for j in TS_loc[idx] if (i,j) in A)
            LHS += quicksum(model._x[i,j] for j in S for idx in Tset for i in TF_loc[idx] if (i,j) in A)
        else:"""
        #breakpoint()
        LHS = quicksum(model._x[i, j] for i in path for j in path if (i,j) in A)
        #if np.random.rand()<0.67:
        if mipsol==True:
            model.cbLazy(
                LHS#for (i,j) in edges)#
                <= len(path)-2
                )
            model._lazy_cuts["IP"] +=1
            print("added lazy illegal path cut ", len(path), path)
            #l_cuts["ipath"].append(path)
        else:
            model.cbCut(
                LHS#for (i,j) in edges)#
                <= len(path)-2
                )
            model._lazy_cuts["IP"] +=1
            print("added user illegal path cut ", len(path), path)
        #else:
         #   fork_constraint(model,x,path,mipsol)
        
        
    def check_location_validity(locations_list):
        # Extract the location indices (second number in the string)
        location_indices = []
        for loc in locations_list:
            parts = loc.split('.')
            if len(parts) == 3:  # Ensure the format is correct
                location_index = int(parts[2])
                location_indices.append(location_index)
        
        # Check if any location index appears more than once
        seen_indices = set()
        for idx in location_indices:
            if idx in seen_indices:
                return False  # Invalid - location index appears multiple times
            seen_indices.add(idx)
        
        return True  # Valid - each location index appears at most once

    def find_duplicate_location_indices(locations_list):
        # Dictionary to store locations grouped by their location index
        locations_by_index = {}
        
        # Group locations by their location index
        for loc in locations_list:
            parts = loc.split('.')
            if len(parts) == 3:  # Ensure the format is correct
                location_index = int(parts[2])
                
                if location_index not in locations_by_index:
                    locations_by_index[location_index] = []
                
                locations_by_index[location_index].append(loc)
        
        # Find duplicates (indices with more than one location)
        duplicates = {}
        for index, locs in locations_by_index.items():
            if len(locs) > 1:
                duplicates[index] = locs
        
        return duplicates    

    def get_path_in_cycle(start_node, end_node,cycle_edges):
        """
        Find the path between two nodes in a cycle.
        
        Args:
            cycle_edges: List of tuples representing edges in the cycle
            start_node: Starting node
            end_node: Ending node
        
        Returns:
            List of nodes representing the path from start_node to end_node
        """
        # Build adjacency map from the cycle edges
        graph = {}
        for from_node, to_node in cycle_edges:
            graph[from_node] = to_node
        
        # Find path by following the cycle
        path = []
        current = start_node
        
        # Keep following edges until we reach the end node
        while current != end_node:
            path.append(current)
            if current not in graph:
                # Node not found in cycle
                return None
            current = graph[current]
        
        # Add the end node to complete the path
        path.append(end_node)
        
        return path[1:-1]
    
    def check_illegal_transfer02(model, x, y, z, cur_obj):
        #returns true if cut was added

        G = nx.DiGraph()
        #for e in z:
         #  G.add_edge(e[0],e[1],arrival_time=z[e])
        
        G.add_edges_from(x)
        #check path length
        for node in VO:
            if node in G.nodes:
                z_val = 0.0
                for u, v in nx.dfs_edges(G, source=node):
                    z_val+=c[u,v]
                    G[u][v]["arrival_time"] = z_val

        transfers = list()
        transfer_order = dict(sorted(
            {a: x[a] for a in x if "ts" in a[0]}.items(),
            key=lambda item: item[1]
        ))
        #create precedence graph
        transfer_requests = []
        for tedge in transfer_order:
            for a in list(y.select(tedge[0],"*","*"))+list(y.select("*",tedge[1],"*")):
                if (a[0],a[1]) in TIy:
                    trans_edge = (a[0],a[1])
                    if trans_edge not in transfers:
                        if (a[0],a[0].replace("ts","tf")) in x and (a[1].replace("tf","ts"),a[1]) in x:
                            G.add_edge(a[0],a[1],arrival_time=G[a[0]][a[0].replace("ts","tf")]["arrival_time"])
                            transfers.append(trans_edge)
                            transfer_requests.append(a)

        if len(transfers)==0:
            return False
        try:
             cycle = nx.find_cycle(G, orientation=None)
             illegal_requests = [a for a in transfer_requests if (a[0],a[1]) in cycle]
             for i,j,r2 in illegal_requests:
                 model.cbLazy(model._ti[i,j]>= model._y[i,j,r2])
                 model._lazy_cuts["transferCycleCutR2"] +=1
             #reverse_requests = [(e[1].replace("f","s"),e[0].replace("s","f"),e[2]) for e in illegal_requests]
             x_cycle = {a for a in cycle if a not in TIy}
             S = set()
             for edge in x_cycle:
                 # Each edge is a tuple (source, target)
                 source, target = edge
                 S.add(source)
                 S.add(target)
             #for e in reverse_requests:
                 #S.add(e[0])
                 #S.add(e[1])
             S = frozenset(S)
             if S not in model._cb_cuts:
                 LHS_check = 0.0
                 model._cb_cuts.add(S)
                 LHS = quicksum(model._x[i,j] for i in S for j in S if (i,j) in A)
                 LHS += quicksum(model._ti[e[0],e[1]] for e in illegal_requests)#+reverse_requests)
                 LHS_check += len(illegal_requests)+sum(x[i,j] for i in S for j in S if (i,j) in x)
                 #l_cuts["1cycle"].append((S,tuple(illegal_requests)))
                 #strngthened version of cycle cut performs worse?
                 #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                 model.cbLazy(
                        LHS
                        #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                        <= len(cycle)-1
                 )
                 model._lazy_cuts["transferCycleCutR1"] +=1
                 if LHS_check-(len(cycle)-1)>1.5:
                        model._error_msgs +="added wrong lazy illegal request transfer cut 1 {LHS_check}<={len(cycle)-1}; "
                 #print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)
                 print(f"added lazy illegal request transfer cut {LHS_check}<={len(cycle)-1}", illegal_requests,cycle)
                 #if LHS_check<= len(cycle)-1:
                  #   breakpoint()
                   #  print("lol")
             return True

        except nx.NetworkXNoCycle:
             pass
         
        # Step 1: Initialize all arrival times
        for u in G.nodes():
            G.nodes[u]["arrival_time"] = 0.0
        
        # Step 2: Topological propagation
        arrival_time = {u: 0.0 for u in G.nodes()}
        for u in nx.topological_sort(G):
            for v in G.successors(u):
                # Store arrival time at u on edge (u, v)
                G[u][v]["arrival_time"] = arrival_time[u]
                
                # Compute arrival at v
                arrival_time[v] = max(arrival_time[v],timeWindows[v][0], arrival_time[u] + c.get((u, v), 0))
                # Step 3: check time violation
                if G[u][v]["arrival_time"]>wbTW.get((u,v),df.b.max()):
                    """
                    S = set(nx.ancestors(G, v)) | {v}
                    SA =  [(i,j) for i in S for j in S if (i,j) in x]
                    LHS = quicksum(model._x[e] for e in SA)+quicksum(model._y[e] for e in transfer_requests) 
                    RHS = len(SA)+len(transfer_requests)-1
                    model.cbLazy(
                        LHS#for (i,j) in edges)#
                        <= RHS
                        )"""
                    LHS = quicksum(model._x[e] for e in model._A if e not in x) 
                    LHS_check = sum(x.get(e,0) for e in model._A if e not in x)
                    RHS = 1.0
                    model.cbLazy(
                        LHS#for (i,j) in edges)#
                        >= RHS
                        )
                    #print(f"added lazy illegal transfer path cut {LHS_check}<={RHS}")
                    #print(u,arrival_time[u],x)
                    #if LHS_check>=RHS:
                        #breakpoint()
                        #model._error_msgs +=f"error IP_trans: {LHS_check}>={RHS}; "
                    model._lazy_cuts["IP_trans"] += 1
                    return True
            

                #print(path)
        #nx.get_edge_attributes(G, "arrival_time")
        return False
    
    def check_illegal_transfer0(model, x, y, z, cur_obj):
        #returns true if cut was added

        G = nx.DiGraph()
        #for e in z:
         #  G.add_edge(e[0],e[1],arrival_time=z[e])
        
        G.add_edges_from(x)
        #check path length
        for node in VO:
            if node in G.nodes:
                z_val = 0.0
                for u, v in nx.dfs_edges(G, source=node):
                    z_val+=c[u,v]
                    G[u][v]["arrival_time"] = z_val

        transfers = list()
        transfer_order = dict(sorted(
            {a: x[a] for a in x if "ts" in a[0]}.items(),
            key=lambda item: item[1]
        ))
        #create precedence graph
        transfer_requests = []
        for tedge in transfer_order:
            for a in list(y.select(tedge[0],"*","*"))+list(y.select("*",tedge[1],"*")):
                if (a[0],a[1]) in TIy:
                    trans_edge = (a[0],a[1])
                    if trans_edge not in transfers:
                        if (a[0],a[0].replace("ts","tf")) in x and (a[1].replace("tf","ts"),a[1]) in x:
                            G.add_edge(a[0],a[1],arrival_time=G[a[0]][a[0].replace("ts","tf")]["arrival_time"])
                            transfers.append(trans_edge)
                            transfer_requests.append(a)

        if len(transfers)==0:
            return False
        try:
             cycle = nx.find_cycle(G, orientation=None)
             illegal_requests = [a for a in transfer_requests if (a[0],a[1]) in cycle]
             #reverse_requests = [(e[1].replace("f","s"),e[0].replace("s","f"),e[2]) for e in illegal_requests]
             x_cycle = {a for a in cycle if a not in TIy}
             S = set()
             for edge in x_cycle:
                 # Each edge is a tuple (source, target)
                 source, target = edge
                 S.add(source)
                 S.add(target)
             #for e in reverse_requests:
                 #S.add(e[0])
                 #S.add(e[1])
             LHS_check = 0.0
             LHS = quicksum(model._x[i,j] for i in S for j in S if (i,j) in A)
             LHS += quicksum(model._y[e] for e in illegal_requests)#+reverse_requests)
             LHS_check += len(illegal_requests)+sum(x[i,j] for i in S for j in S if (i,j) in x)
             #l_cuts["cycle"].append((S,tuple(illegal_requests)))
             #strngthened version of cycle cut performs worse?
             #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
             model.cbLazy(
                    LHS
                    #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                    <= len(cycle)-1
             )
             model._lazy_cuts["transferCycleCutR1"] +=1
             if LHS_check-(len(cycle)-1)>1.5:
                    model._error_msgs +="added wrong lazy illegal request transfer cut 1 {LHS_check}<={len(cycle)-1}; "
             #print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)
             print(f"added lazy illegal request transfer cut {LHS_check}<={len(cycle)-1}", illegal_requests,cycle)
             #breakpoint()
             return True

        except nx.NetworkXNoCycle:
             pass
         
        # Step 1: Initialize all arrival times
        for u in G.nodes():
            G.nodes[u]["arrival_time"] = 0.0
        
        # Step 2: Topological propagation
        arrival_time = {u: 0.0 for u in G.nodes()}
        for u in nx.topological_sort(G):
            for v in G.successors(u):
                # Store arrival time at u on edge (u, v)
                G[u][v]["arrival_time"] = arrival_time[u]
                
                # Compute arrival at v
                arrival_time[v] = max(arrival_time[v],timeWindows[v][0], arrival_time[u] + c.get((u, v), 0))
                # Step 3: check time violation
                if G[u][v]["arrival_time"]>wbTW.get((u,v),df.b.max()):
                    """
                    S = set(nx.ancestors(G, v)) | {v}
                    SA =  [(i,j) for i in S for j in S if (i,j) in x]
                    LHS = quicksum(model._x[e] for e in SA)+quicksum(model._y[e] for e in transfer_requests) 
                    RHS = len(SA)+len(transfer_requests)-1
                    model.cbLazy(
                        LHS#for (i,j) in edges)#
                        <= RHS
                        )"""
                    LHS = quicksum(model._x[e] for e in model._A if e not in x) 
                    LHS_check = sum(x.get(e,0) for e in model._A if e not in x)
                    RHS = 1.0
                    model.cbLazy(
                        LHS#for (i,j) in edges)#
                        >= RHS
                        )
                    print(f"added lazy illegal transfer path cut {LHS}<={RHS}")
                    print(u,arrival_time[u],x)
                    #if LHS_check>=RHS:
                        #breakpoint()
                        #model._error_msgs +=f"error IP_trans: {LHS_check}>={RHS}; "
                    #model._lazy_cuts["IP_trans"] += 1
                    return True
            

        
                #print(path)
        #nx.get_edge_attributes(G, "arrival_time")
        return False
    
    class TransferConnector:
        def __init__(self, 
                     i,j,r,S_sets=[]):
            self.i = i
            self.j = j
            self.r = r
            for idx in S_sets:
                if i in S_sets[idx]:
                    self.in_set_id = idx
                if j in S_sets[idx]:
                    self.out_set_id = idx
        def get_params(self):
            return self.i, self.j, self.r, self.in_set_id, self.out_set_id
        def set_in_set(self,idx):
            self.in_set_id = idx
        def set_out_set(self,idx):
            self.out_set_id = idx
        
        def reverse(self):
            rev_tc = TransferConnector(self.j.replace("f","s"),self.i.replace("s","f"),self.r)
            rev_tc.set_in_set(self.out_set_id)
            rev_tc.set_out_set(self.in_set_id)
            return rev_tc
        
        
    def create_vehicle_connector_copies(transfer_connector):
        copies = set()
        copies.add(transfer_connector)
        copies.add(transfer_connector.reverse())
        i,j,r,in_set_id, out_set_id = transfer_connector.get_params()
        for k,l in TIy:
            if k!=i and l!=j and k.replace("s","f")!=l:
                new_transfer_connector = TransferConnector(k,l,r)
                new_transfer_connector.set_in_set(in_set_id)
                new_transfer_connector.set_out_set(out_set_id)
                copies.add(new_transfer_connector)
                copies.add(new_transfer_connector.reverse())
        return copies
    
    
                
    def check_illegal_transfer_simple(model, x, y, z, cur_obj):
        G = nx.DiGraph()
        #for e in z:
         #  G.add_edge(e[0],e[1],arrival_time=z[e])
        
        G.add_edges_from(x)
        #check path length
        for node in VO:
            if node in G.nodes:
                z_val = 0.0
                for u, v in nx.dfs_edges(G, source=node):
                    z_val+=c[u,v]
                    G[u][v]["arrival_time"] = z_val

        transfers = list()
        transfer_order = dict(sorted(
            {a: x[a] for a in x if "ts" in a[0]}.items(),
            key=lambda item: item[1]
        ))
        #create precedence graph
        transfer_requests = []
        for tedge in transfer_order:
            for a in list(y.select(tedge[0],"*","*"))+list(y.select("*",tedge[1],"*")):
                if (a[0],a[1]) in TIy:
                    trans_edge = (a[0],a[1])
                    if trans_edge not in transfers:
                        if (a[0],a[0].replace("ts","tf")) in x and (a[1].replace("tf","ts"),a[1]) in x:
                            G.add_edge(a[0],a[1],arrival_time=G[a[0]][a[0].replace("ts","tf")]["arrival_time"])
                            transfers.append(trans_edge)
                            transfer_requests.append(a)

        if len(transfers)==0:
            return False
        try:
             cycle = nx.find_cycle(G, orientation=None)
             transfer_map = {(e[0], e[1]): e for e in transfer_requests}

             illegal_requests = [transfer_map[(a[0], a[1])] 
                               for a in cycle 
                               if (a[0], a[1]) in transfer_map]
             x_cycle = {a for a in cycle if a not in TIy}
             Gx = nx.Graph()
             cycle_dict = {}
             Gx.add_edges_from(x_cycle)
             connected_components = list(nx.connected_components(Gx))
             y_set = set()
             shared_x_sets = {i: component for i, component in enumerate(connected_components)}
             all_tcs = set()
             for r in illegal_requests:
                 tc = TransferConnector(r[0],r[1],r[2],shared_x_sets)
                 all_tcs = all_tcs.union(create_vehicle_connector_copies(tc))
             for tc in all_tcs:
                 y_set.add((tc.i,tc.j,tc.r))
                 shared_x_sets[tc.in_set_id].add(tc.i)
                 shared_x_sets[tc.out_set_id].add(tc.j)
             LHS = quicksum(model._y[e] for e in y_set)
             LHS_check = len(illegal_requests)
             for key in shared_x_sets:
                 LHS += quicksum(model._x[i,j] for i in shared_x_sets[key] for j in shared_x_sets[key] if (i,j) in A)
                 
             #model.cbLazy(LHS<=len(cycle)-1)
             print("cycke cut", len(illegal_requests))
             model._lazy_cuts[f"transferCycleCutR{len(illegal_requests)}"] +=1
        except nx.NetworkXNoCycle:
             pass
        # Step 1: Initialize all arrival times
        for u in G.nodes():
            G.nodes[u]["arrival_time"] = 0.0
        
        # Step 2: Topological propagation
        arrival_time = {u: 0.0 for u in G.nodes()}
        for u in nx.topological_sort(G):
            for v in G.successors(u):
                # Store arrival time at u on edge (u, v)
                G[u][v]["arrival_time"] = arrival_time[u]
                
                # Compute arrival at v
                arrival_time[v] = max(arrival_time[v],timeWindows[v][0], arrival_time[u] + c.get((u, v), 0))
                # Step 3: check time violation
                if G[u][v]["arrival_time"]>wbTW.get((u,v),df.b.max()):
                    LHS = quicksum(model._x[e] for e in model._A if e not in x)
                    LHS_check = sum(x.get(e,0) for e in model._A if e not in x)
                    RHS = 1.0
                    model.cbLazy(
                        LHS#for (i,j) in edges)#
                        >= RHS
                        )
                    #print(f"added lazy illegal transfer path cut {LHS_check}<={RHS}")
                    #print(p1,p2)
                    if LHS_check>=RHS:
                        #breakpoint()
                        model._error_msgs +=f"error IP_trans: {LHS_check}>={RHS}; "
                    model._lazy_cuts["IP_trans"] += 1
                    #l_cuts["infp"].append(LHS)
                    return True
        
    def check_illegal_transfer(model, x, y, z, cur_obj):
        #returns true if cut was added

        G = nx.DiGraph()
        #for e in z:
         #  G.add_edge(e[0],e[1],arrival_time=z[e])
        
        G.add_edges_from(x)
        #check path length
        for node in VO:
            if node in G.nodes:
                z_val = 0.0
                for u, v in nx.dfs_edges(G, source=node):
                    z_val+=c[u,v]
                    G[u][v]["arrival_time"] = z_val

        transfers = list()
        transfer_order = dict(sorted(
            {a: x[a] for a in x if "ts" in a[0]}.items(),
            key=lambda item: item[1]
        ))
        #create precedence graph
        transfer_requests = []
        for tedge in transfer_order:
            for a in list(y.select(tedge[0],"*","*"))+list(y.select("*",tedge[1],"*")):
                if (a[0],a[1]) in TIy:
                    trans_edge = (a[0],a[1])
                    if trans_edge not in transfers:
                        if (a[0],a[0].replace("ts","tf")) in x and (a[1].replace("tf","ts"),a[1]) in x:
                            G.add_edge(a[0],a[1],arrival_time=G[a[0]][a[0].replace("ts","tf")]["arrival_time"])
                            transfers.append(trans_edge)
                            transfer_requests.append(a)

        if len(transfers)==0:
            return False
        try:
             cycle = nx.find_cycle(G, orientation=None)
             transfer_map = {(e[0], e[1]): e for e in transfer_requests}

             illegal_requests = [transfer_map[(a[0], a[1])] 
                               for a in cycle 
                               if (a[0], a[1]) in transfer_map]
             x_cycle = {a for a in cycle if a not in TIy}
             S = set()
             LHS_check_edges = set()
             #l_cuts["cycle"].append((cycle,transfer_requests))
             for edge in x_cycle:
                 # Each edge is a tuple (source, target)
                 source, target = edge
                 S.add(source)
                 S.add(target)
             
             if len(illegal_requests)==1:
                LHS_check = 0.0
                LHS = quicksum(model._x[i,j] for i in S for j in S if (i,j) in A)
                LHS_check = sum(x[i,j] for i in S for j in S if (i,j) in x)
                LHS_check_edges = set((i,j) for i in S for j in S if (i,j) in A)
                illegal_requests = set(illegal_requests)
                for e in illegal_requests:
                    S.remove(e[0])
                    S.remove(e[1])
                tidx = int(e[0].split(".")[-1])
                
                for i in TS_loc[tidx]:
                    for k,j in TIy.select(i,"*"):
                        if (k not in S and j not in S):
                            illegal_requests.add((k,j,e[2]))
                LHS = +quicksum(model._y[e] for e in illegal_requests)
                LHS_check += 1
                added_cuts = set()
                for e in illegal_requests:
                    if e[0] not in added_cuts:
                        LHS += quicksum(model._x[i,j] for i in S for j in [e[0]] if (i,j) in A)
                        LHS_check += sum(x[i,j] for i in S for j in [e[0]] if (i,j) in x)
                        added_cuts.add(e[0])
                    if e[1] not in added_cuts:
                        LHS += quicksum(model._x[j,i] for i in S for j in [e[1]] if (j,i) in A)
                        LHS_check += sum(x[j,i] for i in S for j in [e[1]] if (j,i) in x)#"""
                        added_cuts.add(e[1])
                    #"""
                    
                    
                #l_cuts["1cycle"].append((S,tuple(illegal_requests)))
                #strngthened version of cycle cut performs worse?
                #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                model.cbLazy(
                    LHS
                    #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                    <= len(cycle)-1
                )
                
                model._lazy_cuts["transferCycleCutR1"] +=1
                if LHS_check-(len(cycle)-1)>1.5:
                    model._error_msgs +="added wrong lazy illegal request transfer cut 1 {LHS_check}<={len(cycle)-1}; "
                #print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)
                print(f"added lazy illegal request transfer cut {LHS_check}<={len(cycle)-1}", illegal_requests,cycle)
                #breakpoint()
                return True
             if len(illegal_requests)==2:
                  LHS_check = 0.0
                  e1,e2 = illegal_requests[0],illegal_requests[1]
                  k,l = e1[0], e1[1]
                  u,v = e2[0], e2[1]
                  S1 = get_path_in_cycle(l,u,cycle)
                  S2 =  get_path_in_cycle(v,k,cycle)
                  illegal_requests = set()
                  illegal_requests.add((e1,e2))
                  tidx1 = int(k.split(".")[-1])
                  tidx2 = int(u.split(".")[-1])
                  for i in TS_loc[tidx1]:
                      for l in TS_loc[tidx2]:
                          for k,j in TIy.select(i,"*"):
                              if (k not in G.nodes and j not in G.nodes):
                                  for k2,j2 in TIy.select(l,"*"):
                                      if (k2 not in G.nodes and j2 not in G.nodes ):
                                          illegal_requests.add(((k,j,e1[2]),(k2,j2,e2[2])))
                  LHS = quicksum(model._x[i,j] for i in S1 for j in S1 if (i,j) in A)+quicksum(model._x[i,j] for i in S2 for j in S2 if (i,j) in A)
                  #breakpoint()
                  added_cuts = set()
                  added_y = set()
                  LHS_check += sum(x[i,j] for i in S1 for j in S1 if (i,j) in x)+sum(x[i,j] for i in S2 for j in S2 if (i,j) in x)
                  for e1,e2 in illegal_requests:
                      k,l = e1[0], e1[1]
                      u,v = e2[0], e2[1]
                      if e1 not in added_y:
                          LHS += model._y[e1]
                          added_y.add(e1)
                          if e1 in y:
                              LHS_check +=1
                      if e2 not in added_y:
                          LHS += model._y[e2]
                          added_y.add(e2)
                          if e2 in y:
                              LHS_check +=1
                      if l not in added_cuts:
                          LHS += quicksum(model._x[i,j] for j in S1 for i in [l] if (i,j) in A)
                          LHS_check += quicksum(x[i,j] for j in S1 for i in [l] if (i,j) in x)
                          added_cuts.add(l)
                      if u not in added_cuts:
                         LHS += quicksum(model._x[i,j] for i in S1 for j in [u] if (i,j) in A)
                         LHS_check += quicksum(x[i,j] for i in S1 for j in [u] if (i,j) in x)
                         added_cuts.add(u)
                      if k not in added_cuts:
                         LHS += quicksum(model._x[i,j] for i in S2 for j in [k] if (i,j) in A)
                         LHS_check += quicksum(x[i,j] for i in S2 for j in [k] if (i,j) in x)
                         added_cuts.add(k)
                      if v not in added_cuts:
                         LHS += quicksum(model._x[j,i] for i in S2 for j in [v] if (j,i) in A)
                         LHS_check += quicksum(x[j,i] for i in S2 for j in [v] if (j,i) in x)
                         added_cuts.add(v)
                      if (l,u) in A:
                          if (l,u) in x and (l,u) not in LHS_check_edges:
                              LHS += model._x[l,u]
                              LHS_check += x[l,u]
                              LHS_check_edges.add((l,u))
                      if (v,k) in A:
                          if(v, k) in x and (v,k) not in LHS_check_edges:
                              LHS += model._x[v,k]              
                              LHS_check +=x[v,k]
                              LHS_check_edges.add((l,u))
                      if (k,l) in A:
                          if(k,l) in x and (k,l) not in LHS_check_edges:
                              LHS += model._x[k,l]
                              LHS_check +=x[k,l]
                              LHS_check_edges.add((l,u))
                      if (u,v) in A:
                          if(u,v) in x and (u,v) not in LHS_check_edges:
                             LHS += model._x[u,v]
                             LHS_check +=x[u,v]
                             LHS_check_edges.add((l,u))
                  #l_cuts["2cycle"].append((S1,S2,tuple(illegal_requests)))
                  #if set(S1) == set(['d9', 'd8', 'p11', 'p5', 'p19', 'd5', 'p15']):
                   #   if set(S2)== set(['d23', 'd11', 'p14', 'd14', 'p17', 'd19', 'd17', 'p3', 'd3', 'p20', 'd20', 'p21', 'd21', 'p1', 'p7', 'd7', 'p9']):
                    #     breakpoint()
                  #strngthened version of cycle cut performs worse?
                  #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                  model._lazy_cuts["transferCycleCutR2"] +=1
                  model.cbLazy(
                      LHS
                      #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                      <= len(cycle)-1
                      )
                  print(f"added lazy illegal request transfer cut, {LHS_check}<={len(cycle)-1},  {len(illegal_requests)}, {len(cycle)}", illegal_requests,cycle)
                  #print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)#, illegal_requests,cycle)
                  if round(LHS_check.getValue())<=len(cycle)-1 or round(LHS_check.getValue())-len(cycle)-1>1.5:
                      breakpoint()
                      print("fail")
                  return True
              
             if len(illegal_requests)==3:
                  LHS_check = 0.0
                  e1,e2,e3 = illegal_requests[0],illegal_requests[1],illegal_requests[2]
                  k,l = e1[0], e1[1]
                  u,v = e2[0], e2[1]
                  m,n = e3[0], e3[1]
                  S1 = get_path_in_cycle(l,u,cycle)
                  S2 =  get_path_in_cycle(v,m,cycle)
                  S3 =  get_path_in_cycle(n,k,cycle)
                  illegal_requests = set()
                  illegal_requests.add((e1,e2,e3))
                  tidx1 = int(k.split(".")[-1])
                  tidx2 = int(u.split(".")[-1])
                  tidx3 = int(m.split(".")[-1])
                  for i in TS_loc[tidx1]:
                      for l in TS_loc[tidx2]:
                          for o in TS_loc[tidx3]:
                              for k,j in TIy.select(i,"*"):
                                  if (k not in G.nodes and j not in G.nodes):
                                      for k2,j2 in TIy.select(l,"*"):
                                          if (k2 not in G.nodes and j2 not in G.nodes):
                                              for k3,j3 in TIy.select(o,"*"):
                                                  if (k3 not in G.nodes and j3 not in G.nodes):
                                                      illegal_requests.add(((k,j,e1[2]),(k2,j2,e2[2]),(k3,j3,e3[2])))
                  LHS = quicksum(model._x[i,j] for i in S1 for j in S1 if (i,j) in A)+quicksum(model._x[i,j] for i in S2 for j in S2 if (i,j) in A)+quicksum(model._x[i,j] for i in S3 for j in S3 if (i,j) in A)
                  #breakpoint()
                  added_cuts = set()
                  added_y = set()
                  LHS_check += sum(x[i,j] for i in S1 for j in S1 if (i,j) in x)+sum(x[i,j] for i in S2 for j in S2 if (i,j) in x)+sum(x[i,j] for i in S3 for j in S3 if (i,j) in x)
                  for e1,e2,e3 in illegal_requests:
                      k,l = e1[0], e1[1]
                      u,v = e2[0], e2[1]
                      m,n = e3[0], e3[1]
                      if e1 not in added_y:
                          LHS += model._y[e1]
                          added_y.add(e1)
                          if e1 in y:
                              LHS_check +=1
                      if e2 not in added_y:
                          LHS += model._y[e2]
                          added_y.add(e2)
                          if e2 in y:
                              LHS_check +=1
                      if e3 not in added_y:
                         LHS += model._y[e3]
                         added_y.add(e3)
                         if e3 in y:
                             LHS_check +=1
                      if l not in added_cuts:
                          LHS += quicksum(model._x[i,j] for j in S1 for i in [l] if (i,j) in A)
                          LHS_check += quicksum(x[i,j] for j in S1 for i in [l] if (i,j) in x)
                          added_cuts.add(l)
                      if u not in added_cuts:
                         LHS += quicksum(model._x[i,j] for i in S1 for j in [u] if (i,j) in A)
                         LHS_check += quicksum(x[i,j] for i in S1 for j in [u] if (i,j) in x)
                         added_cuts.add(u)
                      if k not in added_cuts:
                         LHS += quicksum(model._x[i,j] for i in S3 for j in [k] if (i,j) in A)
                         LHS_check += quicksum(x[i,j] for i in S3 for j in [k] if (i,j) in x)
                         added_cuts.add(k)
                      if v not in added_cuts:
                         LHS += quicksum(model._x[j,i] for i in S2 for j in [v] if (j,i) in A)
                         LHS_check += quicksum(x[j,i] for i in S2 for j in [v] if (j,i) in x)
                         added_cuts.add(v)
                      if m not in added_cuts:
                         LHS += quicksum(model._x[i,j] for i in S2 for j in [m] if (i,j) in A)
                         LHS_check += quicksum(x[i,j] for i in S2 for j in [m] if (i,j) in x)
                         added_cuts.add(k)
                      if n not in added_cuts:
                         LHS += quicksum(model._x[j,i] for i in S3 for j in [n] if (j,i) in A)
                         LHS_check += quicksum(x[j,i] for i in S3 for j in [n] if (j,i) in x)
                         added_cuts.add(v)
                      if (l,u) in A:
                          if (l,u) in x and (l,u) not in LHS_check_edges:
                              LHS += model._x[l,u]
                              LHS_check += x[l,u]
                              LHS_check_edges.add((l,u))
                      if (v,k) in A:
                          if(v, k) in x and (v,k) not in LHS_check_edges:
                              LHS += model._x[v,k]              
                              LHS_check +=x[v,k]
                              LHS_check_edges.add((l,u))
                      if (u,n) in A:
                          if (u,n) in x and (u,n) not in LHS_check_edges:
                              LHS += model._x[u,n]
                              LHS_check += x[u,n]
                              LHS_check_edges.add((u,n))
                      if (v,m) in A:
                          if(v, m) in x and (v,m) not in LHS_check_edges:
                              LHS += model._x[v,m]              
                              LHS_check +=x[v,m]
                              LHS_check_edges.add((v,m))
                      if (n,k) in A:
                          if(n, k) in x and (n,k) not in LHS_check_edges:
                              LHS += model._x[n,k]              
                              LHS_check +=x[n,k]
                              LHS_check_edges.add((n,k))
                      if (l,m) in A:
                          if(l, m) in x and (l,m) not in LHS_check_edges:
                              LHS += model._x[l,m]              
                              LHS_check +=x[l,m]
                              LHS_check_edges.add((l,m))
                      if (k,l) in A:
                          if(k,l) in x and (k,l) not in LHS_check_edges:
                              LHS += model._x[k,l]
                              LHS_check +=x[k,l]
                              LHS_check_edges.add((l,u))
                      if (u,v) in A:
                          if(u,v) in x and (u,v) not in LHS_check_edges:
                             LHS += model._x[u,v]
                             LHS_check +=x[u,v]
                             LHS_check_edges.add((l,u))
                      if (m,n) in A:
                         if(m,n) in x and (m,n) not in LHS_check_edges:
                            LHS += model._x[m,n]
                            LHS_check +=x[m,n]
                            LHS_check_edges.add((m,n))
                  #l_cuts["3cycle"].append((S1,S2,S3,tuple(illegal_requests)))
                  #if set(S1) == set(['d9', 'd8', 'p11', 'p5', 'p19', 'd5', 'p15']):
                   #   if set(S2)== set(['d23', 'd11', 'p14', 'd14', 'p17', 'd19', 'd17', 'p3', 'd3', 'p20', 'd20', 'p21', 'd21', 'p1', 'p7', 'd7', 'p9']):
                    #     breakpoint()
                  #strngthened version of cycle cut performs worse?
                  #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                  model._lazy_cuts["transferCycleCutR3"] +=1
                  model.cbLazy(
                      LHS
                      #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                      <= len(cycle)-1
                      )
                  print(f"added lazy illegal request transfer cut, {LHS_check}<={len(cycle)-1},  {len(illegal_requests)}, {len(cycle)}", illegal_requests,cycle)
                  #print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)#, illegal_requests,cycle)
                  if round(LHS_check.getValue())<=len(cycle)-1 or round(LHS_check.getValue())-len(cycle)-1>1.5:
                      breakpoint()
                      print("fail")
                  return True
             if len(illegal_requests)==4:
                LHS_check = 0.0
                e1,e2,e3,e4 = illegal_requests[0],illegal_requests[1],illegal_requests[2],illegal_requests[3]
                k,l = e1[0], e1[1]
                u,v = e2[0], e2[1]
                m,n = e3[0], e3[1]
                p,q = e4[0], e4[1]
                S1 = get_path_in_cycle(l,u,cycle)
                S2 = get_path_in_cycle(v,m,cycle)
                S3 = get_path_in_cycle(n,p,cycle)
                S4 = get_path_in_cycle(q,k,cycle)
                illegal_requests = set()
                illegal_requests.add((e1,e2,e3,e4))
                tidx1 = int(k.split(".")[-1])
                tidx2 = int(u.split(".")[-1])
                tidx3 = int(m.split(".")[-1])
                tidx4 = int(p.split(".")[-1])
                for i in TS_loc[tidx1]:
                    for l_idx in TS_loc[tidx2]:
                        for o in TS_loc[tidx3]:
                            for r in TS_loc[tidx4]:
                                for k,j in TIy.select(i,"*"):
                                    if (k not in G.nodes and j not in G.nodes):
                                        for k2,j2 in TIy.select(l_idx,"*"):
                                            if (k2 not in G.nodes and j2 not in G.nodes):
                                                for k3,j3 in TIy.select(o,"*"):
                                                    if (k3 not in G.nodes and j3 not in G.nodes):
                                                        for k4,j4 in TIy.select(r,"*"):
                                                            if (k4 not in G.nodes and j4 not in G.nodes):
                                                                illegal_requests.add(((k,j,e1[2]),(k2,j2,e2[2]),(k3,j3,e3[2]),(k4,j4,e4[2])))
                LHS = quicksum(model._x[i,j] for i in S1 for j in S1 if (i,j) in A)+quicksum(model._x[i,j] for i in S2 for j in S2 if (i,j) in A)+quicksum(model._x[i,j] for i in S3 for j in S3 if (i,j) in A)+quicksum(model._x[i,j] for i in S4 for j in S4 if (i,j) in A)
                #breakpoint()
                added_cuts = set()
                added_y = set()
                LHS_check += sum(x[i,j] for i in S1 for j in S1 if (i,j) in x)+sum(x[i,j] for i in S2 for j in S2 if (i,j) in x)+sum(x[i,j] for i in S3 for j in S3 if (i,j) in x)+sum(x[i,j] for i in S4 for j in S4 if (i,j) in x)
                for e1,e2,e3,e4 in illegal_requests:
                    k,l = e1[0], e1[1]
                    u,v = e2[0], e2[1]
                    m,n = e3[0], e3[1]
                    p,q = e4[0], e4[1]
                    if e1 not in added_y:
                        LHS += model._y[e1]
                        added_y.add(e1)
                        if e1 in y:
                            LHS_check +=1
                    if e2 not in added_y:
                        LHS += model._y[e2]
                        added_y.add(e2)
                        if e2 in y:
                            LHS_check +=1
                    if e3 not in added_y:
                        LHS += model._y[e3]
                        added_y.add(e3)
                        if e3 in y:
                            LHS_check +=1
                    if e4 not in added_y:
                        LHS += model._y[e4]
                        added_y.add(e4)
                        if e4 in y:
                            LHS_check +=1
                    
                    # Cut connections for each node (following the pattern from 3-case)
                    if l not in added_cuts:
                        LHS += quicksum(model._x[i,j] for j in S1 for i in [l] if (i,j) in A)
                        LHS_check += quicksum(x[i,j] for j in S1 for i in [l] if (i,j) in x)
                        added_cuts.add(l)
                    if u not in added_cuts:
                        LHS += quicksum(model._x[i,j] for i in S1 for j in [u] if (i,j) in A)
                        LHS_check += quicksum(x[i,j] for i in S1 for j in [u] if (i,j) in x)
                        added_cuts.add(u)
                    if k not in added_cuts:
                        LHS += quicksum(model._x[i,j] for i in S4 for j in [k] if (i,j) in A)
                        LHS_check += quicksum(x[i,j] for i in S4 for j in [k] if (i,j) in x)
                        added_cuts.add(k)
                    if v not in added_cuts:
                        LHS += quicksum(model._x[j,i] for i in S2 for j in [v] if (j,i) in A)
                        LHS_check += quicksum(x[j,i] for i in S2 for j in [v] if (j,i) in x)
                        added_cuts.add(v)
                    if m not in added_cuts:
                        LHS += quicksum(model._x[i,j] for i in S2 for j in [m] if (i,j) in A)
                        LHS_check += quicksum(x[i,j] for i in S2 for j in [m] if (i,j) in x)
                        added_cuts.add(m)
                    if n not in added_cuts:
                        LHS += quicksum(model._x[j,i] for i in S3 for j in [n] if (j,i) in A)
                        LHS_check += quicksum(x[j,i] for i in S3 for j in [n] if (j,i) in x)
                        added_cuts.add(n)
                    if p not in added_cuts:
                        LHS += quicksum(model._x[i,j] for i in S3 for j in [p] if (i,j) in A)
                        LHS_check += quicksum(x[i,j] for i in S3 for j in [p] if (i,j) in x)
                        added_cuts.add(p)
                    if q not in added_cuts:
                        LHS += quicksum(model._x[j,i] for i in S4 for j in [q] if (j,i) in A)
                        LHS_check += quicksum(x[j,i] for i in S4 for j in [q] if (j,i) in x)
                        added_cuts.add(q)
                    
                    # Cross-segment connection edges (extending the pattern from 3-case)
                    # Connections between consecutive segments
                    if (l,u) in A:
                        if (l,u) in x and (l,u) not in LHS_check_edges:
                            LHS += model._x[l,u]
                            LHS_check += x[l,u]
                            LHS_check_edges.add((l,u))
                    if (v,m) in A:
                        if(v, m) in x and (v,m) not in LHS_check_edges:
                            LHS += model._x[v,m]              
                            LHS_check +=x[v,m]
                            LHS_check_edges.add((v,m))
                    if (n,p) in A:
                        if (n,p) in x and (n,p) not in LHS_check_edges:
                            LHS += model._x[n,p]
                            LHS_check += x[n,p]
                            LHS_check_edges.add((n,p))
                    if (q,k) in A:
                        if(q, k) in x and (q,k) not in LHS_check_edges:
                            LHS += model._x[q,k]              
                            LHS_check +=x[q,k]
                            LHS_check_edges.add((q,k))
                    
                    # Skip-one connections (like l,m in 3-case)
                    if (l,m) in A:
                        if(l, m) in x and (l,m) not in LHS_check_edges:
                            LHS += model._x[l,m]              
                            LHS_check +=x[l,m]
                            LHS_check_edges.add((l,m))
                    if (v,p) in A:
                        if(v, p) in x and (v,p) not in LHS_check_edges:
                            LHS += model._x[v,p]              
                            LHS_check +=x[v,p]
                            LHS_check_edges.add((v,p))
                    if (n,k) in A:
                        if(n, k) in x and (n,k) not in LHS_check_edges:
                            LHS += model._x[n,k]              
                            LHS_check +=x[n,k]
                            LHS_check_edges.add((n,k))
                    if (q,u) in A:
                        if(q, u) in x and (q,u) not in LHS_check_edges:
                            LHS += model._x[q,u]              
                            LHS_check +=x[q,u]
                            LHS_check_edges.add((q,u))
                    
                    # Skip-two connections
                    if (l,p) in A:
                        if(l, p) in x and (l,p) not in LHS_check_edges:
                            LHS += model._x[l,p]              
                            LHS_check +=x[l,p]
                            LHS_check_edges.add((l,p))
                    if (v,k) in A:
                        if(v, k) in x and (v,k) not in LHS_check_edges:
                            LHS += model._x[v,k]              
                            LHS_check +=x[v,k]
                            LHS_check_edges.add((v,k))
                    
                    # Internal edges of each illegal request
                    if (k,l) in A:
                        if(k,l) in x and (k,l) not in LHS_check_edges:
                            LHS += model._x[k,l]
                            LHS_check +=x[k,l]
                            LHS_check_edges.add((k,l))
                    if (u,v) in A:
                        if(u,v) in x and (u,v) not in LHS_check_edges:
                            LHS += model._x[u,v]
                            LHS_check +=x[u,v]
                            LHS_check_edges.add((u,v))
                    if (m,n) in A:
                        if(m,n) in x and (m,n) not in LHS_check_edges:
                            LHS += model._x[m,n]
                            LHS_check +=x[m,n]
                            LHS_check_edges.add((m,n))
                    if (p,q) in A:
                        if(p,q) in x and (p,q) not in LHS_check_edges:
                            LHS += model._x[p,q]
                            LHS_check +=x[p,q]
                            LHS_check_edges.add((p,q))
                
                #l_cuts["4cycle"].append((S1,S2,S3,S4,tuple(illegal_requests)))
                #if round(LHS_check.getValue())<=len(cycle)-1:
                    #breakpoint()
                    #print("fail")
                model.cbLazy(
                    LHS
                    <= len(cycle)-1
                    )
                print(f"added lazy illegal request transfer cut, {LHS_check}<={len(cycle)-1},  {len(illegal_requests)}, {len(cycle)}", illegal_requests,cycle)
                model._lazy_cuts["transferCycleCutR4"] +=1
                return True     
             if len(illegal_requests)>4:
                 x_cycle = {a for a in cycle if a not in TIy}
                 S = set()
                 for edge in x_cycle:
                     # Each edge is a tuple (source, target)
                     source, target = edge
                     S.add(source)
                     S.add(target)
                 LHS_check = 0.0
                 LHS = quicksum(model._x[i,j] for i in S for j in S if (i,j) in A)
                 LHS += quicksum(model._y[e] for e in illegal_requests)
                 LHS_check += len(illegal_requests)+sum(x[i,j] for i in S for j in S if (i,j) in x)
                 #l_cuts["1cycle"].append((S,tuple(illegal_requests)))
                 #strngthened version of cycle cut performs worse?
                 #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                 model.cbLazy(
                        LHS
                        #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                        <= len(cycle)-1
                 )
                 model._lazy_cuts["transferCycleCutR1"] +=1
                 if LHS_check-(len(cycle)-1)>1.5:
                        model._error_msgs +="added wrong lazy illegal request transfer cut 1 {LHS_check}<={len(cycle)-1}; "
                 #print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)
                 print(f"added lazy illegal request transfer cut {LHS_check}<={len(cycle)-1}", illegal_requests,cycle)
                 #breakpoint()
                 return True
    
        except nx.NetworkXNoCycle:
             pass
         
        # Step 1: Initialize all arrival times
        for u in G.nodes():
            G.nodes[u]["arrival_time"] = 0.0
        
        # Step 2: Topological propagation
        arrival_time = {u: 0.0 for u in G.nodes()}
        for u in nx.topological_sort(G):
            for v in G.successors(u):
                # Store arrival time at u on edge (u, v)
                G[u][v]["arrival_time"] = arrival_time[u]
                
                # Compute arrival at v
                arrival_time[v] = max(arrival_time[v],timeWindows[v][0], arrival_time[u] + c.get((u, v), 0))
                # Step 3: check time violation
                if G[u][v]["arrival_time"]>wbTW.get((u,v),df.b.max()):
                    LHS = quicksum(model._x[e] for e in model._A if e not in x)
                    LHS_check = sum(x.get(e,0) for e in model._A if e not in x)
                    RHS = 1.0
                    model.cbLazy(
                        LHS#for (i,j) in edges)#
                        >= RHS
                        )
                    #print(f"added lazy illegal transfer path cut {LHS_check}<={RHS}")
                    #print(p1,p2)
                    if LHS_check>=RHS:
                        #breakpoint()
                        model._error_msgs +=f"error IP_trans: {LHS_check}>={RHS}; "
                    model._lazy_cuts["IP_trans"] += 1
                    l_cuts["infp"].append(LHS)
                    return True
            

        
                #print(path)
        #nx.get_edge_attributes(G, "arrival_time")
        return False
    
    def check_illegal_transfer2(model, x, y, z, cur_obj):
        #returns true if cut was added

        G = nx.DiGraph()
        #for e in z:
         #  G.add_edge(e[0],e[1],arrival_time=z[e])
        
        G.add_edges_from(x)
        #check path length
        for node in VO:
            z_val = 0.0
            for u, v in nx.dfs_edges(G, source=node):
                z_val+=c[u,v]
                G[u][v]["arrival_time"] = z_val

        transfers = list()
        transfer_order = dict(sorted(
            {a: x[a] for a in x if "ts" in a[0]}.items(),
            key=lambda item: item[1]
        ))
        #create precedence graph
        transfer_requests = []
        for tedge in transfer_order:
            for a in list(y.select(tedge[0],"*","*"))+list(y.select("*",tedge[1],"*")):
                if (a[0],a[1]) in TIy:
                    trans_edge = (a[0],a[1])
                    if trans_edge not in transfers:
                        if (a[0],a[0].replace("ts","tf")) in x and (a[1].replace("tf","ts"),a[1]) in x:
                            G.add_edge(a[0],a[1],arrival_time=G[a[0]][a[0].replace("ts","tf")]["arrival_time"])
                            transfers.append(trans_edge)
                            transfer_requests.append(a)

        
        try:
            cycle = nx.find_cycle(G, orientation=None)
            illegal_requests = [a for a in transfer_requests if (a[0],a[1]) in cycle]
            x_cycle = {a for a in cycle if a not in TIy}
            S = set()
            for edge in x_cycle:
                # Each edge is a tuple (source, target)
                source, target = edge
                S.add(source)
                S.add(target)
            if len(illegal_requests)==1:
                LHS_check = 0.0
                illegal_requests = set(illegal_requests)
                for e in illegal_requests:
                    S.remove(e[0])
                    S.remove(e[1])
                tidx = int(e[0].split(".")[-1])
                
                for i in TS_loc[tidx]:
                    for k,j in TIy.select(i,"*"):
                        if (k not in S and j not in S):
                            illegal_requests.add((k,j,e[2]))
                LHS = quicksum(model._y[e] for e in illegal_requests)+quicksum(model._x[i,j] for i in S for j in S if (i,j) in A)
                LHS_check += 1+sum(x[i,j] for i in S for j in S if (i,j) in x)
                added_cuts = set()
                for e in illegal_requests:
                    if e[0] not in added_cuts:
                        LHS += quicksum(model._x[i,j] for i in S for j in [e[0]] if (i,j) in A)
                        LHS_check += sum(x[i,j] for i in S for j in [e[0]] if (i,j) in x)
                        added_cuts.add(e[0])
                    if e[1] not in added_cuts:
                        LHS += quicksum(model._x[j,i] for i in S for j in [e[1]] if (j,i) in A)
                        LHS_check += sum(x[j,i] for i in S for j in [e[1]] if (j,i) in x)#"""
                        added_cuts.add(e[1])
                    #"""
                    
                    
                #l_cuts["1cycle"].append((S,tuple(illegal_requests)))
                #strngthened version of cycle cut performs worse?
                #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                model.cbLazy(
                    LHS
                    #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                    <= len(cycle)-1
                )
                model._lazy_cuts["transferCycleCutR1"] +=1
                if LHS_check-(len(cycle)-1)>1.5:
                    model._error_msgs +="added wrong lazy illegal request transfer cut 1 {LHS_check}<={len(cycle)-1}; "
                #print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)
                print(f"added lazy illegal request transfer cut {LHS_check}<={len(cycle)-1}", illegal_requests,cycle)
                #breakpoint()
                return True
            if len(illegal_requests)==2:
                 LHS_check = 0.0
                 LHS_check_edges = set()
                 e1,e2 = illegal_requests[0],illegal_requests[1]
                 k,l = e1[0], e1[1]
                 u,v = e2[0], e2[1]
                 S1 = get_path_in_cycle(l,u,cycle)
                 S2 =  get_path_in_cycle(v,k,cycle)
                 illegal_requests = set()
                 illegal_requests.add((e1,e2))
                 tidx1 = int(k.split(".")[-1])
                 tidx2 = int(u.split(".")[-1])
                 for i in TS_loc[tidx1]:
                     for l in TS_loc[tidx2]:
                         for k,j in TIy.select(i,"*"):
                             if (k not in S and j not in S):
                                 for k2,j2 in TIy.select(l,"*"):
                                     if (k2 not in S and j2 not in S):
                                         illegal_requests.add(((k,j,e1[2]),(k2,j2,e2[2])))
                 LHS = quicksum(model._x[i,j] for i in S1 for j in S1 if (i,j) in A)+quicksum(model._x[i,j] for i in S2 for j in S2 if (i,j) in A)
                 #breakpoint()
                 added_cuts = set()
                 added_y = set()
                 LHS_check += sum(x[i,j] for i in S1 for j in S1 if (i,j) in x)+sum(x[i,j] for i in S2 for j in S2 if (i,j) in x)
                 for e1,e2 in illegal_requests:
                     k,l = e1[0], e1[1]
                     u,v = e2[0], e2[1]
                     if e1 not in added_y:
                         LHS += model._y[e1]
                         added_y.add(e1)
                         if e1 in y:
                             LHS_check +=1
                     if e2 not in added_y:
                         LHS += model._y[e2]
                         added_y.add(e2)
                         if e2 in y:
                             LHS_check +=1
                     if l not in added_cuts:
                         LHS += quicksum(model._x[i,j] for j in S1 for i in [l] if (i,j) in A)
                         LHS_check += quicksum(x[i,j] for j in S1 for i in [l] if (i,j) in x)
                         added_cuts.add(l)
                     if u not in added_cuts:
                        LHS += quicksum(model._x[i,j] for i in S1 for j in [u] if (i,j) in A)
                        LHS_check += quicksum(x[i,j] for i in S1 for j in [u] if (i,j) in x)
                        added_cuts.add(u)
                     if k not in added_cuts:
                        LHS += quicksum(model._x[i,j] for i in S2 for j in [k] if (i,j) in A)
                        LHS_check += quicksum(x[i,j] for i in S2 for j in [k] if (i,j) in x)
                        added_cuts.add(k)
                     if v not in added_cuts:
                        LHS += quicksum(model._x[j,i] for i in S2 for j in [v] if (j,i) in A)
                        LHS_check += quicksum(x[j,i] for i in S2 for j in [v] if (j,i) in x)
                        added_cuts.add(v)
                     if (l,u) in A:
                         if (l,u) in x and (l,u) not in LHS_check_edges:
                             LHS += model._x[l,u]
                             LHS_check += x[l,u]
                             LHS_check_edges.add((l,u))
                     if (v,k) in A:
                         if(v, k) in x and (v,k) not in LHS_check_edges:
                             LHS += model._x[v,k]              
                             LHS_check +=x[v,k]
                             LHS_check_edges.add((l,u))
                     if (k,l) in A:
                         if(k,l) in x and (k,l) not in LHS_check_edges:
                             LHS += model._x[k,l]
                             LHS_check +=x[k,l]
                             LHS_check_edges.add((l,u))
                     if (u,v) in A:
                         if(u,v) in x and (u,v) not in LHS_check_edges:
                            LHS += model._x[u,v]
                            LHS_check +=x[u,v]
                            LHS_check_edges.add((l,u))
                 #l_cuts["2cycle"].append((S1,S2,tuple(illegal_requests)))
                 #if set(S1) == set(['d9', 'd8', 'p11', 'p5', 'p19', 'd5', 'p15']):
                  #   if set(S2)== set(['d23', 'd11', 'p14', 'd14', 'p17', 'd19', 'd17', 'p3', 'd3', 'p20', 'd20', 'p21', 'd21', 'p1', 'p7', 'd7', 'p9']):
                   #     breakpoint()
                 #strngthened version of cycle cut performs worse?
                 #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                 model._lazy_cuts["transferCycleCutR2"] +=1
                 model.cbLazy(
                     LHS
                     #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                     <= len(cycle)-1
                     )
                 print(f"added lazy illegal request transfer cut, {LHS_check}<={len(cycle)-1},  {len(illegal_requests)}, {len(cycle)}", illegal_requests,cycle)
                 #print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)#, illegal_requests,cycle)
                 #if round(LHS_check.getValue()<=len(cycle)-1):
                  #   breakpoint()
                   #  print("fail")
                 return True
             
            if len(illegal_requests)==3:
                 LHS_check = 0.0
                 LHS_check_edges = set()
                 e1,e2,e3 = illegal_requests[0],illegal_requests[1],illegal_requests[2]
                 k,l = e1[0], e1[1]
                 u,v = e2[0], e2[1]
                 m,n = e3[0], e3[1]
                 S1 = get_path_in_cycle(l,u,cycle)
                 S2 =  get_path_in_cycle(v,m,cycle)
                 S3 =  get_path_in_cycle(n,k,cycle)
                 illegal_requests = set()
                 illegal_requests.add((e1,e2,e3))
                 tidx1 = int(k.split(".")[-1])
                 tidx2 = int(u.split(".")[-1])
                 tidx3 = int(m.split(".")[-1])
                 for i in TS_loc[tidx1]:
                     for l in TS_loc[tidx2]:
                             for k,j in TIy.select(i,"*"):
                                 if (k not in S and j not in S):
                                     for k2,j2 in TIy.select(l,"*"):
                                         if (k2 not in S and j2 not in S):
                                             for k3,j3 in TIy.select(o,"*"):
                                                 if (k3 not in S and j3 not in S):
                                                     illegal_requests.add(((k,j,e1[2]),(k2,j2,e2[2]),(k3,j3,e3[2])))
                 LHS = quicksum(model._x[i,j] for i in S1 for j in S1 if (i,j) in A)+quicksum(model._x[i,j] for i in S2 for j in S2 if (i,j) in A)+quicksum(model._x[i,j] for i in S3 for j in S3 if (i,j) in A)
                 #breakpoint()
                 added_cuts = set()
                 added_y = set()
                 LHS_check += sum(x[i,j] for i in S1 for j in S1 if (i,j) in x)+sum(x[i,j] for i in S2 for j in S2 if (i,j) in x)+sum(x[i,j] for i in S3 for j in S3 if (i,j) in x)
                 for e1,e2,e3 in illegal_requests:
                     k,l = e1[0], e1[1]
                     u,v = e2[0], e2[1]
                     m,n = e3[0], e3[1]
                     if e1 not in added_y:
                         LHS += model._y[e1]
                         added_y.add(e1)
                         if e1 in y:
                             LHS_check +=1
                     if e2 not in added_y:
                         LHS += model._y[e2]
                         added_y.add(e2)
                         if e2 in y:
                             LHS_check +=1
                     if e3 not in added_y:
                        LHS += model._y[e3]
                        added_y.add(e3)
                        if e3 in y:
                            LHS_check +=1
                     if l not in added_cuts:
                         LHS += quicksum(model._x[i,j] for j in S1 for i in [l] if (i,j) in A)
                         LHS_check += quicksum(x[i,j] for j in S1 for i in [l] if (i,j) in x)
                         added_cuts.add(l)
                     if u not in added_cuts:
                        LHS += quicksum(model._x[i,j] for i in S1 for j in [u] if (i,j) in A)
                        LHS_check += quicksum(x[i,j] for i in S1 for j in [u] if (i,j) in x)
                        added_cuts.add(u)
                     if k not in added_cuts:
                        LHS += quicksum(model._x[i,j] for i in S3 for j in [k] if (i,j) in A)
                        LHS_check += quicksum(x[i,j] for i in S3 for j in [k] if (i,j) in x)
                        added_cuts.add(k)
                     if v not in added_cuts:
                        LHS += quicksum(model._x[j,i] for i in S2 for j in [v] if (j,i) in A)
                        LHS_check += quicksum(x[j,i] for i in S2 for j in [v] if (j,i) in x)
                        added_cuts.add(v)
                     if m not in added_cuts:
                        LHS += quicksum(model._x[i,j] for i in S2 for j in [m] if (i,j) in A)
                        LHS_check += quicksum(x[i,j] for i in S2 for j in [m] if (i,j) in x)
                        added_cuts.add(k)
                     if n not in added_cuts:
                        LHS += quicksum(model._x[j,i] for i in S3 for j in [n] if (j,i) in A)
                        LHS_check += quicksum(x[j,i] for i in S3 for j in [n] if (j,i) in x)
                        added_cuts.add(v)
                     if (l,u) in A:
                         if (l,u) in x and (l,u) not in LHS_check_edges:
                             LHS += model._x[l,u]
                             LHS_check += x[l,u]
                             LHS_check_edges.add((l,u))
                     if (v,k) in A:
                         if(v, k) in x and (v,k) not in LHS_check_edges:
                             LHS += model._x[v,k]              
                             LHS_check +=x[v,k]
                             LHS_check_edges.add((l,u))
                     if (u,n) in A:
                         if (u,n) in x and (u,n) not in LHS_check_edges:
                             LHS += model._x[u,n]
                             LHS_check += x[u,n]
                             LHS_check_edges.add((u,n))
                     if (v,m) in A:
                         if(v, m) in x and (v,m) not in LHS_check_edges:
                             LHS += model._x[v,m]              
                             LHS_check +=x[v,m]
                             LHS_check_edges.add((v,m))
                     if (n,k) in A:
                         if(n, k) in x and (n,k) not in LHS_check_edges:
                             LHS += model._x[n,k]              
                             LHS_check +=x[n,k]
                             LHS_check_edges.add((n,k))
                     if (l,m) in A:
                         if(l, m) in x and (l,m) not in LHS_check_edges:
                             LHS += model._x[l,m]              
                             LHS_check +=x[l,m]
                             LHS_check_edges.add((l,m))
                     if (k,l) in A:
                         if(k,l) in x and (k,l) not in LHS_check_edges:
                             LHS += model._x[k,l]
                             LHS_check +=x[k,l]
                             LHS_check_edges.add((l,u))
                     if (u,v) in A:
                         if(u,v) in x and (u,v) not in LHS_check_edges:
                            LHS += model._x[u,v]
                            LHS_check +=x[u,v]
                            LHS_check_edges.add((l,u))
                     if (m,n) in A:
                        if(m,n) in x and (m,n) not in LHS_check_edges:
                           LHS += model._x[m,n]
                           LHS_check +=x[m,n]
                           LHS_check_edges.add((m,n))
                 #l_cuts["3cycle"].append((S1,S2,S3,tuple(illegal_requests)))
                 #if set(S1) == set(['d9', 'd8', 'p11', 'p5', 'p19', 'd5', 'p15']):
                  #   if set(S2)== set(['d23', 'd11', 'p14', 'd14', 'p17', 'd19', 'd17', 'p3', 'd3', 'p20', 'd20', 'p21', 'd21', 'p1', 'p7', 'd7', 'p9']):
                   #     breakpoint()
                 #strngthened version of cycle cut performs worse?
                 #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                 model._lazy_cuts["transferCycleCutR3"] +=1
                 model.cbLazy(
                     LHS
                     #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                     <= len(cycle)-1
                     )
                 print(f"added lazy illegal request transfer cut, {LHS_check}<={len(cycle)-1},  {len(illegal_requests)}, {len(cycle)}", illegal_requests,cycle)
                 #print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)#, illegal_requests,cycle)
                 #if round(LHS_check.getValue()<=len(cycle)-1):
                  #   breakpoint()
                   #  print("fail")
                 return True
            if len(illegal_requests)>3:
                LHS_check = 0.0
                LHS_check_edges = set()
                e1,e2,e3 = illegal_requests[0],illegal_requests[1],illegal_requests[2]
                k,l = e1[0], e1[1]
                u,v = e2[0], e2[1]
                m,n = e3[0], e3[1]
                x_cycle = {a for a in cycle if a not in TIy}
                S = {u for e in x_cycle for u in e}
                LHS = quicksum(model._x[i,j] for i in S for j in S if (i,j) in A)+quicksum(model._y[e] for e in illegal_requests)
                #breakpoint()
                added_cuts = set()
                added_y = set()
                LHS_check += sum(x[i,j] for i in S for j in S if (i,j) in x)+len(illegal_requests)
            
                #strngthened version of cycle cut performs worse?
                #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                model._lazy_cuts["transferCycleCutR3"] +=1
                #l_cuts["3cycle"].append((S1,S2,S3,tuple(illegal_requests)))
                model.cbLazy(
                    LHS
                    #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                    <= len(cycle)-1
                    )
                print(f"added lazy illegal request transfer cut, {LHS_check}<={len(cycle)-1},  {len(illegal_requests)}, {len(cycle)}", illegal_requests,cycle)
                print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)#, illegal_requests,cycle)
                #if round(LHS_check.getValue()<=len(cycle)-1):
                 #   breakpoint()
                  #  print("fail")
                return True
        except nx.NetworkXNoCycle:
             pass
        G3 = nx.DiGraph()
        G3.add_edges_from(x)
        #if cur_obj<1060:
            #breakpoint()
            #print("error")

        processed_transfers = set()
        cut_transfers = set()
        transfers = set()
        while True:
            # Recalculate transfer order based on current arrival times
            available_transfers = {}
            for tedge in {a: x[a] for a in x if "ts" in a[0]}:
                if tedge not in processed_transfers:
                    for a in list(y.select(tedge[0],"*","*"))+list(y.select("*",tedge[1],"*")):
                        if (a[0],a[1]) in TIy:
                            trans_edge = (a[0],a[1])
                            if trans_edge not in transfers:
                                if (a[0],a[0].replace("ts","tf")) in x and (a[1].replace("tf","ts"),a[1]) in x:
                                    # Use current arrival time from graph G
                                    current_arrival = G[a[0]][a[0].replace("ts","tf")]["arrival_time"]
                                    available_transfers[trans_edge] = current_arrival
                                    transfers.add(trans_edge)
            
            if not available_transfers:
                break
                
            # Process the transfer with earliest arrival time
            next_transfer = min(available_transfers.items(), key=lambda item: item[1])
            a= next_transfer[0]
            processed_transfers.add(a)
            delta = G[a[0]][a[0].replace("ts","tf")]["arrival_time"]-G[a[1].replace("tf","ts")][a[1]]["arrival_time"]
            if delta>0:
                #print(delta)
                #G.add_edge(a[0],a[1],arrival_time=G[a[0]][a[0].replace("ts","tf")]["arrival_time"])
                # Find all successors of a[1] and update all arcs in the path
                curr_vehicle = int(a[1].split(".")[1])
                path = {curr_vehicle:[a[1]]}
                delta_p = {curr_vehicle:delta}
                for u, v in nx.dfs_edges(G, source=a[1]):
                    G[u][v]["arrival_time"] += delta_p[curr_vehicle]
                    if (u,v) in transfers:
                        available_transfers[u,v] = G[u][v]["arrival_time"]
                        curr_vehicle_temp = int(v.split(".")[1])
                        if curr_vehicle_temp not in path:
                            path[curr_vehicle_temp]=[]
                            if G[v.replace("f","s")][v]["arrival_time"]<G[u][v]["arrival_time"]:
                                delta_p[curr_vehicle_temp] = G[u][v]["arrival_time"]-G[v.replace("f","s")][v]["arrival_time"]
                            else:
                                delta_p[curr_vehicle_temp] = 0
                            curr_vehicle =  curr_vehicle_temp 
                    path[curr_vehicle].append(v)
                    if G[u][v]["arrival_time"]>wbTW.get((u,v),df.b.max()):
                        """
                        #breakpoint()
                        p1 = list(nx.ancestors(G3,a[0]) | {a[0]})
                        p2 = path[curr_vehicle]
                        edges1 = [(i,j) for i in p1 for j in p1 if (i,j) in x]
                        edges2 = [(i,j) for i in p2 for j in p2 if (i,j) in x]
                        illegal_request = [ir for ir in transfer_requests if (ir[0],ir[1])==a]
                        LHS = quicksum(model._x[i, j] for i in p1 for j in p1 if (i,j) in A)+quicksum(model._x[i, j] for i in p2 for j in p2 if (i,j) in A)
                        LHS_check = sum(x[i, j] for i in p1 for j in p1 if (i,j) in x)+sum(x[i, j] for i in p2 for j in p2 if (i,j) in x)
                        RHS = len(edges1)+len(edges2)
                        #l_cuts["tTime"].append((p1,p2,illegal_request))
                        #case 1
                        if p2[0]==a[1]:                        
                            LHS_check += len(illegal_request)
                        else:
                            #case 2
                            p3 = nx.shortest_path(G,a[1],p2[0])
                            a2 = (p3[-2],p3[-1])
                            p3 = p3[:-1]
                            edges3 = [(i,j) for i in p3 for j in p3 if (i,j) in x]
                            illegal_request += [ir for ir in transfer_requests if (ir[0],ir[1])==a2]
                            LHS +=quicksum(model._x[i, j] for i in p3 for j in p3 if (i,j) in A)
                            LHS_check += len(illegal_request)+sum(x[i, j] for i in p3 for j in p3 if (i,j) in x)
                            RHS += len(edges3)
                            #l_cuts["tTime"][-1] = (p1,p2,p3,illegal_request)
                            for a in transfers:
                                if a in edges3:
                                    model._error_msgs += f"case 3 in illegal transfer path cut; "
                        LHS += quicksum(model._y[e] for e in illegal_request)
                        RHS += len(illegal_request)-1
                        model.cbLazy(
                            LHS#for (i,j) in edges)#
                            <= RHS
                            )
                        print(f"added lazy illegal transfer path cut {LHS_check}<={RHS}",p1,p2)
                        """
                        for i,j in cut_transfers:
                            model.cbLazy(model._z.sum(i,"*")+service_time[j] -Mij[i,j]*(1-model._ti[i,j])<= model._z.sum(j,"*"))
                            
                        print(f"added lazy illegal transfer path cut {processed_transfers}")
 
                        model._lazy_cuts["IP_trans"] += 1
                        return True
                #print(path)
        #nx.get_edge_attributes(G, "arrival_time")
        return False
    
    def check_illegal_transfer3(model, x, y, z, cur_obj):
        #returns true if cut was added

        G = nx.DiGraph()
        #for e in z:
         #  G.add_edge(e[0],e[1],arrival_time=z[e])
        
        G.add_edges_from(x)
        #check path length
        for node in VO:
            z_val = 0.0
            for u, v in nx.dfs_edges(G, source=node):
                z_val+=c[u,v]
                G[u][v]["arrival_time"] = z_val

        transfers = list()
        transfer_order = dict(sorted(
            {a: x[a] for a in x if "ts" in a[0]}.items(),
            key=lambda item: item[1]
        ))
        #create precedence graph
        transfer_requests = []
        for tedge in transfer_order:
            for a in list(y.select(tedge[0],"*","*"))+list(y.select("*",tedge[1],"*")):
                if (a[0],a[1]) in TIy:
                    trans_edge = (a[0],a[1])
                    if trans_edge not in transfers:
                        if (a[0],a[0].replace("ts","tf")) in x and (a[1].replace("tf","ts"),a[1]) in x:
                            G.add_edge(a[0],a[1],arrival_time=G[a[0]][a[0].replace("ts","tf")]["arrival_time"])
                            transfers.append(trans_edge)
                            transfer_requests.append(a)

        
        try:
             cycle = nx.find_cycle(G, orientation=None)
             illegal_requests = [a for a in transfer_requests if (a[0],a[1]) in cycle]
             x_cycle = {a for a in cycle if a not in TIy}
             S = set()
             for edge in x_cycle:
                 # Each edge is a tuple (source, target)
                 source, target = edge
                 S.add(source)
                 S.add(target)
             

             if len(illegal_requests)==1:
                 LHS_check = 0.0
                 illegal_requests = set(illegal_requests)
                 for e in illegal_requests:
                     S.remove(e[0])
                     S.remove(e[1])
                 tidx = int(e[0].split(".")[-1])
                 
                 for i in TS_loc[tidx]:
                     for k,j in TIy.select(i,"*"):
                         if (k not in S and j not in S):
                             illegal_requests.add((k,j,e[2]))
                 LHS = quicksum(model._ti[e[0],e[1]] for e in illegal_requests)+quicksum(model._x[i,j] for i in S for j in S if (i,j) in A)
                 LHS_check += 1+sum(x[i,j] for i in S for j in S if (i,j) in x)
                 added_cuts = set()
                 for e in illegal_requests:
                     if e[0] not in added_cuts:
                         LHS += quicksum(model._x[i,j] for i in S for j in [e[0]] if (i,j) in A)
                         LHS_check += sum(x[i,j] for i in S for j in [e[0]] if (i,j) in x)
                         added_cuts.add(e[0])
                     if e[1] not in added_cuts:
                         LHS += quicksum(model._x[j,i] for i in S for j in [e[1]] if (j,i) in A)
                         LHS_check += sum(x[j,i] for i in S for j in [e[1]] if (j,i) in x)#"""
                         added_cuts.add(e[1])
                     #"""
                     
                     
                 #l_cuts["1cycle"].append((S,tuple(illegal_requests)))
                 #strngthened version of cycle cut performs worse?
                 #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                 model.cbLazy(
                     LHS
                     #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                     <= len(cycle)-1
                 )
                 model._lazy_cuts["transferCycleCutR1"] +=1
                 if LHS_check-(len(cycle)-1)>1.5:
                     model._error_msgs +="added wrong lazy illegal request transfer cut 1 {LHS_check}<={len(cycle)-1}; "
                 #print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)
                 print(f"added lazy illegal request transfer cut {LHS_check}<={len(cycle)-1}", illegal_requests,cycle)
                 #breakpoint()
                 for i, j in illegal_requests:
                     for r in model._R:
                         model.cbCut(model._ti[i,j]>= model._y[i,j,r])
                 return True
             if len(illegal_requests)==2:
                  LHS_check = 0.0
                  LHS_check_edges = set()
                  e1,e2 = illegal_requests[0],illegal_requests[1]
                  k,l = e1[0], e1[1]
                  u,v = e2[0], e2[1]
                  S1 = get_path_in_cycle(l,u,cycle)
                  S2 =  get_path_in_cycle(v,k,cycle)
                  illegal_requests = set()
                  illegal_requests.add((e1,e2))
                  tidx1 = int(k.split(".")[-1])
                  tidx2 = int(u.split(".")[-1])
                  for i in TS_loc[tidx1]:
                      for l in TS_loc[tidx2]:
                          for k,j in TIy.select(i,"*"):
                              if (k not in S and j not in S):
                                  for k2,j2 in TIy.select(l,"*"):
                                      if (k2 not in S and j2 not in S):
                                          illegal_requests.add(((k,j,e1[2]),(k2,j2,e2[2])))
                  LHS = quicksum(model._x[i,j] for i in S1 for j in S1 if (i,j) in A)+quicksum(model._x[i,j] for i in S2 for j in S2 if (i,j) in A)
                  #breakpoint()
                  added_cuts = set()
                  added_y = set()
                  LHS_check += sum(x[i,j] for i in S1 for j in S1 if (i,j) in x)+sum(x[i,j] for i in S2 for j in S2 if (i,j) in x)
                  for e1,e2 in illegal_requests:
                      k,l = e1[0], e1[1]
                      u,v = e2[0], e2[1]
                      if e1 not in added_y:
                          LHS += model._ti[e1[0],e1[1]]
                          added_y.add(e1)
                          if e1 in y:
                              LHS_check +=1
                      if e2 not in added_y:
                          LHS += model._ti[e2[0],e2[1]]
                          added_y.add(e2)
                          if e2 in y:
                              LHS_check +=1
                      if l not in added_cuts:
                          LHS += quicksum(model._x[i,j] for j in S1 for i in [l] if (i,j) in A)
                          LHS_check += quicksum(x[i,j] for j in S1 for i in [l] if (i,j) in x)
                          added_cuts.add(l)
                      if u not in added_cuts:
                         LHS += quicksum(model._x[i,j] for i in S1 for j in [u] if (i,j) in A)
                         LHS_check += quicksum(x[i,j] for i in S1 for j in [u] if (i,j) in x)
                         added_cuts.add(u)
                      if k not in added_cuts:
                         LHS += quicksum(model._x[i,j] for i in S2 for j in [k] if (i,j) in A)
                         LHS_check += quicksum(x[i,j] for i in S2 for j in [k] if (i,j) in x)
                         added_cuts.add(k)
                      if v not in added_cuts:
                         LHS += quicksum(model._x[j,i] for i in S2 for j in [v] if (j,i) in A)
                         LHS_check += quicksum(x[j,i] for i in S2 for j in [v] if (j,i) in x)
                         added_cuts.add(v)
                      if (l,u) in A:
                          if (l,u) in x and (l,u) not in LHS_check_edges:
                              LHS += model._x[l,u]
                              LHS_check += x[l,u]
                              LHS_check_edges.add((l,u))
                      if (v,k) in A:
                          if(v, k) in x and (v,k) not in LHS_check_edges:
                              LHS += model._x[v,k]              
                              LHS_check +=x[v,k]
                              LHS_check_edges.add((l,u))
                      if (k,l) in A:
                          if(k,l) in x and (k,l) not in LHS_check_edges:
                              LHS += model._x[k,l]
                              LHS_check +=x[k,l]
                              LHS_check_edges.add((l,u))
                      if (u,v) in A:
                          if(u,v) in x and (u,v) not in LHS_check_edges:
                             LHS += model._x[u,v]
                             LHS_check +=x[u,v]
                             LHS_check_edges.add((l,u))
                  #l_cuts["2cycle"].append((S1,S2,tuple(illegal_requests)))
                  #if set(S1) == set(['d9', 'd8', 'p11', 'p5', 'p19', 'd5', 'p15']):
                   #   if set(S2)== set(['d23', 'd11', 'p14', 'd14', 'p17', 'd19', 'd17', 'p3', 'd3', 'p20', 'd20', 'p21', 'd21', 'p1', 'p7', 'd7', 'p9']):
                    #     breakpoint()
                  #strngthened version of cycle cut performs worse?
                  #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                  model._lazy_cuts["transferCycleCutR2"] +=1
                  model.cbLazy(
                      LHS
                      #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                      <= len(cycle)-1
                      )
                  print(f"added lazy illegal request transfer cut, {LHS_check}<={len(cycle)-1},  {len(illegal_requests)}, {len(cycle)}", illegal_requests,cycle)
                  #print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)#, illegal_requests,cycle)
                  #if round(LHS_check.getValue()<=len(cycle)-1):
                   #   breakpoint()
                    #  print("fail")
                  for i, j in illegal_requests:
                      for r in model._R:
                          model.cbCut(model._ti[i,j]>= model._y[i,j,r])
                  return True
              
             if len(illegal_requests)==3:
                  LHS_check = 0.0
                  LHS_check_edges = set()
                  e1,e2,e3 = illegal_requests[0],illegal_requests[1],illegal_requests[2]
                  k,l = e1[0], e1[1]
                  u,v = e2[0], e2[1]
                  m,n = e3[0], e3[1]
                  S1 = get_path_in_cycle(l,u,cycle)
                  S2 =  get_path_in_cycle(v,m,cycle)
                  S3 =  get_path_in_cycle(n,k,cycle)
                  illegal_requests = set()
                  illegal_requests.add((e1,e2,e3))
                  tidx1 = int(k.split(".")[-1])
                  tidx2 = int(u.split(".")[-1])
                  tidx3 = int(m.split(".")[-1])
                  for i in TS_loc[tidx1]:
                      for l in TS_loc[tidx2]:
                          for o in TS_loc[tidx3]:
                              for k,j in TIy.select(i,"*"):
                                  if (k not in S and j not in S):
                                      for k2,j2 in TIy.select(l,"*"):
                                          if (k2 not in S and j2 not in S):
                                              for k3,j3 in TIy.select(o,"*"):
                                                  if (k3 not in S and j3 not in S):
                                                      illegal_requests.add(((k,j,e1[2]),(k2,j2,e2[2]),(k3,j3,e3[2])))
                  LHS = quicksum(model._x[i,j] for i in S1 for j in S1 if (i,j) in A)+quicksum(model._x[i,j] for i in S2 for j in S2 if (i,j) in A)+quicksum(model._x[i,j] for i in S3 for j in S3 if (i,j) in A)
                  #breakpoint()
                  added_cuts = set()
                  added_y = set()
                  LHS_check += sum(x[i,j] for i in S1 for j in S1 if (i,j) in x)+sum(x[i,j] for i in S2 for j in S2 if (i,j) in x)+sum(x[i,j] for i in S3 for j in S3 if (i,j) in x)
                  for e1,e2,e3 in illegal_requests:
                      k,l = e1[0], e1[1]
                      u,v = e2[0], e2[1]
                      m,n = e3[0], e3[1]
                      if e1 not in added_y:
                          LHS += model._ti[e1[0], e1[1]]
                          added_y.add(e1)
                          if e1 in y:
                              LHS_check +=1
                      if e2 not in added_y:
                          LHS += model._ti[e2[0], e2[1]]
                          added_y.add(e2)
                          if e2 in y:
                              LHS_check +=1
                      if e3 not in added_y:
                         LHS += model._ti[e3[0], e3[1]]
                         added_y.add(e3)
                         if e3 in y:
                             LHS_check +=1
                      if l not in added_cuts:
                          LHS += quicksum(model._x[i,j] for j in S1 for i in [l] if (i,j) in A)
                          LHS_check += quicksum(x[i,j] for j in S1 for i in [l] if (i,j) in x)
                          added_cuts.add(l)
                      if u not in added_cuts:
                         LHS += quicksum(model._x[i,j] for i in S1 for j in [u] if (i,j) in A)
                         LHS_check += quicksum(x[i,j] for i in S1 for j in [u] if (i,j) in x)
                         added_cuts.add(u)
                      if k not in added_cuts:
                         LHS += quicksum(model._x[i,j] for i in S3 for j in [k] if (i,j) in A)
                         LHS_check += quicksum(x[i,j] for i in S3 for j in [k] if (i,j) in x)
                         added_cuts.add(k)
                      if v not in added_cuts:
                         LHS += quicksum(model._x[j,i] for i in S2 for j in [v] if (j,i) in A)
                         LHS_check += quicksum(x[j,i] for i in S2 for j in [v] if (j,i) in x)
                         added_cuts.add(v)
                      if m not in added_cuts:
                         LHS += quicksum(model._x[i,j] for i in S2 for j in [m] if (i,j) in A)
                         LHS_check += quicksum(x[i,j] for i in S2 for j in [m] if (i,j) in x)
                         added_cuts.add(k)
                      if n not in added_cuts:
                         LHS += quicksum(model._x[j,i] for i in S3 for j in [n] if (j,i) in A)
                         LHS_check += quicksum(x[j,i] for i in S3 for j in [n] if (j,i) in x)
                         added_cuts.add(v)
                      if (l,u) in A:
                          if (l,u) in x and (l,u) not in LHS_check_edges:
                              LHS += model._x[l,u]
                              LHS_check += x[l,u]
                              LHS_check_edges.add((l,u))
                      if (v,k) in A:
                          if(v, k) in x and (v,k) not in LHS_check_edges:
                              LHS += model._x[v,k]              
                              LHS_check +=x[v,k]
                              LHS_check_edges.add((l,u))
                      if (u,n) in A:
                          if (u,n) in x and (u,n) not in LHS_check_edges:
                              LHS += model._x[u,n]
                              LHS_check += x[u,n]
                              LHS_check_edges.add((u,n))
                      if (v,m) in A:
                          if(v, m) in x and (v,m) not in LHS_check_edges:
                              LHS += model._x[v,m]              
                              LHS_check +=x[v,m]
                              LHS_check_edges.add((v,m))
                      if (n,k) in A:
                          if(n, k) in x and (n,k) not in LHS_check_edges:
                              LHS += model._x[n,k]              
                              LHS_check +=x[n,k]
                              LHS_check_edges.add((n,k))
                      if (l,m) in A:
                          if(l, m) in x and (l,m) not in LHS_check_edges:
                              LHS += model._x[l,m]              
                              LHS_check +=x[l,m]
                              LHS_check_edges.add((l,m))
                      if (k,l) in A:
                          if(k,l) in x and (k,l) not in LHS_check_edges:
                              LHS += model._x[k,l]
                              LHS_check +=x[k,l]
                              LHS_check_edges.add((l,u))
                      if (u,v) in A:
                          if(u,v) in x and (u,v) not in LHS_check_edges:
                             LHS += model._x[u,v]
                             LHS_check +=x[u,v]
                             LHS_check_edges.add((l,u))
                      if (m,n) in A:
                         if(m,n) in x and (m,n) not in LHS_check_edges:
                            LHS += model._x[m,n]
                            LHS_check +=x[m,n]
                            LHS_check_edges.add((m,n))
                  #l_cuts["3cycle"].append((S1,S2,S3,tuple(illegal_requests)))
                  #if set(S1) == set(['d9', 'd8', 'p11', 'p5', 'p19', 'd5', 'p15']):
                   #   if set(S2)== set(['d23', 'd11', 'p14', 'd14', 'p17', 'd19', 'd17', 'p3', 'd3', 'p20', 'd20', 'p21', 'd21', 'p1', 'p7', 'd7', 'p9']):
                    #     breakpoint()
                  #strngthened version of cycle cut performs worse?
                  #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                  model._lazy_cuts["transferCycleCutR3"] +=1
                  model.cbLazy(
                      LHS
                      #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                      <= len(cycle)-1
                      )
                  print(f"added lazy illegal request transfer cut, {LHS_check}<={len(cycle)-1},  {len(illegal_requests)}, {len(cycle)}", illegal_requests,cycle)
                  #print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)#, illegal_requests,cycle)
                  #if round(LHS_check.getValue()<=len(cycle)-1):
                   #   breakpoint()
                    #  print("fail")
                  for i, j in illegal_requests:
                      for r in model._R:
                          model.cbCut(model._ti[i,j]>= model._y[i,j,r])
                  return True
             if len(illegal_requests)>3:
                 LHS_check = 0.0
                 LHS_check_edges = set()
                 e1,e2,e3 = illegal_requests[0],illegal_requests[1],illegal_requests[2]
                 k,l = e1[0], e1[1]
                 u,v = e2[0], e2[1]
                 m,n = e3[0], e3[1]
                 x_cycle = {a for a in cycle if a not in TIy}
                 S = {u for e in x_cycle for u in e}
                 LHS = quicksum(model._x[i,j] for i in S for j in S if (i,j) in A)+quicksum(model._ti[e[0],e[1]] for e in illegal_requests)
                 #breakpoint()
                 added_cuts = set()
                 added_y = set()
                 LHS_check += sum(x[i,j] for i in S for j in S if (i,j) in x)+len(illegal_requests)
             
                 #strngthened version of cycle cut performs worse?
                 #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                 model._lazy_cuts["transferCycleCutR3"] +=1
                 #l_cuts["3cycle"].append((S1,S2,S3,tuple(illegal_requests)))
                 model.cbLazy(
                     LHS
                     #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                     <= len(cycle)-1
                     )
                 print(f"added lazy illegal request transfer cut, {LHS_check}<={len(cycle)-1},  {len(illegal_requests)}, {len(cycle)}", illegal_requests,cycle)
                 print(f"added lazy illegal request transfer cut: {len(illegal_requests)}, {len(cycle)}",illegal_requests, cycle)#, illegal_requests,cycle)
                 #if round(LHS_check.getValue()<=len(cycle)-1):
                  #   breakpoint()
                   #  print("fail")
                 for i, j in illegal_requests:
                      for r in model._R:
                          model.cbCut(model._ti[i,j]>= model._y[i,j,r])
                 return True
        except nx.NetworkXNoCycle:
             pass
        G3 = nx.DiGraph()
        G3.add_edges_from(x)
        #if cur_obj<1060:
            #breakpoint()
            #print("error")

        processed_transfers = set()
        transfers = set()
        while True:
            # Recalculate transfer order based on current arrival times
            available_transfers = {}
            for tedge in {a: x[a] for a in x if "ts" in a[0]}:
                if tedge not in processed_transfers:
                    for a in list(y.select(tedge[0],"*","*"))+list(y.select("*",tedge[1],"*")):
                        if (a[0],a[1]) in TIy:
                            trans_edge = (a[0],a[1])
                            if trans_edge not in transfers:
                                if (a[0],a[0].replace("ts","tf")) in x and (a[1].replace("tf","ts"),a[1]) in x:
                                    # Use current arrival time from graph G
                                    current_arrival = G[a[0]][a[0].replace("ts","tf")]["arrival_time"]
                                    available_transfers[trans_edge] = current_arrival
                                    transfers.add(trans_edge)
            
            if not available_transfers:
                break
                
            # Process the transfer with earliest arrival time
            next_transfer = min(available_transfers.items(), key=lambda item: item[1])
            a= next_transfer[0]
            processed_transfers.add(a)
            delta = G[a[0]][a[0].replace("ts","tf")]["arrival_time"]-G[a[1].replace("tf","ts")][a[1]]["arrival_time"]
            if delta>0:
                #print(delta)
                #G.add_edge(a[0],a[1],arrival_time=G[a[0]][a[0].replace("ts","tf")]["arrival_time"])
                # Find all successors of a[1] and update all arcs in the path
                curr_vehicle = int(a[1].split(".")[1])
                path = {curr_vehicle:[a[1]]}
                delta_p = {curr_vehicle:delta}
                for u, v in nx.dfs_edges(G, source=a[1]):
                    G[u][v]["arrival_time"] += delta_p[curr_vehicle]
                    if (u,v) in transfers:
                        available_transfers[u,v] = G[u][v]["arrival_time"]
                        curr_vehicle_temp = int(v.split(".")[1])
                        if curr_vehicle_temp not in path:
                            path[curr_vehicle_temp]=[]
                            if G[v.replace("f","s")][v]["arrival_time"]<G[u][v]["arrival_time"]:
                                delta_p[curr_vehicle_temp] = G[u][v]["arrival_time"]-G[v.replace("f","s")][v]["arrival_time"]
                            else:
                                delta_p[curr_vehicle_temp] = 0
                            curr_vehicle =  curr_vehicle_temp 
                    path[curr_vehicle].append(v)
                    if G[u][v]["arrival_time"]>wbTW.get((u,v),df.b.max()):
                        """
                        #breakpoint()
                        p1 = list(nx.ancestors(G3,a[0]) | {a[0]})
                        p2 = path[curr_vehicle]
                        edges1 = [(i,j) for i in p1 for j in p1 if (i,j) in x]
                        edges2 = [(i,j) for i in p2 for j in p2 if (i,j) in x]
                        illegal_request = [ir for ir in transfer_requests if (ir[0],ir[1])==a]
                        LHS = quicksum(model._x[i, j] for i in p1 for j in p1 if (i,j) in A)+quicksum(model._x[i, j] for i in p2 for j in p2 if (i,j) in A)
                        LHS_check = sum(x[i, j] for i in p1 for j in p1 if (i,j) in x)+sum(x[i, j] for i in p2 for j in p2 if (i,j) in x)
                        RHS = len(edges1)+len(edges2)
                        #l_cuts["tTime"].append((p1,p2,illegal_request))
                        #case 1
                        if p2[0]==a[1]:                        
                            LHS_check += len(illegal_request)
                        else:
                            #case 2
                            p3 = nx.shortest_path(G,a[1],p2[0])
                            a2 = (p3[-2],p3[-1])
                            p3 = p3[:-1]
                            edges3 = [(i,j) for i in p3 for j in p3 if (i,j) in x]
                            illegal_request += [ir for ir in transfer_requests if (ir[0],ir[1])==a2]
                            LHS +=quicksum(model._x[i, j] for i in p3 for j in p3 if (i,j) in A)
                            LHS_check += len(illegal_request)+sum(x[i, j] for i in p3 for j in p3 if (i,j) in x)
                            RHS += len(edges3)
                            #l_cuts["tTime"][-1] = (p1,p2,p3,illegal_request)
                            for a in transfers:
                                if a in edges3:
                                    model._error_msgs += f"case 3 in illegal transfer path cut; "
                        LHS += quicksum(model._y[e] for e in illegal_request)
                        RHS += len(illegal_request)-1
                        model.cbLazy(
                            LHS#for (i,j) in edges)#
                            <= RHS
                            )
                        print(f"added lazy illegal transfer path cut {LHS_check}<={RHS}",p1,p2)
                        """
                        LHS = quicksum(model._x[e] for e in model._A if e not in x)
                        LHS_check = sum(x.get(e,0) for e in model._A if e not in x)
                        RHS = 1.0
                        model.cbLazy(
                            LHS#for (i,j) in edges)#
                            >= RHS
                            )
                        print(f"added lazy illegal transfer path cut {LHS_check}<={RHS}")
                        #print(p1,p2)
                        if LHS_check>=RHS:
                            #breakpoint()
                            model._error_msgs +=f"error IP_trans: {LHS_check}>={RHS}; "
                        model._lazy_cuts["IP_trans"] += 1
                        return True
                #print(path)
        #nx.get_edge_attributes(G, "arrival_time")
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
    
    def separate_strengthened_capacity_constraint(model,x):
        
        heuristic = StrengthenedCapacitySeparation(P, D, VC, qnode)
        cuts = heuristic.separate(x)
        cut_added = False
        for cut in cuts:
            expr, RHS = heuristic.get_cut_expr(model._x, cut)
            breakpoint()
            print("strengthened capacity cut",RHS,cut)
            cut_added = True
        return cut_added
    
    
    def build_igraph_graph(edges, VD, VO):
        g = ig.Graph(directed=True)
        nodes = set(u for e in edges for u in e).union(set(["source", "target"]))
        node_map = {v: i for i, v in enumerate(nodes)}
        g.add_vertices(len(nodes))
    
        capacity = []
        edge_list = []
        
        for (u, v), cap in edges.items():
            if u in node_map and v in node_map:
                edge_list.append((node_map[u], node_map[v]))
                capacity.append(cap)
    
    
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
        #return False
        added_st_cut = False
        g, node_map = build_igraph_graph(edges, VD, VO)
        for u in model._P|model._D:
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
        #"""
        for u in TS:
            if u in edges:
                mincut, partition = g.st_mincut(node_map[u], node_map["target"], capacity='capacity')
                if mincut<1.0-pow(10,-1):#f["ts"+u[-1]]-pow(10,-1):
                    print("ST user cut", mincut, u)
                    for part in partition:
                        if "target" in part:
                            S_comp = part
                        else:
                            S = part
                    S = {rev_node_map[i] for i in S}
                    S_comp = V-S
                    model.cbCut(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A)>=f["ts"+u[-1]])
                    model._user_cuts["ST2"] +=1
                    #return True
                    added_st_cut = True

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
                breakpoint()
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
            
            ### --- π-Cut --- ###
            exclude_nodes = frozenset([pr]) | VO
            add_edges = [(d, "target", 1.0) for d in VD]
    
            g, node_map, rev_node_map = build_pi_sigma_graph(x, exclude_nodes, add_edges)
            if dr not in node_map or "target" not in node_map:
                continue
    
            result = g.st_mincut(node_map[dr], node_map["target"], capacity='capacity')
            if result.value < 1 - 1e-1:               
                for part in result.partition:
                    if node_map["target"] in part:
                        S_comp = part
                    else:
                        S = part
                S = {rev_node_map[i] for i in S}
                S_comp = V-(frozenset([pr]) | VO|S)
                print("weak pi cut", result.value, dr)
                #cut_pool.append((S,S_comp,dr))
                if mipsol:
                    model.cbLazy(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A) >= 1)
                    model._lazy_cuts["pi"] +=1
                else:
                    model.cbCut(quicksum(model._x[i,j] for i in S for j in S_comp if (i,j) in A) >= 1)
                    model._user_cuts["pi"] +=1
                return True
            
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
                    model._lazy_cuts["sig"] +=1
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
    
    def check_for_illegal_subtour(component):
        def have_different_numbers(pair):
            # Extract numbers from the strings
            numbers = [re.search(r'\d+', elem).group() for elem in pair]
            # Check if the numbers are different
            return numbers[0] != numbers[1]
        #not connected to depot
        if len(set(VO).intersection(set(component)))==0 or len(set(VD).intersection(set(component)))==0:
            return 1
        #two different depots
        if have_different_numbers(component-P-D-TS-TF)==True:
            return 2
        return -1
    
    def eliminate_subtours_components(model, x,mipsol=True):
        G = nx.Graph()
        G.add_edges_from(x)
        scc = [
            c
            for c in sorted(nx.connected_components(G), key=len) if len(c)>1
        ]
        for comp in scc:
                st_case = check_for_illegal_subtour(comp)
                if st_case==1:
                    if mipsol==False:
                            if frozenset(comp) not in model._solver_state.cut_pool:
                                model._solver_state.cut_pool.add(frozenset(comp))
                            else:
                                continue
                    if len(comp.intersection(TS))>0 or len(comp.intersection(TF))>0:
                        filtered = [(i,j) for j in comp for i in comp if (i,j) in A]
                        #print("st check:" ,len(comp),sum(edges[i, j] for (i,j) in filtered if (i,j) in edges))
                        if sum(x[i, j] for (i,j) in filtered if (i,j) in x)-pow(10,-4)>len(comp)-1.0:
                            #print("st user cut added", len(comp),sum(edges[i, j] for (i,j) in filtered if (i,j) in edges))
                            #glob_st_cuts.append(len(comp))
                            if mipsol==True:
                                model.cbLazy(
                                    quicksum(model._x[i, j] for (i,j) in filtered)
                                    <= len(comp)-1
                                )
                                model._lazy_cuts["ST1"] +=1
                                #l_cuts["st"].append(comp)
                                #print("added ST lazy cut: ", len(comp), comp)
                            else:
                                model.cbCut(
                                    quicksum(model._x[i, j] for (i,j) in filtered)
                                    <= len(comp)-1
                                )
                                model._user_cuts["ST1"] +=1
                                #print("added ST cut user: ", len(comp), comp)
                            
                            return True
                    else:
                        filtered = [(i,j) for j in V-comp for i in comp if (i,j) in A]
                        #print("st check:" ,len(comp),sum(edges[i, j] for (i,j) in filtered if (i,j) in edges))
                        if sum(x[i, j] for (i,j) in filtered if (i,j) in x)<1.0-pow(10,-4):
                            #print("st user cut added", len(comp),sum(edges[i, j] for (i,j) in filtered if (i,j) in edges))
                            #glob_st_cuts.append(len(comp))
                            if mipsol==True:
                                model.cbLazy(
                                    quicksum(model._x[i, j] for (i,j) in filtered)
                                    >= 1
                                )
                                model._lazy_cuts["ST2"] +=1
                                #print("added ST lazy cut: ", len(comp), comp)
                            else:
                                model.cbCut(
                                    quicksum(model._x[i, j] for (i,j) in filtered)
                                    >= 1
                                )
                                model._user_cuts["ST2"] +=1
                                #print("added ST cut user: ", len(comp), comp)
                            
                            return True
                if st_case==100:#should be case 2
                    if mipsol==True:
                        o_depot = comp-P-D-TS-TF-VD
                        o_depot = o_depot.pop()
                        e_depot = comp-P-D-TS-TF-VO
                        e_depot = e_depot.pop()
                        correct_target = o_depot.replace("o","e")
                        correct_o_depot = e_depot.replace("e","o")
                        pe = next(G.neighbors(e_depot))
                        so = next(G.neighbors(o_depot))
                        illegal_o_depots = VO-set((correct_o_depot,o_depot))
                        illegal_d_depots = VD-set((correct_target,e_depot))
                        filtered = [(i,j) for j in comp for i in comp if (i,j) in A]
                        t_edges =  comp.intersection(TS)
                        """
                        S = comp
                        Tset   = set()
                        for i in t_edges:
                            Tset.add(int(i[-1]))
                        #+edges = list(zip(path, path[1:]))
                        if len(Tset)>0 and len(find_duplicate_location_indices(t_edges-TF))==0:
                            S = S - t_edges
                            #oint(breakpoint()
                            LHS = quicksum(model._x[i, j] for i in S for j in S if (i,j) in A)
                            LHS += quicksum(model._f[f"ts{idx}"] for idx in Tset)
                            LHS += quicksum(model._x[i,j] for i in S for idx in Tset for j in TS_loc[idx] if (i,j) in A)
                            LHS += quicksum(model._x[i,j] for j in S for idx in Tset for i in TF_loc[idx] if (i,j) in A)"""
                        LHS = quicksum(model._x[i, j] for i in comp for j in comp if (i,j) in A)
                        LHS += quicksum(model._x[i, j] for i in comp for j in illegal_d_depots if (i,j) in model._A)
                        LHS_check = 0
                        #LHS_check += sum(x[i, j] for (i,j) in filtered if (i,j) in x)+sum(x[i, j] for i in comp for j in illegal_d_depots if (i,j) in x)
                        """
                        for i in t_edges:
                            tidx = int(i.split(".")[-1])
                            for j in TS_loc[tidx]:
                                if j!=i:
                                    if (j,j.replace("s","f")) not in x:
                                        LHS += model._x[j,j.replace("s","f")]+quicksum(model._x[l,j] for l in comp if (l!=i.replace("s","f") and (l,j) in A))+quicksum(model._x[j.replace("s","f"),l] for l in comp if (l!=i and (j.replace("s","f"),l) in A))+quicksum(model._x[j.replace("s","f"),l] for l in illegal_d_depots if (l!=i and (j.replace("s","f"),l) in A))"""
                                        #LHS_check += x.get((j,j.replace("s","f")),0)+sum(model._x[l,j] for l in comp if (l!=i.replace("s","f") and (l,j) in x))+sum(x[j.replace("s","f"),l] for l in comp if (l!=i and (j.replace("s","f"),l) in x))+sum(x[j.replace("s","f"),l] for l in illegal_d_depots if (l!=i and (j.replace("s","f"),l) in x))
                        model.cbLazy(
                                LHS
                                <= len(comp)-2)
                        model._lazy_cuts["depotFixingPathCut"] +=1
                        #print(f"added depot fixing lazy cut: {LHS_check}<={len(comp)-2}",o_depot,e_depot,t_edges, comp)
                        #l_cuts["df"].append((comp,tuple(illegal_d_depots)))
                        print(f"added depot fixing lazy cut: ",o_depot,e_depot,t_edges, comp)
                        #model.cbLazy(
                         #       quicksum(model._x[i, j] for (i,j) in filtered)+quicksum(model._x[j,so ] for j in illegal_o_depots if (j,so) in model._A)
                          #      <= len(comp)-2)
                        return True
                    
                """
                else:
                    subG = nx.subgraph(G,comp)
                    edges = subG.edges
                    z_val = sum(c[e] for e in edges)
                    if z_val>df.b.max():
                        o = set(subG.nodes)-P-D-TS-TF-VD
                        e = set(subG.nodes)-P-D-TS-TF-VO
                        path = nx.shortest_path(G,o[0],e[0])
                        illegal_path_cut(model, path)
                        return True"""
        return False
    
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
        model._cb_last_lower_bound = 0.0
        model._cb_last_ub = np.inf
        model._cb_cuts = set()

        
        return model
    
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
                        #TF_comp = model._TF-frozenset([de])
                        S2 = model._V-frozenset([do,de])-S1
                        RHS =  quicksum(model._x[i, do] for i in S1 if (i,do) in model._A)+quicksum(model._x[de,i] for i in S2 if (de,i) in model._A)
                        RHS+=quicksum(model._x[i, j] for i in S2 for j in S1 if (i,j) in model._A)
                        RHS+= quicksum(model._x[i, j] for i in S1 for j in S2 if (i,j) in model._A and j!=de_cut)
                        RHS_check= sum(x[i, do] for i in S1 if (i,do) in x)+sum(x[de,i] for i in S2 if (de,i) in x)+sum(x[i, j] for i in S2 for j in S1 if (i,j) in x)+sum(x[i, j] for i in S1 for j in S2 if (i,j) in x and j!=de_cut)
                        LHS = model._f[f"ts{node_id}"]
                        print(f"Shortest path for node_id {node_id}: {min_path},(length: {min_length}), RHS: {RHS_check}")
                        model.cbLazy(RHS>=LHS)
                        #l_cuts["multTrans"].append((S1,do,de_cut))
                        model._lazy_cuts["double_trans_cut"] +=1
                        #if RHS_check>=1:
                            #breakpoint()
                            #print("Stop")
                        return
    
    
    def ub_callback(model, where):
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
                    analyze_growth_rate(model)
        if where == GRB.Callback.MIPSOL:
            model._stats["lazy_calls"] += 1
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
            all_z_vars = model.cbGetSolution(model._z)
            #all_f_vars = model.cbGetSolution(model._f)
            #f_arcs = {a:all_f_vars[a] for a in TS_pure if all_f_vars[a] > 0.5}
            #if len(f_arcs)>0:
            #if cur_obj<=503.236 and cur_obj>=503.23:
             #   print("violation", cur_obj)
                #breakpoint()
            x_arcs = {a:all_x_vars[a] for a in A if all_x_vars[a] > 0.5}
            
            
            #if eliminate_subtours_components(model, x_arcs)==True:
                #return
            if cutTrans==True:
                added_cut = check_multiple_transfer_stations(model,x_arcs)
                if added_cut == True:
                    return
            y_arcs = tuplelist({a for a in Ay if all_y_vars[a] > 0.5})
            z_arcs = {a:all_z_vars[a] for a in A if all_z_vars[a] > pow(10,-4)}
            added_cut = check_illegal_transfer0(model, x_arcs, y_arcs, z_arcs,cur_obj)
            if added_cut == True:
                return
            #if cur_obj<1060:
                #breakpoint()
                #print("error")
            #separate_weak_pi_and_sigma_cuts(model, x_arcs, mipsol=True)
            #separate_weak_pi_cuts(model, x_arcs, mipsol=True)
            #separate_weak_sigma_cuts(model, x_arcs, mipsol=True)
            if sol_cnt>0:
                if cur_obj < model._solver_state.model_ub:
                    model._solver_state.model_ub = cur_obj
            
            else:
                if model._solver_state.model_ub<np.inf:
                    model._sols.add(np.round(model._solver_state.model_ub,4))
                    temp_sol = model._solver_state.new_solution
                    tempx, tempy = model._x, model._y
                    new_vars = [tempx[var] for var in temp_sol["x"]] + [tempy[var] for var in temp_sol["y"]]#+[model._z[var] for var in temp_sol["z"]]+[model._bz[var] for var in temp_sol["bz"]]+[model._bl[var] for var in temp_sol["bl"]]
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
            status = model.cbGet(GRB.Callback.MIPNODE_STATUS)
            #phase = model.cbGet(GRB.Callback.MIPNODE_PHASE)
            #"""
            if status == GRB.OPTIMAL:
                all_x_vars = model.cbGetNodeRel(model._x)
                x_arcs = {a:all_x_vars[a] for a in A if all_x_vars[a] > 0.00001 }
                nodecnt = model.cbGet(GRB.Callback.MIPNODE_NODCNT)
                #if nodecnt<1:
                 #  exact_subtour_elemination(model,  x_arcs)
                #else:
                
                if nodecnt<1:#and model._cb_nroot<251:
                        print(f"{int(nodecnt)} - MIPNODE separation -")
                        model._cb_lastnode= nodecnt
                        all_f_vars = model.cbGetNodeRel(model._f)
                        f_vars = {a:all_f_vars[a] for a in all_f_vars if all_f_vars[a] > 0.00001 }
                        all_y_vars = model.cbGetNodeRel(model._y)
                        y_arcs = {a:all_y_vars[a] for a in Ay if all_y_vars[a] > 0.001 }
                        if eliminate_subtours_components(model, x_arcs)==False:
                            if separate_weak_pi_and_sigma_cuts(model, x_arcs,y_arcs, mipsol=False)==False:
                                pass
                                #capcut = separate_rounded_capacity_inequalities(model,x_arcs,P,D,model._Q)
                                #if capcut==True:
                                   #model._cb_nroot += 1

                            else:
                                model._cb_nroot += 1
                        else:
                            model._cb_nroot += 1

                
                else:
                    epsilon = pow(10, -4)
                    cur_lb =  model.cbGet(GRB.Callback.MIPNODE_OBJBND)
                    cur_ub = model.cbGet(GRB.Callback.MIPNODE_OBJBST)
                    sep = True
                      
                    if (nodecnt - model._cb_lastnode >= 400 and model._cb_mipnode_stop ==False):
                        if model._cb_last_lower_bound<cur_lb-epsilon or model._cb_last_ub-epsilon>cur_ub:
                            sep = False
                        model._cb_last_lower_bound = cur_lb
                        model._cb_last_ub = cur_ub
                        model._cb_lastnode= nodecnt
                        if sep==False:
                            return
                        print(f"{int(nodecnt)} - MIPNODE separation -")
                        all_f_vars = model.cbGetNodeRel(model._f)
                        f_vars = {a:all_f_vars[a] for a in all_f_vars if all_f_vars[a] > 0.00001 }
                        #if exact_subtour_elemination(model,x_arcs, f_vars , mipsol=False)==False:
                        if eliminate_subtours_components(model, x_arcs, mipsol=False)==False:
                            all_y_vars = model.cbGetNodeRel(model._y)
                            y_arcs = {a:all_y_vars[a] for a in Ay if all_y_vars[a] > 0.001 }
                            separate_weak_pi_and_sigma_cuts(model, x_arcs,y_arcs, mipsol=False)
                            #if separate_weak_pi_and_sigma_cuts(model, x_arcs,y_arcs, mipsol=False)==False:
                                #separate_rounded_capacity_inequalities(model,x_arcs,P,D,model._Q)

                #separate_weak_pi_cuts(model, x_arcs, mipsol=False)
                #separate_weak_sigma_cuts(model, x_arcs, mipsol=False)
                #print("check new solution",model_ub)
            if sol_cnt>0:
                if np.round(cur_obj,4) > np.round(model._solver_state.model_ub,4)+pow(10,-4):
                    if np.round(model._solver_state.model_ub,4) not in model._sols:
                        model._sols.add(np.round(model._solver_state.model_ub,4))
                        with model._solver_state.mutex:
                            temp_sol = model._solver_state.new_solution
                            new_vars = [model._x[var] for var in temp_sol["x"]] + [model._y[var] for var in temp_sol["y"]]#+[model._bl[var] for var in temp_sol["bl"]]
                            new_vals = list(temp_sol["x"].values()) + list(temp_sol["y"].values())#+ list(temp_sol["bl"].values())
                        print("new solution:", model._solver_state.model_ub, cur_obj)
                        #model.cbSetSolution(model._vars,[0.0]*len(model._vars))
                        model.cbSetSolution(new_vars, new_vals)
                        model.cbUseSolution()

            else:
                if model._solver_state.model_ub<np.inf:
                    model._sols.add(np.round(model._solver_state.model_ub,4))
                    with model._solver_state.mutex:
                        temp_sol = model._solver_state.new_solution
                        new_vars = [model._x[var] for var in temp_sol["x"]] + [model._y[var] for var in temp_sol["y"]]#+[model._bl[var] for var in temp_sol["bl"]]
                        new_vals = list(temp_sol["x"].values()) + list(temp_sol["y"].values())#+ list(temp_sol["z"].values())+ list(temp_sol["bz"].values())+ list(temp_sol["bl"].values())
                    print("new solution:", model._solver_state.model_ub, cur_obj)
                    #model.cbSetSolution(model._vars,[0.0]*len(model._vars))
                    model.cbSetSolution(new_vars, new_vals)
            model._stats["usercut_t"] += time.time()-start


            
    def get_tour(arcs):
        tours = []
        #breakpoint()
        try:
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
                    print(tour,sum(c[e] for e in tour))
                    tours.append(tour)
        except:
            #breakpoint()
            print("error")
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
                    Q_vehicle = Qmin+model._vl[v].x
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
    
    def solve_compact(barrier=None, env=None,solver_state=None ,mode="two",timeFlow=True):
        if env==None:
            model = gp.Model()
        else:
            model = gp.Model(env=env)
     
    
        
        model = Model(f'myTwoIndexModel_noBigM_BC_{mode}Phase_illegalTrans02')
        model._solver_state = solver_state
        x = model.addVars(xIndex, vtype=GRB.BINARY, name='x')
        y = model.addVars(Ay, vtype=GRB.BINARY, name='y')
        #Idee wenn zwei vehicle unterschiedliche StartPositionen haben, b trackt vehicle flow
        #b = model.addVars(arcs,lb=0.0,ub=len(K)-1, vtype=GRB.CONTINUOUS, name='b')
        #bl = model.addVars(kArcs, vtype=GRB.BINARY, name='bl')
        if VC<0:
            vl = model.addVars(V, vtype=GRB.CONTINUOUS, name='vl')
            model._vl = vl
        bl = model.addVars(V,ub=len(K), vtype=GRB.CONTINUOUS, name='bl')
        z = model.addVars(xIndex,lb=0.0 ,vtype=GRB.CONTINUOUS, name="z")
        #a = model.addVars([(i,r) for i in TS for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="a")
        ti = model.addVars(TIy, vtype=GRB.BINARY, name='ti')
        #b = model.addVars(xIndex,lb=0.0, ub=nVehicles ,vtype=GRB.CONTINUOUS, name="b")
        #z = model.addVars(xIndex,vtype=GRB.CONTINUOUS, name="z")
        #a = model.addVars([(i,r) for i in TS for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="a")
        #bz = model.addVars(zIndex,lb=0.0 ,vtype=GRB.CONTINUOUS, name="bz")
        #ba = model.addVars([(i,r) for i in TF for r in pd.RangeIndex(nRequests) ],lb=0.0 ,vtype=GRB.CONTINUOUS, name="ba")
        f = model.addVars([i for i in TS_pure], vtype=GRB.BINARY, name='f')
        
        model.modelSense = GRB.MINIMIZE
        model.setObjective(quicksum(c[i,j] * x[i, j] for (i,j) in arcs))
        model.update()
        
        
       
        """
        Arc flows
        """
    
   
        if "Lim" not in filename and "Ghilas" not in filename:
            model.addConstrs((quicksum(x[vo, j] for j in [a[1] for a in A.select(vo,'*')]) == 1 for vo in VO), name = "ct.route_startFirst")
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
            #model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if r!=int(i.replace("p","").replace("d","")) and j in [a[1] for a in Ay.select(i,'*',r)]) <= (VC-abs(qnode[i]))*x[i,j] for i in P|D  for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacityStrong2")
            model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if j in [a[1] for a in Ay.select(i,'*',r)]) <= (VC)*x[i,j] for i in TS|TF  for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacityStrong2")
            #model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)]) <= VC*x[i,j] for i in P|D for j in [a[1] for a in Ay.select(i,'*','*')]), name="ct.VehicleCapacity")

            model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if r!=int(i.replace("p","").replace("d","")) for j in [a[1] for a in Ay.select(i,'*',r)]) <= quicksum((VC-abs(qnode[i]))*x[i,j] for j in [a[1] for a in A.select(i,'*')]) for i in P|D), name="ct.VehicleCapacityStrong2")
            #model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R if r in [a[2] for a in Ay.select(i,j,r)]) <= VC*x[i,j] for i in P|D|TF for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacity")
            #model.addConstrs((quicksum(q[r]*y[i,j,r]  for r in R if r!=int(i.replace("p","")) and j!=f"p{r}") <= (VC-abs(qnode[i]))*x[i,j] for i in P for j in [a[1] for a in A.select(i,'*')]), name="ct.VehicleCapacityStrong2")

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
           
            model.addConstrs((quicksum(q[r]*y[i, j,r] for r in R for j in [a[1] for a in Ay.select(i,'*',r)]) <= Qmin+vl[i] for i in P|D|TF), name="ct.VehicleCapacity")
           
        
    
        
        """
        Vehicle Flow Burger
        """
   
        
        model.addConstrs((bl[f"o{k}"]  == k+1 for k in K), name = "ct.route_startVehicleLabel")
        
        model.addConstrs((bl[f"e{k}"]  == k+1 for k in K), name = "ct.route_startVehicleLabel")
        
        if HET == False:
            if cutTrans==False:
        
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
        
    
                    
        
        
        

        
        """
        Request Transfer Time
        """
     
        #model.addConstrs((ti[i,j]+1>=(quicksum(y[j,i,r] for j in [a[0] for a in Ay.select('*',i,r)])-quicksum(y[i,j,r] for j in [a[1] for a in Ay.select(i,'*',r)]))+(quicksum(y[j,i,r] for i in [a[1] for a in Ay.select(j,'*',r)])-quicksum(y[i,j,r] for i in [a[0] for a in Ay.select('*',j,r)])) for r in R for i in TS for j in [a[1] for a in Ay.select(i,'*',r) if (a[0],a[1]) in TIy] ), name="transfer_indicator")

        #model.addConstrs((ti[i,j]>= y[i,j,r] for r in R for i in TS for j in [a[1] for a in Ay.select(i,'*',r) if (a[0],a[1]) in TIy] ), name="transfer_indicator")
    
        #model.addConstrs((z[i]+service_time[i] -Mt[i,j]*(1-ti[i,j])<= bz[j] for i in TS for j in [a[1] for a in Ay.select(i,'*',0) if (a[0],a[1]) in TIy]), name = "ct.transferTimeWait")
        
    
        """
        Transfer location open
        """
        model.addConstrs((1 >= x[i,j] for j in TS for i in [a[0] for a in A.select('*',j)]), name = "ct.TransferVITS")
    
        model.addConstrs((1 >= x[i,j] for i in TF for j in [a[1] for a in A.select(i,'*')]), name = "ct.TransferVITF")
    
    
        model.addConstrs((f[f"ts{n}"] >= quicksum(x[i,j] for j in [a[1] for a in A.select(i,'*')]) for n in TS_loc for i in TS_loc[n]), name = "ct.TransferFlowLink")
        model.addConstrs((f[f"ts{n}"] <= quicksum(y[i,j,r] for r in R for i in TS_loc[n] for j in [a[1] for a in Ay.select(i,'*',r) if a[1].replace("f","s")!=i]) for n in TS_loc), name = "ct.TransferRequestFlowLink")
        
        #model.addConstrs((f[f"ts{n}"] <= quicksum(y[i,j,r] for r in R for i in TS_loc[n] for j in [a[1] for a in Ay.select(i,'*',r) if a[1].replace("f","s")!=i]) for n in TS_loc), name = "ct.TransferRequestFlowLink")
        model.addConstrs((2*f[f"ts{n}"] <= quicksum(x[j,i] for i in TS_loc[n] for j in [a[0] for a in A.select('*',i)]) for n in TS_loc), name = "ct.AtLeastTwoVehicles")

    
        #model.addConstrs((quicksum(z[i,j] for j in [a[1] for a in A.select(i,'*')])-quicksum(z[j,i] for j in [a[0] for a in A.select('*',i)])== quicksum((c[i,j]+service_time[i])*x[i,j] for j in [a[1] for a in A.select(i,'*')])  for i in V-VD), name = "ct.time_flowA")

        
        #model1.addConstrs((bz[i]+c[i,j]-Mij[i,j]*(1-x[i,j])+(Mij[i,j]-c[i,j]+min(-c[j,i],timeWindows[j][0]-timeWindows[i][0]))*x[j,i]<= z[j] for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.time_flowLifted")
        #subtour constraints
        #model.addConstrs((1 >= x[i,j]+x[j,i] for i in V for j in V if (i,j) in A and (j,i) in A), name = "ct.ST_size2")

        """
        Time Windows
        """
        
        #model.addConstrs((z[i,j] >= (c[i,j]+service_time[i])*x[i,j] for (i,j) in A), name='ct.TimeLB')
        
        #model.addConstrs((z[i,j] <= (timeWindows[j][1])*x[i,j] for (i,j) in A), name='ct.TimeUB')
        
        #model.addConstr((quicksum((c[i,j]+service_time[i])*x[i,j] for (i,j) in A)<= int(df.b.max())*len(K)), name='ct.GlobalUB')
        
        if timeFlow==True:
               if VC>0:
                    model.addConstrs(
                       (
                           gp.quicksum(
                               z[i, j] + (c[i,j]+service_time[i]) * x[i, j]
                               for i in V-VD
                               if (i, j) in A
                           )
                           <= z.sum(j,"*")
                           for j in V-VO-VD
                       ),
                           name="ct.time_flowA",
                     )
                    #model.addConstrs((z.sum(i,"*")+service_time[i] -Mij[i,j]*(1-ti[i,j])<= z.sum(j,"*") for (i,j) in TIy), name = "ct.transferTimeWait")
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
                    model.addConstrs(
                       (
                           gp.quicksum(
                               z[i, j] + (c[i,j]+service_time[j]) * x[i, j]
                               for i in V-VD
                               if (i, j) in A
                           )
                           <= z.sum(j,"*")
                           for j in V-VO-VD
                       ),
                           name="ct.time_flowA",
                     )
                    
                    for tf in TFC:
                        r = int(tf.split(".")[1])
                        model.addConstr((z.sum(tf.replace("fc","sr"),"*")+service_time[tf.replace("fc","sr")]<= z.sum(j,"*")), name = "ct.transferTimeWait")
                    #model.addConstrs((z.sum(i,"*")+service_time[j] -Mij[i,j]*(1-ti[i,j])<= z.sum(j,"*") for i in TS for j in [a[1] for a in Ay.select(i,'*',0) if (a[0],a[1]) in TIy]), name = "ct.transferTimeWait")
                    """
                    Time Windows
                    """
                    model.addConstrs(
                    (
                        z[i, j] >= (timeWindows[i][0]) * x[i, j]
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
            if VC>0:
                model.addConstrs((z[i]+service_time[i]+c[i,j]-(Mij[i,j])*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A.select(i,'*')]), name = "ct.time_flowA")

                #super valid inequality
                #model.addConstrs((bz[i]+service_time[i]+t[i,j]-(Mij[i,j])*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) not in A), name = "ct.time_flowA")
                
                #model.addConstrs((bz[i]-z[j]+Mij[i,j]*x[i,j]+(Mij[i,j]-service_time[i]-t[i,j]+min(-t[j,i]-service_time[j],timeWindows[j][0]-timeWindows[i][1]))*x[j,i]<= Mij[i,j]-t[i,j]-service_time[i]  for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) in A), name = "ct.time_flowLifted")
                
                
                model.addConstrs((z[i]+0.01 <= z[i] for i in TS|TF), name='ct.DepartureA')
                """
                Time Windows
                """
                #model.addConstrs((min(max(timeWindows[f"e{k}"][1]-c[i,f"e{k}"] for k in K),timeWindows[i][1]) >= bz[i]-service_time[i] for i in V-VD), name="ct.TimeWindowLatest")
                model.addConstrs((timeWindows[i][1] >= z[i] for i in V), name="ct.TimeWindowLatestVD")
            
                #model.addConstrs((min([max(timeWindows[i][0],c[f"o{k}",i]) for k in K]) <= z[i] for i in V-VO), name="ct.timeWindowEarliestbVO")
                model.addConstrs((timeWindows[i][0] <= z[i] for i in V), name="ct.timeWindowEarliestb")
                
            else:
                model.addConstrs((z[i]+service_time[j]+c[i,j]-(Mij[i,j])*(1-x[i,j])<= z[j] for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) not in A), name = "ct.time_flowA")
                
                model.addConstrs((z[i]-z[j]+Mij[i,j]*x[i,j]+(Mij[i,j]-service_time[j]-c[i,j]+min(-c[j,i]-service_time[i],timeWindows[j][0]-timeWindows[i][1]))*x[j,i]<= Mij[i,j]-c[i,j]-service_time[j]  for i in V for j in [a[1] for a in A.select(i,'*')] if (j,i) in A), name = "ct.time_flowLifted")
                
                
                for tf in TFC:
                    r = int(tf.split(".")[1])
                    model.addConstr((z[tf.replace("fc","sr")] +service_time[tf.replace("fc","sr")]<= z[tf]), name = "ct.transferTimeWait")
                """
                Time Windows
                """
                #model.addConstrs((min(max(timeWindows[f"e{k}"][1]-c[i,f"e{k}"] for k in K),timeWindows[i][1]) >= bz[i]-service_time[i] for i in V-VD), name="ct.TimeWindowLatest")
                model.addConstrs((timeWindows[i][1] >= z[i]-service_time[i] for i in V-VO-VD), name="ct.TimeWindowLatestVD")
                model.addConstrs((timeWindows[i][1] >= z[i] for i in VO|VD), name="ct.TimeWindowLatestVD")

            
                #model.addConstrs((min([max(timeWindows[i][0],c[f"o{k}",i]) for k in K]) <= z[i] for i in V-VO), name="ct.timeWindowEarliestbVO")
                model.addConstrs((timeWindows[i][0] <= z[i]-service_time[i] for i in V-VO-VD), name="ct.timeWindowEarliestb")
                model.addConstrs((timeWindows[i][0] <= z[i] for i in VO|VD), name="ct.timeWindowEarliestb")

        """
        for idx,cut in enumerate([({'ts.1.0', 'd14', 'ts.0.2', 'p10', 'd12', 'p19', 'tf.0.0', 'tf.0.2'}, frozenset({'p1', 'd0', 'd18', 'd10', 'p15', 'p16', 'd15', 'd4', 'd7', 'p5', 'p13', 'd1', 'p3', 'p14', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd19', 'd6', 'p17', 'd3', 'p7', 'p11', 'd5', 'd8', 'd16', 'd2', 'd17', 'p8', 'p0', 'd13', 'p6'}), 'ts.0.0', 0), ({'ts.1.0', 'd14', 'ts.0.2', 'p10', 'd19', 'd12', 'p19', 'tf.0.0', 'tf.0.2'}, frozenset({'p1', 'd0', 'd18', 'd10', 'p15', 'p16', 'd15', 'd4', 'd7', 'p5', 'p13', 'd1', 'p3', 'p14', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd6', 'p17', 'd3', 'p7', 'p11', 'd5', 'd8', 'd16', 'd2', 'd17', 'p8', 'p0', 'd13', 'p6'}), 'ts.0.0', 0), ({'d14', 'ts.1.2', 'tf.1.2', 'ts.2.2', 'tf.2.2', 'd8', 'p10', 'tf.1.0', 'd19', 'p8', 'd12', 'ts.0.0', 'p19', 'd15'}, frozenset({'d18', 'p1', 'd0', 'd10', 'p15', 'p16', 'd4', 'd7', 'p5', 'p13', 'd1', 'p3', 'p14', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd6', 'p17', 'd3', 'p7', 'p11', 'd5', 'd16', 'd2', 'd17', 'p0', 'd13', 'p6'}), 'ts.1.0', 0), ({'p7', 'd16', 'p18', 'tf.1.0', 'd17', 'p17', 'd10', 'ts.0.0', 'd7'}, frozenset({'d14', 'p1', 'd0', 'd18', 'd12', 'p15', 'p16', 'd15', 'd4', 'p5', 'p13', 'd1', 'p3', 'p10', 'p14', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd19', 'd6', 'p19', 'd3', 'p11', 'd5', 'd8', 'd2', 'p8', 'p0', 'd13', 'p6'}), 'ts.1.0', 0), ({'d14', 'ts.1.2', 'tf.1.2', 'p10', 'tf.2.0', 'd19', 'd12', 'ts.0.0', 'p19'}, frozenset({'p1', 'd0', 'd18', 'd10', 'p15', 'p16', 'd15', 'd4', 'd7', 'p5', 'p13', 'd1', 'p3', 'p14', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd6', 'p17', 'd3', 'p7', 'p11', 'd5', 'd8', 'd16', 'd2', 'd17', 'p8', 'p0', 'd13', 'p6'}), 'ts.2.0', 0), ({'ts.2.2', 'd8', 'p8', 'd15', 'tf.0.2'}, frozenset({'d14', 'p1', 'd0', 'd18', 'd12', 'd10', 'p15', 'p16', 'd4', 'd7', 'p5', 'p13', 'd1', 'p3', 'p10', 'p14', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd19', 'd6', 'p17', 'p19', 'd3', 'p7', 'p11', 'd5', 'd16', 'd2', 'd17', 'p0', 'd13', 'p6'}), 'ts.0.2', 2), ({'d14', 'ts.0.2', 'p10', 'tf.1.0', 'd19', 'd12', 'ts.0.0', 'p19', 'tf.0.2'}, frozenset({'p1', 'd0', 'd18', 'd10', 'p15', 'p16', 'd15', 'd4', 'd7', 'p5', 'p13', 'd1', 'p3', 'p14', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd6', 'p17', 'd3', 'p7', 'p11', 'd5', 'd8', 'd16', 'd2', 'd17', 'p8', 'p0', 'd13', 'p6'}), 'ts.1.0', 0), ({'ts.0.2', 'tf.1.2', 'd8', 'p8', 'd15'}, frozenset({'d14', 'p1', 'd0', 'd18', 'd12', 'd10', 'p15', 'p16', 'd4', 'd7', 'p5', 'p13', 'd1', 'p3', 'p10', 'p14', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd19', 'd6', 'p17', 'p19', 'd3', 'p7', 'p11', 'd5', 'd16', 'd2', 'd17', 'p0', 'd13', 'p6'}), 'ts.1.2', 2), ({'ts.1.0', 'p7', 'd16', 'p18', 'd10', 'tf.0.0', 'd7'}, frozenset({'d14', 'p1', 'd0', 'd18', 'd12', 'p15', 'p16', 'd15', 'd4', 'p5', 'p13', 'd1', 'p3', 'p10', 'p14', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd19', 'd6', 'p17', 'p19', 'd3', 'p11', 'd5', 'd8', 'd2', 'd17', 'p8', 'p0', 'd13', 'p6'}), 'ts.0.0', 0), ({'d14', 'ts.0.2', 'ts.2.2', 'tf.2.2', 'd8', 'p10', 'tf.2.0', 'd19', 'p8', 'd12', 'ts.0.0', 'p19', 'd15', 'tf.0.2'}, frozenset({'d18', 'p1', 'd0', 'd10', 'p15', 'p16', 'd4', 'd7', 'p5', 'p13', 'd1', 'p3', 'p14', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd6', 'p17', 'd3', 'p7', 'p11', 'd5', 'd16', 'd2', 'd17', 'p0', 'd13', 'p6'}), 'ts.2.0', 0), ({'p13', 'd0', 'p3', 'p14', 'tf.2.0', 'p0', 'd13', 'd3', 'ts.0.0', 'p16'}, frozenset({'d14', 'd18', 'p1', 'd12', 'd10', 'p15', 'd4', 'd15', 'd7', 'p5', 'd1', 'p10', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd19', 'd6', 'p17', 'p19', 'p7', 'p11', 'd5', 'd8', 'd16', 'd2', 'd17', 'p8', 'p6'}), 'ts.2.0', 0), ({'d14', 'ts.2.2', 'tf.2.2', 'p10', 'tf.1.0', 'd19', 'ts.2.0', 'd12', 'p19'}, frozenset({'p1', 'd0', 'd18', 'd10', 'p15', 'p16', 'd15', 'd4', 'd7', 'p5', 'p13', 'd1', 'p3', 'p14', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd6', 'p17', 'd3', 'p7', 'p11', 'd5', 'd8', 'd16', 'd2', 'd17', 'p8', 'p0', 'd13', 'p6'}), 'ts.1.0', 0), ({'ts.1.0', 'd14', 'ts.1.2', 'tf.1.2', 'p10', 'd12', 'p19', 'tf.0.0'}, frozenset({'p1', 'd0', 'd18', 'd10', 'p15', 'p16', 'd15', 'd4', 'd7', 'p5', 'p13', 'd1', 'p3', 'p14', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd19', 'd6', 'p17', 'd3', 'p7', 'p11', 'd5', 'd8', 'd16', 'd2', 'd17', 'p8', 'p0', 'd13', 'p6'}), 'ts.0.0', 0), ({'p13', 'd0', 'p3', 'p14', 'ts.2.0', 'p0', 'd13', 'd3', 'tf.0.0', 'p16'}, frozenset({'d14', 'd18', 'p1', 'd12', 'd10', 'p15', 'd4', 'd15', 'd7', 'p5', 'd1', 'p10', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd19', 'd6', 'p17', 'p19', 'p7', 'p11', 'd5', 'd8', 'd16', 'd2', 'd17', 'p8', 'p6'}), 'ts.0.0', 0), ({'d14', 'ts.1.2', 'tf.1.2', 'p10', 'ts.2.0', 'd19', 'd12', 'p19', 'tf.0.0'}, frozenset({'p1', 'd0', 'd18', 'd10', 'p15', 'p16', 'd15', 'd4', 'd7', 'p5', 'p13', 'd1', 'p3', 'p14', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd6', 'p17', 'd3', 'p7', 'p11', 'd5', 'd8', 'd16', 'd2', 'd17', 'p8', 'p0', 'd13', 'p6'}), 'ts.0.0', 0), ({'d0', 'd18', 'ts.2.0', 'd3', 'tf.0.0', 'p16', 'p13', 'p11', 'p3', 'p14', 'd2', 'p18', 'p2', 'p0', 'd13', 'd11'}, frozenset({'d14', 'p1', 'd12', 'd10', 'p15', 'd4', 'd15', 'd7', 'p5', 'd1', 'p10', 'p4', 'd9', 'p12', 'p9', 'd19', 'd6', 'p17', 'p19', 'p7', 'd5', 'd8', 'd16', 'd17', 'p8', 'p6'}), 'ts.0.0', 0), ({'p7', 'd16', 'p18', 'tf.1.0', 'ts.0.0', 'd10', 'd7'}, frozenset({'d14', 'p1', 'd0', 'd18', 'd12', 'p15', 'p16', 'd15', 'd4', 'p5', 'p13', 'd1', 'p3', 'p10', 'p14', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd19', 'd6', 'p17', 'p19', 'd3', 'p11', 'd5', 'd8', 'd2', 'd17', 'p8', 'p0', 'd13', 'p6'}), 'ts.1.0', 0), ({'d14', 'ts.2.2', 'tf.2.2', 'p10', 'tf.2.0', 'd19', 'd12', 'ts.0.0', 'p19'}, frozenset({'p1', 'd0', 'd18', 'd10', 'p15', 'p16', 'd15', 'd4', 'd7', 'p5', 'p13', 'd1', 'p3', 'p14', 'p18', 'p4', 'p2', 'd11', 'd9', 'p12', 'p9', 'd6', 'p17', 'd3', 'p7', 'p11', 'd5', 'd8', 'd16', 'd2', 'd17', 'p8', 'p0', 'd13', 'p6'}), 'ts.2.0', 0)]):
            S_comp,S,source,transfer_idx = cut[0],cut[1], cut[2],cut[3]
            model.addConstr(quicksum(x[j,source] for j in S_comp if (j,source) in A)+
            quicksum(x[i,j] for i in S_comp for j in S if (i,j) in A)+
            quicksum(x[source.replace("s","f"),j] for j in S if (source.replace("s","f"),j) in A)
            >= f[f"ts{transfer_idx}"], name=f"ctCut_{idx}")
            
        """
        """
        for route in  [[('o2', 'ts.2.0'), ('ts.2.0', 'tf.2.0'), ('tf.2.0', 'ts.2.1'), ('ts.2.1', 'tf.2.1'), ('tf.2.1', 'd3'), ('d3', 'd2'), ('d2', 'e2')],
        [('o0', 'p1'), ('p1', 'p4'), ('p4', 'p0'), ('p0', 'ts.0.0'), ('ts.0.0', 'tf.0.0'), ('tf.0.0', 'e0')],
        [('o3', 'p3'), ('p3', 'ts.3.0'), ('ts.3.0', 'tf.3.0'), ('tf.3.0', 'd0'), ('d0', 'd4'), ('d4', 'd1'), ('d1', 'e3')],
        [('o1', 'p2'), ('p2', 'ts.1.1'), ('ts.1.1', 'tf.1.1'), ('tf.1.1', 'e1')]]:
            for e in route:
                model.addConstr(x[e]==1)"""
        
        """
        
        for idx,cut in enumerate([({'p13', 'tf.0.0', 'd2', 'ts.0.0', 'o1', 'p0', 'd8', 'p9', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'tf.1.0', 'd10', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'd16', 'p18', 'p2', 'p6', 'd4', 'd1', 'd18', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'p10', 'd9', 'ts.1.0', 'tf.1.2', 'o0', 'p5'}, {'ts.2.2', 'tf.2.2', 'p15', 'd19', 'p8', 'ts.0.1', 'd11', 'tf.2.1', 'p4', 'd7', 'd0', 'ts.2.1', 'p11', 'tf.0.1', 'p19', 'tf.1.1', 'p7', 'ts.1.1'}, ('p15',)), ({'d2', 'ts.0.0', 'o1', 'd8', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd5', 'p3', 'o2', 'p16', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'd16', 'ts.0.1', 'p6', 'd1', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'p10', 'ts.1.0', 'tf.1.2', 'o0', 'p5'}, {'p13', 'ts.2.2', 'tf.2.2', 'p15', 'd19', 'p0', 'p8', 'p18', 'p2', 'p9', 'd11', 'p4', 'd7', 'd0', 'p11', 'd15', 'd13', 'p19', 'd9', 'd18', 'p7'}, ('p4',)), ({'p13', 'ts.2.0', 'd2', 'ts.0.0', 'd13', 'd8', 'p9', 'd4', 'ts.1.0'}, {'ts.2.2', 'tf.2.2', 'd19', 'p0', 'p8', 'p4', 'ts.1.2', 'd3', 'p11', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'p14', 'p3', 'p16', 'target', 'd10', 'ts.1.1', 'p17', 'tf.0.2', 'd6', 'p1', 'p15', 'd16', 'e0', 'p18', 'ts.0.1', 'p6', 'd11', 'd1', 'tf.2.1', 'd7', 'd0', 'ts.2.1', 'p12', 'd17', 'e1', 'd15', 'tf.0.1', 'p10', 'd9', 'tf.1.1', 'p19', 'd18', 'tf.1.2', 'p7', 'p5'}, ('d2',)), ({'p13', 'd2', 'o1', 'd8', 'p9', 'ts.1.2', 'ts.0.2', 'd3', 'd5', 'd13', 'p3', 'o2', 'p16', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'd6', 'd16', 'ts.0.1', 'p6', 'd4', 'tf.2.1', 'ts.2.1', 'ts.2.0', 'd17', 'tf.2.0', 'tf.0.1', 'p10', 'd9', 'tf.1.1', 'tf.1.2', 'o0', 'p5'}, {'tf.0.0', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'ts.1.0', 'p15', 'p1', 'd19', 'p8', 'p0', 'p18', 'p2', 'd1', 'p4', 'd7', 'd0', 'p12', 'p11', 'd12', 'd15', 'p14', 'tf.1.0', 'd14', 'p19', 'd18', 'p7'}, ('p11',)), ({'p15', 'd11', 'ts.1.0', 'p7', 'd7'}, {'p13', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'p14', 'p3', 'p16', 'd13', 'target', 'd10', 'ts.1.1', 'p17', 'tf.0.2', 'd6', 'p1', 'd16', 'e0', 'ts.0.1', 'p18', 'p6', 'p2', 'd4', 'd1', 'tf.2.1', 'ts.2.1', 'd0', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'e1', 'd15', 'tf.0.1', 'p10', 'd9', 'tf.1.1', 'p19', 'd18', 'tf.1.2', 'p5'}, ('d11',)), ({'p13', 'd18', 'tf.0.0', 'ts.0.0', 'd13', 'd8', 'p18', 'p2', 'p9', 'd4', 'd9', 'ts.1.0', 'd0'}, {'d2', 'ts.2.2', 'tf.2.2', 'd19', 'p8', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'p11', 'e2', 'd12', 'd5', 'd14', 'p14', 'p3', 'p16', 'target', 'd10', 'ts.1.1', 'p17', 'tf.0.2', 'd6', 'p1', 'p15', 'd16', 'e0', 'ts.0.1', 'p6', 'd11', 'd1', 'tf.2.1', 'd7', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'e1', 'd15', 'tf.0.1', 'p10', 'p19', 'tf.1.1', 'tf.1.2', 'p7', 'p5'}, ('d0',)), ({'ts.2.2', 'ts.0.0', 'tf.2.2', 'ts.0.1', 'ts.2.1', 'p19', 'd11', 'p7', 'ts.1.1', 'd7'}, {'p13', 'd2', 'd19', 'p8', 'p0', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'tf.1.0', 'd13', 'p3', 'p16', 'd14', 'p14', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'ts.1.0', 'p1', 'p15', 'd16', 'e0', 'p18', 'p2', 'p6', 'd4', 'd1', 'd0', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'e1', 'd15', 'p10', 'd9', 'd18', 'tf.1.2', 'p5'}, ('d11',)), ({'p13', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'o1', 'p0', 'd8', 'p9', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd1', 'd4', 'tf.2.1', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'tf.0.1', 'd9', 'p10', 'd18', 'tf.1.2', 'o0', 'p5'}, {'p11', 'p15', 'd19', 'ts.1.1', 'p8', 'p19', 'tf.1.1', 'd11', 'p4', 'p7', 'd7', 'd0'}, ('p15',)), ({'p13', 'ts.2.2', 'd2', 'tf.2.2', 'ts.0.0', 'o1', 'p0', 'd8', 'p9', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'tf.1.0', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'ts.1.0', 'd6', 'd16', 'p18', 'p2', 'p6', 'd1', 'd4', 'tf.2.1', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'd15', 'd9', 'p10', 'tf.1.1', 'd18', 'o0', 'p5'}, {'ts.1.2', 'p11', 'p15', 'p8', 'tf.0.1', 'ts.0.1', 'p19', 'd11', 'p4', 'tf.1.2', 'p7', 'd7', 'd0'}, ('p19',)), ({'tf.0.0', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'o1', 'd19', 'p0', 'p8', 'p4', 'ts.1.2', 'ts.0.2', 'p11', 'd3', 'd12', 'p14', 'd14', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'p15', 'd6', 'ts.1.0', 'd16', 'ts.0.1', 'p6', 'd11', 'd1', 'tf.2.1', 'ts.2.1', 'd0', 'd7', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'd15', 'tf.0.1', 'p19', 'p10', 'd9', 'd18', 'tf.1.2', 'o0', 'p7', 'p5'}, {'p13', 'p18', 'p2', 'd8', 'p9', 'd4', 'd13'}, ('p2',)), ({'tf.0.0', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'o1', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd1', 'tf.2.1', 'd18', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'tf.0.1', 'p10', 'ts.1.0', 'o0', 'p5'}, {'p13', 'd2', 'p15', 'd19', 'p8', 'p0', 'd8', 'p9', 'd4', 'd11', 'p4', 'd7', 'd0', 'p11', 'd15', 'ts.1.1', 'p19', 'tf.1.1', 'p7'}, ('p9',)), ({'p13', 'd2', 'ts.0.0', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'p11', 'd13', 'ts.1.1', 'p15', 'p18', 'p2', 'ts.0.1', 'd11', 'd4', 'd18', 'd7', 'd0', 'ts.2.1', 'ts.2.0', 'd15', 'd9', 'ts.1.0', 'p7'}, {'p17', 'ts.2.2', 'tf.2.2', 'tf.0.2', 'd6', 'p1', 'd16', 'e0', 'p6', 'd1', 'ts.1.2', 'p12', 'd3', 'ts.0.2', 'd17', 'e1', 'e2', 'd12', 'd5', 'd14', 'p14', 'p3', 'p16', 'p10', 'target', 'd10', 'tf.1.2', 'p5'}, ('d19',)), ({'p12', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'p1', 'ts.2.0', 'd17', 'd12', 'p14', 'd14', 'ts.0.1', 'd1', 'ts.1.0'}, {'p13', 'd19', 'p8', 'p0', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'p11', 'e2', 'd5', 'd13', 'p16', 'p3', 'target', 'd10', 'ts.1.1', 'p17', 'tf.0.2', 'd6', 'p15', 'd16', 'e0', 'p18', 'p6', 'd11', 'd4', 'tf.2.1', 'd7', 'ts.2.1', 'd0', 'e1', 'd15', 'p10', 'd9', 'tf.1.1', 'p19', 'd18', 'tf.1.2', 'p7', 'p5'}, ('d2',)), ({'p13', 'd2', 'ts.2.2', 'tf.2.2', 'ts.0.0', 'o1', 'p0', 'd8', 'p9', 'p4', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'tf.1.0', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd1', 'd4', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'p10', 'd9', 'd18', 'o0', 'p5'}, {'ts.1.2', 'p11', 'p15', 'd19', 'p8', 'p19', 'd11', 'tf.1.2', 'p7', 'd7', 'd0'}, ('p15',)), ({'p13', 'ts.2.2', 'd2', 'tf.2.2', 'ts.0.0', 'o1', 'p0', 'd8', 'p9', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'p18', 'p2', 'p6', 'd1', 'd4', 'tf.2.1', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'd9', 'p10', 'tf.1.1', 'd18', 'tf.1.2', 'o0', 'p5'}, {'p11', 'p15', 'd19', 'p8', 'tf.0.1', 'ts.0.1', 'p19', 'd11', 'p4', 'p7', 'd7', 'd0'}, ('p15',)), ({'ts.2.0', 'ts.0.0', 'd11', 'ts.1.0', 'p7', 'd7'}, {'p13', 'd2', 'ts.2.2', 'tf.2.2', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'p14', 'p3', 'p16', 'd13', 'target', 'd10', 'ts.1.1', 'p17', 'tf.0.2', 'd6', 'p1', 'p15', 'd16', 'e0', 'p18', 'ts.0.1', 'p6', 'p2', 'd4', 'd1', 'tf.2.1', 'ts.2.1', 'd0', 'p12', 'd17', 'e1', 'd15', 'tf.0.1', 'p10', 'd9', 'p19', 'tf.1.1', 'd18', 'tf.1.2', 'p5'}, ('d11',)), ({'p13', 'tf.0.0', 'ts.2.2', 'd2', 'ts.0.0', 'tf.2.2', 'o1', 'p0', 'd8', 'p9', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'ts.0.1', 'p18', 'p6', 'p2', 'd1', 'd4', 'tf.2.1', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'tf.0.1', 'd9', 'p10', 'tf.1.1', 'd18', 'o0', 'p5'}, {'ts.1.2', 'p11', 'p15', 'd19', 'p8', 'p19', 'd11', 'p4', 'tf.1.2', 'p7', 'd7', 'd0'}, ('p15',)), ({'p13', 'ts.2.2', 'd2', 'tf.2.2', 'ts.0.0', 'o1', 'p0', 'd8', 'p9', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'tf.1.0', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd1', 'd4', 'tf.2.1', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'tf.0.1', 'd9', 'p10', 'tf.1.1', 'd18', 'o0', 'p5'}, {'ts.1.2', 'p11', 'p15', 'd19', 'p8', 'p19', 'd11', 'p4', 'tf.1.2', 'p7', 'd7', 'd0'}, ('p15',)), ({'p13', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'o1', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'p18', 'p2', 'p6', 'd1', 'd4', 'tf.2.1', 'ts.2.1', 'd0', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'p10', 'd9', 'd18', 'o0', 'p5'}, {'p11', 'p15', 'd19', 'ts.1.1', 'tf.0.1', 'ts.0.1', 'p19', 'tf.1.1', 'd11', 'p7', 'd7'}, ('p15',)), ({'ts.2.2', 'tf.2.2', 'o1', 'd19', 'p0', 'p8', 'p4', 'ts.1.2', 'ts.0.2', 'p11', 'd3', 'd12', 'p14', 'd14', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'p15', 'd6', 'ts.1.0', 'd16', 'ts.0.1', 'p6', 'd11', 'd1', 'tf.2.1', 'd7', 'd0', 'ts.2.1', 'p12', 'd17', 'd15', 'tf.0.1', 'p19', 'd9', 'p10', 'tf.1.1', 'd18', 'tf.1.2', 'o0', 'p7', 'p5'}, {'p13', 'tf.0.0', 'ts.2.0', 'ts.0.0', 'tf.2.0', 'd13', 'p18', 'p2', 'd8', 'p9', 'd4'}, ('p2',)), ({'p7', 'd11', 'd7', 'ts.1.0'}, {'p13', 'tf.0.0', 'd2', 'ts.2.2', 'tf.2.2', 'ts.0.0', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'd13', 'p3', 'p16', 'p14', 'target', 'd10', 'ts.1.1', 'p17', 'tf.0.2', 'd6', 'p1', 'p15', 'd16', 'e0', 'p18', 'p2', 'p6', 'ts.0.1', 'd4', 'd1', 'tf.2.1', 'ts.2.1', 'd0', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'e1', 'd15', 'tf.0.1', 'p10', 'd9', 'tf.1.1', 'p19', 'd18', 'tf.1.2', 'p5'}, ('d11',)), ({'p12', 'd2', 'd17', 'p1', 'd12', 'p14', 'd14', 'd1', 'ts.1.0', 'ts.1.1'}, {'p13', 'tf.0.0', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'd19', 'p8', 'p0', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'p11', 'e2', 'd5', 'd13', 'p3', 'p16', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p15', 'd16', 'e0', 'p18', 'ts.0.1', 'p6', 'd11', 'd4', 'tf.2.1', 'd7', 'ts.2.1', 'd0', 'ts.2.0', 'tf.2.0', 'e1', 'd15', 'tf.0.1', 'p10', 'd9', 'p19', 'd18', 'tf.1.2', 'p7', 'p5'}, ('d2',)), ({'p12', 'd2', 'd17', 'p1', 'd12', 'p14', 'tf.1.0', 'd14', 'd1', 'ts.1.0'}, {'p13', 'tf.0.0', 'ts.2.2', 'tf.2.2', 'ts.0.0', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'p11', 'e2', 'd5', 'd13', 'p3', 'p16', 'target', 'd10', 'ts.1.1', 'p17', 'tf.0.2', 'd6', 'p15', 'd16', 'e0', 'p18', 'ts.0.1', 'p6', 'd4', 'd11', 'tf.2.1', 'd7', 'd0', 'ts.2.1', 'ts.2.0', 'tf.2.0', 'e1', 'd15', 'tf.0.1', 'p10', 'd9', 'p19', 'tf.1.1', 'd18', 'tf.1.2', 'p7', 'p5'}, ('d2',)), ({'ts.2.2', 'tf.2.2', 'o1', 'd19', 'p0', 'p8', 'p4', 'ts.1.2', 'ts.0.2', 'p11', 'd3', 'd12', 'p14', 'd14', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'p15', 'd6', 'ts.1.0', 'd16', 'p6', 'ts.0.1', 'd11', 'd1', 'tf.2.1', 'ts.2.1', 'd0', 'd7', 'p12', 'd17', 'd15', 'tf.0.1', 'p19', 'd9', 'p10', 'd18', 'tf.1.2', 'o0', 'p7', 'p5'}, {'p13', 'tf.0.0', 'ts.2.0', 'ts.0.0', 'tf.2.0', 'd13', 'p18', 'p2', 'd8', 'p9', 'd4'}, ('p2',)), ({'p13', 'tf.0.0', 'ts.2.2', 'd2', 'ts.0.0', 'tf.2.2', 'o1', 'd19', 'p0', 'd8', 'p9', 'p4', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd4', 'd1', 'tf.2.1', 'd0', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'd15', 'tf.0.1', 'd9', 'p10', 'd18', 'tf.1.2', 'o0', 'p5'}, {'p19', 'p11', 'p15', 'p7', 'd7', 'p8'}, ('p11',)), ({'ts.2.2', 'tf.2.2', 'o1', 'd19', 'p0', 'p8', 'p4', 'ts.1.2', 'ts.0.2', 'p11', 'd3', 'd12', 'p14', 'd14', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'p15', 'd6', 'ts.1.0', 'd16', 'p6', 'ts.0.1', 'd11', 'd1', 'tf.2.1', 'd7', 'd0', 'ts.2.1', 'p12', 'd17', 'd15', 'tf.0.1', 'p19', 'd9', 'p10', 'd18', 'tf.1.2', 'o0', 'p7', 'p5'}, {'p13', 'tf.0.0', 'ts.2.0', 'ts.0.0', 'tf.2.0', 'd13', 'p18', 'p2', 'd8', 'p9', 'd4'}, ('p2',)), ({'p13', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'o1', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd4', 'd1', 'tf.2.1', 'ts.2.1', 'd0', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'd15', 'tf.0.1', 'p10', 'd9', 'tf.1.1', 'd18', 'tf.1.2', 'o0', 'p5'}, {'p19', 'p11', 'p15', 'p7', 'd7'}, ('p11',)), ({'ts.1.2', 'ts.2.0', 'p11', 'ts.0.0', 'd19', 'd15', 'ts.0.1', 'ts.2.1', 'd11', 'p7', 'ts.1.0', 'ts.1.1', 'd7'}, {'p13', 'd2', 'ts.2.2', 'tf.2.2', 'p8', 'p0', 'd8', 'p9', 'p4', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'd13', 'p3', 'p16', 'p14', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p15', 'p1', 'd16', 'e0', 'p18', 'p2', 'p6', 'd4', 'd1', 'd0', 'p12', 'd17', 'e1', 'p10', 'd9', 'd18', 'p5'}, ('d19',)), ({'ts.1.2', 'ts.2.0', 'p11', 'ts.0.0', 'd19', 'd15', 'ts.0.1', 'ts.2.1', 'd11', 'p7', 'ts.1.0', 'ts.1.1', 'd7'}, {'p13', 'd2', 'ts.2.2', 'tf.2.2', 'p8', 'p0', 'd8', 'p9', 'p4', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'd13', 'p3', 'p16', 'p14', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p15', 'p1', 'd16', 'e0', 'p18', 'p2', 'p6', 'd4', 'd1', 'd0', 'p12', 'd17', 'e1', 'p10', 'd9', 'd18', 'p5'}, ('d19',)), ({'p13', 'tf.0.0', 'd2', 'ts.0.0', 'o1', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'ts.0.2', 'p11', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'p15', 'd6', 'ts.1.0', 'p18', 'p2', 'p6', 'ts.0.1', 'd11', 'd1', 'd4', 'tf.2.1', 'ts.2.1', 'd0', 'd7', 'ts.2.0', 'p12', 'd17', 'tf.2.0', 'd15', 'tf.0.1', 'p19', 'p10', 'd9', 'd18', 'tf.1.2', 'o0', 'p7'}, {'tf.2.2', 'ts.2.2', 'd16', 'p5'}, ('p5',)), ({'p13', 'tf.0.0', 'ts.2.2', 'd2', 'ts.0.0', 'tf.2.2', 'o1', 'p0', 'd8', 'p9', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd1', 'd4', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'tf.0.1', 'd9', 'p10', 'tf.1.1', 'd18', 'tf.1.2', 'o0', 'p5'}, {'p11', 'p15', 'd19', 'p8', 'ts.2.1', 'p19', 'd11', 'tf.2.1', 'p4', 'p7', 'd7', 'd0'}, ('p15',)), ({'p13', 'tf.0.0', 'ts.2.2', 'd2', 'ts.0.0', 'tf.2.2', 'o1', 'p0', 'd8', 'p9', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd1', 'd4', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'd15', 'tf.0.1', 'd9', 'p10', 'tf.1.1', 'd18', 'tf.1.2', 'o0', 'p5'}, {'p11', 'p15', 'p8', 'ts.2.1', 'p19', 'd11', 'tf.2.1', 'p4', 'p7', 'd7', 'd0'}, ('p19',)), ({'ts.2.2', 'tf.2.2', 'o1', 'd19', 'p0', 'p8', 'p4', 'ts.1.2', 'ts.0.2', 'p11', 'd3', 'd12', 'p14', 'd14', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'p15', 'd6', 'ts.1.0', 'd16', 'p6', 'ts.0.1', 'd11', 'd1', 'tf.2.1', 'd7', 'ts.2.1', 'd0', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'd15', 'tf.0.1', 'p19', 'd9', 'p10', 'd18', 'tf.1.2', 'o0', 'p7', 'p5'}, {'p13', 'tf.0.0', 'ts.0.0', 'd13', 'p18', 'p2', 'd8', 'p9', 'd4'}, ('p2',)), ({'d15', 'p11', 'ts.1.0'}, {'p13', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'd13', 'p3', 'p16', 'p14', 'target', 'd10', 'ts.1.1', 'p17', 'tf.0.2', 'd6', 'p1', 'd16', 'e0', 'p18', 'p2', 'p6', 'ts.0.1', 'd4', 'd1', 'd11', 'tf.2.1', 'd7', 'd0', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'e1', 'tf.0.1', 'p10', 'd9', 'tf.1.1', 'p19', 'd18', 'tf.1.2', 'p7', 'p5'}, ('d15',)), ({'p13', 'ts.2.0', 'tf.2.0', 'd13', 'd8', 'p18', 'p2', 'p9', 'd4', 'd9', 'd18', 'd0'}, {'tf.0.0', 'ts.2.2', 'd2', 'tf.2.2', 'ts.0.0', 'd19', 'p8', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'p11', 'e2', 'd12', 'd5', 'tf.1.0', 'd14', 'p3', 'p16', 'p14', 'target', 'd10', 'ts.1.1', 'p17', 'tf.0.2', 'd6', 'p1', 'p15', 'd16', 'e0', 'ts.0.1', 'p6', 'd11', 'd1', 'tf.2.1', 'd7', 'ts.2.1', 'p12', 'd17', 'e1', 'd15', 'tf.0.1', 'p10', 'p19', 'tf.1.1', 'ts.1.0', 'tf.1.2', 'p7', 'p5'}, ('d0',)), ({'tf.0.0', 'ts.0.0', 'o1', 'p0', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'd16', 'p18', 'p2', 'p6', 'd1', 'd18', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'p10', 'd9', 'ts.1.0', 'tf.1.2', 'o0', 'p5'}, {'p13', 'ts.2.2', 'd2', 'tf.2.2', 'p15', 'd19', 'p8', 'ts.0.1', 'd8', 'p9', 'd11', 'd4', 'tf.2.1', 'p4', 'd7', 'ts.2.1', 'd0', 'p11', 'tf.0.1', 'p19', 'p7'}, ('p15',)), ({'ts.2.2', 'tf.2.2', 'o1', 'd19', 'p0', 'p8', 'p4', 'ts.1.2', 'ts.0.2', 'p11', 'd3', 'd12', 'p14', 'd14', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'p15', 'd6', 'ts.1.0', 'd16', 'ts.0.1', 'p6', 'd11', 'd1', 'tf.2.1', 'ts.2.1', 'd7', 'd0', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'd15', 'tf.0.1', 'p19', 'd9', 'p10', 'd18', 'tf.1.2', 'o0', 'p7', 'p5'}, {'p13', 'tf.0.0', 'ts.0.0', 'd13', 'p18', 'p2', 'd8', 'p9', 'd4'}, ('p2',)), ({'ts.2.0', 'ts.0.0', 'p15', 'tf.0.1', 'ts.0.1', 'tf.1.1', 'd11', 'p7', 'ts.1.0', 'ts.1.1', 'd7'}, {'p13', 'd2', 'ts.2.2', 'tf.2.2', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'd13', 'p3', 'p16', 'p14', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p1', 'd16', 'e0', 'p18', 'p2', 'p6', 'd4', 'd1', 'tf.2.1', 'ts.2.1', 'd0', 'p12', 'd17', 'e1', 'd15', 'p10', 'd9', 'p19', 'd18', 'tf.1.2', 'p5'}, ('d11',)), ({'ts.1.2', 'ts.2.2', 'd17', 'tf.2.2', 'd16', 'ts.1.0', 'ts.1.1', 'p5'}, {'p13', 'tf.0.0', 'd2', 'ts.0.0', 'd19', 'p8', 'p0', 'd8', 'p9', 'p4', 'd3', 'ts.0.2', 'p11', 'e2', 'd12', 'd5', 'd14', 'd13', 'p3', 'p16', 'p14', 'target', 'd10', 'tf.0.2', 'd6', 'p15', 'p1', 'e0', 'p18', 'p2', 'p6', 'ts.0.1', 'd4', 'd11', 'tf.2.1', 'd1', 'd7', 'd0', 'ts.2.1', 'p12', 'ts.2.0', 'tf.2.0', 'e1', 'd15', 'tf.0.1', 'p10', 'd9', 'p19', 'd18', 'p7'}, ('d17',)), ({'tf.0.0', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'o1', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd1', 'd18', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'tf.0.1', 'p10', 'ts.1.0', 'tf.1.2', 'o0', 'p5'}, {'p13', 'd2', 'p15', 'd19', 'p8', 'p0', 'd8', 'p9', 'd4', 'd11', 'tf.2.1', 'p4', 'd7', 'd0', 'ts.2.1', 'p11', 'd15', 'p19', 'p7'}, ('p9',)), ({'ts.2.2', 'tf.2.2', 'o1', 'd3', 'ts.0.2', 'd5', 'p3', 'o2', 'p16', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'd6', 'd16', 'ts.0.1', 'p6', 'ts.2.1', 'ts.2.0', 'd17', 'tf.2.0', 'p10', 'o0', 'p5'}, {'p13', 'tf.0.0', 'd2', 'ts.0.0', 'd19', 'p8', 'p0', 'd8', 'p9', 'p4', 'ts.1.2', 'p11', 'd12', 'p14', 'tf.1.0', 'd13', 'd14', 'ts.1.0', 'p1', 'p15', 'p18', 'p2', 'd4', 'd1', 'd7', 'd0', 'p12', 'd15', 'p19', 'd9', 'd18', 'tf.1.2', 'p7'}, ('p11',)), ({'ts.2.0', 'p11', 'ts.0.0', 'd19', 'd15', 'tf.2.1', 'p8', 'ts.2.1', 'd11', 'p7', 'ts.1.0', 'ts.1.1', 'd7'}, {'p13', 'd2', 'ts.2.2', 'tf.2.2', 'p0', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'd13', 'p3', 'p16', 'p14', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p15', 'p1', 'd16', 'e0', 'ts.0.1', 'p18', 'p6', 'p2', 'd4', 'd1', 'd0', 'p12', 'd17', 'e1', 'tf.0.1', 'p10', 'd9', 'd18', 'tf.1.2', 'p5'}, ('d19',)), ({'p13', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'o1', 'p0', 'd8', 'p9', 'p4', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd4', 'd1', 'tf.2.1', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'd9', 'p10', 'd18', 'o0', 'p5'}, {'p11', 'p15', 'd15', 'ts.1.1', 'p8', 'p19', 'tf.1.1', 'd11', 'p7', 'd7', 'd0'}, ('p19',)), ({'p13', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'o1', 'p0', 'd8', 'p9', 'p4', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd4', 'd1', 'tf.2.1', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'd9', 'p10', 'd18', 'o0', 'p5'}, {'p11', 'p15', 'd15', 'ts.1.1', 'p8', 'p19', 'tf.1.1', 'd11', 'p7', 'd7', 'd0'}, ('p19',)), ({'p13', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'o1', 'p0', 'd8', 'p9', 'p4', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd4', 'd1', 'tf.2.1', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'd9', 'p10', 'd18', 'tf.1.2', 'o0', 'p5'}, {'p11', 'p15', 'd15', 'ts.1.1', 'p8', 'p19', 'tf.1.1', 'd11', 'p7', 'd7', 'd0'}, ('p19',)), ({'p13', 'd18', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'p0', 'p8', 'd8', 'p18', 'p2', 'd9', 'd4', 'ts.1.0', 'p4', 'd0'}, {'d19', 'ts.1.2', 'd3', 'ts.0.2', 'p11', 'e2', 'd12', 'd5', 'd14', 'd13', 'p3', 'p16', 'p14', 'target', 'd10', 'ts.1.1', 'p17', 'tf.0.2', 'd6', 'p1', 'p15', 'd16', 'e0', 'ts.0.1', 'p6', 'd11', 'd1', 'tf.2.1', 'ts.2.1', 'd7', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'e1', 'd15', 'tf.0.1', 'p10', 'p19', 'tf.1.1', 'tf.1.2', 'p7', 'p5'}, ('d9',)), ({'tf.0.0', 'd2', 'p12', 'ts.0.0', 'p1', 'd12', 'p14', 'd14', 'd1', 'ts.1.0'}, {'p13', 'ts.2.2', 'tf.2.2', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'p11', 'ts.0.2', 'e2', 'd5', 'd13', 'p3', 'p16', 'target', 'd10', 'ts.1.1', 'p17', 'tf.0.2', 'd6', 'p15', 'd16', 'e0', 'p18', 'ts.0.1', 'p6', 'd11', 'd4', 'tf.2.1', 'ts.2.1', 'd0', 'd7', 'ts.2.0', 'd17', 'tf.2.0', 'e1', 'd15', 'tf.0.1', 'p10', 'd9', 'p19', 'tf.1.1', 'd18', 'tf.1.2', 'p7', 'p5'}, ('d2',)), ({'ts.1.2', 'p17', 'ts.2.2', 'tf.2.2', 'p1', 'p14', 'd14', 'd16', 'd1', 'ts.1.0', 'tf.1.2', 'ts.1.1', 'p5'}, {'p13', 'tf.0.0', 'd2', 'ts.0.0', 'd19', 'p8', 'p0', 'd8', 'p9', 'p4', 'ts.0.2', 'p11', 'd3', 'e2', 'd12', 'd5', 'd13', 'p3', 'target', 'd10', 'tf.0.2', 'd6', 'p15', 'e0', 'ts.0.1', 'p18', 'p6', 'p2', 'd4', 'd11', 'tf.2.1', 'd7', 'd0', 'ts.2.1', 'ts.2.0', 'p12', 'd17', 'tf.2.0', 'e1', 'd15', 'tf.0.1', 'p10', 'p19', 'd9', 'd18', 'p7'}, ('d16',)), ({'ts.1.2', 'p17', 'ts.2.2', 'd17', 'tf.2.2', 'p14', 'd14', 'd16', 'p16', 'd1', 'ts.1.0', 'ts.1.1', 'p5'}, {'p13', 'tf.0.0', 'd2', 'ts.0.0', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'd3', 'ts.0.2', 'p11', 'e2', 'd12', 'd5', 'd13', 'p3', 'target', 'd10', 'tf.0.2', 'd6', 'p15', 'e0', 'ts.0.1', 'p18', 'p6', 'p2', 'd4', 'd11', 'tf.2.1', 'd7', 'd0', 'ts.2.1', 'ts.2.0', 'p12', 'tf.2.0', 'e1', 'd15', 'tf.0.1', 'p10', 'd9', 'p19', 'd18', 'p7'}, ('d1',)), ({'ts.2.0', 'p11', 'ts.0.0', 'd19', 'd15', 'ts.1.0', 'ts.1.1'}, {'p13', 'd2', 'ts.2.2', 'tf.2.2', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'd13', 'p3', 'p16', 'p14', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p1', 'd16', 'e0', 'p18', 'p2', 'p6', 'ts.0.1', 'd11', 'd1', 'd4', 'tf.2.1', 'd7', 'd0', 'ts.2.1', 'p12', 'd17', 'e1', 'tf.0.1', 'p10', 'd9', 'p19', 'd18', 'tf.1.2', 'p7', 'p5'}, ('d15',)), ({'ts.2.0', 'p11', 'ts.0.0', 'd19', 'd15', 'ts.1.0', 'ts.1.1'}, {'p13', 'd2', 'ts.2.2', 'tf.2.2', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'd13', 'p3', 'p16', 'p14', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p1', 'd16', 'e0', 'p18', 'p2', 'p6', 'ts.0.1', 'd11', 'd1', 'tf.2.1', 'd4', 'd7', 'ts.2.1', 'd0', 'p12', 'd17', 'e1', 'tf.0.1', 'p10', 'd9', 'p19', 'd18', 'tf.1.2', 'p7', 'p5'}, ('d15',)), ({'p13', 'tf.0.0', 'ts.0.0', 'p8', 'p0', 'd8', 'p9', 'd13', 'ts.1.1', 'ts.1.0', 'p15', 'p18', 'p2', 'ts.0.1', 'd4', 'ts.2.1', 'd0', 'd9', 'd18'}, {'d2', 'ts.2.2', 'tf.2.2', 'd19', 'ts.1.2', 'd3', 'p11', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'p14', 'p3', 'p16', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p1', 'd16', 'e0', 'p6', 'd11', 'd1', 'd7', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'e1', 'd15', 'p10', 'p19', 'tf.1.2', 'p7', 'p5'}, ('d4',)), ({'ts.2.0', 'ts.0.0', 'd6', 'p10', 'ts.1.0', 'd10'}, {'p13', 'd2', 'ts.2.2', 'tf.2.2', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'ts.0.2', 'p11', 'd3', 'e2', 'd12', 'd5', 'd14', 'd13', 'p16', 'p14', 'p3', 'target', 'ts.1.1', 'p17', 'tf.0.2', 'p1', 'p15', 'd16', 'e0', 'p18', 'p2', 'ts.0.1', 'd4', 'd11', 'tf.2.1', 'd1', 'd7', 'ts.2.1', 'd0', 'p12', 'd17', 'e1', 'd15', 'tf.0.1', 'p19', 'd9', 'tf.1.1', 'd18', 'tf.1.2', 'p7', 'p5'}, ('d6',)), ({'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'o1', 'd19', 'p8', 'p4', 'ts.1.2', 'ts.0.2', 'p11', 'd3', 'd12', 'p14', 'd14', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'p15', 'd6', 'ts.1.0', 'd16', 'p6', 'ts.0.1', 'd11', 'd1', 'tf.2.1', 'ts.2.1', 'd7', 'ts.2.0', 'p12', 'd17', 'tf.2.0', 'd15', 'tf.0.1', 'p19', 'p10', 'tf.1.1', 'tf.1.2', 'o0', 'p7', 'p5'}, {'p13', 'p0', 'd13', 'p18', 'p2', 'd9', 'p9', 'd4', 'd8', 'd18'}, ('p0',)), ({'d2', 'ts.2.2', 'tf.2.2', 'o1', 'd19', 'p8', 'p4', 'ts.1.2', 'ts.0.2', 'p11', 'd3', 'd12', 'p14', 'd14', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'p15', 'd6', 'ts.1.0', 'd16', 'p6', 'ts.0.1', 'd11', 'd1', 'tf.2.1', 'ts.2.1', 'd7', 'ts.2.0', 'p12', 'd17', 'tf.2.0', 'd15', 'tf.0.1', 'p19', 'p10', 'tf.1.1', 'tf.1.2', 'o0', 'p7', 'p5'}, {'p13', 'tf.0.0', 'ts.0.0', 'p0', 'd13', 'p18', 'p2', 'd9', 'p9', 'd4', 'd8', 'd18'}, ('p0',)), ({'tf.0.0', 'ts.0.0', 'o1', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd1', 'd18', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'tf.0.1', 'p10', 'ts.1.0', 'tf.1.2', 'o0', 'p5'}, {'p13', 'd2', 'ts.2.2', 'tf.2.2', 'p15', 'd19', 'p0', 'p8', 'd8', 'p9', 'd4', 'd11', 'tf.2.1', 'p4', 'd7', 'd0', 'ts.2.1', 'p11', 'd15', 'p19', 'p7'}, ('p9',)), ({'ts.2.0', 'ts.0.0', 'p15', 'tf.2.1', 'ts.2.1', 'tf.1.1', 'd11', 'p7', 'ts.1.0', 'ts.1.1', 'd7'}, {'p13', 'ts.2.2', 'd2', 'tf.2.2', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'd13', 'p3', 'p16', 'p14', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p1', 'd16', 'e0', 'p18', 'ts.0.1', 'p6', 'p2', 'd4', 'd1', 'd0', 'p12', 'd17', 'e1', 'd15', 'tf.0.1', 'p10', 'd9', 'p19', 'd18', 'tf.1.2', 'p5'}, ('d11',)), ({'p15', 'ts.2.1', 'tf.1.1', 'd11', 'p7', 'tf.2.1', 'ts.1.1', 'd7'}, {'p13', 'tf.0.0', 'ts.2.2', 'd2', 'tf.2.2', 'ts.0.0', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'tf.1.0', 'd13', 'p3', 'p16', 'd14', 'p14', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'ts.1.0', 'p1', 'd16', 'e0', 'p18', 'p2', 'p6', 'ts.0.1', 'd4', 'd1', 'd0', 'ts.2.0', 'p12', 'd17', 'tf.2.0', 'e1', 'd15', 'tf.0.1', 'p10', 'd9', 'p19', 'd18', 'tf.1.2', 'p5'}, ('d11',)), ({'ts.0.0', 'p15', 'ts.2.1', 'tf.1.1', 'd11', 'p7', 'tf.2.1', 'ts.1.1', 'd7'}, {'p13', 'ts.2.2', 'd2', 'tf.2.2', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'tf.1.0', 'd13', 'p3', 'p16', 'd14', 'p14', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'ts.1.0', 'p1', 'd16', 'e0', 'p18', 'p2', 'p6', 'ts.0.1', 'd4', 'd1', 'd0', 'ts.2.0', 'p12', 'd17', 'tf.2.0', 'e1', 'd15', 'tf.0.1', 'p10', 'd9', 'p19', 'd18', 'tf.1.2', 'p5'}, ('d11',)), ({'p13', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'o1', 'p0', 'd8', 'p9', 'p4', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'tf.1.0', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd1', 'd4', 'ts.2.1', 'ts.2.0', 'p12', 'd17', 'tf.2.0', 'p10', 'd9', 'd18', 'o0', 'p5'}, {'ts.1.2', 'p11', 'p15', 'd19', 'p8', 'p19', 'd11', 'tf.1.2', 'p7', 'd7', 'd0'}, ('p15',)), ({'ts.1.2', 'ts.2.0', 'p11', 'ts.0.0', 'p15', 'd7', 'tf.2.1', 'p19', 'd11', 'ts.1.0', 'tf.1.2', 'ts.1.1', 'ts.2.1'}, {'p13', 'd2', 'ts.2.2', 'tf.2.2', 'd19', 'p8', 'p0', 'd8', 'p9', 'p4', 'ts.0.2', 'd3', 'e2', 'd12', 'd5', 'd14', 'd13', 'p16', 'p3', 'p14', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p1', 'd16', 'e0', 'ts.0.1', 'p18', 'p6', 'p2', 'd4', 'd1', 'd0', 'p12', 'd17', 'e1', 'd15', 'tf.0.1', 'p10', 'd9', 'd18', 'p5'}, ('d7',)), ({'p11', 'p15', 'd19', 'd15', 'd7', 'tf.2.1', 'p19', 'tf.1.1', 'd11', 'ts.1.0', 'ts.1.1', 'ts.2.1'}, {'p13', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'p8', 'p0', 'd8', 'p9', 'p4', 'ts.1.2', 'ts.0.2', 'd3', 'e2', 'd12', 'd5', 'd14', 'd13', 'p16', 'p3', 'p14', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p1', 'd16', 'e0', 'p18', 'ts.0.1', 'p6', 'p2', 'd4', 'd1', 'd0', 'ts.2.0', 'p12', 'd17', 'tf.2.0', 'e1', 'tf.0.1', 'p10', 'd9', 'd18', 'tf.1.2', 'p5'}, ('d7',)), ({'ts.1.2', 'p11', 'd19', 'd15', 'tf.2.1', 'tf.0.1', 'ts.0.1', 'ts.2.1', 'p19', 'tf.1.1', 'd11', 'p7', 'ts.1.0', 'ts.1.1', 'd7'}, {'p13', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'p8', 'p0', 'd8', 'p9', 'p4', 'd3', 'ts.0.2', 'e2', 'd12', 'd5', 'd14', 'd13', 'p3', 'p16', 'p14', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p1', 'd16', 'e0', 'p18', 'p2', 'p6', 'd4', 'd1', 'd0', 'ts.2.0', 'p12', 'd17', 'tf.2.0', 'e1', 'p10', 'd9', 'd18', 'p5'}, ('d15',)), ({'p13', 'tf.0.0', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'o1', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'ts.0.2', 'p11', 'd3', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p15', 'd6', 'ts.1.0', 'd16', 'ts.0.1', 'p18', 'p6', 'd11', 'd4', 'tf.2.1', 'ts.2.1', 'd0', 'd7', 'd17', 'd15', 'tf.0.1', 'p19', 'd9', 'p10', 'd18', 'tf.1.2', 'o0', 'p7', 'p5'}, {'p12', 'ts.2.0', 'tf.2.0', 'p1', 'd12', 'p14', 'd14', 'p2', 'd1'}, ('p2',)), ({'p13', 'tf.0.0', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'o1', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'ts.0.2', 'p11', 'd3', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p15', 'd6', 'd16', 'ts.0.1', 'p18', 'p6', 'd11', 'd4', 'tf.2.1', 'ts.2.1', 'd0', 'd7', 'ts.2.0', 'd17', 'tf.2.0', 'd15', 'tf.0.1', 'p19', 'd9', 'p10', 'tf.1.1', 'd18', 'tf.1.2', 'o0', 'p7', 'p5'}, {'p12', 'p1', 'd12', 'p14', 'tf.1.0', 'd14', 'p2', 'd1', 'ts.1.0'}, ('p2',)), ({'ts.1.2', 'p17', 'd16', 'ts.0.1', 'ts.1.0', 'tf.1.2', 'p5'}, {'p13', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'd3', 'ts.0.2', 'p11', 'e2', 'd12', 'd5', 'd14', 'd13', 'p3', 'p14', 'target', 'd10', 'ts.1.1', 'tf.0.2', 'd6', 'p1', 'p15', 'e0', 'p18', 'p2', 'p6', 'd11', 'd1', 'tf.2.1', 'd4', 'ts.2.1', 'd7', 'd0', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'e1', 'd15', 'p10', 'd9', 'tf.1.1', 'p19', 'd18', 'p7'}, ('d16',)), ({'p13', 'd2', 'ts.2.2', 'ts.0.0', 'p0', 'p8', 'd8', 'p4', 'ts.1.2', 'ts.0.2', 'd12', 'tf.1.0', 'ts.1.1', 'p18', 'p2', 'd11', 'd4', 'd18', 'd0', 'p12', 'd15', 'd9', 'ts.1.0'}, {'d19', 'd3', 'p11', 'e2', 'd5', 'd14', 'd13', 'p16', 'p3', 'p14', 'target', 'd10', 'p17', 'd6', 'p15', 'p1', 'd16', 'e0', 'ts.0.1', 'p6', 'd1', 'tf.2.1', 'ts.2.1', 'd7', 'ts.2.0', 'd17', 'tf.2.0', 'e1', 'tf.0.1', 'p10', 'p19', 'p7', 'p5'}, ('d9',)), ({'p13', 'tf.0.0', 'd2', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'o1', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'tf.1.0', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'd16', 'p18', 'p2', 'p6', 'ts.0.1', 'd11', 'd1', 'd18', 'd4', 'd7', 'd0', 'ts.2.1', 'ts.2.0', 'p12', 'd17', 'tf.2.0', 'd15', 'p10', 'd9', 'ts.1.0', 'tf.1.2', 'o0', 'p7', 'p5'}, {'p15', 'p19', 'p11'}, ('p19',)), ({'p13', 'd18', 'ts.2.0', 'ts.0.0', 'tf.2.0', 'tf.1.0', 'd13', 'p0', 'p18', 'p2', 'd9', 'p9', 'd4', 'ts.1.0', 'ts.1.1', 'd0'}, {'d2', 'ts.2.2', 'tf.2.2', 'd19', 'p8', 'd8', 'ts.1.2', 'd3', 'p11', 'ts.0.2', 'e2', 'd12', 'p14', 'd14', 'd5', 'p3', 'p16', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p1', 'p15', 'd16', 'e0', 'ts.0.1', 'p6', 'd11', 'd1', 'tf.2.1', 'd7', 'ts.2.1', 'p12', 'd17', 'e1', 'd15', 'tf.0.1', 'p10', 'p19', 'tf.1.2', 'p7', 'p5'}, ('d4',)), ({'p13', 'ts.1.2', 'd18', 'd2', 'p8', 'p0', 'd8', 'd13', 'd9', 'p9', 'd4', 'ts.1.0', 'p4', 'ts.1.1', 'd0'}, {'tf.0.0', 'ts.2.2', 'ts.0.0', 'tf.2.2', 'd19', 'd3', 'p11', 'ts.0.2', 'e2', 'd12', 'p14', 'd14', 'd5', 'p3', 'p16', 'target', 'd10', 'p17', 'tf.0.2', 'd6', 'p15', 'p1', 'd16', 'e0', 'ts.0.1', 'p2', 'p6', 'd11', 'd1', 'tf.2.1', 'd7', 'ts.2.1', 'ts.2.0', 'p12', 'd17', 'tf.2.0', 'e1', 'd15', 'tf.0.1', 'p10', 'p19', 'p7', 'p5'}, ('d18',)), ({'p13', 'tf.0.0', 'ts.2.2', 'd2', 'ts.0.0', 'tf.2.2', 'o1', 'p0', 'd8', 'p9', 'ts.1.2', 'ts.0.2', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'tf.1.0', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'd6', 'ts.1.0', 'd16', 'ts.0.1', 'p18', 'p2', 'p6', 'd1', 'd4', 'tf.2.1', 'ts.2.1', 'p12', 'ts.2.0', 'd17', 'tf.2.0', 'tf.0.1', 'd9', 'p10', 'tf.1.1', 'd18', 'tf.1.2', 'o0', 'p5'}, {'p11', 'p15', 'd19', 'p8', 'p19', 'd11', 'p4', 'p7', 'd7', 'd0'}, ('p15',)), ({'p13', 'ts.2.2', 'tf.2.2', 'o1', 'd19', 'p0', 'p8', 'd8', 'p9', 'p4', 'ts.1.2', 'ts.0.2', 'p11', 'd3', 'd12', 'p14', 'd14', 'd13', 'p3', 'o2', 'p16', 'd5', 'd10', 'ts.1.1', 'source', 'p17', 'tf.0.2', 'p1', 'p15', 'd6', 'ts.1.0', 'd16', 'ts.0.1', 'p18', 'p6', 'd11', 'd1', 'd4', 'tf.2.1', 'ts.2.1', 'd0', 'd7', 'ts.2.0', 'p12', 'd17', 'tf.2.0', 'd15', 'tf.0.1', 'p19', 'd9', 'p10', 'd18', 'tf.1.2', 'o0', 'p7', 'p5'}, {'p2', 'ts.0.0', 'tf.0.0'}, ('p2',))]):
            S,Sp, _ = cut
            model.addConstr((quicksum(x[i,j] for i in S for j in Sp if (i,j) in A)>=1), name=f"weakpisig_cut_{idx}")
         #"""
        if cutTrans==True:
            for n in TS_loc:
                for k in K:
                    t1 = f"ts.{k}.{n}"
                    if k== 0:
                        model.addConstr(quicksum(y[t1,j,r] for r in R for j in [a[1] for a in Ay.select(t1,'*',r)])>=quicksum(x[t1,j] for j in [a[1] for a in A.select(t1,'*')]))
                    if k>0:
                        t2 = f"ts.{k-1}.{n}"
                        model.addConstr(quicksum(y[t1,j,r]*r for r in R for j in [a[1] for a in Ay.select(t1,'*',r)])<=quicksum(y[t2,j,r]*r for r in R for j in [a[1] for a in Ay.select(t2,'*',r)]))
                       
        if HET==True:
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
            
        # Data for callback
        model._obj = None
        model._bd = None
        model._gap = None
        model._data = []
        model._x = x
        model._y = y
        model._z = z
        #model._bl = bl
        model._f = f
        model._ti = ti
        model._A = A
        model._Ay = Ay
        model._VO = VO
        model._VD = VD
        model._V = V
        model._P = P
        model._D = D
        model._Q = VC
        model._q = qnode
        model._TS = TS
        model._TF = TF
        model._found_cuts = 0
        model._cap_cuts = set()
        model._sols = set()
        model._vars = model.getVars()
        model._start = time.time()
        #debug
        model = add_cut_check(model)
        model.Params.LazyConstraints = 1
        model.Params.PreCrush = 1
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
        model._error_msgs = ""
        model._stats  = {"usercut_t":0.0, "lazy_t":0.0, "user_calls":0, "lazy_calls":0}
        # Redirect Gurobi output to a file
        #log_file_path = f"gurobi_BC_output_{time.time()}.log"
        #model.setParam("LogFile",log_file_path)
        model._cb_lastnode = 0
        model._cb_nroot = 0
        model._test_cuts = []
        model._cap_cuts = set()
        model._user_cuts = {"ST1":0,"ST2":0,"CapC":0,"pi-sig-depot":0,"pi":0,"pi-sig":0,"sig":0}
        model._lazy_cuts = {"pi":0,"sig":0,"ST1":0,"ST2":0,"IP":0, "IP_trans":0,"depotFixingPathCut":0,"transferCycleCutR1":0,"transferCycleCutR2":0,"transferCycleCutR3":0,"transferCycleCutR4":0,"multiTransPathCut":0,"double_trans_cut":0}
        model = setup_mip_node_tracker(model)
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
        lp = compute_LP_relax_bound(model)
        if barrier!=None:
            barrier.wait()
        model.optimize(callback=ub_callback)
        #model.write("model.lp")
        # model.optimize()
        # model.computeIIS()
        #
        if model.status==3:
            model.computeIIS()
            model.write("infeasible_model.ilp")
        
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
        
        sol_transfers = 0
        #with open(log_file_path, "r") as filer:
         #   gurobi_output = filer.read()
        #filer.close()
        
        #calls, call_time = parse_gurobi_output(gurobi_output)
        #print("Extracted",calls,call_time)
        error_msg =  model._error_msgs
        sol_req_trans = 0
        if model.Status == GRB.OPTIMAL:
            ratio = lp/model.ObjVal*100
            xarcs = plotLocation(df)
            
            _, errors =  check_tours(model)
            error_msg += errors 
            #tours = get_tour([a for a in x if x[a].x>0.5])
            with open(f"{filename.replace('.txt','')}_sol.txt", "w") as output:
                output.write(str([a for a in x if x[a].x>0.5]))
            sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
            sol_req_trans = quicksum(y[i,j,r] for (i,j) in TIy for r in R if (i,j,r) in Ay).getValue()
            infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sol_transfers,sol_req_trans,"",error_msg,ratio]  
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
            print(model._stats)
            #cut debugging
            print(model._test_cuts)
        elif model.Status == GRB.TIME_LIMIT:
            if model.SolCount == 0:
                sol_transfers = None
                infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sol_transfers,sol_req_trans,"","",lp]    
            else:
                ratio = lp/model.ObjVal*100
                _, errors =  check_tours(model)
                error_msg += errors 
                xarcs = plotLocation(df)
                with open(f"{filename.replace('.txt','')}_sol.txt", "w") as output:
                    output.write(str([a for a in x if x[a].x>0.5]))
                sol_transfers = quicksum(f[f"ts{n}"] for n in TS_loc).getValue()
                sol_req_trans = quicksum(y[i,j,r] for (i,j) in TIy for r in R if (i,j,r) in Ay).getValue()
                infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),model.ObjVal, model.MIPGap,model.ObjBound, model.Runtime,sol_transfers,sol_req_trans,"",error_msg,ratio]    
        else:
            infos = [filename, model.ModelName ,gurobi_status_dict.get(model.Status),"inf","inf",model.ObjBound, model.Runtime,sol_transfers,sol_req_trans,"","",lp]  
        for key in model._lazy_cuts:
            infos.append(model._lazy_cuts[key])
        for key in ["pi","sig"]:
            infos.append(model._user_cuts[key])
        for key in model._stats:
            infos.append(model._stats[key])
        model._solver_state.infos_sol = infos
        print(l_cuts)
        #for key in l_cuts:
            #with open(f"cut_lst_{key}.txt", 'w') as file:
                #file.write(str(l_cuts[key]))
        #os.remove(log_file_path)
        model._solver_state.master_finished=True
        model._solver_state.infos_sol = infos
        model.close()
        #print(np.array(stats_RCCP[1]).mean(),np.array(stats_RCCP[2]).mean())
        return infos#.append(stats_RCCP)
    
    def solve_iterative(barrier,env,state):
        #barrier.wait()
        start = time.time()
        obj = np.inf
        last_sol = None
        models = {}
        for i in range(5,20):
            models[i] = create_pdptw_model(filename, cut=1, strCap=True, env=env,solver_state=state)
        models[21] = create_pdptw_model(filename, cut=None, strCap=True, env=env)
        barrier.wait()
        for i in range(5,20):
            if  state.master_finished==True:
                print("finished first loop")
                break
            infos = solve_pdptw(models[i],20, None,cut=i,last_sol=last_sol)
            #infos = solve_pdptw(filename, 200,i,last_sol, True)
            obj = infos[3]
            if obj<np.inf:
                last_sol=i
        for i in range(12,15):
            if state.master_finished==True:
                break
            infos = solve_pdptw(models[i],600, None,cut=i,last_sol=last_sol)
            obj = infos[3]
            if obj<np.inf:
                last_sol=i
        if state.master_finished==True:
            print("finished")
            env.close()
            return []
        last_time = (60*60 )- (time.time()-start)
        infos = solve_pdptw(models[14],last_time, None,cut=i,last_sol=last_sol)
        env.close()
        #print("end run", infos)
        return infos
    
    def solve_two_phase(barrier,env,state):
        #barrier.wait()
        start = time.time()
        obj = np.inf
        last_sol = None
        model_run_1 = create_pdptw_model(filename, cut=-2, strCap=True, env=env,solver_state=state)
        model_run_2 = create_pdptw_model(filename, cut=None, strCap=True, env=env,solver_state=state)
        infos = solve_pdptw(model_run_1,3600, barrier,cut=-2,last_sol=last_sol, sollim=None)
        obj = infos[3]
        if obj<np.inf:
            last_sol=-2
        
        print("finished model 1")
        if state.master_finished==True:
            env.close()
            return []
        
        last_time = max((60*60)- (time.time()-start),0.0)
        if last_time>0.0:
            print("go model 2", last_sol)
            infos = solve_pdptw(model_run_2,last_time, barrier=None,cut=None,last_sol=last_sol)

        #infos = solve_pdptw(filename, last_time,None,-2,last_sol, True, env=env)
        #infos = solve_pdptw(filename, last_time ,None,last_sol,True)
        print("end parallel")
        env.close()
        return infos
    
    def solve_one_phase(barrier, env,state):
        model = create_pdptw_model(filename, cut=-2, strCap=True, env=env,solver_state=state)

        infos = solve_pdptw(model,3600, barrier=barrier,cut=-2,last_sol=None)

        return infos

    def add_cut_check(model):
        solution = [
            [('o1', 'p21'), ('p21', 'p19'), ('p19', 'd21'), ('d21', 'p18'), ('p18', 'd18'), ('d18', 'p13'), ('p13', 'd19'), ('d19', 'd13'), ('d13', 'p4'), ('p4', 'ts.2.2'), ('ts.2.2', 'tf.2.2'), ('tf.2.2', 'p2'), ('p2', 'd2'), ('d2', 'p3'), ('p3', 'd3'), ('d3', 'd7'), ('d7', 'p11'), ('p11', 'p5'), ('p5', 'd11'), ('d11', 'p14'), ('p14', 'd5'), ('d5', 'd14'), ('d14', 'e1')] ,
            [('o2', 'p6'), ('p6', 'p24'), ('p24', 'd6'), ('d6', 'ts.0.2'), ('ts.0.2', 'tf.0.2'), ('tf.0.2', 'd24'), ('d24', 'p17'), ('p17', 'd10'), ('d10', 'p15'), ('p15', 'd17'), ('d17', 'd15'), ('d15', 'e2')] ,
            [('o0', 'p1'), ('p1', 'd1'), ('d1', 'p12'), ('p12', 'd12'), ('d12', 'p10'), ('p10', 'p7'), ('p7', 'ts.1.2'), ('ts.1.2', 'tf.1.2'), ('tf.1.2', 'd4'), ('d4', 'p9'), ('p9', 'd9'), ('d9', 'p23'), ('p23', 'd23'), ('d23', 'p16'), ('p16', 'p20'), ('p20', 'd16'), ('d16', 'd20'), ('d20', 'p8'), ('p8', 'p22'), ('p22', 'd8'), ('d8', 'p0'), ('p0', 'd0'), ('d0', 'd22'), ('d22', 'e0')]
                    ]
        solution = []
        for route in solution:
            for e in route:
                model.addConstr(model._x[e]==1)
                
        l_cuts = ["multTrans"]#,"cycle"]
        cuts = [(frozenset({'d17', 'p17', 'd24', 'd18', 'p10', 'd10', 'p24'}), 'ts.0.2', 'ts.1.2'),
                (frozenset({'p5', 'd17', 'p17', 'd24', 'd18', 'p10', 'd5', 'd10', 'p3', 'p24', 'd3'}), 'ts.0.2', 'ts.1.2'),
                (frozenset({'p2'}), 'ts.2.2', 'ts.0.2'), 
                (frozenset({'p2'}), 'ts.1.2', 'ts.0.2'), 
                (frozenset({'d20', 'p8'}), 'ts.2.0', 'ts.0.0'),
                (frozenset({'d2', 'd7', 'p2', 'p6', 'p3', 'p24', 'd6', 'd3'}), 'ts.0.2', 'ts.1.2'), 
                (frozenset({'p2'}), 'ts.0.2', 'ts.2.2'), 
                (frozenset({'d2', 'd7', 'p6', 'p2', 'p3', 'p24', 'd6', 'd3'}), 'ts.1.2', 'ts.0.2'),
                (frozenset({'d2', 'd7', 'p6', 'p2', 'p3', 'p24', 'd6', 'd3'}), 'ts.2.2', 'ts.0.2')]
        #for key in l_cuts:
           # with open(f'cut_lst_{key}.txt', 'r') as file:
               # content = file.read()
        # Convert the string representation to a Python object
        #cuts = ast.literal_eval(content)
        cuts = []
        idx = 0
        print(len(cuts))
        for cut in cuts:
            #if key =="multTrans":
                S1,do_cut ,de_cut  = cut
                de = do_cut.replace("s","f")
                do = do_cut
                node_id = int(do.split(".")[-1])
                TS_comp = model._TS-frozenset([do,de_cut])
                S2 = (V-frozenset([do,de]))-S1
                RHS =  quicksum(model._x[i, do] for i in S1 if (i,do) in model._A)+quicksum(model._x[de,i] for i in S2 if (de,i) in model._A)
                RHS+=quicksum(model._x[i, j] for i in S2 for j in S1 if (i,j) in model._A)+quicksum(model._x[i, j] for i in S1 for j in S2.intersection(P|D) if (i,j) in model._A and int(i.replace("p","").replace("d",""))==int(j.replace("p","").replace("d","")))
                LHS = model._f[f"ts{node_id}"]
                model.addConstr((RHS>=LHS), name=f"cut{idx}")
                idx+=1
        """
        for cut in cuts:
            if key =="ipath":
                path = cut
                last_leg = path[-2]
                path = path[:-1]
                LHS = quicksum(model._x[i, j] for i in path for j in path if (i,j) in A)
                #LHS += quicksum(model._x[last_leg, j] for j in outfork_set )
                model.addConstr((
                       LHS#for (i,j) in edges)#
                        <= len(path)-2
                        ), name=f"ipath.{idx}")
                idx += 1
            if key == "df":
                comp, illegal_d_depots = cut
                LHS = quicksum(model._x[i, j] for i in comp for j in comp if (i,j) in model._A)+quicksum(model._x[i, j] for i in comp for j in illegal_d_depots if (i,j) in model._A)
                model.addConstr((
                        LHS
                        <= len(comp)-2), name=f"df.{idx}")
                idx += 1
            if key =="tcycle":
                S,source_set,target_set = cut
                model.addConstr((
                    quicksum(model._x[i,j] for i in S for j in S if (i,j) in A)+
                    quicksum(model._x[i,j] for i in source_set for j in S if (i,j) in A)+
                    quicksum(model._x[i,j] for i in S for j in target_set if (i,j) in A)
                    <= len(S)
                    ), name=f"tcycle.{idx}")
                idx += 1
            if key == "1cycle":
                S, illegal_requests = cut
                LHS = quicksum(model._y[e] for e in illegal_requests)+quicksum(model._x[i,j] for i in S for j in S if (i,j) in A)
                added_cuts = set()
                for e in illegal_requests:
                    if e[0] not in added_cuts:
                        LHS += quicksum(model._x[i,j] for i in S for j in [e[0]] if (i,j) in A)
                        added_cuts.add(e[0])
                    if e[1] not in added_cuts:
                        LHS += quicksum(model._x[j,i] for i in S for j in [e[1]] if (j,i) in A)
                        added_cuts.add(e[1])
                model.addConstr((
                    LHS
                    <= len(S)+2
                ), name=f"1cycle.{idx}")
                idx += 1
            if key =="2cycle":
                S1,S2, illegal_requests = cut
                LHS = quicksum(model._x[i,j] for i in S1 for j in S1 if (i,j) in A)+quicksum(model._x[i,j] for i in S2 for j in S2 if (i,j) in A)
                #breakpoint()
                added_cuts = set()
                for e1,e2 in illegal_requests:
                    k,l = e1[0], e1[1]
                    u,v = e2[0], e2[1]
                    LHS += model._y[e1]+model ._y[e2]
                    if l not in added_cuts:
                        LHS += quicksum(model._x[i,j] for j in S1 for i in [l] if (i,j) in A)
                        added_cuts.add(l)
                    if u not in added_cuts:
                       LHS += quicksum(model._x[i,j] for i in S1 for j in [u] if (i,j) in A)
                       added_cuts.add(u)
                    if k not in added_cuts:
                       LHS += quicksum(model._x[i,j] for i in S2 for j in [k] if (i,j) in A)
                       added_cuts.add(k)
                    if v not in added_cuts:
                       LHS += quicksum(model._x[j,i] for i in S2 for j in [v] if (j,i) in A)
                       added_cuts.add(v)
                    if (l,u) in A:
                        LHS += model._x[l,u]
                    if (v,k) in A:
                        LHS += model._x[v,k]
                    if (k,l) in A:
                        LHS += model._x[k,l]
                    if (u,v) in A:
                       LHS += model._x[u,v]
                model.addConstr((
                    LHS
                    #quicksum(model._y[e] for e in illegal_requests)+quicksum(model._y[e[1].replace("f","s"),e[0].replace("s","f"),e[2]] for e in illegal_requests)+quicksum(model._x[i,j] for i in cycle for j in cycle if (i,j) in A)
                    <= len(S1)+len(S2)+3
                    ), name=f"2cycle.{idx}")
                idx += 1"""
   
        return model
                
        

    def solve_parallel(mode="two"):
        state = SolverState()
        env2 = gp.Env()
        env1 = gp.Env()
        barrier = threading.Barrier(2) 
        #t1 = threading.Thread(target=solve_iterative,args=(barrier,env1))
        #t1 = threading.Thread(target=solve_pdptw)
        if mode=="two":
            t1 = threading.Thread(target=solve_two_phase, args=(barrier,env1,state))
        else:
            t1 = threading.Thread(target=solve_one_phase, args=(barrier,env1,state))
        t2 = threading.Thread(target=solve_compact, args=(barrier,env2,state, mode))
        t1.start()
        t2.start()
    
        t1.join()
        t2.join()
        env2.close()
        env1.close()
        
        return state.infos_sol
    
    #barrier = threading.Barrier(1) 
    #infos_sol = solve_compact()
    infos_sol = solve_parallel(mode)
    #state = SolverState()
    #infos_sol = solve_compact(None,gp.Env(),solver_state=SolverState())
    #model = create_pdptw_model(filename, cut=-2, strCap=True, env=gp.Env())
    return infos_sol


#info = twoIndexModelUB(filename, mode="two",timeFlow=True,cutTrans=False)
#print("old capacity cut")
#print(info)
#csvIndex = ['Instace name','model','Status', 'Obj.Value','MIPGap','Obj. Bound', 't(s)','used_transfer_stations']
#resultDf = pd.DataFrame([info])
#resultDf.to_csv("result_VehicleFlow.csv",mode='a', encoding='utf-8', index=False)

#print(time_measure1, time_measure2, time_measure3)