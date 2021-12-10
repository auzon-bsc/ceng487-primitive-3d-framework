from OpenGL.GL import *
from OpenGL.GLUT import *

from vec3d import Vec3d


class DrawHandler:
    @staticmethod
    def drawQuad(vertexList):
        """Draw quads for given vertices and face

        Args:
            vertices (list[Vec3d]): vertices of the object
            face (list[int]): a list contains index of vertices for a face
        """
        # begin drawing quads
        glBegin(GL_QUADS)
        # set color to white
        glColor3f(1, 1, 1)
        # draw first vertex
        glVertex3f(vertexList[0].x, vertexList[0].y, vertexList[0].z)
        # draw second vertex
        glVertex3f(vertexList[1].x, vertexList[1].y, vertexList[1].z)
        # draw third vertex
        glVertex3f(vertexList[2].x, vertexList[2].y, vertexList[2].z)
        # draw last vertex
        glVertex3f(vertexList[3].x, vertexList[3].y, vertexList[3].z)
        # end drawing quads
        glEnd()

    @staticmethod
    def drawObjectQuad(vertexList, faceList):
        """Draw quads for given vertices and face

        Args:
            vertices (list[Vec3d]): vertices of the object
            face (list[int]): a list contains index of vertices for a face
        """
        for face in faceList:
            quadVertexList = []
            for vertexIndex in face:
                selectedVertex = vertexList[vertexIndex]
                quadVertexList.append(selectedVertex)
            DrawHandler.drawQuad(quadVertexList)

    @staticmethod
    def drawLine(vertex1, vertex2):
        glBegin(GL_LINES)
        glColor3f(0, 0, 0)
        glVertex3f(vertex1.x, vertex1.y, vertex1.z)
        glVertex3f(vertex2.x, vertex2.y, vertex2.z)
        glEnd()

    @staticmethod
    def drawMultipleLines(vertexList, face):
        # Calculate range of the vertex list to iterate
        faceLength = len(face)
        faceRange = range(faceLength)
        # Loop for all indexes of vertex list
        for i in faceRange:
            # Find previous vertex
            previousVertexIndex = face[i - 1]
            previousVertex = vertexList[previousVertexIndex]
            # Find current vertex
            currentVertexIndex = face[i]
            currentVertex = vertexList[currentVertexIndex]
            # Draw a line from previous vertex to current vertex
            DrawHandler.drawLine(previousVertex, currentVertex)

    @staticmethod
    def drawObjectLines(vertexList, faceList):
        lineVertexList = []
        for vertex in vertexList:
            vertexClone = vertex.clone()
            offsetVertex = Vec3d([0, 0, 0.03, 1])
            lineVertex = vertexClone + offsetVertex
            lineVertexList.append(lineVertex)
        for face in faceList:
            DrawHandler.drawMultipleLines(lineVertexList, face)

    @staticmethod
    def drawPoints(vertexList):
        glBegin(GL_POINTS)
        for vertex in vertexList:
            glVertex3f(vertex.x, vertex.y, vertex.z)
        glEnd()

    @staticmethod
    def drawText(text, posX, posY):
        # Color red for text
        glColor3f(1, 0, 0.3)
        # Position text
        glWindowPos2i(posX, posY)
        # draw each character
        for c in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    @staticmethod
    def drawTextList(textList, posX, posY):
        for text in textList:
            DrawHandler.drawText(text, posX, posY)
            posY = posY - 18
