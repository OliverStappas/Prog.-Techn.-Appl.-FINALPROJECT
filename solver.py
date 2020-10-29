"""
Xu Zhe Zhang
1731153
Oliver Stappas
1730124
Maxwell Zhixing Lee
1730320
"""
import copy

VALUE = 0
class matrix(list):
    '''Each matrix object is represented by itself'''
    def __init__(self):
        self.matrix = [] # Original matrix

    def __repr__(self):
        matrix_repr = ""
        dimMatrix = len(self.matrix)
        for j in range(dimMatrix):
            for k in range(dimMatrix):
                
                matrix_repr += "{:<10} ".format(self.matrix[j][k])
                if k == dimMatrix - 1:
                    matrix_repr += "\n"
        return matrix_repr

    def construct_matrix(self, file):
        '''Creates a list-of-lists matrix based on the input file'''
        while True: #  for construction of normal matrix
            line = [i for i in file.readline().strip().split()]
            self.matrix.append(line)
            if line == []:
                self.matrix.pop()
                break

    def x_counter(self):
        '''Counts the number of X's in an input matrix'''
        num_X = 0
        for row in self.matrix:
            num_X += row.count("X")
        return num_X     

    def matrix_(self):
        '''Returns the matrix'''
        return self.matrix       

    def zero_Matrix(self):
        '''Replaces all X's with zeros in matrix if matrix contains only zeros'''
        self.matrix = [[0 for i in range(len(self.matrix))] for i in range(len(self.matrix))]

    def construct_transpose(self, other):
        '''Creates a list-of-lists transpose matrix based on the original matrix'''
        index = 0
        column = [] # Column of input matrix or row of tranpose matrix
        while index != len(self.matrix):  # For the construction of matrix formed according to column (transpose of the matrix)
            for i, row in enumerate(self.matrix):
                column.append(row[index])
                if i == len(self.matrix) - 1:
                    other.matrix.append(column)
                    column = []
            index += 1                           
   
    def convert_int(self):
        '''Converts the number strings in the row and column matrices to integers'''
        for row in range(len(self.matrix)):
            self.matrix[row] = [i if i == "X" else int(i) for i in self.matrix[row]]  # Only convert numbers to integers in the matrix   

    def basic_op(self, row):
        '''Calculates and returns X based on other values in its row or column 
        considering their position in the row or column'''
        if row[0] == "X":  
            new_val = row[1] - (row[2] - row[1]) 
            return int(new_val)
        if row[1] == "X":
            new_val = (row[2] + row[0]) / 2
            return int(new_val)
        if row[2] == "X":
            new_val = (row[1] - row[0]) * 2 + row[0]
            return int(new_val)

    def value_replace(self, other, updated):
        '''Replaces X with a number if this results 
        in X's row and column forming an arithmetic sequence'''
        for row in range(len(self.matrix)):
            if self.matrix[row].count("X") == 1:   # If there is only one x in a row
                val = self.basic_op(self.matrix[row])  # Calculate and return the value of X in the row
                column = self.matrix[row].index("X")  # The position of X that was previously replaced
                self.matrix[row][column] = val  # Replacing X with the new value in the matrix
                other.matrix[column][row] = val  # Replacing X with the new value in the transpose matrix
                updated = True  # Have we performed a basic operation (basic_op)?
        return updated 

    def contains_X(self, contains_x):
        '''Returns whether or not a row in a matrix contains X'''
        for row in self.matrix:
            if "X" in row:
                return True
        return False       

    def add_val(self, other, change):
        '''Adding an arbitrary value to an X when there is no possible way of 
        calculating this X without having additional information'''
        global VALUE
        for index in range(len(self.matrix)): 
            row = self.matrix[index]
            if row.count("X") == len(self.matrix) - 1:  # Additional value will be added to single row that has two X's
                for column in range(len(row)):
                    if row[column] != "X" and column != len(row) - 1:  # If the non-X integer value in the row is
                                                                       # not located in the last column, it adds
                                                                       # the value in the spot ahead of the integer
                        row[column + 1] = row[column] + VALUE
                        other.matrix[column + 1][index] = row[column] + VALUE #By default it will set the already existing value in the row/column as
                        change = True                                         #the "random" value, but it will add 'VALUE' to it if the previous answer didn't work
                        break
                    elif row[column] != "X" and column == len(row) - 1: # If the non-X integer value in the row is 
                                                                        # located in the last column, it adds the 
                        row[column - 1] = row[column] + VALUE                # value in the spot before the integer
                        other.matrix[column - 1][index] = row[column] + VALUE
                        change = True
                        break
                if change:
                    return change
                else:
                    return False

    def set_matrix(self, matrix):
        '''This method takes a matrix and an object so that it can set
           the object's matrix to the one given'''
        self.matrix = matrix
    
    def verifier(self):
        '''Verifies if a matrix's rows follow an arithmetic sequence'''
        for row in self.matrix:
            if row[2] - row[1] == row[1] - row[0]:
                continue
            else:
                return False
        return True

def main_code(grid, grid_2):
    '''This is the main code that makes use of the above functions
       to solve the arithmatic square'''
    updated = False 
    while True:
        updated = grid.value_replace(grid_2, updated)  # Updates the matrix if it can update any of the values 
        updated = grid_2.value_replace(grid, updated)  # through regular calculations and sets updated to True if it could
        contains_x = False  # Indicates whether there are still any X's in the matrix
        contains_x = grid.contains_X(contains_x) # Checks if there are any X's left in the matrix
        if contains_x and not updated:  # This runs if the matrix is not complete and the remaining values could not be calculated
            change = False  # It remains False if it wasn't able to replace a value in the rows of the matrix
            change = grid.add_val(grid_2, change)  # Replaces one of the X's in the row with a "random" value
            if not change:
                grid_2.add_val(grid, change)  # Replaces one of the X's in the column with a "random" value
        if not updated and not contains_x:  # If the matrix is complete
            break
        updated = False
    return grid,grid_2

    
while True:
    file_name = input('''Please enter the input found in all_data downloadable from canadian computing competition problem s3:arithmatic square):''') + ".in"
    file = open(file_name)
    grid = matrix()  # Input matrix represented as a list of lists
    grid_2 = matrix()# Transpose matrix represented as a list of list
    updated = False  # Have we performed a basic operation (basic_op)?
    print(file_name)
    print("\n")
    grid.construct_matrix(file)# Construct the matrix from the input file
    print("original unsolved matrix:")
    print(grid)
    if grid.x_counter() == len(grid.matrix_()) ** 2: # If the entire matrix contains only X
        grid.zero_Matrix() 
        
        
    else:
        grid.construct_transpose(grid_2)  # Constructs the transpose matrix of grid
        
        grid.convert_int()  # Converts all numbers in grid from strings into integers
        
        grid_2.convert_int()  # Converts all numbers in grid_2 from strings into integers
        
        grid_backup = matrix()
        listy = copy.deepcopy(grid.matrix_())  # Creates a backup of the original grid
        grid_backup.set_matrix(listy)          # for later use if a brute force solving
                                               # method is needed
       
        grid_2_backup = matrix()
        listy = copy.deepcopy(grid_2.matrix_())  # Creates a backup of the transpose grid
        grid_2_backup.set_matrix(listy)          # for later use if a brute force solving
                                                 # method is needed

        grid,grid_2 = main_code(grid,grid_2)# Initial attempt to solve the arithmetic square
        
        
    
        while True:
            if not grid.verifier() or not grid_2.verifier(): #This is the brute force method used if the first method does not work
                VALUE += 1  # Increments the "random" value in "add_val" by 1. This is essentially a brute force method       
                listy = copy.deepcopy(grid_backup.matrix_())  # Resets the grids by taking a copy of the backup
                grid.set_matrix(listy)
                listy = copy.deepcopy(grid_2_backup.matrix_())
                grid_2.set_matrix(listy)              
                grid,grid_2 = main_code(grid,grid_2)
            else:
                VALUE = 0
                break
    print("\n")
    print("validity of rows:")
    print(grid.verifier())
    print("\n")
    print("validity of columns:")
    print(grid_2.verifier())
    print("\n")
    print("solved matrix:")
    print(grid)
    print("-------------------------------------------")
