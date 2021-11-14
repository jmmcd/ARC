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

# ------------------------------------------------------------------------------------------

# solving task bdad9b1f

def solve_bdad9b1f(x):
    new_grid = np.copy(x)
    # get the index and colour of the vertical and horizontal row start pixel
    vertical = locate_index_and_colour(new_grid[0])
    horizontal = locate_index_and_colour([row[0] for row in new_grid])

    # if no pixels found in the left row check the right
    if horizontal[1] == -1:
        horizontal = locate_index_and_colour([row[len(new_grid)-1] for row in new_grid])

    # draw the horizontal and vertical line at correct index with correct colour
    draw_line(vertical[0], vertical[1], "vertical", new_grid)
    draw_line(horizontal[0], horizontal[1], "horizontal", new_grid)
    # draw the correct colour pixel where the two lines intersect and return
    return draw_intersection(vertical[0], horizontal[0], new_grid)

# takes a row or column as input and returns the colour and location of the start pixel
# if none found return -1 for both
def locate_index_and_colour(data_list):
    for i, y in enumerate(data_list):
        if y != 0:
            return [i, y]
    return [-1, -1]

# draws a line in a grid given the index, axis colour and grid
def draw_line(index, colour, axis, grid):
    line = np.full(len(grid[0]), colour)
    if axis == "horizontal":
        grid[index, :] = line
    elif axis == "vertical":
        grid[:, index] = line
    return grid

# draws the correct colour pixel at the intersection of the two lines
# given the vertical and horizontal index and the grid
def draw_intersection(vertical_index, horizontal_index, grid):
    grid[horizontal_index, vertical_index] = 4
    return grid

# ------------------------------------------------------------------------------------------

# solving task 780d0b14

def solve_780d0b14(x):
    return x

# ------------------------------------------------------------------------------------------

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
    if y.shape != yhat.shape:
        print(f"False. Incorrect shape: {y.shape} v {yhat.shape}")
    else:
        print(np.all(y == yhat))


if __name__ == "__main__": main()

