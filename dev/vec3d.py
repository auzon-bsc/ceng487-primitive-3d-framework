# CENG 487 Assignment1 by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

class Vec3d:
  w = 0

  def __init__(self, x = 0, y = 0, z = 0):
    self.x = x
    self.y = y
    self.z = z
    
  def __str__(self):
      str = "(x, y, z): (%s, %s, %s)" % (self.x, self.y, self.z)
      return str

  def add(self, other):
    self.x += other.x
    self.y += other.y
    self.z += other.z
    
    print("\nRESULT OF ADDITION: %s" % self)
  
  def substract(self, vec2):
    """Substract vec2 from vec1 (vec1 - vec2)

    Args:
        vec1 (Vec3d): Minuend
        vec2 (Vec3d): Subtrahend
    """    
    vec2.negative()
    self.add(vec2)
    vec2.negative()

    print("\nRESULT OF SUBSTRACTION: %s" % (self))
  
  def clone(self):
    new_x = self.x
    new_y = self.y
    new_z = self.z
    new_vec3d = Vec3d(new_x, new_y, new_z)

    print("\nCLONE: %s" % (new_vec3d))

    return new_vec3d

  def negative(self):
    self.x = -self.x
    self.y = -self.y
    self.z = -self.z

    print("\nNEGATED VECTOR %s" % self)

  def scale(self, factor):
    self.x *= factor
    self.y *= factor
    self.z *= factor

    print("\nSCALED VECTOR %s" % self)

  def dot_product(self, other):
    x = self.x * other.x
    y = self.y * other.y
    z = self.z * other.z

    result = Vec3d(x, y, z)
    
    print("\n DOT PRODUCT RESULT: %s" % result)

    return result








def main():
  vec1 = Vec3d(1.3, 2.4, 5)
  vec2 = Vec3d(1.7, 2.6, 15)
  vec1.add(vec2)

  vec3 = Vec3d(2.9, 1.5, 3)
  vec4 = Vec3d(0.9, 0.5, 3)
  vec3.substract(vec4)

  vec5 = Vec3d(0.2, 0.5, 0.7)
  vec5.scale(10)

  vec6 = Vec3d(2.0, 3.0, 4.0)
  vec7 = Vec3d(5.0, 6.0, 7.0)
  vec6.dot_product(vec7)

main()