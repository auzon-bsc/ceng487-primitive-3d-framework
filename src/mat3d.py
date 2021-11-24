# CENG 487 Assignment by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

import math

from matrix import Matrix


class Mat3d:
    def __init__(self, matrix_arr) -> None:
        self.matrix = Matrix(matrix_arr)

    def __str__(self) -> str:
        return self.matrix

    @staticmethod
    def identity():
        """Create a 4x4 identity matrix

        Returns:
            Mat3d: 4x4 identity matrix
        """
        return Mat3d([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

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
        return Mat3d([[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]])

    @staticmethod
    def inverse_translation(x, y, z):
        """Calculate the inverse translation matrix

        Args:
            x (float): x coordinate
            y (float): y coordinate
            z (float): z coordinate

        Returns:
            Mat3d: Inverse translation matrix
        """
        return Mat3d([[1, 0, 0, -x], [0, 1, 0, -y], [0, 0, 1, -z],
                      [0, 0, 0, 1]])

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
        return Mat3d([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0],
                      [0, 0, 0, 1]])

    @staticmethod
    def inverse_scale(sx, sy, sz):
        """Calculate a inverse scale matrix

        Args:
            sx (float): Scale amount on x axis
            sy (float): Scale amount on y axis
            sz (float): Scale amount on z axis

        Returns:
            Mat3d: Inverse scale matrix
        """
        return Mat3d([[1 / sx, 0, 0, 0], [0, 1 / sy, 0, 0], [0, 0, 1 / sz, 0],
                      [0, 0, 0, 1]])

    @staticmethod
    def rotation(axis, degree):
        """Calculate rotation matrix

        Args:
            axis (str): The axis that rotation matrix will be calculated
            degree (float): Rotation degree

        Returns:
            Mat3d: Rotation matrix
        """
        radians = math.radians(degree)
        c = math.cos(radians)
        s = math.sin(radians)

        if axis == "x":
            tmp_mat = ([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0],
                        [0, 0, 0, 1]])

        elif axis == "y":
            tmp_mat = ([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0],
                        [0, 0, 0, 1]])

        elif axis == "z":
            tmp_mat = ([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        else:
            raise ValueError("Invalid axis")

        return Mat3d(tmp_mat)

    @staticmethod
    def inverse_rotation(axis, degree):
        """Calculate inverse rotation matrix

        Args:
            axis (str): The axis that rotation matrix will be calculated
            degree (float): Rotation degree

        Returns:
            Mat3d: Inverse rotation matrix
        """
        radians = math.radians(degree)
        c = math.cos(radians)
        # When calculating inverse rotation matrix sin becomes negative
        s = math.sin(radians)

        if axis == "x":
            tmp_mat = ([[1, 0, 0, 0], [0, c, s, 0], [0, -s, c, 0],
                        [0, 0, 0, 1]])
        elif axis == "y":
            tmp_mat = ([[c, 0, -s, 0], [0, 1, 0, 0], [s, 0, c, 0],
                        [0, 0, 0, 1]])
        elif axis == "z":
            tmp_mat = ([[c, s, 0, 0], [-s, c, 0, 0], [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        else:
            raise ValueError("Invalid axis")

        return Mat3d(tmp_mat)

    def multiply(self, other):
        """Multiply this 4x4 matrix with 4x? any matrix

        Args:
            other (Matrix): A matrix which has 4 rows and any arbitrary columns

        Returns:
            Matrix: Multiplied 4x? matrix
        """
        multiplied_matrix = self.matrix.multiply(other.matrix)
        matrix_arr = multiplied_matrix.matrix_arr
        return Mat3d(matrix_arr)
