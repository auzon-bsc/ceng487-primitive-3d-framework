# CENG 487 Assignment1 by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

from abc import ABC, abstractmethod
from typing import *
import copy
from mat3d import Mat3d
from enum import Enum
from vec3d import Vec3d
from dataclasses import dataclass

@dataclass
class Adjacency():
    adjacentVertices = set()
    adjacentFaces = set()
    adjacentEdges = set()

    def addVertex(self, vertex):
        self.adjacentVertices.add(vertex)
    
    def addFace(self, face):
        self.adjacentFaces.add(face)
    
    def addEdge(self, edge):
        self.adjacentEdges.add(edge)

@dataclass
class AdjacencyTable():
    adjacencies = set()
    
    def addAdjacency(self, adjacency):
        self.adjacencies.add(adjacency)

    def getAdjacency(self, index):
        return self.adjacencies[index]

@dataclass
class FullAdjacencyList:
    vertexAdjacencyTable: AdjacencyTable()
    faceAdjacencyTable: AdjacencyTable()
    edgeAdjacencyTable: AdjacencyTable()
    
    def fillAdjacency(self, vertices, faces, edges):
        self._fillVertexAdjacencyTable(vertices, faces, edges)
        self._fillFaceAdjacencyTable(faces, edges)
        self._fillEdgeAdjacencyTable(vertices, faces, edges)
    
    def _fillVertexAdjacencyTable(self, vertices, faces, edges):
        lenVertices = len(vertices)
        rangeVertices = range(lenVertices)
        for vertexIndex in rangeVertices:
            vertexAdjacency = self._findVertexAdjacency(vertexIndex, faces, edges)
            self.vertexAdjacencyTable.add(vertexAdjacency)

    def _findVertexAdjacency(self, vertexIndex, faces, edges):
        """Find single vertex adjacency"""
        vertexAdjacency = Adjacency()
        for edge in edges:
            if vertexIndex == edge[0]:
                vertexAdjacency.addEdge(edge)
                edgeEnd = edge[1]
                vertexAdjacency.addVertex(edgeEnd)
            elif vertexIndex == edge[1]:
                vertexAdjacency.addEdge(edge)
                edgeStart = edge[0]
                vertexAdjacency.addVertex(edgeStart)
        for face in faces:
            if vertexIndex in face:
                vertexAdjacency.addFace(face)
        return vertexAdjacency

    def _fillFaceAdjacencyTable(self, faces, edges):
        for face in faces:
            faceAdjacency = self._findFaceAdjacency(face, faces, edges)
            self.faceAdjacencyTable.addAdjacency(faceAdjacency)
    
    def _findFaceAdjacency(self, face, faces, edges):
        faceAdjacency = Adjacency()
        # find adjacent edges
        for edge in edges:
            # add the edges of the face
            if edge[0] in face and edge[1] in face:
                faceAdjacency.addEdge(edge)
        # find adjacent vertices
        for vertexIndex in face:
            # add the vertices of the face
            faceAdjacency.addVertex(vertexIndex)
        # find adjacent faces
        for otherFace in faces:
            # a face cannot be adjacent to itself
            if otherFace == face:
                continue
            else:
                for edge in edges:
                    # add the otherFace if they share an edge
                    if edge[0] in face and edge[1] in face and edge[0] in otherFace and edge[1] in otherFace:
                        faceAdjacency.addFace(otherFace)
        return faceAdjacency

    def _fillEdgeAdjacencyTable(self, vertices, faces, edges):
        for edge in edges:
            edgeAdjacency = self._findEdgeAdjacency(edge, faces, vertices, edges)
            self.edgeAdjacencyTable.addAdjacency(edgeAdjacency)

    def _findEdgeAdjacency(self, edge, vertices, faces, edges):
        edgeAdjacency = Adjacency()
        edgeStart = edge[0]
        edgeEnd = edge[1]
        # adjacent vertices: start and end vertices of the edge   
        edgeAdjacency.addVertex(edgeStart)
        edgeAdjacency.addVertex(edgeEnd)
        # adjacent faces: any face including start and end vertices of the edge
        for aFace in faces:
            startExists = False
            endExists = False
            for vertexIndex in aFace:
                currentVertex = vertices[vertexIndex]
                if currentVertex == edgeStart:
                    startExists = True
                elif currentVertex == edgeEnd:
                    endExists = True
            # the start vertex and end vertex of the edge is on the face
            if startExists and endExists:
                edgeAdjacency.addFace(aFace)
        # find adjacent edges
        for anEdge in edges:
            for aFace in edgeAdjacency.adjacentFaces:
                # same edge
                if anEdge[0] in aFace and anEdge[1] in aFace:
                    continue
                 # an edge shares a point of base edge and it's on adjacent face
                elif anEdge[0] in aFace or anEdge[1] in aFace:
                    edgeAdjacency.addEdge(anEdge)




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

    _adjacencyList: FullAdjacencyList

    def __init__(self) -> None:
        # create vec3d objects from vertices and add them to vertices array of this object
        self._vertexList = []
        self._faceList = []
        self._edgeList = []

        # set all transformation matrices to identity (objects won't be transformed)
        self._compositeScalingMatrix = Mat3d.identity()
        self._compositeRotationMatrix = Mat3d.identity()
        self._compositeTranslationMatrix = Mat3d.identity()

        # adjacency list
        self._adjacencyList = FullAdjacencyList()

    def getVertexList(self):
        vertexList = self._vertexList
        vertexListClone = copy.deepcopy(vertexList)
        return vertexListClone

    def getFaceList(self):
        faceList = self._faceList
        faceListClone = copy.deepcopy(faceList)
        return faceListClone

    def getAdjacentFacesFromVertexIndex(self, vertexIndex):
        return self._adjacencyList.vertexAdjacencyTable.adjacencies.getAdjacency(vertexIndex).adjacentFaces
    
    def getAdjacentVerticesFromVertexIndex(self, vertexIndex):
        return self._adjacencyList.vertexAdjacencyTable.adjacencies.getAdjacency(vertexIndex).adjacentVertices
    
    def getAdjacentEdgesFromVertexIndex(self, vertexIndex):
        return self._adjacencyList.vertexAdjacencyTable.adjacencies.getAdjacency(vertexIndex).adjacentEdges

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

    def addEdge(self, edge):
        self._edgeList.append(edge)

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

    def catmullClark(self, faces, edges):
        """
        To make catmull clark subdivision, 
        
        For each face add a face point, 
            To find face point,
            Find the average of all original points for the respective face
                To find the average,
                Sum all points and divide the number of points
        
        For each edge, add an edge point, 
            To find the edge point,
            Find the average of the two neighboring face points and its two original endpoints
                To find the average,
                Sum all points and divide the number of points
        
        For each original point (P), 
        take the average (F) of all n (recently created) face points for faces touching P, 
        and take the average (R) of all n edge midpoints for original edges touching P, 
        where each edge midpoint is the average of its two endpoint vertices,
        Move each original point to the new vertex point ( F + 2R + (n - 3)P ) / n -barycenter-
        
        Form edges and meshes in the new mesh
            Connect each new face point to the new edge points of all original edges defining the original face
            Connect each new vertex point to the new edge points of all original edges incident on the original vertex
            Define new faces as enclosed by edges
        """
        self._adjacencyList.fillAdjacencyTable()

        newPoints = []
        originalPoints = self._getVertexList()
        lenOriginalPoints = len(originalPoints)
        rangeOriginalPoints = range(lenOriginalPoints)
        for aPointIndex in rangeOriginalPoints:
            P = originalPoints[aPointIndex]
            
            adjacentFaces = self.getAdjacentFacesFromVertexIndex(aPointIndex)
            facePoints = []
            for aFace in adjacentFaces:
                faceMiddle = self._findFacePoint(aFace)
                facePoints.append(faceMiddle)
            
            adjacentEdges = self.getAdjacentFacesFromVertexIndex(aPointIndex)
            edgePoints = []
            for anEdge in adjacentEdges:
                edgeMiddle = self._findEdgePoint(anEdge)
                edgePoints.append(edgeMiddle)
            
            F = self._avarageVertex(facePoints)
            R = self._avarageVertex(edgePoints)
            n = len(facePoints)
            newPoint = (F + 2*R + (n - 3)*P) / n
            newPoints.append(newPoint)

    
    def _findFacePoint(self, face):
        pass

    def _findEdgePoint(self, edge):
        pass

    def _avarageVertex(self, vertexList):
        pass