import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from math import pi,sin,cos,sqrt,acos
from shader import Shader
from vector import *
from matrix import *
from boundingbox import *
from defs import DrawStyle

__all__ = ['_Shape', 'Cube', 'DrawStyle']

class _Shape:
    def __init__(self, name, vertices, faces, colors, UVs):
        self.vertices = vertices
        self.edges = []
        self.faces = faces
        self.colors = colors
        self.UVs = UVs
        self.obj2World = Matrix()
        self.drawStyle = DrawStyle.NODRAW
        self.wireOnShaded = False
        self.wireWidth = 2
        self.name = name
        self.fixedDrawStyle = False
        self.wireColor = ColorRGBA(0.7, 1.0, 0.0, 1.0)
        self.wireOnShadedColor = ColorRGBA(1.0, 1.0, 1.0, 1.0)
        self.bboxObj = BoundingBox()
        self.bboxWorld = BoundingBox()
        self.calcBboxObj()
        self.VBO = None
        self.EBO = None
        self.programID = None                                           # shader programID

    def initializeVBO(self):
        if self.VBO is not None and self.EBO is not None:
            return

        # concatenate our vertex data
        verticesToNumpy = self._toNumpy(self.vertices)
        colorsToNumpy = self._toNumpy(self.colors)
        UVsToNumpy = self._toNumpy(self.UVs)
        vertexData = numpy.concatenate((verticesToNumpy, colorsToNumpy, UVsToNumpy))      
        
        # generate buffer for VBO and bind it
        VBO = glGenBuffers(1)   
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        
        # set the data and reset the binding
        glBufferData( GL_ARRAY_BUFFER, vertexData, GL_STATIC_DRAW )       
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        
        # construct index data (faces as 1d numpy array)
        indexData = (numpy.array(self.faces, dtype='uintc')).flatten()

        # generate buffer for vertex indices (faces) and bind it
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO) 

        # set the data and reset the binding
        glBufferData( GL_ELEMENT_ARRAY_BUFFER, indexData, GL_STATIC_DRAW ) 
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        
        # set the VBO id and index id
        self.VBO = VBO
        self.EBO = EBO

    def _toNumpy(self, listOfObjects):
        tmpList = []
        
        for obj in listOfObjects:
            objAttributes = obj.toList()
            tmpList += objAttributes
  
        return numpy.array(tmpList, dtype='float32')

    def calcBboxObj(self):
        for vertex in self.vertices:
            self.bboxObj.expand(vertex)


    def setDrawStyle(self, style):
        self.drawStyle = style


    def setWireColor(self, r, g, b, a):
        self.wireColor = ColorRGBA(r, g, b, a)


    def setWireWidth(self, width):
        self.wireWidth = width


    def draw(self):
        # set the draw style
        if self.drawStyle is DrawStyle.WIRE:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glLineWidth(self.wireWidth)

        # set uniform model matrix of the shader
        modelLocation = glGetUniformLocation( self.programID, "model" )
        glUniformMatrix4fv(
            modelLocation,              #  
            1,                          #
            GL_FALSE,                   #
            self.obj2World.asNumpy()    # model matrix
        )
        
        # initialize our vertex buffer object and bind to array buffer
        self.initializeVBO()
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        # get how many bytes one axis value of our hcoordinates 
        # (i.e x axis = 1 * float32 = 4 bytes)
        elementSize = numpy.dtype(numpy.float32).itemsize

        # dimensions needed for stride and offset calculation
        vertexDim = 4       # (x, y, z, w)
        colorDim = 4        # (r, g, b, a)
        uvDim = 2           # (u, v)

        # set the starting position of the vertex attribute
        offset = 0
        # enable vertex position attribute and set its pointer
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(
            0, 
            vertexDim, 
            GL_FLOAT, 
            GL_FALSE, 
            elementSize * vertexDim,        # stride
            ctypes.c_void_p(offset)         # starting position
        )
        
        # set the starting position of the color attribute
        offset += (elementSize * vertexDim * len(self.vertices))
        # enable vertex color attribute and set its pointer
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(
            1, 
            colorDim, 
            GL_FLOAT, 
            GL_FALSE, 
            elementSize * colorDim,         # stride
            ctypes.c_void_p(offset)         # first color position
        )
        
        # set the starting position of the uv attribute
        offset += elementSize * colorDim * len(self.colors)
        # enable vertex uv pos attribute and set its pointer
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(
            2, 
            vertexDim, 
            GL_FLOAT, 
            GL_FALSE, 
            elementSize * uvDim,            # stride
            ctypes.c_void_p(offset)         # first uv position
        )
        
        faceDim = 4
        # draw elements (indexed draw / drawing according to faces)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glDrawElements(GL_QUADS, len(self.faces) * faceDim, GL_UNSIGNED_INT, None)

        # reset attribute arrays
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)

        # reset binded buffer
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # reset polygon mode
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

    def Translate(self, x, y, z):
        translate = Matrix.T(x, y, z)
        self.obj2World = self.obj2World.product(translate)

class Cube(_Shape):
    def __init__(self, name, xSize, ySize, zSize):
        vertices = []

        #add corners
        vertices.append( Point3f(-xSize / 2.0, -ySize / 2.0, zSize / 2.0) )
        vertices.append( Point3f(xSize / 2.0, -ySize / 2.0, zSize / 2.0) )
        vertices.append( Point3f(-xSize / 2.0, ySize / 2.0, zSize / 2.0) )
        vertices.append( Point3f(xSize / 2.0, ySize / 2.0, zSize / 2.0) )
        vertices.append( Point3f(-xSize / 2.0, -ySize / 2.0, -zSize / 2.0) )
        vertices.append( Point3f(xSize / 2.0, -ySize / 2.0, -zSize / 2.0) )
        vertices.append( Point3f(-xSize / 2.0, ySize / 2.0, -zSize / 2.0) )
        vertices.append( Point3f(xSize / 2.0, ySize / 2.0, -zSize / 2.0) )

        # add faces
        faces = []
        faces.append( [0, 2, 3, 1] )
        faces.append( [4, 6, 7, 5] )
        faces.append( [4, 6, 2, 0] )
        faces.append( [1, 3, 7, 5] )
        faces.append( [2, 6, 7, 3] )
        faces.append( [4, 0, 1, 5] )

        # add colors to each vertex
        colors = []
        for _ in range (len(vertices)):
            r = random.uniform(0, 1)
            g = random.uniform(0, 1)
            b = random.uniform(0, 1)
            colors.append( ColorRGBA(r, g, b, 1.0) )

        # UVs
        UVs = []

        _Shape.__init__(self, name, vertices, faces, colors, UVs)
        self.drawStyle = DrawStyle.SMOOTH

        


