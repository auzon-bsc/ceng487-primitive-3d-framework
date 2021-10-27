# Note:
# -----
# This Uses PyOpenGL and PyOpenGL_accelerate packages.  It also uses GLUT for UI.
# To get proper GLUT support on linux don't forget to install python-opengl package using apt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

from obj3d import Obj3d
from vec3d import Vec3d
from mat3d import Mat3d

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0

# Triangle obj
tri_v1 = Vec3d(0.0, 1.0, 0.0, 1.0)	# Top vertice
tri_v2 = Vec3d(-1.0, -1.0, 0.0, 1.0)	# Bottom left vertice
tri_v3 = Vec3d(1.0, -1.0, 0.0, 1.0)	# Bottom right vertice
tri_vertices = [tri_v1, tri_v2, tri_v3]
tri = Obj3d(tri_vertices)
tri_r = Mat3d.rotation("z", 0.5)
tri.append_transformation(tri_r)

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
	
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix
										# Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
	    Height = 1

    glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# The main drawing function. 
def DrawGLScene():
	# Clear The Screen And The Depth Buffer
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()					# Reset The View 

	# Move Left 1.5 units and into the screen 6.0 units.
	glTranslatef(-1.5, 0.0, -6.0)

	# Since we have smooth color mode on, this will be great for the Phish Heads :-).
	# Draw a triangle
	glBegin(GL_POLYGON)                 # Start drawing a polygon
	glColor3f(1.0, 0.0, 0.0)            # Red
	glVertex3f(tri.vertices[0].x, tri.vertices[0].y, tri.vertices[0].z)           # Top
	glColor3f(0.0, 1.0, 0.0)            # Green
	glVertex3f(tri.vertices[1].x, tri.vertices[1].y, tri.vertices[1].z)          # Bottom Right
	glColor3f(0.0, 0.0, 1.0)            # Blue
	glVertex3f(tri.vertices[2].x, tri.vertices[2].y, tri.vertices[2].z)         # Bottom Left
	glEnd()                             # We are done with the polygon

	for i in range(3):
		tri.vertices[i] = tri.vertices[i].transform(tri_r)

	# Move Right 3.0 units.
	glTranslatef(3.0, 0.0, 0.0)

	# Draw a square (quadrilateral)
	glColor3f(0.3, 0.5, 1.0)            # Bluish shade
	glBegin(GL_QUADS)                   # Start drawing a 4 sided polygon
	glVertex3f(-1.0, 1.0, 0.0)          # Top Left
	glVertex3f(1.0, 1.0, 0.0)           # Top Right
	glVertex3f(1.0, -1.0, 0.0)          # Bottom Right
	glVertex3f(-1.0, -1.0, 0.0)         # Bottom Left
	glEnd()                             # We are done with the polygon

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
	# If escape is pressed, kill everything.
    if args[0] == ESCAPE:
	    sys.exit()

def main():
	global window
	glutInit(sys.argv)

	# Select type of Display mode:   
	#  Double buffer 
	#  RGBA color
	# Alpha components supported 
	# Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	
	# get a 640 x 480 window 
	glutInitWindowSize(640, 480)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	window = glutCreateWindow("CENG487 Template")

	# Display Func
	glutDisplayFunc(DrawGLScene)

	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)
	
	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)
	
	# Register the function called when the keyboard is pressed.  
	glutKeyboardFunc(keyPressed)

	# Initialize our window. 
	InitGL(640, 480)

	# Start Event Processing Engine	
	glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
print("Hit ESC key to quit.")
main()
    	