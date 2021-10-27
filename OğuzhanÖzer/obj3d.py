# CENG 487 Assignment1 by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

class Obj3d:
  def __init__(self, arr) -> None:
    self.vertices = []
    for point in arr:
      self.vertices.append(point)
    self.stack = []

  def append_transformation(self, transformation):
    """Append transformation to the stack

    Args:
        transformation (Mat3d): Transformation matrix to be added
    """
    self.stack.append(transformation)

  def pop_transformation(self):
    """Pop transformation from the stack

    Args:
        transformation (Mat3d): Transformation matrix to be popped
    """
    self.stack.pop()

  def transform(self, tra_mat):
    """Transform the vertices of this object

    Args:
        tra_mat (Mat3d): Transformation matrix for transforming vertices
    """
    for i in range(len(self.vertices)):
      self.vertices[i] = self.vertices[i].transform(tra_mat)
    self.append_transformation(tra_mat)
