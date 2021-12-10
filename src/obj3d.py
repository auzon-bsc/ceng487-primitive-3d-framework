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
    # ---- Type Definitions ----
    _vertexList: List[Vec3d]
    _faceList: List[List[int]]

    _compositeScalingMatrix: Mat3d
    _compositeRotationMatrix: Mat3d
    _compositeTranslationMatrix: Mat3d

    _subdivisionAmount: int

    # vertex adjacency table
    _vAT: List[Tuple[List, List, List]]
    # face adjacency table
    _fAT: List[Tuple[List, List, List]]
    # edge adjacency table
    _eAT: List[Tuple[List, List, List]]
    

    def __init__(self, vertexList, faceList) -> None:
        # create vec3d objects from vertices and add them to vertices array of this object
        self._vertexList = vertexList
        self._faceList = faceList
        self._edgeList = self._calculateEdges()
        # adjacency list
        self._vAT = self._calculateVAT()
        self._fAT = self._calculateFAT()
        self._eAT = self._calculateEAT()

        # set all transformation matrices to identity (objects won't be transformed)
        self._compositeScalingMatrix = Mat3d.identity()
        self._compositeRotationMatrix = Mat3d.identity()
        self._compositeTranslationMatrix = Mat3d.identity()


    # ---- Getters ----

    def getVertexList(self):
        vertexList = self._vertexList
        vertexListClone = copy.deepcopy(vertexList)
        
        return vertexListClone

    def getFaceList(self):
        faceList = self._faceList
        faceListClone = copy.deepcopy(faceList)
        
        return faceListClone


    # ---- Edge Calculations ----

    def _calculateEdges(self):
        objectEdges = []
        
        for face in self._faceList:
            faceEdges = []
            
            lenFace = len(face)
            rangeFace = range(lenFace)
            # find the edges of the face
            for i in rangeFace:
                startVertex = face[i]
                endVertex = face[(i + 1) % lenFace]
                edge = self._createEdge(startVertex, endVertex)
                inverseEdge = self._createEdge(endVertex, startVertex)
                # if edge is not already in edges append that edge
                if edge not in objectEdges and inverseEdge not in objectEdges:
                    faceEdges.append(edge)
            # concatenate the edges of the face to all edges
            objectEdges += faceEdges
        
        return objectEdges


    def _createEdge(self, startVertex, endVertex):
        # create an edge
        return startVertex, endVertex

    # ---- Adjacency Table Calculations of Vertices ----

    def _calculateVAT(self):
        vAT = []
        # calculate adjacencies of the vertices
        for vertexIndex in range(len(self._vertexList)):
            adjacenciesOfVertex: Tuple
            adjacenciesOfVertex = self._calculateVA(vertexIndex)
            vAT.append(adjacenciesOfVertex)
        
        return vAT

    ## ----- Adjacency Calculations of Single Vertex ----
    
    def _calculateVA(self, vertexIndex):
        """Calculate the adjacencies of a single vertex"""
        adjacenciesOfVertex: Tuple
        vVA = self._calculateVVA(vertexIndex)
        vFA = self._calculateVFA(vertexIndex)
        vEA = self._calculateVEA(vertexIndex)
        adjacenciesOfVertex = (vVA, vFA, vEA)
        
        return adjacenciesOfVertex

    def _calculateVVA(self, vertexIndex):
        """Calculate the vertex adjacencies of a single vertex"""
        vVA = []
        
        for edgeIndex in range(len(self._edgeList)):
            edge = self._edgeList[edgeIndex]
            if vertexIndex == edge[0]:
                vVA.append(edge[1])
            
            elif vertexIndex == edge[1]:
                vVA.append(edge[0])

        return vVA
    
    def _calculateVFA(self, vertexIndex):
        """Calculate the face adjacencies of a single vertex"""
        vFA = []
        
        for faceIndex in range(len(self._faceList)):
            face = self._faceList[faceIndex]
            
            if vertexIndex in face:
                vFA.append(faceIndex)

        return vFA
    
    def _calculateVEA(self, vertexIndex):
        """Calculate the edge adjacencies of a single vertex"""
        vEA = []

        for edgeIndex in range(len(self._edgeList)):
            edge = self._edgeList[edgeIndex]
            
            if vertexIndex == edge[0] or vertexIndex == edge[1]:
                vEA.append(edgeIndex)
        
        return vEA
    
    # ---- Adjacency Table Calculations of Faces ----

    def _calculateFAT(self):
        """Calculate the adjacencies of the faces"""
        fAT = []

        for faceIndex in range(len(self._faceList)):
            adjacenciesOfFace: Tuple
            adjacenciesOfFace = self._calculateFA(faceIndex)
            fAT.append(adjacenciesOfFace)

        return fAT

    ## ----- Adjacency Calculations of Single Face ----

    def _calculateFA(self, faceIndex):
        """Calculate the adjacencies of a single face"""
        adjacenciesOfFace: Tuple
        fVA = self._calculateFVA(faceIndex)
        fFA = self._calculateFFA(faceIndex)
        fEA = self._calculateFEA(faceIndex)
        adjacenciesOfFace = (fVA, fFA, fEA)

        return adjacenciesOfFace

    def _calculateFVA(self, faceIndex):
        """Calculate the vertex adjacencies of a single face"""
        fVA = self._faceList[faceIndex]

        return fVA
    
    def _calculateFFA(self, faceIndex):
        """Calculate the face adjacencies of a single face"""
        fFA = []
        face = self._faceList[faceIndex]
        
        for otherFaceIndex in range(len(self._faceList)):
            
            if otherFaceIndex == faceIndex:
                continue
            
            else:
                otherFace = self._faceList[otherFaceIndex]
                
                for edgeIndex in range(len(self._edgeList)):
                    edge = self._edgeList[edgeIndex]

                    if edge[0] in face and edge[1] in face and edge[0] in otherFace and edge[1] in otherFace and otherFaceIndex not in fFA:

                        fFA.append(otherFaceIndex)
                            
        return fFA
        
    def _calculateFEA(self, faceIndex):
        """Calculate the edge adjacencies of a single face"""
        fEA = []
        face = self._faceList[faceIndex]

        for edgeIndex in range(len(self._edgeList)):
            edge = self._edgeList[edgeIndex]

            if edge[0] in face and edge[1] in face:

                fEA.append(edgeIndex)

        return fEA
    
    # # ----- Calculate Edge Adjacency Table ----

    def _calculateEAT(self):
        """Calculate the adjacencies of the edges"""
        eAT = []

        for edgeIndex in range(len(self._edgeList)):
            adjacenciesOfEdge: Tuple
            adjacenciesOfEdge = self._calculateEA(edgeIndex)
            eAT.append(adjacenciesOfEdge)

        return eAT

    ## ----- Adjacency Calculations of Single Edge ----

    def _calculateEA(self, edgeIndex):
        """Calculate the adjacencies of a single edge"""
        adjacenciesOfEdge: Tuple
        eVA = self._calculateEVA(edgeIndex)
        eFA = self._calculateEFA(edgeIndex)
        eEA = self._calculateEEA(edgeIndex)
        adjacenciesOfEdge = (eVA, eFA, eEA)

        return adjacenciesOfEdge

    def _calculateEVA(self, edgeIndex):
        """Calculate the vertex adjacencies of a single edge"""
        eVA = []
        edge = self._edgeList[edgeIndex]
        eVA.append(edge[0])
        eVA.append(edge[1])

        return eVA
    
    def _calculateEFA(self, edgeIndex):
        """Calculate the face adjacencies of a single edge"""
        eFA = []
        edge = self._edgeList[edgeIndex]
        
        for otherFaceIndex in range(len(self._faceList)):
            face = self._faceList[otherFaceIndex]
            
            if otherFaceIndex in eFA:
                continue

            if edge[0] in face and edge[1] in face:
                eFA.append(otherFaceIndex)
                            
        return eFA
        
    def _calculateEEA(self, edgeIndex):
        """Calculate the edge adjacencies of a single edge"""
        eEA = []
        edge = self._edgeList[edgeIndex]

        for otherEdgeIndex in range(len(self._edgeList)):
            otherEdge = self._edgeList[otherEdgeIndex]
            
            if otherEdgeIndex == edgeIndex:
                continue
            
            elif edge[0] in otherEdge or edge[1] in otherEdge:

                for faceIndex in range(len(self._faceList)):
                    face = self._faceList[faceIndex]

                    if edge[0] in face and edge[1] in face and otherEdge[0] in face and otherEdge[1] in face:
                        eEA.append(otherEdgeIndex)
                        break
                        

        return eEA
   

    # ---- Matrix Operations ----

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

    def _calculateCompositeTransformationMatrix(self):
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
                print(f"ERROR: There is no val '{val}' in TransformationOrder ENUM")

        compositeTransformationMatrix = cumulativeMatrix
        return compositeTransformationMatrix

    def calculateTransformedVertexList(self):
        vertexList = self._vertexList
        compositeTransformationMatrix = self._calculateCompositeTransformationMatrix()
        tempVertexList = []
        for vertex in vertexList:
            transformedVertex = vertex.transform(compositeTransformationMatrix)
            tempVertexList.append(transformedVertex)
        transformedVertexList = tempVertexList
        return transformedVertexList

    # ---- Catmull-Clark Subdivision Operations ----
    def catmullClark(self, subdivisionAmount):
        """Subdivide the object subdivisionAmount of times with catmull clark algorithm"""
        obj3D = self
        
        for _ in range(subdivisionAmount):
            obj3D = obj3D._catmullClarkOnce()
        
        return obj3D
    
    def _catmullClarkOnce(self):
        """Subdivide the object once with catmull clark algorithm"""
        facePoints = self._calculateFacePoints()
        edgePoints = self._calculateEdgePoints(facePoints)
        cornerPoints = self._calculateCornerPoints(facePoints)

        newVertices = cornerPoints + facePoints + edgePoints
        
        newFaces = []
        
        lCP = len(cornerPoints)
        lFP = len(facePoints)
        for vertexIndex in range(len(self._vertexList)):
            vFA = self._vAT[vertexIndex][1]
            vEA = self._vAT[vertexIndex][2]

            for adjacentFacePointIndex in vFA:
                fEA = self._fAT[adjacentFacePointIndex][2]
                sameEdgeIndexes = list(set(vEA).intersection(fEA))
                newFace = [vertexIndex, lCP+lFP+sameEdgeIndexes[0], lCP+adjacentFacePointIndex, lCP+lFP+sameEdgeIndexes[1]]
                newFaces.append(newFace)
        
        return Obj3d(newVertices, newFaces)

    ## ---- Catmull-Clark Point Calculations ----

    def _calculateFacePoints(self):
        """Calculate face points for the catmull clark algorithm"""
        facePoints = []

        for faceIndex in range(len(self._faceList)):
            face = self._faceList[faceIndex]
            sumVertex = Vec3d([0, 0, 0, 1])
            
            for vertexIndex in face:
                vertex = self._vertexList[vertexIndex]
                sumVertex += vertex
            
            sumVertex.scale(1/len(face))
            facePoint = sumVertex

            facePoints.append(facePoint)
        

        return facePoints

    def _calculateEdgePoints(self, facePoints):
        """Calculate edge points for the catmull clark algorithm"""
        edgePoints = []

        for edgeIndex in range(len(self._edgeList)):
            
            edge = self._edgeList[edgeIndex]
            
            sumVertex = self._vertexList[edge[0]] + self._vertexList[edge[1]]
            eFA = self._eAT[edgeIndex][1]
            
            for faceIndex in eFA:
                sumVertex += facePoints[faceIndex]

            sumVertex.scale(1/(len(eFA) + 2))
            edgePoint = sumVertex
            edgePoints.append(edgePoint)

        return edgePoints

    def _calculateCornerPoints(self, facePoints):
        """Calculate corner points (new positions of old vertices) for the catmull clark algorithm"""
        cornerPoints = []

        for vertexIndex in range(len(self._vertexList)):

            vFA = self._vAT[vertexIndex][1]
            F = Vec3d([0, 0, 0, 1])
            
            for adjacentFacePointIndex in vFA:
                F += facePoints[adjacentFacePointIndex]
            F.scale(1/len(vFA)) 

            vEA = self._vAT[vertexIndex][2]
            R = Vec3d([0, 0, 0, 1])
            
            for adjacentEdgePointIndex in vEA:
                edge = self._edgeList[adjacentEdgePointIndex]
                linearEdgePoint = self._vertexList[edge[0]] + self._vertexList[edge[1]]
                linearEdgePoint.scale(1/2)
                R += linearEdgePoint
            R.scale(1/len(vEA)) 
            
            P = self._vertexList[vertexIndex].clone()
            
            n = len(vFA)
            R.scale(2)
            P.scale(n-3)
            cornerPoint = (F + R + P)
            cornerPoint.scale(1/n)
            cornerPoints.append(cornerPoint)

        return cornerPoints