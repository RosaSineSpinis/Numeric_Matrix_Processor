import sys


# Prints a menu consisting of 4 options. The example shows what the menu should look like.
def menu():
    print("1. Add matrices")
    print("2. Multiply matrix by a constant")
    print("3. Multiply matrices")
    print("4. Transpose matrix")
    print("5. Calculate a determinant")
    print("6. Inverse matrix")
    print("0. Exit")


# Reads the user's choice.

def menu_transposition():
    print("1. Main diagonal")
    print("2. Side diagonal")
    print("3. Vertical line")
    print("4. Horizontal line")


def choice():
    choice = input("Your choice:", )
    return choice


# Reads all data (matrices, constants) needed to perform the chosen operation. The example shows the input format in each case.
def read_data():
    rows, cols = [int(x) for x in input().split()]
    matrix = [[float(num) for num in input().split()] for _ in range(rows)]
    return rows, cols, matrix


def print_matrix(matrix):
    print("The result is:")
    for row in matrix:
        for column in row:
            print(column, end=" ")
        print()


# Reads all data (matrices, constants) needed to perform the chosen operation. The example shows the input format in each case.
# Calculates the result and outputs it. The example shows how your output should look like.
# multiplication - read data, check conditions, return porduct
def add_matrixes():
    rows_a, cols_a, matrix_a = read_data()
    rows_b, cols_b, matrix_b = read_data()
    if rows_a == rows_b and cols_a == cols_b:
        matrix_added = [[matrix_a[j][i] + matrix_b[j][i] for i in range(rows_a)] for j in range(cols_a)]
        print_matrix(matrix_added)
    else:
        print("The operation cannot be performed.")


def multiplication_con():
    rows_a, cols_a, matrix_a = read_data()
    con = int(input("Enter constant:", ))
    matrix_multiplied = [[matrix_a[j][i] * con for i in range(len(matrix_a[0]))] for j in range(len(matrix_a))]
    print_matrix(matrix_multiplied)

def multiplication_con_to_inverse(matrix_a, rows_a, cols_a, con):
    matrix_multiplied = [[matrix_a[j][i] * con for i in range(len(matrix_a[0]))] for j in range(len(matrix_a))]
    return matrix_multiplied

def multiplication_matrix():
    rows_a, cols_a, matrix_a = read_data()
    rows_b, cols_b, matrix_b = read_data()
    if cols_a == rows_b:
        product_matrix = [[sum(matrix_a[k][i] * matrix_b[i][j] for i in range(cols_a)) for j in range(cols_b)] for k in
                          range(rows_a)]
        print_matrix(product_matrix)
    else:
        print("The operation cannot be performed.")


def trans_main_diagonal():
    rows, cols, matrix = read_data()
    matrix_main_diagonal = [[matrix[i][j] for i in range(len(matrix[0]))] for j in range(len(matrix))]
    print_matrix(matrix_main_diagonal)


def trans_side_diagonal():
    rows, cols, matrix = read_data()
    matrix_side_diagonal = [[matrix[i][j] for i in (range(len(matrix[0])-1, -1, -1))] for j in range(len(matrix)-1, -1, -1)]
    print_matrix(matrix_side_diagonal)


def trans_vertical_line():
    rows, cols, matrix = read_data()
    matrix_vertical_line = [[matrix[j][rows - i-1] for i in range(len(matrix[0]))] for j in range(len(matrix))]
    print_matrix(matrix_vertical_line)


def trans_horizontal_line():
    rows, cols, matrix = read_data()
    matrix_horizontal_line = [[matrix[cols - j-1][i] for i in range(len(matrix[0]))] for j in range(len(matrix))]
    print_matrix(matrix_horizontal_line)

def determinant_recursive(matrix, value=0):
    # Section 1: store indices in list for row referencing
    indices = list(range(len(matrix))) # we can do that because it is square matrix
    # Section 2: when at 2x2 submatrices recursive calls end
    if len(matrix) == 2 and len(matrix[0]) == 2:
        val = matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
        return val
    if len(matrix) == 1:
        for row in matrix:
            for column in row:
                return column

    # Section 3: define submatrix for focus column and
    #      call this function
    for del_col in indices:  # A) for each focus column, ...
        # find the submatrix ...
        copy_matrix = [[matrix[j][i] for i in indices] for j in indices] #make copy
        copy_matrix = copy_matrix[1:]  # ... C) remove the first row
        height = len(copy_matrix)  # D) we check

        for i in range(height):
            # E) for each remaining row of submatrix ...
            #     remove the focus column elements
            copy_matrix[i] = copy_matrix[i][0:del_col] + copy_matrix[i][del_col + 1:]

        sign = (-1) ** (del_col % 2)  # F)
        # G) pass submatrix recursively
        sub_det = determinant_recursive(copy_matrix)
        # H) total all returns from recursion
        value += sign * matrix[0][del_col] * sub_det

    return value
    
    
def cof_matrix(matrix):

    inverse_mat = [[None for row in range(len(matrix))] for col in range(len(matrix))]
    #print("inverse_mat, ", inverse_mat)

    if len(matrix) == 2 and len(matrix[0]) == 2:
        val = matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
        return val
    if len(matrix) == 1:
        for row in matrix:
            for column in row:
                return column

    indices = list(range(len(matrix)))
    for del_row in indices:
        for del_col in indices:

            copy_matrix = matrix
            #print("copy_matrix_full", copy_matrix)
            copy_matrix = [[copy_matrix[j][i] for i in range(len(copy_matrix)) if i != del_col] for j in range(len(copy_matrix))]
            #print("copy_matrix del_col", copy_matrix)

            copy_matrix = copy_matrix[0:del_row][:] + copy_matrix[del_row+1:][:]
            #print("copy_matrix del_row", copy_matrix)
            #print("matrix, ", copy_matrix)

            inverse_mat[del_col][del_row] = determinant_recursive(copy_matrix) * (-1) ** (del_row + del_col)# it has to be multiplied by
            #print("cof, ", (-1) ** (del_row + del_col), " del_row= ", del_row, " del_col ", del_col)
            #print("inverse_mat[del_col][del_row], ", inverse_mat[del_col][del_row])

    return inverse_mat

def inverse_matrix(matrix):
    
    det_matrix = determinant_recursive(matrix)
    if det_matrix == 0:
        return -1
    cof_mat = cof_matrix(matrix)
    cof_mat = multiplication_con_to_inverse(cof_mat, len(matrix), len(matrix), 1 / det_matrix)

    return cof_mat
    
def start_program():
    user_choice = None
    while (user_choice != 0):
        menu()
        user_choice = choice()
        if user_choice == "1":
            add_matrixes()
        elif user_choice == "2":
            multiplication_con()
        elif user_choice == "3":
            multiplication_matrix()
        elif user_choice == "0":
            break
        elif user_choice == "4":
            menu_transposition()
            trans_choice = choice()
            if trans_choice == "1":
                trans_main_diagonal()
            elif trans_choice == "2":
                trans_side_diagonal()
            elif trans_choice == "3":
                trans_vertical_line()
            elif trans_choice == "4":
                trans_horizontal_line()
        elif user_choice == "5":
            rows, cols, matrix = read_data()
            print("The result is:")
            print(determinant_recursive(matrix))
        elif user_choice == "6":
            rows, cols, matrix = read_data()
            print_matrix(inverse_matrix(matrix))
        else:
            print("Wrong input, please choose again")


# Repeats all these steps.

start_program()