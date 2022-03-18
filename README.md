# sudokuSolver
Sudoku solver in python

I wrote this a couple of years ago, with the intention of polishing it, but haven't looked at it since

Given a set of starting numbers, this program will find a solution if it exists

Starting numbers can be hardcoded, or entered in turn at prompt

An array of possible numbers is created for each cell, these are then eliminated in order
first pass will fill in cells with only one possible number etc

After each cell has a value entered, the potential arrays are updated

Some puzzles can be solved entirely in this manner, but some will require a choice to be made
If after entering all values where cells have only single potential number puzzle is still not solved, 
it will make a guess as to next value, and then try to solve again, and repeat until solved


# Changes to make
Give choice on run to use hardcoded numbers or ask for entry
Allow it pull csv file for starting numbers
Sometimes it just gives up when too many guesses needed - resolve
Add GUI for number entry
