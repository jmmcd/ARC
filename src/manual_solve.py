#!/usr/bin/python

import os, sys
import json
import numpy as np
import re

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.

#0d3d703e.json replace colours
#d4a91cb9.json draw a line between two points with verticality/horizontality contraints
#c3f564a4.json find the repeated pattern and finish it

def solve_0d3d703e(x):
    #Relpace each colour with the corresponding colour
    y = x.copy()
    size = np.shape(y)
    for i in range(0,size[0]):
        for j in range(0,size[1]):
            if y[i,j] == 1:
                    y[i,j] = 5
            elif y[i,j] == 2:
                    y[i,j] =6     
            elif y[i,j] == 3:
                    y[i,j] = 4
            elif y[i,j] == 4:
                    y[i,j] = 3
            elif y[i,j] == 5:
                    y[i,j] = 1
            elif y[i,j] == 6:
                    y[i,j] = 2
            elif y[i,j] == 8:
                    y[i,j] = 9
            elif y[i,j] == 9:
                    y[i,j] = 8
    return y

def solve_d4a91cb9(x):
    #Find instance of 8
    #Find instance of 2
    #Draw a vertical line from 8
    #draw a horizontal line from 2   
    y=x.copy()
    posy=0
    for array in y:
        posx=0
        for el in array:
            if str(el) == "8":
                loc = (posy,posx)
            elif str(el) == "2":
                loc2 = (posy,posx)
            posx+=1
        posy+=1
    #To go up or down must compare y coordinate of 8 location against y coordinate of 2 location
    if loc[0] < loc2[0]: #If 8 appears closer to the top of the grid, inputs must move downwards
        num = loc2[0] - loc[0]
        xloc = loc[0]
        for i in range(0,num):
            if loc[0] < loc2[0]:
                xloc = xloc+1    
                y[xloc,loc[1]]=4
        #Move right
        if loc[1] < loc2[1]:
            num2 = loc2[1] - loc[1]
            yloc = loc2[1]
            for i in range(0,num2):
                if loc[1] < loc2[1]:
                    yloc = yloc-1    
                    y[loc2[1]-1,yloc]=4  
        #move left
        if loc[1] > loc2[1]:
            num2 = loc[1] - loc2[1]
            yloc = loc2[1]
            for i in range(0,num2):
                if loc[1] > loc2[1]:
                    yloc = yloc+1    
                    y[loc2[0],yloc]=4
    if loc[0] > loc2[0]:    #Move up instead of down
        num = loc[0] - loc2[0]
        xloc = loc[0]
        for i in range(0,num):
            if loc[0] > loc2[0]:
                xloc = xloc-1    
                y[xloc,loc[1]]=4
        if loc[1] < loc2[1]:    #move right
            num2 = loc2[1] - loc[1]
            yloc = loc[1]
            for i in range(0,num2-1):
                if loc[1] < loc2[1]:
                    yloc = yloc +1
                    y[loc2[0],yloc]=4
        if loc[1] > loc2[1]:    #move left
            num2 = loc[1] - loc2[1]
            yloc = loc2[1]
            for i in range(0,num2-1):
                if loc[1] > loc2[1]:
                    yloc = yloc -1
                    y[loc2[0],yloc]=4          
    return y

def solve_c3f564a4(x):
    y=x.copy()
    length = np.shape(y)
    #need to find a row with no 0's
    #Can then use that row to find what comes next by checking the cell to the left or right
    #If blank cell, check cell to the left, if thats blank check cell to the right, if blank keep moving until a non blank is found
    #if blank cell and cell to left = number find number in row and change blank cell to next number
    #if blank cell and cell to right = number, find number in row and change blank cell to previous number
    pattern = []
    for row in y:
        flag = 0
        for el in row:
            if el == 0:
                flag=1
        if flag == 0:
            pattern = row
    
    for i in range(0,length[0]):
        for j in range(0,length[1]):
            if y[i,j] == 0:
                if y[i-1,j] != 0:
                    numToFind = y[i-1,j]
                    #find the number after numtofind in pattern
                    for num in range(0,len(pattern)-1):
                        if pattern[num] == numToFind:
                            y[i,j] = pattern[num+1]
    return y



def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": main()

