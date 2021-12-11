import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from math import pi,sin,cos,sqrt,acos
from vector import *
from matrix import *
from boundingbox import *
from defs import DrawStyle

__all__ = ['_Shape', 'Cube', 'DrawStyle']

class _Shape:
	def __init__(self, name, vertices, faces):
		self.vertices = vertices
		self.edges = []
		self.faces = faces
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
		index = 0
		for face in self.faces:
			if self.drawStyle == DrawStyle.FACETED or self.drawStyle == DrawStyle.SMOOTH:
				glBegin(GL_POLYGON)

				if len(self.colors) > 0:
					glColor3f(self.colors[index].r, self.colors[index].g, self.colors[index].b)
				else:
					glColor3f(1.0, 0.6, 0.0)

				for vertex in face:
					glVertex3f(self.vertices[vertex].x, self.vertices[vertex].y, self.vertices[vertex].z)
				glEnd()

			if self.drawStyle == DrawStyle.WIRE or self.wireOnShaded == True:
				glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
				glLineWidth(self.wireWidth)
				#glDisable(GL_LIGHTING)

				glBegin(GL_POLYGON)

				if self.wireOnShaded == True:
					if self.fixedDrawStyle == True:
						glColor3f(self.wireColor.r, self.wireColor.g, self.wireColor.b)
					else:
						glColor3f(self.wireOnShadedColor.r, self.wireOnShadedColor.g, self.wireOnShadedColor.b)
				else:
					glColor3f(self.wireColor.r, self.wireColor.g, self.wireColor.b)

				for vertex in face:
					glVertex3f(self.vertices[vertex].x, self.vertices[vertex].y, self.vertices[vertex].z)
				glEnd()

				glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
				#glEnable(GL_LIGHTING)

			index += 1

	def Translate(self, x, y, z):
		translate = Matrix.T(x, y, z)
		self.obj2World = self.obj2World.product(translate)


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

		_Shape.__init__(self, name, vertices, faces)
		self.drawStyle = DrawStyle.SMOOTH

		for i in range (0, len(faces) + 1):
			r = random.uniform(0, 1)
			g = random.uniform(0, 1)
			b = random.uniform(0, 1)
			self.colors.append( ColorRGBA(r, g, b, 1.0) )


