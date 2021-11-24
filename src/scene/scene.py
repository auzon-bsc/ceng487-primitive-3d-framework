from draw_handler.draw_handler import DrawHandler
from obj3d import Obj3d
from OpenGL.GL import *
from OpenGL.GLUT import *


class Scene:
    """
    Scene class holds 3D objects.

    """
    _objectList: list
    _textList: list
    _projectedVertexList2D: list
    _parameterDict: dict

    def __init__(self) -> None:
        """
        Initialize empty Scene object
        """
        self._objectList = []
        self._textList = []
        self._parameterDict = {
            'objectToDraw': 0,
            'subdivisionAmount': 0
        }
    
    def setParameter(self, parameterKey, parameterValue):
        self._parameterDict[parameterKey] = parameterValue

    def incrementSubdivision(self):
        parameterDict = self._parameterDict
        subdivisionAmount = parameterDict['subdivisionAmount']
        incrementedValue = subdivisionAmount + 1
        self.setParameter('subdivisionAmount', incrementedValue)

    def decrementSubdivision(self):
        parameterDict = self._parameterDict
        subdivisionAmount = parameterDict['subdivisionAmount']
        if subdivisionAmount > 0:
            decrementedValue = subdivisionAmount - 1
            self.setParameter('subdivisionAmount', decrementedValue)

    def addText(self, text):
        textList = self._textList
        textList.append(text)

    def addObj3D(self, obj3D):
        """
        Add a 3D object

        Args:
            obj3D (Obj3d): 3D object to add
        """
        self._objectList.append(obj3D)

    def removeObj3D(self, obj3D):
        """
        Remove a 3D object

        Args:
            obj3D (Obj3d): 3D object to remove

        Returns:
            Obj3d: Removed object
        """
        removedObj3D = self._objectList.remove(obj3D)
        return removedObj3D

    def popObj3D(self, index):
        """
        Pop a 3D object according to given index

        Args:
            index (int): Index of the 3D object that wanted to be popped

        Returns:
            Obj3d: Popped 3D object
        """
        poppedObj3D = self._objectList.pop(index)
        return poppedObj3D

    def getObj3D(self, index):
        """
        Get 3D object where the given index points

        Args:
            index (int): Index of the wanted 3D object

        Returns:
            Obj3d: 3D object at the given index
        """
        wantedObj3D = self._objectList[index]
        return wantedObj3D

    def getVertices(self, index):
        wantedObj3D: Obj3d

        wantedObj3D = self.getObj3D(index)
        wantedVertices = wantedObj3D.transform()
        return wantedVertices

    def getFaces(self, index):
        wantedObj3D: Obj3d

        wantedObj3D = self.getObj3D(index)
        wantedFaces = wantedObj3D.faces()
        return wantedFaces

    def drawScene(self):
        object: Obj3d

        # Clear The Screen And The Depth Buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Reset The View
        glLoadIdentity()

        # Move Into The Screen
        glTranslatef(0.0, 0.0, -10.0)

        # Draw all objects
        for object in self._objectList:
            subdividedObject = object.subdivision(self._parameterDict['subdivisionAmount'])
            subdividedObject.rotate("x", 0.1)
            subdividedTransformedVertexList = subdividedObject.calculateTransformedVertexList()
            subdividedObjectFaceList = subdividedObject.getFaceList()
            DrawHandler.drawObjectQuad(subdividedTransformedVertexList, subdividedObjectFaceList)
            DrawHandler.drawObjectLines(subdividedTransformedVertexList, subdividedObjectFaceList)

        # Draw text
        text = "Subdivision number: "
        text += f"{self._parameterDict['subdivisionAmount']}"
        posX = 0
        posY = 0
        DrawHandler.drawText(text, posX, posY)

        # Draw menu
        textList = self._textList
        menuPosX = 0
        menuPosY = 575
        DrawHandler.drawTextList(textList, menuPosX, menuPosY)

        #  since this is double buffered, swap the buffers to display what just got drawn.
        glutSwapBuffers()

    