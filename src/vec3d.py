# CENG 487 Assignment by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

import math

from mat3d import Mat3d
from matrix import Matrix


class Vec3d:
    def __init__(self, coordinate=[0, 0, 0, 0]):
        self.matrix = Matrix([[coordinate[0]], [coordinate[1]],
                              [coordinate[2]], [coordinate[3]]])

    @property
    def x(self):
        return self.matrix.matrix_arr[0][0]

    @property
    def y(self):
        return self.matrix.matrix_arr[1][0]

    @property
    def z(self):
        return self.matrix.matrix_arr[2][0]

    @property
    def w(self):
        return self.matrix.matrix_arr[3][0]

    @x.setter
    def x(self, val):
        self.matrix.matrix_arr[0][0] = val

    @y.setter
    def y(self, val):
        self.matrix.matrix_arr[1][0] = val

    @z.setter
    def z(self, val):
        self.matrix.matrix_arr[2][0] = val

    @w.setter
    def w(self, val):
        self.matrix.matrix_arr[3][0] = val

    @property
    def tuple(self):
        return (self.x, self.y, self.z)
        
    def __str__(self):
        str = "(x, y, z): (%s, %s, %s)" % (self.x, self.y, self.z)
        return str

    def __add__(self, other):
        if (self.w != other.w):
            raise TypeError("Vectors and point cannot be added")

        else:
            addedX = self.x + other.x
            addedY = self.y + other.y
            addedZ = self.z + other.z
            w = self.w
            return Vec3d([addedX, addedY, addedZ, w])
    
    def __sub__(self, other):
        if (self.w != other.w):
            raise TypeError("Vectors and point cannot be subtracted")
        
        else:
            return Vec3d(
                [self.x - other.x, self.y - other.y, self.z]
            )

    def substract(self, vec2):
        """Substract vec2 from vec1 (vec1 - vec2)

        Args:
            vec1 (Vec3d): Minuend
            vec2 (Vec3d): Subtrahend
        """
        vec2.negative()
        self.add(vec2)
        vec2.negative()

    def clone(self):
        """Clone this vector

        Returns:
            Vec3d: The cloned vector which its coordinates are the same as the original one
        """
        coordinate = [self.x, self.y, self.z, self.w]
        return Vec3d(coordinate)

    def negative(self):
        """Convert this vector to its negative
        """
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

    def scale(self, factor):
        """Scale this vector

        Args:
            factor (int): Scaling factor
        """
        self.x *= factor
        self.y *= factor
        self.z *= factor

    def dot_product(self, other):
        """Dot product of the vector with another vector

        Args:
            other (Vec3d): Other vector to calculate its dot product with this vector

        Returns:
            float: Result of the dot product
        """
        x = self.x * other.x
        y = self.y * other.y
        z = self.z * other.z
        result = x + y + z
        return result

    def magnitude(self):
        """Calculate the magnitude of this vector

        Returns:
            float: Magnitude of this vector
        """
        dp = self.dot_product(self)
        sqrt = math.sqrt(dp)
        return sqrt

    def angle(self, other):
        """Find angle between two vectors in radian

        Returns:
            float: angle between vectors in radian
        """
        dp = self.dot_product(other)
        magn_mult = self.magnitude() * other.magnitude()
        radian = math.acos(dp / magn_mult)
        degree = math.degrees(radian)
        return degree

    def basis(self):
        """Calculate basis vector of this vector

        Returns:
            Vec3d: Basis vector of this vector
        """
        magn = self.magnitude()
        basis_x = self.x / magn
        basis_y = self.y / magn
        basis_z = self.z / magn
        basis = Vec3d(basis_x, basis_y, basis_z)
        return basis

    def project(self, other):
        """Take projection of this vector onto another one

        Args:
            other (Vec3d): The vector to be projected on

        Returns:
            Vec3d: Projected vector of this vector onto other vector
        """
        dp = self.dot_product(other)
        proj_magn = dp / other.magnitude()
        temp_vec = other.basis()
        temp_vec.scale(proj_magn)
        return temp_vec

    def cross_product(self, other):
        """Calculate cross product of this vector with another one

        Args:
            other (Vec3d): The vector to be cross product with this vector

        Returns:
            Vec3d: The vector of the cross product result
        """
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        cp = Vec3d(x, y, z)
        return cp

    def transform(self, tra_mat: Mat3d):
        """Create tranformed vertices

        Args:
            tra_mat (Mat3d): Transformation matrix to multiply with this vertex

        Returns:
            Vec3d: Transormed Vec3d created from this object
        """
        clone = self.clone()
        clone.matrix = tra_mat.matrix.multiply(clone.matrix)
        return clone
