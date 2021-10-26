# CENG 487 Assignment1 by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

import numpy as np

class Mat3d:
  m = 4
  n = 4
  def __init__(self) -> None:
      self.matrix = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
  
  def __str__(self) -> str:
      s = ""
      for row in self.matrix:
        s += "\n|"
        for num in row:
          s += " " + str(num)
        s += " |"
      return s

  def fill(self, array2d):
    is_rows_equal = len(array2d) == self.m
    is_columns_equal = True
    for i in range(0, len(array2d)):
      is_columns_equal = len(array2d[i]) == self.n
      if is_columns_equal == False:
        break
    
    if is_rows_equal == False:
      print("Error: size of the rows in the array does not match with matrix")
    elif is_columns_equal == False:
      print("Error: size of the columns in the array does not match with matrix")
    
    else:
      for i in range(0, self.m):
        for j in range(0, self.n):
          self.matrix[i][j] = array2d[i][j]
        
  def set_num(self, num, row, col):
    if (row - 1) > self.m or (col - 1) > self.n:
      print("Error: Invalid row and column locations")
    else:
      self.matrix[row - 1][col - 1] = num

  def multipy(self, other):
    if(self.n != other.m):
      print("Error: You cannot multiply %d column matrix with %d row matrix" % (self.n, other.m))
    else:
      tmp_m = self.m
      tmp_n = other.n
      tmp_mat = Mat3d(tmp_m, tmp_n)
      for i in range(0, tmp_m):
        for j in range(0, tmp_n):
          for k in range(0, self.n):
            tmp_mat.matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
      return tmp_mat
  
  def inverse(self):
    return np.linalg.inv(self.matrix)

def main():
  A = ([[6, 1, 1, 3],
              [4, -2, 5, 1],
              [2, 8, 7, 6],
              [3, 1, 9, 7]])
  x = Mat3d()
  x.fill(A)
  print(x)
  print(x.inverse())
  pass

main()