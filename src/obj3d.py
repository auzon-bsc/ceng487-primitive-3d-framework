# CENG 487 Assignment1 by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

import math
from logging import error

from mat3d import Mat3d
from enum import Enum
from vec3d import Vec3d

class TransformationOrder(Enum):
  """Determines the transformation order
  """
  SCALE = 0
  ROTATION = 1
  TRANSLATION = 2

class Obj3d:
  """Create and manipulate 3D objects

    Args:
        vertices (list[list[float]]): Vertex list contains vertices, vertices contains float values
    """
  def __init__(self, vertices: list[list[float]], faces: list[list[int]]) -> None:
    # create vec3d objects from vertices and add them to vertices array of this object
    self.vertices: list[Vec3d] = [Vec3d(vertex) for vertex in vertices]
    
    # add all faces to faces list of this object
    self.faces: list[list] = [face for face in faces]
    
    # set all transformation matrices to identity (objects won't be transformed)
    self.transformation = Mat3d.identity() 
    self.translation = Mat3d.identity()
    self.rotation = Mat3d.identity()
    self.scaling = Mat3d.identity()
   
    # transformation stack for remembering previous transformations
    self.stack = [Mat3d.identity()]

  def push_transformation(self):
    """Push current transformation to the stack

    Args:
        transformation (Mat3d): Transformation matrix to be added
    """
    self.stack.append(self.transformation)

  def pop_transformation(self):
    """Pop a transformation from the stack

    Args:
        transformation (Mat3d): Transformation matrix to be popped
    """
    self.stack.pop()

  def scale(self, sx, sy, sz):
    """Scale the object.

    Args:
        sx (float): Scale amount on x axis
        sy (float): Scale amount on y axis
        sz (float): Scale amount on z axis
    """
    tmp_sca = Mat3d.scale(sx, sy, sz)
    self.scaling.matrix = self.scaling.matrix.multiply(tmp_sca.matrix)

  def rotate(self, axis: str, point: Vec3d, degree: float):
    """Rotate the object around an axis and around a point

    Args:
        axis (str): The axis to rotate around
        point (Vec3d): The point to rotate around
        degree (float): Rotation amount/degree
    """
    tmp_tra = Mat3d.translation(-point.x, -point.y, -point.z)
    tmp_rot = Mat3d.rotation(axis, degree)
    tmp_tra_inv = Mat3d.inverse_translation(-point.x, -point.y, -point.z)
    self.rotation.matrix = self.rotation.matrix.multiply(tmp_tra.matrix)
    self.rotation.matrix = self.rotation.matrix.multiply(tmp_rot.matrix)
    self.rotation.matrix = self.rotation.matrix.multiply(tmp_tra_inv.matrix)
    
  def translate(self, x, y, z):
    """Translate the object

    Args:
        x (float): Translation amount on x axis
        y (float): Translation amount on y axis
        z (float): Translation amount on z axis
    """
    tmp_tra = Mat3d.translation(x, y, z)
    self.translation.matrix = self.translation.matrix.multiply(tmp_tra.matrix)

  def transform(self):
    """Calculate composite transformation matrix and generate transformed vertices based on this object

    Raises:
        error: When there is a problem related to transformation order enumeration

    Returns:
        list[Matrix]: Transformed 4x1 matrix list
    """
    self.push_transformation()

    for val in TransformationOrder:
      match val:
        case TransformationOrder.SCALE:
          self.transformation.matrix = self.transformation.matrix.multiply(self.scaling.matrix)
          self.scaling = Mat3d.identity()
          
        case TransformationOrder.ROTATION:
          self.transformation.matrix = self.transformation.matrix.multiply(self.rotation.matrix)
          self.rotation = Mat3d.identity()

        case TransformationOrder.TRANSLATION:
          self.transformation.matrix = self.transformation.matrix.multiply(self.translation.matrix)
          self.translation = Mat3d.identity()
        
        case _:
          raise error("There is a problem with TransformationOrder ENUM")

    # multiply vertices with transformation matrix and return the list that contains 4x1 Mat3d objects
    return [self.transformation.multiply(vertex.matrix) for vertex in self.vertices]
    

  # @staticmethod
  # def sphere(radius, sector_count, stack_count):
  #   point_arr = []
  #   for stack_step in range(stack_count + 1):
  #     sector_arr = []
  #     for sector_step in range(sector_count + 1):
  #       theta = (2 * math.pi) * (sector_step / sector_count)
  #       phi = (math.pi / 2) - (math.pi * stack_step / stack_count)

  #       x = radius * math.cos(phi) * math.cos(theta)
  #       y = radius * math.cos(phi) * math.sin(theta)
  #       z = radius * math.sin(phi)
  #       w = 1

  #       tmp_vec = Vec3d(x, y, z, w)
  #       sector_arr.append(tmp_vec)
  #     point_arr.append(sector_arr)

  #   poly_arr = []
  #   for i in range(sector_count):
  #     for j in range(stack_count):
  #       tmp_arr = []
  #       tmp_arr.append(point_arr[i][j].clone())
  #       tmp_arr.append(point_arr[i+1][j].clone())
  #       tmp_arr.append(point_arr[i+1][j+1].clone())
  #       tmp_arr.append(point_arr[i][j+1].clone())
  #       poly_arr.append(tmp_arr)

  #   return Obj3d(poly_arr)

  # @staticmethod
  # def cylinder(radius, height, sector_count):
  #   top_points = []
  #   bot_points = []

  #   for sector_step in range(sector_count + 1):
  #     theta = (2 * math.pi) * (sector_step / sector_count)
  #     x = radius * math.cos(theta)
  #     z = radius * math.sin(theta)
  #     y = height / 2
  #     w = 1
  #     top_points.append(Vec3d(x, y, z, w))
  #     bot_points.append(Vec3d(x, -y, z, w))

  #   poly_arr = []
    
  #   poly_arr.append(top_points)

  #   for i in range(sector_count):
  #     quad_points = []
  #     quad_points.append(top_points[i].clone())
  #     quad_points.append(bot_points[i].clone())
  #     quad_points.append(bot_points[i+1].clone())
  #     quad_points.append(top_points[i+1].clone())
  #     poly_arr.append(quad_points)
    
  #   poly_arr.append(bot_points)

  #   return Obj3d(poly_arr)
    
  # @staticmethod
  # def square(a, sector_count):
  #   poly_arr = []   # array of polygons/vertice arrays
  #   pivot_vertice = Vec3d(-(a/2),(a/2),0,1)
  #   point_arr = []
  #   for i in range(sector_count + 1):
  #     tmp_arr = []
      
  #     offset_y = a * i / sector_count   # offset_y
  #     for j in range(sector_count + 1):
  #       offset_x = a * j / sector_count   # offset_x
  #       tmp_v = pivot_vertice.clone()
  #       tmp_v.x += offset_x
  #       tmp_v.y -= offset_y
  #       tmp_arr.append(tmp_v)
  #     point_arr.append(tmp_arr)       
    
  #   for i in range(sector_count):
  #     for j in range(sector_count):
  #       tmp_arr = []
  #       tmp_arr.append(point_arr[i][j])
  #       tmp_arr.append(point_arr[i][j+1])
  #       tmp_arr.append(point_arr[i+1][j+1])
  #       tmp_arr.append(point_arr[i+1][j])
  #       poly_arr.append(Poly(tmp_arr))

  #   s1 = Obj3d(copy.deepcopy(poly_arr))   # Surface 1
  #   s2 = Obj3d(copy.deepcopy(poly_arr))
  #   s3 = Obj3d(copy.deepcopy(poly_arr))
  #   s4 = Obj3d(copy.deepcopy(poly_arr))
  #   s5 = Obj3d(copy.deepcopy(poly_arr))
  #   s6 = Obj3d(copy.deepcopy(poly_arr))

  #   s1.translate(0, 0, a/2)
  
  #   s2.translate(0, 0, -a/2)
    
  #   s3.rotate("y", Vec3d(0, 0, 0), 90)
  #   s3.translate(a/2, 0, 0)

  #   s4.rotate("y", Vec3d(0, 0, 0), -90)
  #   s4.translate(-a/2, 0, 0)

  #   s5.rotate("x", Vec3d(0, 0, 0), 90)
  #   s5.translate(0, a/2, 0)
    
  #   s6.rotate("x", Vec3d(0, 0, 0), -90)
  #   s6.translate(0, -a/2, 0)

  #   return Obj3d(poly_arr)


