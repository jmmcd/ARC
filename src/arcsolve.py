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
     
    def fitmatrix(self):
        for index,data in enumerate(self.train):
            self.train_ip[index+1] = np.array(data["input"])
            self.train_op[index+1] = np.array(data["output"])
            self.sum_col[index+1] = np.sum(np.array(data["input"]), axis = 1)
            self.sum_row[index+1] = np.sum(np.array(data["input"]), axis = 0)

        
        for obj_index in range(len(self.sum_row)):
            moveup = False
            row_fix_obj = False
            for i in range(len(self.sum_row[obj_index+1])-1):
                if not row_fix_obj:
                    row_fix_obj = ((self.sum_row[obj_index+1])[i] == (self.sum_row[obj_index+1])[i+1]) and ((self.sum_row[obj_index+1])[i]==16) and ((self.sum_row[obj_index+1])[i+1]==16)

                if not moveup:
                    moveup = (self.sum_row[obj_index+1])[i] > 0
                    self.move_vertical[i] = moveup
                    obj_index = i+1
                    if row_fix_obj:
                        break 
            if row_fix_obj:
                self.move_firstHalf[i] = obj_index > len(self.sum_row)/2
            else:
                self.move_firstHalf[i] = False
                    
        
    def fit(self, X, y):
        self.X = X
        self.y = y
        return self