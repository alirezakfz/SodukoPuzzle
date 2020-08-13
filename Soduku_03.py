# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 03:12:48 2020

@author: Admin
"""

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

#Sample Case
grid='..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

# `grid` is defined in the test code scope as the following:
# (note: changing the value here will _not_ change the test code)
# grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

#def grid_values(grid):
#    """Convert grid string into {<box>: <value>} dict with '.' value for empties.
#
#    Args:
#        grid: Sudoku grid in string form, 81 characters long
#    Returns:
#        Sudoku grid in dictionary form:
#        - keys: Box labels, e.g. 'A1'
#        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
#    """
#    
#    #return dict((key,value) for key,value in zip(boxes,grid))
#    #solution
#    #assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
#    #return dict(zip(boxes, grid))
#      
#    pass




def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    #Solution
#    values = []
#    all_digits = '123456789'
#    for c in grid:
#        if c == '.':
#            values.append(all_digits)
#        elif c in all_digits:
#            values.append(c)
#    assert len(values) == 81
#    return dict(zip(boxes, values))

    items=dict()
    
    for i in range(len(grid)):
        key=boxes[i]
        if grid[i] == '.':
            value='123456789'
        else:
            value=grid[i]
        items[key]=value
    
    return items
    pass


#test the functions
#test=grid_values(grid)
#display(test)
#display(grid_values(grid))

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
        
    """
    
    #Solution
#    solved_values = [box for box in values.keys() if len(values[box]) == 1]
#    for box in solved_values:
#        digit = values[box]
#        for peer in peers[box]:
#            values[peer] = values[peer].replace(digit,'')
#    return values
    #Check all the boxes and select boxes with len == 1
    select=dict()
    
    for v in values:
        if len(values[v])==1:
            key=v
            value=values[v]
            select[key]=value
        
    for v in select:
        key=v
        value=select[v]
        for p in peers[key]:
            if len(values[p]) > 1 :
                temp=values[p]
                temp=temp.replace(value,'')
                values[p]=temp           
        
    return values        
    pass


#print('\n*******************************************\n')
#el=eliminate(test)
#display(el)
#display(eliminate(grid_values(grid)))


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    #Solution
#    for unit in unitlist:
#        for digit in '123456789':
#            dplaces = [box for box in unit if digit in values[box]]
#            if len(dplaces) == 1:
#                values[dplaces[0]] = digit
    
    # TODO: Implement only choice strategy here
    for boxs in square_units:
        freq={}
        for box in boxs:
            if len(values[box]) > 1:
                value=values[box]
                for v in value: #count the number of occurances
                    if v in freq:
                        freq[v]+=1
                    else:
                        freq[v]=1
        unique=[]
        for f in freq:
            if freq[f]==1:
                unique.append(f)
        
        for box in boxs:
            if len(values[box]) > 1:
                value=values[box]
                for u in unique:
                    if u in value:
                        value=u
                        values[box]=value
            
    return values

#print('\n*******************************************\n')
#choice=only_choice(el)
#display(choice)


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values=eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values=only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
#    values=reduce_puzzle(values)
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    select={box:len(values[box]) for box in values.keys() if len(values[box]) > 1 }
    
#    if not bool(select):
#        return values
    
    min_len=min(select, key=select.get)
    
#    print('\nThe input soduko to search is')
#    display(values)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for v in values[min_len]:
        temp=values.copy()
        temp[min_len]=v
        attempt=search(temp)
        if attempt:
            return attempt
#        print('\n The Temporary seach soduku is:\n')
#        display(temp)

    # If you're stuck, see the solution.py tab!
    
    









values=grid_values(grid)
result=search(values)
print('\n******************************************************')
print('\n******************************************************')
display(result)


    
#New Puzzle
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
values = grid_values(grid2)
result=search(values)
print('\n******************************************************')
print('\n******************************************************')
display(result)

