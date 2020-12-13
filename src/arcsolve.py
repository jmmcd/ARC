#================================================================================
#Author : Vin Padmanabhan
#This class aims to solve ARC puzzles
#Selected tasks : 05f2a901.json, 6f8cd79b,json
#
#
#
#
#
#
#================================================================================

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import json
from sklearn.base import BaseEstimator, ClassifierMixin

class arcsolve(BaseEstimator):
    def __init__(self, json):
        self.json = json
        self.train = json["train"]
        self.train_ip = {}
        self.train_op = {}
        self.sum_row = {}
        self.sum_col = {}
        self.predict_op = []
        self.move_vertical = {}
        self.move_firstHalf = {}
    
    #get values like input, output  
    def fitmatrix(self):
        for index,data in enumerate(self.train):
            self.train_ip[index+1] = np.array(data["input"])
            self.train_op[index+1] = np.array(data["output"])
            self.sum_col[index+1] = np.sum(np.array(data["input"]), axis = 1)
            self.sum_row[index+1] = np.sum(np.array(data["input"]), axis = 0)  
    
    #find how object movement for :05f2a901
    def find05f2a901Moves(self):
        for obj_index in range(len(self.sum_row)):
            moveup = False #True - object transformed vertically, False - object transformed horizondally
            row_first_half = False #True - object transformed from first half, False - object transformed from seconf half
            for i in range(len(self.sum_row[obj_index+1])-1):
                if not row_first_half:
                    row_first_half = ((self.sum_row[obj_index+1])[i] == (self.sum_row[obj_index+1])[i+1]) and ((self.sum_row[obj_index+1])[i]==16) and ((self.sum_row[obj_index+1])[i+1]==16)

                if not moveup:
                    moveup = (self.sum_row[obj_index+1])[i] > 0
                    self.move_vertical[i] = moveup
                    obj_index = i+1
                    if row_first_half:
                        break 
            if row_first_half:
                self.move_firstHalf[i] = obj_index > len(self.sum_row)/2
            else:
                self.move_firstHalf[i] = False
    
    #solve puzzle :05f2a901   
    #sample : solve_6f8cd79b()
    #with open('..\\data\\training\\6f8cd79b.json') as f:
    #    jsondata = json.load(f)
    #mysol = arcsolve(jsondata)
    #mysol.fitmatrix()
    #mysol.solve6f8cd79b(np.zeros((2,2)))
    def solve_6f8cd79b(self, testdata):
        _testdata= np.array(testdata)
        row, colum = _testdata.shape
        _getColour = 8
        _testdata[0:1] =_getColour
        _testdata[row-1:row] =_getColour
        _testdata[:,0] = _getColour
        _testdata[:,colum-1] = _getColour
        return _testdata                
    
    def solve_c1d99e64(self, testdata)
        _testdata= np.array(testdata)
        _row, _colum = _testdata.shape
        _getColour = 2
        zero_rows = np.where(~_testdata.any(axis=1))[0]
        zero_cols = np.where(~_testdata.any(axis=0))[0]

        for row in zero_rows:
            _testdata[row:row+1] = _getColour

        for col in zero_cols:
            _testdata[0:,col:col+1] = _getColour        
        return _testdata        
        
    def fit(self, X, y):
        self.X = X
        self.y = y
        return self