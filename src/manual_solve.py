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
    new_grid = np.copy(x)
    # find divides on each axis
    horizontal = locate_divides(new_grid, "horizontal", 0)
    vertical = locate_divides(new_grid, "vertical", 0)
    # find and return all square colours in the correct format
    return identify_colour_of_each_section(horizontal, vertical, new_grid)


# find the divides represented by full rows or columns of zeros given
# the grid and axis to search (vertical or horizontal)
def locate_divides(grid, axis, divide_colour):
    divide_indexes = np.array([])
    if axis == "horizontal":
        divide = np.full(len(grid[0, :]), divide_colour)
        for i, row in enumerate(grid):
            if (row == divide).all():
                divide_indexes = np.append(divide_indexes, i)
        # add the end as a divide
        divide_indexes = np.append(divide_indexes, len(grid[:, 0]))
    elif axis == "vertical":
        divide = np.full(len(grid[:, 0]), divide_colour)
        for i, column in enumerate(grid.T):
            if (column == divide).all():
                divide_indexes = np.append(divide_indexes, i)
        # add the end as a divide
        divide_indexes = np.append(divide_indexes, len(grid[0, :]))

    return divide_indexes


# method returns the colours and locations, given the grid, vertical and horizontal divides
def identify_colour_of_each_section(horizontal_divides, vertical_divides, grid):
    colours = []
    # for each horizontal divide
    for h in horizontal_divides:
        row_colours = []
        # for each vertical divide, search for the colour within the given bounds
        # of the square while it is not found
        for v in vertical_divides:
            found_colour = False
            counter = 0
            while not found_colour:
                counter += 1
                current = grid[int(h)-counter][int(v)-1]
                if current != 0:
                    # save the found colour on this square in this row then
                    # move on to the next divide on this line
                    row_colours = np.append(row_colours, current)
                    found_colour = True
        # once all square colours identified on a horizontal section, append this to the colours
        # and move down to the next row of large squares
        colours.append(row_colours)

    # return all found colours as a np array
    return np.array(colours, int)

# ------------------------------------------------------------------------------------------

# solving task 780d0b14


def solve_6773b310(x):
    new_grid = np.copy(x)
    # find divides on each axis
    horizontal = locate_divides(new_grid, "horizontal", 8)
    vertical = locate_divides(new_grid, "vertical", 8)
    # if number of colour squares in a subgrid is greater than one, mark that subgrid with a blue pixel
    return subgrid_colour_pixel_count(horizontal, vertical, new_grid)


# method returns a grid of blue pixels, each occurrence representing more than one colour pixel in that subgrid
def subgrid_colour_pixel_count(horizontal_divides, vertical_divides, grid):
    colours = []
    # for each horizontal divide
    for h in horizontal_divides:
        output_grid = []
        # for each vertical divide, search for colour pixels within given bounds of the square and count them
        for v in vertical_divides:
            row_counter = 0
            colour_count = 0
            while row_counter < 3:
                row_counter += 1
                line_counter = 0
                while line_counter < 3:
                    line_counter += 1
                    current = grid[int(h)-line_counter][int(v)-row_counter]
                    if current == 6:
                        # if colour found, increment counter
                        colour_count += 1
            if colour_count > 1:
                output_grid = np.append(output_grid, 1)
            else:
                output_grid = np.append(output_grid, 0)

        # once all colours counted in a row, update the output grid
        # and move down to the next row of sub grids
        colours.append(output_grid)

    # return all found colours as a np array
    return np.array(colours, int)

# ------------------------------------------------------------------------------------------

# solving task 54d82841


def solve_54d82841(x):
    new_grid = np.copy(x)

    # getting width and height of input grid
    grid_width = len(new_grid[0, :])
    grid_height = len(new_grid[:, 0])

    marked_x_locations = []

    # for each row and pixel calculate the current pixel colour and the colour of the pixel
    # above and below. Then if a coloured pixel has a black pixel above or below it
    # mark that x location and draw a yellow pixel at the bottom of the grid at that x position
    for row in range(grid_height):
        for y in range(grid_width):
            pixel_above = 0
            pixel_below = 0
            current_pixel = new_grid[row][y]

            # if the above or below pixel is off the grid consider it black
            if row - 1 >= 0:
                pixel_above = new_grid[row - 1][y]
            if row + 1 < grid_height:
                pixel_below = new_grid[row + 1][y]

            # rule check for deciding whether to save x location
            if pixel_below == 0 and pixel_above == 0 and current_pixel != 0:
                marked_x_locations = np.append(marked_x_locations, y)

    # iterate over saved x locations and use them to draw the yellow pixels
    for marked in marked_x_locations:
        new_grid[grid_height-1][int(marked)] = 4

    # return input grid with yellow pixels added
    return new_grid


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

