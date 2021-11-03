# CENG 487 Assignment3 by
# Oğuzhan Özer
# StudentId: 260201039
# November 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math
from obj3d import Obj3d

from vec3d import Vec3d

# Number of the glut window.
window = 0

# Rotation angle for the triangle.
r_angle = 0.0

# Subdivision number
sd = 10

object_to_draw = "NONE"

def generate_sphere_vertices(radius, sector_count, stack_count):
	ver_arr2d = []
	for stack_step in range(stack_count + 1):
		tmp_arr = []
		for sector_step in range(sector_count + 1):
			theta = (2 * math.pi) * (sector_step / sector_count)
			phi = (math.pi / 2) - (math.pi * stack_step / stack_count)

			x = radius * math.cos(phi) * math.cos(theta)
			y = radius * math.cos(phi) * math.sin(theta)
			z = radius * math.sin(phi)

			tmp_vec = Vec3d(x, y, z)
			tmp_arr.append(tmp_vec)
		ver_arr2d.append(tmp_arr)
	return ver_arr2d





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
	global r_angle

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	# Clear The Screen And The Depth Buffer
	glLoadIdentity();				# Reset The View
	
	glTranslatef(0.0,0.0,-6.0);	# Move Left And Into The Screen

	glRotatef(r_angle,1.0,1.0,0.0);	# Rotate The Pyramid On It's Y Axis

	if object_to_draw == "SPHERE":
		sp_ver_arr = generate_sphere_vertices(1, sd, sd)
		for i in range(sd):
			for j in range(sd):
				
				glBegin(GL_QUADS);			# Start Drawing The Pyramid

				glColor3f(1, 0, 0);		# Red
				glVertex3f(sp_ver_arr[i][j].x,sp_ver_arr[i][j].y,sp_ver_arr[i][j].z);		# stack_step = i, sector_step=j

				glColor3f(0, 1, 0);		# Green
				glVertex3f(sp_ver_arr[i+1][j].x,sp_ver_arr[i+1][j].y,sp_ver_arr[i+1][j].z);		# stack_step = i+1, sector_step=j

				glColor3f(0, 0, 1)		# Blue
				glVertex3f(sp_ver_arr[i+1][j+1].x,sp_ver_arr[i+1][j+1].y,sp_ver_arr[i+1][j+1].z);		# stack_step = i+1, sector_step=j+1

				glColor3f(1, 1, 0)		# Yellow
				glVertex3f(sp_ver_arr[i][j+1].x,sp_ver_arr[i][j+1].y,sp_ver_arr[i][j+1].z);		# stack_step = i+1, sector_step=j+1

				glEnd();

		sphere_new = Obj3d.sphere(1, sd, sd)
		glBegin(GL_QUADS)

		for poly in sphere_new.poly_arr:
			glColor3f(1, 0, 0)
			glVertex3f(poly[0].x,poly[0].y,poly[0].z)
		
			glColor3f(0, 1, 0)
			glVertex3f(poly[1].x,poly[1].y,poly[1].z)

			glColor3f(0, 0, 1)
			glVertex3f(poly[2].x,poly[2].y,poly[2].z)

			glColor3f(0, 1, 1)
			glVertex3f(poly[3].x,poly[3].y,poly[3].z)

		glEnd()

	elif object_to_draw == "CYLINDER":
		cylinder = Obj3d.cylinder(1, 3, sd)
		colors = ((1,0,0),(0,1,0),(0,0,1))
		for poly in cylinder.poly_arr:
			glBegin(GL_POLYGON)
			for i in range(len(poly)):
				glColor3f(colors[i%3][0], colors[i%3][1], colors[i%3][2])
				glVertex3f(poly[i].x,poly[i].y,poly[i].z)
			glEnd()

	elif object_to_draw == "CUBE":
		cube = []
		a = 2
		for i in range(6):
			cube.append(Obj3d.square(a, sd))
			
		cube[0].translate(0, 0, a/2)

		cube[1].rotate("y", Vec3d(0, 0, 0), 180)
		cube[1].translate(0, 0, a/2)

		cube[2].rotate("y", Vec3d(0, 0, 0), 90)
		cube[2].translate(0, 0, a/2)

		cube[3].rotate("y", Vec3d(0, 0, 0), -90)
		cube[3].translate(0, 0, a/2)

		cube[4].rotate("x", Vec3d(0, 0, 0), 90)
		cube[4].translate(0, 0, a/2)

		cube[5].rotate("x", Vec3d(0, 0, 0), -90)
		cube[5].translate(0, 0, a/2)
			
		for square in cube:
			vertice_arr = square.transform()
			for i in range(len(vertice_arr) // 4):
				glBegin(GL_POLYGON)
				glColor3f(1,0,0)
				glVertex3f(vertice_arr[i*4].x,vertice_arr[i*4].y,vertice_arr[i*4].z)
				
				glColor3f(0,1,0)
				glVertex3f(vertice_arr[i*4+1].x,vertice_arr[i*4+1].y,vertice_arr[i*4+1].z)
				
				glColor3f(0,0,1)
				glVertex3f(vertice_arr[i*4+2].x,vertice_arr[i*4+2].y,vertice_arr[i*4+2].z)
				
				glColor3f(0.5,0.5,0.5)
				glVertex3f(vertice_arr[i*4+3].x,vertice_arr[i*4+3].y,vertice_arr[i*4+3].z)
				glEnd()

	r_angle  = r_angle + 1				# Increase The Rotation Variable For The Triangle

	#  since this is double buffered, swap the buffers to display what just got drawn.
	glutSwapBuffers()


# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(key, x, y):
	global object_to_draw
	global sd
	# If escape is pressed, kill everything.
	# ord() is needed to get the keycode
	key_ascii = ord(key)
	if key_ascii == 27:
		# Escape key = 27
		glutLeaveMainLoop()
		return
	elif key_ascii == 49:
		object_to_draw = "CUBE"
		
	elif key_ascii == 50:
		object_to_draw = "SPHERE"

	elif key_ascii == 51:
		object_to_draw = "CYLINDER"

	elif key_ascii == 43:
		sd += 1

	elif key_ascii == 45:
		sd -= 1



def main():
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
print ("Hit ESC key to quit.")
main()

