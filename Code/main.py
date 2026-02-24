import Lyu2023Neu as lyu
#import newmodel as nm
import Cortes2010 as ct
#import Cortes2010conditionalConstraints as ctc
#import twoIndex as twoIndex
#import twoIndexthreeRequestIndex_Improved as twoIndexTwoReq
import twoIndexthreeRequestIndex_timeFlowLabel as timemod
#import twoIndexthreeRequestIndex_timeFlow as twoIndexTwoReq
#import Rais2014 as rs
#import Rais2014_WIA as rsi
#import Rais2014NeuImproved as rs
import CombinatorialBendersCuts as CBC
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import gurobipy as gp
from gurobipy import GRB


def main():
    
    mainFolderPath = './InstancesLyu23/PDPT/' 
    #mainFolderPath = './InstancesLyu23/PDPT_small/' 
    #mainFolderPath = './InstancesLyu23/PDPTWT' 
    #mainFolderPath = "./InstancesGhilas/PDPTW_Rewritten/"
    folder = os.fsencode(mainFolderPath)
    filenames = []
    for subdir, dirs, files in os.walk(mainFolderPath):
        for file in files:         
            experiment_folder = subdir.split(os.sep)[-1]
            filepath = os.path.join(subdir, file)
            filenames.append(filepath)
    
    results = []
    n = 0
    for file in filenames:
        #if "test" in file:
            print(file)
            # results.append(ct.cortesModel(file) + rs.raisModel(file))
            #results.append(twoIndexTwoReq.twoIndexModel(file))
            #results.append(timemod.twoIndexModel(file))
            results.append(CBC.CBC_solver(file))
            #results.append(ct.cortesModel(file))
            #results.append(lyu.lyuModel(file))
            #results.append(rs.raisModel(file))
            #results.append(twoIndex.twoIndexModel(file))
            csvIndex = ['Instace name','model','Status', 'Obj.Value','MIPGap','Obj. Bound', 't(s)','used_transfer_stations']
            resultDf = pd.DataFrame(results, columns = csvIndex)
            resultDf.to_csv("result_CombBenders_Oct24.csv", encoding='utf-8', index=False)
            #resultDf.to_csv("result_PDPTWT.csv", encoding='utf-8',index=False)



main()
