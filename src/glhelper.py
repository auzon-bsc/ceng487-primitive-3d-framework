# CENG487 Introduction To Computer Graphics
# Development Env Test Program
# Runs in python 3.x env
# with PyOpenGL and PyOpenGL-accelerate packages

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

from obj3d import Obj3d

# Number of the glut window.
window = 0

#
objects: list[Obj3d] = []


def AddObject(obj3d: Obj3d):
	objects.append(obj3d)


# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width,
		   Height):  # We call this right after our OpenGL window is created.
	glClearColor(0.0, 0.0, 0.0,
				 0.0)  # This Will Clear The Background Color To Black
	glClearDepth(1.0)  # Enables Clearing Of The Depth Buffer
	glDepthFunc(GL_LESS)  # The Type Of Depth Test To Do
	glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
	glShadeModel(GL_SMOOTH)  # Enables Smooth Color Shading

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()  # Reset The Projection Matrix
	# Calculate The Aspect Ratio Of The Window
	gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
	if Height == 0:  # Prevent A Divide By Zero If The Window Is Too Small
		Height = 1

	glViewport(
		0, 0, Width,
		Height)  # Reset The Current Viewport And Perspective Transformation
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)


# The main drawing function.
def DrawGLScene():
	global objects
	# Clear The Screen And The Depth Buffer
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	# Reset The View
	glLoadIdentity()

	# Move Left And Into The Screen
	glTranslatef(0.0, 0.0, -6.0)

	vertices = objects[0].transform()

	for face in objects[0].faces:
		glBegin(GL_QUADS)
		for vertex_index in face:
			glColor3f(vertices[vertex_index-1].matrix_arr[0][0], vertices[vertex_index-1].matrix_arr[1][0],
						vertices[vertex_index-1].matrix_arr[2][0])
			glVertex3f(vertices[vertex_index-1].matrix_arr[0][0], vertices[vertex_index-1].matrix_arr[1][0],
						vertices[vertex_index-1].matrix_arr[2][0])
		glEnd()

	#  since this is double buffered, swap the buffers to display what just got drawn.
	glutSwapBuffers()


# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(key, x, y):
	# If escape is pressed, kill everything.
	# ord() is needed to get the keycode
	if ord(key) == 27:
		# Escape key = 27
		glutLeaveMainLoop()
		return


def start():
	global window
	glutInit(sys.argv)

	# Select type of Display mode:
	#  Double buffer
	#  RGBA color
	#  Alpha components supported
	#  Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

	# get a 640 x 480 window
	glutInitWindowSize(640, 480)

	# the window starts at the upper left corner of the screen
	glutInitWindowPosition(0, 0)

	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
	window = glutCreateWindow("CENG487 Development Env Test")

	# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
	# set the function pointer and invoke a function to actually register the callback, otherwise it
	# would be very much like the C version of the code.
	glutDisplayFunc(DrawGLScene)

	# Uncomment this line to get full screen.
	# glutFullScreen()

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
