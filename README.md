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

20220320 GUI added - needs more work
1) Using cells in grid as border, would prefer simple lines
2) Entry sizes are much larger than they need to be, also rectangular, would prefer smaller squares
3) Validation will stop text / numbers outside of range, but needs to be smooth - .isnumeric() doesn't seem to be catching anything
4) Option to solve, but not display - click on cell to see value. Values hidden by default (except passed), shown when clicked
5) Make window resizeable - grow cells to fit larger - maybe only resizeable stepwise?

# Changes to make
- Sometimes it just gives up when too many guesses needed - resolve
- Entry for this stored as import.csv.issue - will solve based on these numbers. Adding extra numbers, per import.csv.issueUnsolvable causes it to give up after adding 1 number. Numbers added agree with final solution of .issue, unclear why giving more information causes it to stop.

