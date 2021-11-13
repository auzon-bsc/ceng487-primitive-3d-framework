# CENG 487 Assignment by
# Oğuzhan Özer
# StudentId: 260201039
# November 2021

import math
import copy
from mat3d import Mat3d
from matrix import Matrix
from vec3d import Vec3d

class Poly:
  def __init__(self, vertex_arr: list[Vec3d]):
    self.vertex_arr = vertex_arr
  
  def __str__(self):
    copy.deepcopy
    str = ""
    for vertex in self.vertex_arr:
      str += "(x, y, z): (%s, %s, %s)\n" % (vertex.x, vertex.y, vertex.z)
    return str
    
  def clone(self):
    """Clone this polygon

    Returns:
        Poly: The cloned poly which its coordinates are the same as the original one
    """
    vertex: Vec3d
    tmp_arr: list[Vec3d]
    for vertex in self.vertex_arr:
      new_ver = vertex.clone()
      tmp_arr.append(new_ver)
    return Poly(tmp_arr)

  def transform(self, tra_mat: Mat3d):
    """Generate transformed vertices

    Args:
        tra_mat (Mat3d): Transformation matrix

    Returns:
        list[Vec3d]: Transformed vertex array
    """
    vertex: Vec3d
    tmp_arr: list[Vec3d] = []
    for vertex in self.vertex_arr:
      tmp_mat = tra_mat.multiply(vertex.matrix)
      tmp_vec = Vec3d(tmp_mat.matrix_arr[0][0], tmp_mat.matrix_arr[1][0], tmp_mat.matrix_arr[2][0], tmp_mat.matrix_arr[3][0])
      tmp_arr.append(tmp_vec)
    return tmp_arr