# CENG 487 Assignment1 by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

from vec3d import Vec3d

class Obj3d:
  def __init__(self, arr) -> None:
      self.vertices = []
      for point in arr:
        self.vertices.append(point)
      self.stack = []

  def append_transformation(self, transformation):
    self.stack.append(transformation)

  def pop_transformation(self):
    self.stack.pop()

def main():
  pass

main()