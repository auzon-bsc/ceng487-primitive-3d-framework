# CENG 487 Assignment6 by
# Oğuzhan Özer
# StudentId:260201039
# December 2021

import sys

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from light import DirectionalLight, PointLight, Spotlight

from shader import *
from shape_factory import ShapeFactory
from vector import *
from matrix import *
from shapes import *
from camera import *
from scene import *
from view import *
from obj_parser import ObjParser

# window size
width, height = 640, 480

# create grid
grid = Grid("grid", 10, 10)
grid.setDrawStyle(DrawStyle.WIRE)
grid.setWireWidth(0.1)

# create camera
camera = Camera()
camera.createView( 	Point3f(0.0, 50.0, 100.0), \
                    Point3f(0.0, 15.0, 0.0), \
                    Vector3f(0.0, 1.0, 0.0) )
camera.setNear(1)
camera.setFar(1000)
camera.setAspect(width / height)

# create View
view = View(camera, grid)

# init scene
scene = Scene()
view.setScene(scene)

# parse object files from command line
parser = ObjParser()
parser.parseCL()
parser.parseFilesLines()
objsData = parser.parseWavefrontObjFiles()

# create the objects
factory = ShapeFactory(objsData)
shapes = factory.createAll()
d = 0
for shape in shapes:
    shape.addTexture("Bricks_001.png")
    # shape.addTexture("Bricks_003.png")
    shape.Translate(d, 0, 0)
    d += 2
    scene.add(shape)

directionalLight = DirectionalLight(
    dir = numpy.array([1.0, 1.0, 1.0, 1.0], dtype='float32'),
    color = numpy.array([1.0, 1.0, 1.0, 1.0], dtype='float32'),
    intensity = 0.3)
scene.addLight(directionalLight)

pointLight = PointLight(
    pos = numpy.array([5.0, 25.0, 5.0, 1.0], dtype='float32'),
    color = numpy.array([1.0, 1.0, 1.0, 1.0], dtype='float32'),
    intensity = 0.5
)
scene.addLight(pointLight)

spotLight = Spotlight(
    pos = numpy.array([0.0, 50.0, 200.0, 1.0], dtype='float32'),
    cutoff = cos(0.1),
    color = numpy.array([1.0, 1.0, 1.0, 1.0], dtype='float32'),
    intensity = 0.7,
    dir = numpy.array([0.0, -0.15, -1.0, 1.0], dtype='float32'),
)
scene.addLight(spotLight)

# create (default) shader
shader = Shader()


def main():
    global view
    global width, height
    
    glutInit(sys.argv)
    
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)
    
    glutCreateWindow("CENG487 Assigment Template")
    
    # init shader here because it cannot be initialized before creating window
    shader.initProgram()
    # link the objects with shader
    for shape in shapes:
        shape.programID = shader.programID

    grid.programID = shader.programID

    # define callbacks
    glutDisplayFunc( view.draw )
    glutIdleFunc( view.idleFunction )
    glutReshapeFunc( view.resizeView )
    glutKeyboardFunc( view.keyPressed )
    glutSpecialFunc( view.specialKeyPressed )
    glutMouseFunc( view.mousePressed )
    glutMotionFunc( view.mouseMove )

    # # Initialize our window
    glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LEQUAL)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glEnable(GL_LINE_SMOOTH)			# Enable line antialiasing
    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix

    # # create the perpective projection
    gluPerspective( view.camera.fov, float(width)/float(height), camera.near, camera.far )
    glMatrixMode(GL_MODELVIEW)

    # Start Event Processing Engine
    glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
print("Hit ESC key to quit.")
main()

