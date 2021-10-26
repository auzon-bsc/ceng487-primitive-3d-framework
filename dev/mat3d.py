# CENG 487 Assignment1 by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

import numpy as np
import math

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
        
  def set_num(self, num, r_ind, c_ind):
    if (r_ind) > self.m or (c_ind) > self.n:
      print("Error: Invalid row and column locations")
    else:
      self.matrix[r_ind][c_ind] = num

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

  def transpose(self):
    tmp_mat = Mat3d()
    for i in range(self.m):
      for j in range(self.n):
        tmp_mat.set_num(self.matrix[i][j], j, i)
    return tmp_mat

  @staticmethod
  def translation(x, y, z):
    tmp_mat = Mat3d()
    tmp_arr = ([[1, 0, 0, x],
                [0, 1, 0, y],
                [0, 0, 1, z],
                [0, 0, 0, 1]])
    tmp_mat.fill(tmp_arr)
    return tmp_mat

  @staticmethod
  def scale(sx, sy, sz):
    tmp_mat = Mat3d()
    tmp_arr = ([[sx, 0, 0, 0],
                [0, sy, 0, 0],
                [0, 0, sz, 0],
                [0, 0, 0, 1]])
    tmp_mat.fill(tmp_arr)
    return tmp_mat

  @staticmethod
  def rotation(axis, degree):
    tmp_mat = Mat3d()
    radians = math.radians(degree)
    c = math.cos(radians)
    s = math.sin(radians)

    match axis:
      case "x":
        tmp_arr = ([[1, 0, 0, 0],
                    [0, c, -s, 0],
                    [0, s, c, 0],
                    [0, 0, 0, 1]])
      case "y":
        tmp_arr = ([[c, 0, s, 0],
                    [0, 1, 0, 0],
                    [-s, 0, c, 0],
                    [0, 0, 0, 1]])
      case "z":
        tmp_arr = ([[c, -s, 0, 0],
                    [s, c, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
      case _:
        print("Error: Invalid axis")
    
    tmp_mat.fill(tmp_arr)
    return tmp_mat

def main():
  A = ([[6, 1, 1, 3],
        [4, -2, 5, 1],
        [2, 8, 7, 6],
        [3, 1, 9, 7]])
  a = Mat3d()
  a.fill(A)
  print(a)
  print(a.inverse())

  b = Mat3d.translation(2, 3, 4)
  print(b)

  c = Mat3d()
  c.fill(A)
  d = c.transpose()
  print(d)

  e = Mat3d.rotation("x", 30)
  print(e)

  pass

main()