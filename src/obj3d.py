# CENG 487 Assignment1 by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

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
        point_arr (list): Point array
    """
  def __init__(self, point_arr) -> None:
    
    self.ver_arr = []
    self.transformation = Mat3d.identity()
    self.translation = Mat3d.identity()
    self.rotation = Mat3d.identity()
    self.scaling = Mat3d.identity()
    for point in point_arr:
      vertice = Vec3d(point[0], point[1], point[2], point[3])
      self.ver_arr.append(vertice)
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
        Vec3d[]: Transformed vertices array
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

    tmp_ver_arr = []
    for i in range(len(self.ver_arr)):
      tmp_mat = self.transformation.matrix.multiply(self.ver_arr[i].matrix)
      tmp_x = tmp_mat.matrix_arr[0][0]
      tmp_y = tmp_mat.matrix_arr[1][0]
      tmp_z = tmp_mat.matrix_arr[2][0]
      tmp_w = tmp_mat.matrix_arr[3][0]
      tmp_ver = Vec3d(tmp_x, tmp_y, tmp_z, tmp_w)
      tmp_ver_arr.append(tmp_ver)

    return tmp_ver_arr

