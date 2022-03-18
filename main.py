# Terminology
# cell is space for single number
# row, column self explanatory
# each row has 9 cell
# box is a 3 x 3 grid of cells

# Numbers can be entered at runtime, or by hardcoding
# Exports two files

# Global Section -------------------------------------------------------------------------------
# defining grids for use by all functions
rows, cols = 9, 9
# single digit grid
fullgrid = [["-" for x in range(rows)]for y in range(cols)]

# use an array to show the potential values of each cell
# array for each cell, with ten digits
# first digit is a check digit, = total potential values of a cell
# if first digit  = -1, cell is filled
potentialgrid = [[[9, 1, 1, 1, 1, 1, 1, 1, 1, 1] for x in range(rows)]for y in range(cols)]
backup_grids = []

guesses = 0
resets = 0

sub_guesses = 0
# ---------------------------------------------------------------------------------------------

import time

class grid_range():
   # defines a range from start row & col, to end row & col
   def __init__(self, startrow, startcol, endrow, endcol):
       self.startrow = startrow
       self.startcol = startcol
       self.endrow = endrow
       self.endcol = endcol


def get_range(num):
   """
   given a box number, returns the range of that box
   """
   if num < 4:
       startRow = 0
       endRow = 2
   elif num < 7:
       startRow = 3
       endRow = 5
   else:
       startRow = 6
       endRow = 8

   if num % 3 == 0:
       startCol = 6
       endCol = 8
   elif (num + 1) % 3 == 0:
       startCol = 3
       endCol = 5
   else:
       startCol = 0
       endCol = 2

   ref_range = grid_range(startRow, startCol, endRow, endCol)
   return ref_range


def get_box_ref(row, col):
   if col + 1 <= 3:
       basebox = 1
   elif col + 1 <= 6:
       basebox = 2
   else:
       basebox = 3

   if row + 1 <= 3:
       box = basebox + 0
   elif row + 1 <= 6:
       box = basebox + 3
   else:
       box = basebox + 6

   return box


def update_potential_array(row, col, digit):
   if digit < 1 or digit > 9:
       # print("Invalid digit")
       return
   if check_total_poss(potentialgrid[row][col]) < 2:
       # print("Cell has 1 or less possible values")
       return
   if check_potential(potentialgrid[row][col], digit):
       potentialgrid[row][col][digit] = 0
       potentialgrid[row][col][0] -= 1


def check_potential(poss_array, digit):
   if poss_array[digit] == 0:
       return False
   if poss_array[digit] == 1:
       return True


def check_total_poss(poss_array):
   if poss_array[0] == -1:
       return -1
   total = 0
   for x in range(1, 10):
       if poss_array[x] == 1:
           total += 1
   return total


def reset_potential_grid():
   global potentialgrid
   potentialgrid = [[[9, 1, 1, 1, 1, 1, 1, 1, 1, 1] for x in range(rows)]for y in range(cols)]


def update_potential_grid():
   changes = False
   for row in range(9):
       for col in range(9):
           if fullgrid[row][col] != "-":
               if potentialgrid[row][col][0] > -1:
                   digit = fullgrid[row][col]
                   potentialgrid[row][col][0] = -1
                   changes = True
                   for x in range(1, 10):
                       potentialgrid[row][col][x] = 0
                   for allrows in range(9):
                       update_potential_array(allrows, col, digit)
                   for allcols in range(9):
                       update_potential_array(row, allcols, digit)
                   box_range = get_range(get_box_ref(row, col))
                   for boxrows in range(box_range.startrow, box_range.endrow + 1):
                       for boxcols in range(box_range.startcol, box_range.endcol + 1):
                           update_potential_array(boxrows, boxcols, digit)
   return changes


def return_single_option(poss_array):
   for digits in range(1, 10):
       if poss_array[digits] == 1:
           return digits


def find_single_possibilities():
   changes = False
   for rows in range(9):
       for cols in range(9):
           if potentialgrid[rows][cols][0] == 1:
               fullgrid[rows][cols] = return_single_option(potentialgrid[rows][cols])
               update_potential_grid()
               changes = True
   return changes


def check_cell_only_home():
   changes = False
   for digits in range(1, 10):

       # rows
       for rows in range(9):
           total = 0
           cell_row = -1
           cell_col = -1
           for cols in range(9):
               if potentialgrid[rows][cols][digits] == 1:
                   total += 1
                   cell_row = rows
                   cell_col = cols
           if total == 1:
               fullgrid[cell_row][cell_col] = digits
               update_potential_grid()
               # print("Updating row", rows)
               changes = True

       # cols
       for cols in range(9):
           total = 0
           cell_row = -1
           cell_col = -1
           for rows in range(9):
               if potentialgrid[rows][cols][digits] == 1:
                   total += 1
                   cell_row = rows
                   cell_col = cols
           if total == 1:
               fullgrid[cell_row][cell_col] = digits
               update_potential_grid()
               # print("Updating col", cols)
               changes = True

       # boxes
       for boxes in range(1, 10):
           total = 0
           cell_row = -1
           cell_col = -1
           box_range = get_range(boxes)
           for rows in range(box_range.startrow, box_range.endrow + 1):
               for cols in range(box_range.startcol, box_range.endcol + 1):
                   if potentialgrid[rows][cols][digits] == 1:
                       total += 1
                       cell_row = rows
                       cell_col = cols
           if total == 1:
               fullgrid[cell_row][cell_col] = digits
               update_potential_grid()
               # print("Updating box", boxes)
               changes = True

   return changes


def create_backup_grid():
   placeholderGrid = [["-" for x in range(9)] for y in range(9)]
   for rows in range(9):
       for cols in range(9):
           placeholderGrid[rows][cols] = fullgrid[rows][cols]
   return placeholderGrid


def restore_backup(grid):
   for rows in range(9):
       for cols in range(9):
           fullgrid[rows][cols] = grid[rows][cols]
   reset_potential_grid()
   update_potential_grid()


def guess():
   global guesses
   global resets
   global backup_grids
   if check_completed():
       print("No Guesswork")
       return
   if not find_single_possibilities() and not check_cell_only_home():
       for potentials in range(2, 9):
           for rows in range(9):
               for cols in range(9):
                   if potentialgrid[rows][cols][0] == potentials:
                       for digits in range(1, 10):
                           if check_potential(potentialgrid[rows][cols], digits):
                               backup_grids.append(create_backup_grid())
                               guesses += 1
                               fullgrid[rows][cols] = digits
                               #print("Guess", guesses, "putting", digits, "in", rows, cols)
                               update_potential_grid()
                               if solver():
                                   return
                               else:
                                   if not sub_guess():
                                       resets += 1
                                       # print("Grid before reset:")
                                       # export_potentials()
                                       # print_full_grid(fullgrid)
                                       restore_backup(backup_grids.pop())
                                   continue


def sub_guess():
   global sub_guesses
   global resets
   worked = False
   sub_guess_backup = create_backup_grid()
   if not find_single_possibilities() and not check_cell_only_home():
       for potentials in range(2, 9):
           for rows in range(9):
               for cols in range(9):
                   if potentialgrid[rows][cols][0] == potentials:
                       for digits in range(1, 10):
                           if check_potential(potentialgrid[rows][cols], digits):
                               sub_guesses += 1
                               print("SubGuess", sub_guesses, "putting", digits, "in", rows, cols)
                               fullgrid[rows][cols] = digits
                               update_potential_grid()
                               if solver():
                                   print("Sub guesses:", sub_guesses)
                                   return True
                               else:
                                   resets += 1
                                   restore_backup(sub_guess_backup)
                                   continue
   return worked


def eliminate():
   # In boxes with 2/3 boxes left empty, in single row / column, we can rule their potential values out from the rest
   # of the row / column
   for boxes in range(1, 10):
       box_range = get_range(boxes)
       started = False
       common_row = True
       common_col = True
       ref_row = 0
       ref_col = 0
       remaining_array = [9, 1, 1, 1, 1, 1, 1, 1, 1, 1]
       for rows in range(box_range.startrow, box_range.endrow + 1):
           for cols in range(box_range.startcol, box_range.endcol + 1):
               if fullgrid[rows][cols] == "-":
                   if not started:
                       ref_row = rows
                       ref_col = cols
                       started = True
                   else:
                       if rows != ref_row:
                           common_row = False
                       if cols != ref_col:
                           common_col = False
               else:
                   remaining_array[fullgrid[rows][cols]] = 0
                   remaining_array[0] -= 1
       if 1 < remaining_array[0] < 4:
           if common_row:
               for x in range(1, 10):
                   if remaining_array[x] == 1:
                       for all_cols in range(9):
                           if get_box_ref(ref_row, all_cols) != boxes:
                               update_potential_array(ref_row, all_cols, x)
           if common_col:
               for x in range(1, 10):
                   if remaining_array[x] == 1:
                       for all_rows in range(9):
                           if get_box_ref(all_rows, ref_col) != boxes:
                               update_potential_array(all_rows, ref_col, x)
   # while(find_single_possibilities()):
       # find_single_possibilities()


def solver():
   solved = False
   while (check_cell_only_home()):
       while(find_single_possibilities()):
           find_single_possibilities()
           check_cell_only_home()
           eliminate()
   if check_completed():
       solved = True
   return solved


def check_completed():
   completed = True
   for rows in range(9):
       for cols in range(9):
           if fullgrid[rows][cols] == "-":
               completed = False
   if completed:
       if check_accuracy():
           print("Solved!")
           return True
       print("Full. but not correct")
       return False
   return completed


def check_accuracy():
   accurate = True
   # Need to include check for non numerical values / or only run when all cells filled
   check = 45
   for rows in range(9):
       total = 0
       for cols in range(9):
           total += fullgrid[rows][cols]
       if total != check:
           accurate = False
           # print("Issue with row", rows, total)

   for cols in range(9):
       total = 0
       for rows in range(9):
           total += fullgrid[rows][cols]
       if total != check:
           accurate = False
           # print("Issue with col", cols, total)

   for boxes in range(1, 10):
       box_range = get_range(boxes)
       total = 0
       for rows in range(box_range.startrow, box_range.endrow + 1):
           for cols in range(box_range.startcol, box_range.endcol + 1):
               total += fullgrid[rows][cols]
       if total != check:
           accurate = False
           # print("Issue with box", boxes, total)

   return accurate


def export_csv():
   export_string = ""
   for rows in range(9):
       for cols in range(9):
           export_string = export_string + str(fullgrid[rows][cols])
           if cols < 8:
               export_string = export_string + ","
       export_string = export_string + "\n"
   full_file = open("export_grid.txt", "w")
   full_file.write(export_string)
   full_file.close()


def export_potentials():
   potential_string = ""
   for rows in range(9):
       for cols in range(9):
           if fullgrid[rows][cols] != "-":
               potential_string = potential_string + str(fullgrid[rows][cols])
           else:
               for digits in range(1, 10):
                   if check_potential(potentialgrid[rows][cols], digits):
                       potential_string = potential_string + str(digits) + "|"
           if cols < 8:
               potential_string = potential_string + ","
       potential_string = potential_string + "\n"
       full_file = open("export_potentials.txt", "w")
       full_file.write(potential_string)
       full_file.close()


def print_potentials():
   for x in range(9):
       for y in range(9):
           print(potentialgrid[x][y], end=" ")
           if (y + 1) % 3 == 0:
               print("|", end="")
           if y == 8:
               print()
       if (x + 1) % 3 == 0:
           print ("-" * 35)


def print_full_grid(grid):
   print("-" * 25)
   for row in range(9):
       print("| ", end="")
       for col in range(9):
           print(grid[row][col], end=' ')
           if (col + 1) % 3 == 0:
               print("| ", end="")
       print("")
       if (row + 1) % 3 == 0:
           print("-" * 25)
   print()


def assign_starting_numbers():
   # hard coding example for testing
   fullgrid[0][0] = 5
   fullgrid[0][1] = 3
   fullgrid[0][4] = 7

   fullgrid[1][0] = 6
   fullgrid[1][3] = 1
   fullgrid[1][4] = 9
   fullgrid[1][5] = 5

   fullgrid[2][1] = 9
   fullgrid[2][2] = 8
   fullgrid[2][7] = 6

   fullgrid[3][0] = 8
   fullgrid[3][4] = 6
   fullgrid[3][8] = 3

   fullgrid[4][0] = 4
   fullgrid[4][3] = 8
   fullgrid[4][5] = 3
   fullgrid[4][8] = 1

   fullgrid[5][0] = 7
   fullgrid[5][4] = 2
   fullgrid[5][8] = 6

   fullgrid[6][1] = 6
   fullgrid[6][6] = 2
   fullgrid[6][7] = 8

   fullgrid[8][4] = 8
   fullgrid[8][7] = 7
   fullgrid[8][8] = 9


def populate_grid():
   print("Please enter the starting values")
   print("If a cell is blank, enter -")
   for rows in range(9):
       for cols in range(9):
           input_string = "Enter value for cell (" + str(rows) + "," + str(cols) + ")"
           valid = False
           while not valid:
               value = input(input_string)
               if value == "-":
                   value = str(value)
                   valid = True
               elif value.isnumeric():
                   if int(value) > 0 and int(value) < 10:
                       value = int(value)
                       valid = True
               if not valid:
                   print("Please enter either a digit from 1 - 9, or a dash '-'")
           fullgrid[rows][cols] = value
   update_potential_grid()


def main():
   populate_grid() # Uncomment this to enter values by prompt
   ticks_at_start = time.time()
   # assign_starting_numbers() # Uncomment this to enter values hardcoded
   update_potential_grid()
   export_potentials()

   print_full_grid(fullgrid)
   print_potentials()

   if not solver():
       print_full_grid(fullgrid)
       print_potentials()
       guess()

   print_full_grid(fullgrid)
   print_potentials()

   export_csv()
   export_potentials()

   if guesses != 0:
       print("Guesses:", guesses, " SubGuesses:", sub_guesses, " Resets:", resets)

   ticks_at_end = time.time()
   duration = ticks_at_end - ticks_at_start
   print("Solving took", duration, "seconds")


main()
