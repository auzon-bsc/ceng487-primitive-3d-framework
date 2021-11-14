# CENG 487 Assignment by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

import numpy as np
import math


class Matrix:
    def __init__(self, numbers2D: list) -> None:
        m = len(numbers2D)
        n = len(numbers2D[0])
        matrix_arr = []
        for numbers1D in numbers2D:
            if len(numbers1D) != n:
                raise IndexError("The length of the rows are not equal")
            else:
                row = []
                for number in numbers1D:
                    row.append(number)
                matrix_arr.append(row)
        self.m = m
        self.n = n
        self.matrix_arr = matrix_arr

    def __str__(self) -> str:
        s = ""
        for row in self.matrix_arr:
            s += "\n|"
            for num in row:
                s += " " + str(num)
            s += " |"
        return s

    def fill(self, array2d):
        """Fill the matrix 

    Args:
        array2d (list): 4x4 2D list which contains the numbers that wanted to be filled to the matrix
    """
        is_rows_equal = len(array2d) == self.m
        is_columns_equal = True
        for i in range(0, len(array2d)):
            is_columns_equal = len(array2d[i]) == self.n
            if is_columns_equal == False:
                break

        if is_rows_equal == False:
            print(
                "Error: size of the rows in the array does not match with matrix"
            )
        elif is_columns_equal == False:
            print(
                "Error: size of the columns in the array does not match with matrix"
            )

        else:
            for i in range(0, self.m):
                for j in range(0, self.n):
                    self.matrix_arr[i][j] = array2d[i][j]

    def set_num(self, num, r_ind, c_ind):
        """Set a number in the matrix

    Args:
        num (float): The number that wanted to be set
        r_ind (int): Row index
        c_ind (int): Column index
    """
        if (r_ind) > self.m or (c_ind) > self.n:
            raise IndexError("Invalid row and column locations")
        else:
            self.matrix_arr[r_ind][c_ind] = num

    def multiply(self, other):
        """Multiply this matrix with another one

    Args:
        other (Mat3d): The matrix that wanted to be multiplied with this matrix

    Returns:
        Matrix: Multiplied matrix
    """
        if (self.n != other.m):
            raise IndexError(
                "You cannot multiply %d column matrix with %d row matrix" %
                (self.n, other.m))
        else:
            tmp_m = self.m
            tmp_n = other.n
            tmp_matrix = []
            for i in range(0, tmp_m):
                tmp_row = []
                for j in range(0, tmp_n):
                    sum = 0
                    for k in range(0, self.n):
                        sum += self.matrix_arr[i][k] * other.matrix_arr[k][j]
                    tmp_row.append(sum)
                tmp_matrix.append(tmp_row)
            return Matrix(tmp_matrix)

    def transpose(self):
        """Generate transpose of a matrix

    Returns:
        Matrix: Transposed matrix
    """
        tmp_mat = []
        for i in range(self.m):
            tmp_row = []
            for j in range(self.n):
                tmp_row.append(self.matrix_arr[j][i])
            tmp_mat.append(tmp_row)
        return Matrix(tmp_mat)
