#!/usr/bin/python

import os, sys
import json
import numpy as np
import re
import copy
import collections

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.

#Colors
color_dict = {
            "black":0,
            "blue":1,
            "red":2,
            "green":3,
            "yellow":4,
            "gray":5,
            "pink":6,
            "orange":7,
            "turquoise":8,
            "maroon":9
            }

#If the colour of first cell matches the last cell of the row,
# Then colour the entire row to the same colour
def solve_22eb0ac0(x):
    for i in x:
        #if start cell of row matches last cell of row, then connect them
        if(i[0] != 0 and i[0] == i[-1]):
            i[True] = i[0]
    return x

#Divide the input grid into 9 sub blocks
#Then copy the pattern in the first sub-block to rest of the 8 blocks
def solve_1e32b0e9(x):
    #Method to draw the shape 
    def re_shape(x1,x2,y1,y2):
        q = x[x1:x2,y1:y2].reshape(25)
        
        for i in range(25):
            if(a[i] != q[i]):
                q[i] = grid_col
        
        q = q.reshape(5,5)
        output[x1:x2,y1:y2] = q
    
    #Get the first sub-block
    a = x[0:5,0:5]
    
    #Flatten 
    a = a.reshape(25)
    
    #Get the colour of the block border
    grid_col = x[0,5]
    
    #Make a copy of the input grid
    output = copy.deepcopy(x)
    
    #Change the colour of all subblocks to black
    output[output !=grid_col] = 0
    
    #Iterate through all the sub-blocks and call re_shape to draw the pattern
    r_start = -6
    r_end= -1
    for bigrow in range(3):
        r_start = r_start + 6
        r_end = r_end + 6 
        c_start = -6
        c_end = -1
        for bigcol in range(3):
            if(bigrow==0 and bigcol==0): #if its the first sub-block, dont do anything
                c_start = c_start + 6
                c_end = c_end + 6
                continue
            c_start = c_start + 6
            c_end = c_end + 6
            re_shape(r_start,r_end,c_start,c_end)
    
    #Copy the first sub-block from input to output
    output[0:5,0:5] = x[0:5,0:5]         
    return output

#Get the smallest 4 sided shape
#Works by finding all the 4 sided shapes of different colours
#And then, returning the one with smallest size
def solve_23b5c85d(x):
    #Method to check if given shape is a rectangle
    def is_rect(colour,x):
        z = copy.deepcopy(x) #Make a copy of original grid
        z[z != colour] = -1  #Replace all the values with -1 that are of a different color
        pos = np.where(x == z) #Get positions where the shape is present in original grid
        
        #Get size of all rows and columns
        rows = collections.Counter(pos[0])
        cols = collections.Counter(pos[1])
        
        row_val = list(rows.values())[0]
        col_val = list(cols.values())[0]
        
        #Check if size of all the rows and columns is same
        #If not, then the shape has more than 4 sides,so discard it
        for v in rows.values():
            if(v != row_val):
                return False
        for v in cols.values():
            if(v != col_val):
                return False
        
        #Return the size of rows and columns
        return (col_val,row_val)

    uni_cols = np.unique(x)     #Get all the unique colours in the grid
    s=np.delete(uni_cols, 0)    #Delete the color black
    size = { k:0 for k in s}    #Initiate a dictionary for storing sizes of different shapes
    shape = { k:0 for k in s}   #Dictionary to store shapes of different colors
    
    for colour in uni_cols:     #Iterate through all colours
        val_rect = is_rect(colour,x)    #Check if the shape is four sided
        if(val_rect != False):          
           size[colour] = val_rect[0] * val_rect[1] # Get size of the shape
           shape[colour] = val_rect    #Store the shape
    
    #Remove shapes with size 0
    size_dict = { k:v for k,v in size.items() if v > 0} 
    
    min_size = min(size_dict, key=size.get)
    
    #Get shape with minimum size
    shapex = shape[min_size]
    
    #Draw the grid with shape
    output = np.full(shapex,min_size)
    return output   

#This method works by dividing the input grid into 9 smaller 3x3 blocks
#And then iterating through each one to find the block with highest black cells
# Finally, replicate the colors in that block onto a output grid with size of the input
def solve_09629e4f(x):
    max_black = 0
    chosen_block = []
    colour_pattern = []
    
    #Counts the number of black cells
    def count_black(x1,x2,y1,y2,counter=0):
        nonlocal max_black
        nonlocal chosen_block
        nonlocal colour_pattern
        
        #Convert the array to 1D
        q = x[x1:x2,y1:y2].reshape(9)
        
        #Get all the colors present and their count
        cols = collections.Counter(q)
        
        #If number of black cells is greater than existing best
        #Save the block
        if cols[0] > max_black:
            max_black = cols[0]
            chosen_block = [x1,x2,y1,y2]
            colour_pattern = q
    
    #Method to colour the sub-blocks based on block number
    def colouring(x1,x2,y1,y2,counter):
        q = x[x1:x2,y1:y2].reshape(9)
       
        for i in range(9):
              q[i] = colour_pattern[counter]
        q = q.reshape(3,3)
        output[x1:x2,y1:y2] = q
    
    #Method to traverse through the grid
    def grid_traversal(f):
        r_start = -4
        r_end= -1
        counter = -1
        for bigrow in range(3):
            r_start = r_start + 4
            r_end = r_end + 4 
            c_start = -4
            c_end = -1
            for bigcol in range(3):
                counter += 1
                c_start = c_start + 4
                c_end = c_end + 4
                f(r_start, r_end, c_start, c_end,counter)
    
    #Get color 
    grid_col = x[0,3]
    
    #Make a copy of input Grid
    output = copy.deepcopy(x)
    
    #Make all cells that dont match division color to black
    output[output != grid_col] = color_dict["black"]
    
    #Call grid traversal method to count black cells
    grid_traversal(count_black)
    
    #Recolour
    grid_traversal(colouring)
    
    return output



def solve_6430c8c4(x): 
        #Create a 4x4 grid and fill it with zeroes
        output = np.full((4,4),0)
        
        #Divide the input grid into 2 parts upper and lower
        upper = x[0:4,0:4] 
        lower = x[5:9,0:4]
        
        #Get the positions where they match
        posi_match = np.where(upper == lower)
        
        #Iterate through the positions and color the matched grids with green
        for x,y in zip(posi_match[0],posi_match[1]):
            output[x,y] = color_dict["green"]
        
        return output
        
def solve_a85d4709(x):
    #Initialize an output grid
    output = []
    
    #dictionary with colour and the corresponding recolour for the row
    dict_x = { 0:2 , 1:4 , 2:3 }
    
    #Iterate through each row in input Grid
    for i in range(3):
        f = np.where(x[i]==color_dict["gray"]) #get positions where color is Gray
        color = int(dict_x[f[0][0]]) #Get corresponding recolour
        array = [color]*3  #recolor the row
        output.append(array) #append to our output
    output = np.array(output) #Convert list to np array
    return output



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

