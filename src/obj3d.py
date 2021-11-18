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
          vertices (list[list[float]]): Vertex list contains vertices, vertices contains float values
      """
    def __init__(self, vertices, faces) -> None:
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

    def getfaces(self):
        clone = []
        for face in self.faces:
            clone.append([vi for vi in face])
        return clone

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
        self.rotation.matrix = self.rotation.matrix.multiply(
            tmp_tra_inv.matrix)

    def translate(self, x, y, z):
        """Translate the object

        Args:
            x (float): Translation amount on x axis
            y (float): Translation amount on y axis
            z (float): Translation amount on z axis
        """
        tmp_tra = Mat3d.translation(x, y, z)
        self.translation.matrix = self.translation.matrix.multiply(
            tmp_tra.matrix)

    def transform(self):
        """Calculate composite transformation matrix and generate transformed vertices based on this object

        Raises:
            error: When there is a problem related to transformation order enumeration

        Returns:
            list[Matrix]: Transformed 4x1 matrix list
        """
        self.push_transformation()

        for val in TransformationOrder:

            if val is TransformationOrder.SCALE:
                self.transformation.matrix = self.transformation.matrix.multiply(
                    self.scaling.matrix)
                self.scaling = Mat3d.identity()

            elif val is TransformationOrder.ROTATION:
                self.transformation.matrix = self.transformation.matrix.multiply(
                    self.rotation.matrix)
                self.rotation = Mat3d.identity()

            elif val is TransformationOrder.TRANSLATION:
                self.transformation.matrix = self.transformation.matrix.multiply(
                    self.translation.matrix)
                self.translation = Mat3d.identity()

            else:
                raise error("There is a problem with TransformationOrder ENUM")

        # multiply vertices with transformation matrix and return transformed Vec3d list
        return [
            vertex.transform(self.transformation) for vertex in self.vertices
        ]
