# CENG 487 Assignment1 by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

from typing import *
import copy
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
    _vertexList: List[Vec3d]
    _faceList: List[List[int]]

    _compositeScalingMatrix: Mat3d
    _compositeRotationMatrix: Mat3d
    _compositeTranslationMatrix: Mat3d

    _subdivisionAmount: int

    # _linkedScene: Scene

    def __init__(self) -> None:
        # create vec3d objects from vertices and add them to vertices array of this object
        self._vertexList = []
        self._faceList = []

        # set all transformation matrices to identity (objects won't be transformed)
        self._compositeScalingMatrix = Mat3d.identity()
        self._compositeRotationMatrix = Mat3d.identity()
        self._compositeTranslationMatrix = Mat3d.identity()

    def getVertexList(self):
        vertexList = self._vertexList
        vertexListClone = copy.deepcopy(vertexList)
        return vertexListClone

    def getFaceList(self):
        faceList = self._faceList
        faceListClone = copy.deepcopy(faceList)
        return faceListClone

    def setVertexList(self, vertexList):
        vertexListClone = copy.deepcopy(vertexList)
        self._vertexList = vertexListClone
    
    def setFaceList(self, faceList):
        faceListClone = copy.deepcopy(faceList)
        self._faceList = faceListClone

    def addVertex(self, vertex: Vec3d):
        vertexList = self._vertexList
        vertexClone = copy.deepcopy(vertex)
        vertexList.append(vertexClone)

    def removeVertex(self, vertex: Vec3d):
        vertexList = self._vertexList
        vertexList.remove(vertex)

    def popVertex(self, vertexIndex: Vec3d):
        vertexList = self._vertexList
        vertexList.pop(vertexIndex)

    def addFace(self, face: List[int]):
        faceList = self._faceList
        faceClone = copy.deepcopy(face)
        faceList.append(faceClone)

    def scale(self, sx: float, sy: float, sz: float):
        """Scale the object.

        Args:
            sx (float): Scale amount on x axis
            sy (float): Scale amount on y axis
            sz (float): Scale amount on z axis
        """
        scalingMatrix = Mat3d.scale(sx, sy, sz)
        compositeScalingMatrix = self._compositeScalingMatrix
        self._compositeScalingMatrix = scalingMatrix.multiply(
            compositeScalingMatrix)

    def rotate(self, axis: str, degree: float):
        """Rotate the object around an axis and around a point

        Args:
            axis (str): The axis to rotate around
            point (Vec3d): The point to rotate around
            degree (float): Rotation amount/degree
        """
        rotationMatrix = Mat3d.rotation(axis, degree)
        compositeRotationMatrix = self._compositeRotationMatrix
        self._compositeRotationMatrix = rotationMatrix.multiply(
            compositeRotationMatrix)

    def translate(self, dx, dy, dz):
        """Translate the object

        Args:
            dx (float): Translation amount on x axis
            dy (float): Translation amount on y axis
            dz (float): Translation amount on z axis
        """
        translationMatrix = Mat3d.translation(dx, dy, dz)
        compositeTranslationMatrix = self._compositeTranslationMatrix
        self._compositeTranslationMatrix = translationMatrix.multiply(
            compositeTranslationMatrix)

    def calculateCompositeTransformationMatrix(self):
        cumulativeMatrix = Mat3d.identity()
        for val in TransformationOrder:
            if val is TransformationOrder.SCALE:
                compositeScalingMatrix = self._compositeScalingMatrix
                cumulativeMatrix = compositeScalingMatrix.multiply(
                    cumulativeMatrix)

            elif val is TransformationOrder.ROTATION:
                compositeRotationMatrix = self._compositeRotationMatrix
                cumulativeMatrix = compositeRotationMatrix.multiply(
                    cumulativeMatrix)

            elif val is TransformationOrder.TRANSLATION:
                compositeTranslationMatrix = self._compositeTranslationMatrix
                cumulativeMatrix = compositeTranslationMatrix.multiply(
                    cumulativeMatrix)

            else:
                raise KeyError(
                    "There is no key '{key}' in TransformationOrder ENUM")

        compositeTransformationMatrix = cumulativeMatrix
        return compositeTransformationMatrix

    def calculateTransformedVertexList(self):
        vertexList = self._vertexList
        compositeTransformationMatrix = self.calculateCompositeTransformationMatrix(
        )
        tempVertexList = []
        for vertex in vertexList:
            transformedVertex = vertex.transform(compositeTransformationMatrix)
            tempVertexList.append(transformedVertex)
        transformedVertexList = tempVertexList
        return transformedVertexList

    def getFaceVertexList(self, singleFace):
        faceVertexList = []
        vertexList = self._vertexList
        for vertexPointer in singleFace:
            pointeeVertex = vertexList[vertexPointer]
            faceVertexList.append(pointeeVertex)
        return faceVertexList

    def calculateMiddleVertex(self, vertexList):
        sumVertex = Vec3d([0.0, 0.0, 0.0, 1.0])
        vertexListLength = len(vertexList)
        vertexListRange = range(vertexListLength)
        for vertexIndex in vertexListRange:
            currentVertex = vertexList[vertexIndex]
            sumVertex += currentVertex
        avarageCoefficient = 1 / vertexListLength
        sumVertex.scale(avarageCoefficient)
        return sumVertex

    def calculateEdgeMiddleVertexList(self, singleFace):
        baseVertexList = self.getFaceVertexList(singleFace)
        cumulativeEdgeMiddleVertexList = []
        baseVertexListLength = len(baseVertexList)
        baseVertexListRange = range(baseVertexListLength)
        for vertexIndex in baseVertexListRange:
            previousVertexIndex = vertexIndex - 1
            currentVertexIndex = vertexIndex
            previousVertex = baseVertexList[previousVertexIndex]
            currentVertex = baseVertexList[currentVertexIndex]
            consecutiveVertexList = [previousVertex, currentVertex]
            singleEdgeMiddleVertex = self.calculateMiddleVertex(consecutiveVertexList)
            cumulativeEdgeMiddleVertexList.append(singleEdgeMiddleVertex)
        return cumulativeEdgeMiddleVertexList
    
    def divideFace(self, singleFace):
        # Vertex calculation
        baseVertexList = self.getFaceVertexList(singleFace)
        middleVertex = self.calculateMiddleVertex(baseVertexList)
        edgeMiddleVertexList = self.calculateEdgeMiddleVertexList(singleFace)
        dividedVertexList = baseVertexList + edgeMiddleVertexList + [middleVertex]
        # Face calculation
        rightBottomFace = [0, 5, 8, 4]
        rightTopFace = [5, 1, 6, 8]
        leftTopFace = [8, 6, 2, 7]
        leftBottomFace = [4, 8, 7, 3]
        # Append faces to cumulativeFaceList
        cumulativeFaceList = []
        cumulativeFaceList.append(rightBottomFace)
        cumulativeFaceList.append(rightTopFace)
        cumulativeFaceList.append(leftTopFace)
        cumulativeFaceList.append(leftBottomFace)
        dividedFaceList = cumulativeFaceList
        #
        return dividedVertexList, dividedFaceList
    
    def calibrateFaceList(self, moveAmount, faceList):
        cumulativeFaceList = []
        for singleFace in faceList:
            calibratedFace = self.calibrateSingleFace(moveAmount, singleFace)
            cumulativeFaceList.append(calibratedFace)
        return cumulativeFaceList

    def calibrateSingleFace(self, moveAmount, singleFace):
        cumulativeFace = []
        singleFaceLength = len(singleFace)
        singleFaceRange = range(singleFaceLength)
        for vertexPointerIndex in singleFaceRange:
            calibratedVertexPointer = singleFace[vertexPointerIndex] + moveAmount 
            cumulativeFace.append(calibratedVertexPointer)
        calibratedSingleFace = cumulativeFace
        return calibratedSingleFace

    def subdivideVertexListFaceList(self):
        cumulativeVertexList = []
        cumulativeFaceList = []
        faceList = self.getFaceList()
        for singleFace in faceList:
            dividedVertexList, dividedFaceList = self.divideFace(singleFace)
            cumulativeVertexListLength = len(cumulativeVertexList)
            calibratedDividedFaceList = self.calibrateFaceList(cumulativeVertexListLength, dividedFaceList)
            cumulativeVertexList += dividedVertexList
            cumulativeFaceList += calibratedDividedFaceList
        subdividedVertexList = cumulativeVertexList
        subdividedFaceList = cumulativeFaceList
        return subdividedVertexList, subdividedFaceList
        

    def subdivision(self, subdivisionAmount):
        mutantObj3D = copy.deepcopy(self)
        subdivisionRange = range(subdivisionAmount)
        for _ in subdivisionRange:
            subdividedVertexList, subdividedFaceList = mutantObj3D.subdivideVertexListFaceList()
            mutantObj3D.setVertexList(subdividedVertexList)
            mutantObj3D.setFaceList(subdividedFaceList)
        subdividedObject = mutantObj3D
        return subdividedObject
