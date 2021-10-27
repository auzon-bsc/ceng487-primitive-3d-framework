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
      print("Error: size of the rows in the array does not match with matrix")
    elif is_columns_equal == False:
      print("Error: size of the columns in the array does not match with matrix")
    
    else:
      for i in range(0, self.m):
        for j in range(0, self.n):
          self.matrix[i][j] = array2d[i][j]
        
  def set_num(self, num, r_ind, c_ind):
    """Set a number in the matrix

    Args:
        num (float): The number that wanted to be set
        r_ind (int): Row index
        c_ind (int): Column index
    """
    if (r_ind) > self.m or (c_ind) > self.n:
      print("Error: Invalid row and column locations")
    else:
      self.matrix[r_ind][c_ind] = num

  def multiply(self, other):
    """Multiply this matrix with another one

    Args:
        other (Mat3d): The matrix that wanted to be multiplied with this matrix

    Returns:
        Mat3d: Multiplied matrix
    """
    if(self.n != other.m):
      print("Error: You cannot multiply %d column matrix with %d row matrix" % (self.n, other.m))
    else:
      tmp_m = self.m
      tmp_n = other.n
      tmp_mat = Mat3d()
      for i in range(0, tmp_m):
        for j in range(0, tmp_n):
          for k in range(0, self.n):
            tmp_mat.matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
      return tmp_mat
  
  def inverse(self):
    """Take inverse of this matrix

    Returns:
        [type]: [description]
    """
    return np.linalg.inv(self.matrix) # This'll probably cause bugs

  def transpose(self):
    """Generate transpose of a matrix

    Returns:
        Mat3d: Transposed matrix
    """
    tmp_mat = Mat3d()
    for i in range(self.m):
      for j in range(self.n):
        tmp_mat.set_num(self.matrix[i][j], j, i)
    return tmp_mat

  @staticmethod
  def translation(x, y, z):
    """Calculate translation matrix

    Args:
        x (float): x coordinate
        y (float): y coordinate
        z (float): z coordinate

    Returns:
        Mat3d: Translation matrix
    """
    tmp_mat = Mat3d()
    tmp_arr = ([[1, 0, 0, x],
                [0, 1, 0, y],
                [0, 0, 1, z],
                [0, 0, 0, 1]])
    tmp_mat.fill(tmp_arr)
    return tmp_mat

  @staticmethod
  def scale(sx, sy, sz):
    """Calculate a scale matrix

    Args:
        sx (float): Scale amount on x axis
        sy (float): Scale amount on y axis
        sz (float): Scale amount on z axis

    Returns:
        Mat3d: Scale matrix
    """
    tmp_mat = Mat3d()
    tmp_arr = ([[sx, 0, 0, 0],
                [0, sy, 0, 0],
                [0, 0, sz, 0],
                [0, 0, 0, 1]])
    tmp_mat.fill(tmp_arr)
    return tmp_mat

  @staticmethod
  def rotation(axis, degree):
    """Calculate rotation matrix

    Args:
        axis (str): The axis that rotation matrix will be calculated
        degree (float): Rotation degree

    Returns:
        Mat3d: Rotation matrix
    """
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