# -*- coding: utf-8 -*-
"""
Created on Sun May 11 11:58:53 2025

@author: un_po
"""

import numpy as np
import gurobipy as gp
from gurobipy import GRB, quicksum





def separate_rounded_capacity_inequalities(gurobi_model,x,P,D,Q,mipsol=False):
    
    def mycallback(model_sep, where):
        if where == GRB.Callback.MIPSOL:
            cur_obj = model_sep.cbGet(gp.GRB.Callback.MIPSOL_OBJ)
            if cur_obj >= epsilon_2:
                S = {i for i in s if model_sep.cbGetSolution(s[i]) > 0.5}
                #S = frozenset(S)
                #sorted(S)
                S_in_string_form = str(S)
                if S_in_string_form not in gurobi_model._cap_cuts:
                #if True:
                    if mipsol==False:
                        S_comp = [i for i in gurobi_model._V if i not in S]
                        Constr_LHS = quicksum(gurobi_model._x[i, j] for i in S for j in S_comp if (i,j) in gurobi_model._A)
                        #Constr_RHS = quicksum((Q*gurobi_model._z[i,t])-gurobi_model._q[i,t] for i in S if i>0)
                        Constr_RHS = float(np.ceil(sum(gurobi_model._q[i] for i in S)/Q))
    
                        gurobi_model.cbCut(Constr_LHS>=Constr_RHS)
                        gurobi_model._cap_cuts.add(S_in_string_form)
                        gurobi_model._user_cuts["CapC"] += 1
                        print("added rounded capacity cut", S, cur_obj,model_sep.cbGetSolution(alpha) )


    if len(x)<1:
        return
    
    with gp.Env(empty=True) as env:
        env.setParam('OutputFlag', 0)
        env.start()
        with gp.Model(env=env) as model_sep:
            h = {}
            s = {}
            y = {}
            y["d"] = model_sep.addVar(vtype=GRB.BINARY, name='y_d')
            y["p"] = model_sep.addVar(vtype=GRB.BINARY, name='y_p')
            epsilon_1 = 0.5
            epsilon_2 = 0.1
            for i,j in x:
                if i not in gurobi_model._VO:
                #if i in P|D and j in P|D:
                    h[i,j] = model_sep.addVar(vtype=GRB.CONTINUOUS, name=f'h_{i}_{j}')
                    if i not in s:
                        s[i] =  model_sep.addVar(vtype=GRB.BINARY, name=f's_{i}')
                            
                    if j not in s:
                        s[j] =  model_sep.addVar(vtype=GRB.BINARY, name=f's_{j}')
            alpha = model_sep.addVar(vtype=GRB.INTEGER, name='ALPHA')
            relevant_nodes = {i for i in s}
            P = P.intersection(relevant_nodes)
            D = D.intersection(relevant_nodes)
            model_sep.modelSense = GRB.MAXIMIZE
            model_sep.setObjective(quicksum(x[e]*h[e] for e in h)-quicksum(s[j] for j in s)+1+alpha)
            model_sep.addConstr(y["d"]+y["p"]<=1)
            model_sep.addConstrs(s[i]<=y["p"] for i in P)
            model_sep.addConstrs(s[i]<=y["d"] for i in D)
            model_sep.addConstrs((h[e] <= s[i] for i in s for e in h if e[0]==i), name=f"link edges_{i}")
            model_sep.addConstrs((h[e] <= s[j] for j in s for e in h if e[1]==j), name=f"link edges_{j}")
            model_sep.addConstr(quicksum(s[j] for j in s)>=3)
            model_sep.addConstr(quicksum(gurobi_model._q[j]*s[j] for j in s)>=Q * alpha+epsilon_1)
            
            #model_sep.Params.OutputFlag = 0
            #model_sep.Params.LogToConsole=0
            model_sep.Params.Threads = 4
            model_sep._found_cuts = 0
            model_sep.optimize(mycallback)
            env.close()
            if model_sep._found_cuts>0:
                return True
            return False