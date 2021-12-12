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
        self.faces = (numpy.array(faces, dtype='uintc')).flatten()
        self.colors = []
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
        ## newly added code
        # shape data as numpy arrays
        self.position = numpy.array([0.0, 0.0, 0.0, 1.0], dtype='float32')
        self.vertices = self._toNumpy(vertices)
        self.colors = self._toNumpy(colors)
        self.UVs = numpy.array(UVs, dtype='float32')
        print(f"\npositions {self.position}")
        print(f"\nvertices {self.vertices}")
        print(f"\ncolors {self.colors}")
        print(f"\nUVs {self.UVs}")
        print(f"\nfaces {self.faces}")
        # VBO 
        self.VBO = None
        self.EBO = None
        # shader
        self.shader = Shader()

    def initializeVBO(self):
        # generate VBO id
        VBO = glGenBuffers(1)       
        # bind VBO to gl array buffer
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        # concatenate our data
        vertexData = numpy.concatenate((self.vertices, self.colors, self.UVs))      
        # set the data
        glBufferData( GL_ARRAY_BUFFER, vertexData, GL_STATIC_DRAW )       
        
        # generate vertex indices buffer
        EBO = glGenBuffers(1)
        # bind VBO to gl array buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO) 
        # set the data
        elementSize = numpy.dtype(numpy.uintc).itemsize
        glBufferData( GL_ELEMENT_ARRAY_BUFFER, len(self.faces) * elementSize, self.faces, GL_STATIC_DRAW ) 
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        # reset binding
        glBindBuffer(GL_ARRAY_BUFFER, 0)        
        # set the VBO id and index id
        self.VBO = VBO
        self.EBO = EBO

    def initProgram(self):
        self.shader.initProgram()

    def getModelMatrix(self):
        return numpy.array([1.0, 0.0, 0.0, 0.0,
                            0.0, 1.0, 0.0, 0.0,
                            0.0, 0.0, 1.0, 0.0,
                            self.position[0], self.position[1], self.position[2], 1.0], dtype='float32')

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
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # use shader
        glUseProgram(self.shader.programID)

        # get matrices and bind them to vertex shader locations
        modelLocation = glGetUniformLocation( self.shader.programID, "model" )
        glUniformMatrix4fv(modelLocation, 1, GL_FALSE, getModelMatrix())
        viewLocation = glGetUniformLocation(self.shader.programID, "view")
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE, getViewMatrix())
        projLocation = glGetUniformLocation(self.shader.programID, "proj")
        glUniformMatrix4fv(projLocation, 1, GL_FALSE, getProjMatrix(camNear, camFar, camAspect, camFov))

        # reset our vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        elementSize = numpy.dtype(numpy.float32).itemsize

        # setup vertex attributes
        offset = 0

        # location 0
        glVertexAttribPointer(0, vertexDim, GL_FLOAT, GL_FALSE, elementSize * vertexDim, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(0)

        # define colors which are passed in location 1 - they start after all positions and has four floats consecutively
        offset += elementSize * vertexDim * nVertices
        glVertexAttribPointer(1, vertexDim, GL_FLOAT, GL_FALSE, elementSize * vertexDim, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(1)

        glDrawArrays(GL_TRIANGLES, 0, nVertices)

        # reset to defaults
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glUseProgram(0)

        glutSwapBuffers()

    def Translate(self, x, y, z):
        translate = Matrix.T(x, y, z)
        self.obj2World = self.obj2World.product(translate)

    def _toNumpy(self, listOfObjects):
        tmpList = []
        
        for obj in listOfObjects:
            objAttributes = obj.toList()
            tmpList += objAttributes
  
        return numpy.array(tmpList, dtype='float32')

class Cube(_Shape):
    def __init__(self, name, xSize, ySize, zSize, xDiv, yDiv, zDiv):
        vertices = []
        xStep = xSize / (xDiv + 1.0)
        yStep = ySize / (yDiv + 1.0)
        zStep = zSize / (zDiv + 1.0)

        #add corners
        vertices.append( Point3f(-xSize / 2.0, -ySize / 2.0, zSize / 2.0) )
        vertices.append( Point3f(xSize / 2.0, -ySize / 2.0, zSize / 2.0) )
        vertices.append( Point3f(-xSize / 2.0, ySize / 2.0, zSize / 2.0) )
        vertices.append( Point3f(xSize / 2.0, ySize / 2.0, zSize / 2.0) )
        vertices.append( Point3f(-xSize / 2.0, -ySize / 2.0, -zSize / 2.0) )
        vertices.append( Point3f(xSize / 2.0, -ySize / 2.0, -zSize / 2.0) )
        vertices.append( Point3f(-xSize / 2.0, ySize / 2.0, -zSize / 2.0) )
        vertices.append( Point3f(xSize / 2.0, ySize / 2.0, -zSize / 2.0) )

        faces = []
        faces.append( [0, 2, 3, 1] )
        faces.append( [4, 6, 7, 5] )
        faces.append( [4, 6, 2, 0] )
        faces.append( [1, 3, 7, 5] )
        faces.append( [2, 6, 7, 3] )
        faces.append( [4, 0, 1, 5] )

        # colors
        colors = []
        for _ in range (0, len(faces) + 1):
            r = random.uniform(0, 1)
            g = random.uniform(0, 1)
            b = random.uniform(0, 1)
            colors.append( ColorRGBA(r, g, b, 1.0) )

        # UVs
        UVs = []

        _Shape.__init__(self, name, vertices, faces, colors, UVs)
        self.drawStyle = DrawStyle.SMOOTH

        


