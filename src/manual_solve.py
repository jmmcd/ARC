#!/usr/bin/python
"""
NUI Galway CT5132 Programming and Tools for AI - Assignment 3

By writing our names below and submitting this file, we declare that
all additions to the provided manual_solve.py skeleton file are our own work,
and that we have not seen any work on this assignment by another student/group.

Student name(s): Kalyani Prashant Kawale, Apoorva Patil
Student ID(s): 21237189, <Apoorva Student ID>

Link to GitHub Repo: https://github.com/Kalyani011/ARC
"""
import os, sys
import json
import numpy as np
import re


def get_consecutive_num(arr):
    """
    Method to get indices of second number in a pair of consecutive numbers
    Note: solve_90f3ed37 uses this function
    """
    rows = []
    for i in range(len(arr) - 1):
        if (arr[i] + 1) == arr[i + 1]:
            rows.append(arr[i + 1])
    return rows


def rm_elements(arr, remove_rows):
    """
    Method to remove elements given in a list from an numpy array
    Note: solve_90f3ed37 uses this function
    """
    for element in remove_rows:
        arr = arr[arr != element]
    return arr


def solve_90f3ed37(x):
    """
    This method solves the task given in 90f3ed37.json file.
    Task Description:
    Given a grid of size 15x10 (All train and test samples had the same size),
    with cells colored in either black (0), blue (1) or cyan (8) colors,
    identify the pattern created by cyan colored cells across one or multiple rows,
    and apply the pattern to partially cyan color filled cells appearing below the pattern.
    The rows with the pattern to be applied are always above all incompletely colored cells.
    All the colored rows are separated by one or more rows of all black cells.

    # RESULT: This method solves all 4 train (3) and test (1) grids successfully
    """
    # getting indices of all rows consisting of only black(0) cells
    zero_indices = np.array([i for i in range(len(x)) if list(x[i, :]) == [0] * len(x[i, :])])
    # removing consecutive all black rows from zero_indices to maintain a single line of separation
    zero_indices = rm_elements(zero_indices, get_consecutive_num(zero_indices))

    # fetching the solution pattern for the grid
    pattern = x[zero_indices[0] + 1: zero_indices[1], :]

    # removing all zero(black) rows if any were fetched in the pattern
    indices = np.array([i for i in range(len(pattern)) if np.all(pattern[i] == 0, axis=0)])
    pattern = np.delete(pattern, indices.astype(int), axis=0)
    pattern_size = pattern.shape[0]

    # fetching all the rows with one or more colored cells from the grid
    rows_to_transform = [i for i in range(len(x)) if list(x[i, :]) != [0] * len(x[i, :])]
    # removing the rows containing the solution pattern from rows to be transformed
    to_transform = np.array(rows_to_transform[pattern_size:])
    # removing consecutive rows from to_transform to only contain starting row for drawing patterns
    to_transform = rm_elements(to_transform, get_consecutive_num(to_transform))

    # for each starting row in to_transform complete the pattern
    for start in to_transform:
        # setting the index of row where pattern ends
        end = start + pattern_size
        # getting rows where pattern is to be drawn
        chunk = np.copy(x[start:end, :])
        # shift flag checks if cells need to be shifted to fit pattern correctly
        shift = False
        # setting the shift flag to true if
        # for any row in pattern the corresponding row to be filled has more colored items
        # example: training first sample and test sample
        for i in range(len(pattern)):
            colored_pattern = len(pattern[i][pattern[i] != 0])
            colored_x = len(chunk[i][chunk[i] != 0])
            if colored_x > colored_pattern:
                shift = True
                break
        # getting the cells to be colored blue by subtracting sub-grid from pattern
        # if cells are to be shifted, processing the chunks to fit the pattern
        # and reconstruct the sub-grid
        if shift:
            chunk = np.delete(chunk, 0, 1)  # removing the first column initially
            col = np.zeros(chunk.shape[0])
            chunk = np.concatenate([chunk, col.reshape(-1, 1)], axis=1).astype(int)
            chunk = pattern - chunk  # fitting the pattern
            chunk = np.delete(chunk, -1, axis=1)
            # re - adding the first column
            chunk = np.concatenate((np.zeros(len(chunk)).astype(int).reshape(-1, 1), chunk), axis=1)
        else:
            chunk = pattern - chunk  # fitting the pattern
        # setting the color of newly added colored items in incomplete patterns to blue (1)
        for index in np.argwhere(chunk == 8):
            x[start:end, :][index[0], index[1]] = 1
    return x


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

