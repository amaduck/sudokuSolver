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

# Array of values entered in GUI
entries = []
#Differentiate between values passed to program, and values found by program
passedValues = [[0 for x in range(rows)]for y in range(cols)]

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

# Imports
import time
import tkinter
import tkinter.messagebox
from tkinter import *


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


def check_csv():
    with open("import.csv") as testFile:
        lines = 0
        error_message=""
        for line in testFile:
            lines += 1
            if lines > 9:
                error_message = error_message + "Too many lines - max is 9.\n"
            line = line.strip()
            line = line.split(",")
            if len(line) > 9:
                error_message = error_message + "Line " + str(lines) + " is too long\n"
            for values in line:
                if values != "-":
                    if not values.isnumeric():
                        error_message = error_message + "Line " + str(lines) + " contains non numeric values\n"
                    elif int(values) < 1 or int(values) > 9:
                        error_message = error_message + "Line " + str(lines) + " contains a number out of range\n"
        return (error_message)


def import_csv():
    with open("import.csv") as testFile:
        x = 0
        for line in testFile:
            line = line.strip()
            line = line.split(",")
            for y in range(cols):
                value = line[y]
                print("Value: ", value, " x:",x, " y:",y)
                if value != "-":
                    fullgrid[x][y] = int(value)
                    passedValues[x][y] = 1
            x += 1
    update_potential_grid()


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

   fullgrid[7][3] = 4
   fullgrid[7][4] = 1
   fullgrid[7][5] = 9
   fullgrid[7][8] = 5

   fullgrid[8][4] = 8
   fullgrid[8][7] = 7
   fullgrid[8][8] = 9

   mark_passed()


def mark_passed():
    # The following for loops will mark all coded values as having been passed to program
    for x in range(rows):
        for y in range(cols):
            if fullgrid[x][y] != "-":
                passedValues[x][y] = 1


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

   mark_passed()

   update_potential_grid()


def solve():
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

    show_full_grid(fullgrid, "Solution")

    export_csv()
    export_potentials()

    if guesses != 0:
        print("Guesses:", guesses, " SubGuesses:", sub_guesses, " Resets:", resets)
    else:
        print("No guesses")


def show_full_grid(grid, windowTitle):
    solution = tkinter.Tk()
    solution.title(windowTitle)
    solution.geometry("450x400")

    for x in range(rows):
        if x > 5:
            rowPos = x + 2
        elif x > 2:
            rowPos = x + 1
        else:
            rowPos = x
        for y in range(cols):
            if y > 5:
                colPos = y + 3
            elif y > 2:
                colPos = y + 2
            else:
                colPos = y + 1
            if passedValues[x][y] == 1:
                bgColour = "green"
            else:
                bgColour = "white"
            lab = Label(solution, width=5, bg=bgColour, text=grid[x][y]).grid(row = rowPos, column = colPos)
            # print("x: ",x ,"row: ", rowPos," y: ",y, "Col: ", colPos)

    # Drawing borders
    # Can't get canvas item to stick to grid, so using blank cells
    for i in range(11):
        ent2000 = Entry(solution, width=1, bg="black")
        ent2000.grid(row=i, column = 4)
        ent2001 = Entry(solution, width=1, bg="black")
        ent2001.grid(row=i, column=8)

        if i == 3 or i == 7:
            ent2002 = Entry(solution,  width=1, bg="black")
            ent2003 = Entry(solution, width=1, bg="black")
        else:
            ent2002 = Entry(solution, width=5, bg="black")
            ent2003 = Entry(solution, width=5, bg="black")

        ent2002.grid(row=3, column=i + 1)
        ent2003.grid(row=7, column=i + 1)


def check_cells():
    # Checks entries in GUI to ensure anything entered is in the range 0 < x < 10
    for entry in entries:
        value = entry.get()
        if value != "":
            if not value.isnumeric:
                tkinter.messagebox.showinfo("Error", "Values must be numeric")
                return False
            try:
                value = int(value)
                if value < 1 or value >9:
                    tkinter.messagebox.showinfo("Error","Values must be between 1 and 9")
                    return False
            except Exception as ep:
                tkinter.messagebox.showerror("error", ep)
    return True


def number_entry():
    numberEntry = tkinter.Tk(screenName=None, baseName=None, className="Sudoku Solver", useTk=1)
    numberEntry.title("Sudoku Solver - Enter known numbers")
    numberEntry.geometry("450x400")

    for x in range(rows):
        if x > 5:
            rowPos = x + 2
        elif x > 2:
            rowPos = x + 1
        else:
            rowPos = x
        for y in range(cols):
            if y > 5:
                colPos = y + 3
            elif y > 2:
                colPos = y + 2
            else:
                colPos = y + 1
            ent = Entry(numberEntry, width=5, justify=tkinter.CENTER)
            ent.grid(row = rowPos, column = colPos)
            # combining previous 2 lines into single line (ie ent=Entry().grid()) causes error - not added to entries array
            entries.append(ent)
            # print("x: ",x ,"row: ", rowPos," y: ",y, "Col: ", colPos)


    # Drawing borders
    # Can't get canvas item to stick to grid, so using blank cells
    for i in range(11):
        ent2000 = Entry(numberEntry, width=1, bg="black")
        ent2000.grid(row=i, column = 4)
        ent2001 = Entry(numberEntry, width=1, bg="black")
        ent2001.grid(row=i, column=8)

        if i == 3 or i == 7:
            ent2002 = Entry(numberEntry,  width=1, bg="black")
            ent2003 = Entry(numberEntry, width=1, bg="black")
        else:
            ent2002 = Entry(numberEntry, width=5, bg="black")
            ent2003 = Entry(numberEntry, width=5, bg="black")

        ent2002.grid(row=3, column=i + 1)
        ent2003.grid(row=7, column=i + 1)

    def get_numbers():
        if check_cells():
            entry = 1
            x = 0
            y = 0
            xCounter = 0
            for ent in entries:
                value = ent.get()
                if value == "":
                    value = "-"
                else:
                    value = int(value)
                    passedValues[x][y] = 1

                fullgrid[x][y] = value

                xCounter += 1
                if xCounter >8:
                    x += 1
                    xCounter = 0
                if y > 7:
                    y = 0
                else:
                    y += 1
                entry += 1
            numberEntry.destroy()
            solve()

    btn = Button(numberEntry, text="Solve", width=10, height=5, command=get_numbers)
    btn.place(x=170,y=275)

    numberEntry.mainloop()


def welcome_screen():
    welcomeScreen = tkinter.Tk(screenName=None, baseName=None, className="Sudoku Solver", useTk=1)
    welcomeScreen.title("Sudoku Solver")
    welcomeScreen.geometry("450x200")

    choice = IntVar()
    Radiobutton(welcomeScreen, text='Enter into GUI', variable=choice, value=1).pack(anchor=W)
    Radiobutton(welcomeScreen, text='Import csv', variable=choice, value=2).pack(anchor=W)
    Radiobutton(welcomeScreen, text='Enter at text prompt', variable=choice, value=3).pack(anchor=W)
    Radiobutton(welcomeScreen, text='Use hardcoded values', variable=choice, value=4).pack(anchor=W)

    def get_choice():
        if choice.get() ==1:
            welcomeScreen.destroy()
            number_entry()
        elif choice.get() ==2:
            csv_info = "This imports the 'import.csv' file, and assigns the numbers found.\nFile can only contain numbers and dashes. Check 'CSV_template.csv' to see file format."
            if tkinter.messagebox.askokcancel("CSV", csv_info):
                message = check_csv()
                if message == "":
                    welcomeScreen.destroy()
                    import_csv()
                    solve()
                else:
                    tkinter.messagebox.showinfo("CSV", message)
        elif choice.get() == 3:
            welcomeScreen.destroy()
            populate_grid()
            solve()
        elif choice.get() == 4:
            welcomeScreen.destroy()
            assign_starting_numbers()
            solve()
        else:
            tkinter.messagebox.showinfo("Nothing selected", "Please choose an option")

    btn = Button(welcomeScreen, text="Choose", width=5, height=1, command=get_choice)
    btn.place(x=170, y=100)

    welcomeScreen.mainloop()


def main():
   ticks_at_start = time.time()
   welcome_screen()

   ticks_at_end = time.time()
   duration = ticks_at_end - ticks_at_start
   print("Solving took", duration, "seconds")

main()
