# CENG 487 Assignment3 by
# Oğuzhan Özer
# StudentId: 260201039
# November 2021
# Runs in Python 3.10.0

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import sys

from obj3d import Obj3d
from vec3d import Vec3d

# Number of the glut window.
window = 0

# Rotation angle for the objects.
r_angle = 0.0

# Subdivision number
sd = 10

# For determining which object to draw
object_to_draw = "SPHERE"

# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):  # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)  # This Will Clear The Background Color To Black
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
        0, 0, Width, Height
    )  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# The main drawing function.
def DrawGLScene():
    global r_angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Clear The Screen And The Depth Buffer
    glLoadIdentity()
    # Reset The View

    glTranslatef(0.0, 0.0, -6.0)
    # Move Into The Screen

    glRotatef(r_angle, 1.0, 1.0, 0.0)
    # Rotate The Object On It's X and Y Axis

    colors = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (0.3, 0.3, 0.3))

    if object_to_draw == "SPHERE":
        sphere = Obj3d.sphere(2, sd, sd)  # Create a new sphere
        glBegin(GL_QUADS)  # Begin to draw quads
        # Sphere object consists of polygons
        # We have to iterate them and draw them
        for poly in sphere.poly_arr:
            # Iterate vertices of the polygon
            for j in range(len(poly)):
                glColor3f(
                    colors[j][0], colors[j][1], colors[j][2]
                )  # Change color of each vertice of a polygon
                glVertex3f(poly[j].x, poly[j].y, poly[j].z)
        glEnd()

    elif object_to_draw == "CYLINDER":
        cylinder = Obj3d.cylinder(1, 2, sd)  # Create a cylinder object
        # Cylinder object consists of polygons (circles at the bottom and at the top are single polygons)
        # We have to iterate them and draw them
        for poly in cylinder.poly_arr:
            glBegin(GL_POLYGON)  # Begin to draw polygons
            # Iterate vertices of the polygon
            for i in range(len(poly)):
                glColor3f(
                    colors[i % 3][0], colors[i % 3][1], colors[i % 3][2]
                )  # Change color of each vertice of a polygon
                glVertex3f(poly[i].x, poly[i].y, poly[i].z)
            glEnd()

    elif object_to_draw == "CUBE":
        cube = []  # Cube array consists of 6 square object
        a = 2  # a is the edge length
        # Iterate for each surface
        for i in range(6):
            cube.append(Obj3d.square(a, sd))  # Add the surface to the cube array

        # Transformations for surface closest to screen
        cube[0].translate(0, 0, a / 2)

        # Transformations for surface farthest to screen
        cube[1].rotate("y", Vec3d(0, 0, 0), 180)
        cube[1].translate(0, 0, a / 2)

        # Transformations for the right surface
        cube[2].rotate("y", Vec3d(0, 0, 0), 90)
        cube[2].translate(0, 0, a / 2)

        # Transformations for the left surface
        cube[3].rotate("y", Vec3d(0, 0, 0), -90)
        cube[3].translate(0, 0, a / 2)

        # Transformations for the bottom surface
        cube[4].rotate("x", Vec3d(0, 0, 0), 90)
        cube[4].translate(0, 0, a / 2)

        # Transformations for the top surface
        cube[5].rotate("x", Vec3d(0, 0, 0), -90)
        cube[5].translate(0, 0, a / 2)

        # Iterate each square in the cube to draw them
        square: Obj3d
        for square in cube:
            vertice_arr = (
                square.transform()
            )  # Vertice array of all polygons of the square
            # For each 4 vertices of a polygon
            for i in range(len(vertice_arr) // 4):
                glBegin(GL_QUADS)

                glColor3f(1, 0, 0)
                glVertex3f(
                    vertice_arr[i * 4].x, vertice_arr[i * 4].y, vertice_arr[i * 4].z
                )  # Left top vertice

                glColor3f(0, 1, 0)
                glVertex3f(
                    vertice_arr[i * 4 + 1].x,
                    vertice_arr[i * 4 + 1].y,
                    vertice_arr[i * 4 + 1].z,
                )  # Right top vertice

                glColor3f(0, 0, 1)
                glVertex3f(
                    vertice_arr[i * 4 + 2].x,
                    vertice_arr[i * 4 + 2].y,
                    vertice_arr[i * 4 + 2].z,
                )  # Right bottom vertice

                glColor3f(0.5, 0.5, 0.5)
                glVertex3f(
                    vertice_arr[i * 4 + 3].x,
                    vertice_arr[i * 4 + 3].y,
                    vertice_arr[i * 4 + 3].z,
                )  # Left bottom vertice

                glEnd()

    r_angle = r_angle + 1  # Increase The Rotation Variable For The Object

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
        # Key : 1
        object_to_draw = "CUBE"

    elif key_ascii == 50:
        # Key : 2
        object_to_draw = "SPHERE"

    elif key_ascii == 51:
        # Key : 3
        object_to_draw = "CYLINDER"

    elif key_ascii == 43:
        # Key : +
        sd += 1

    elif key_ascii == 45:
        # Key : -
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
print("Press 1 for CUBE")
print("Press 2 for SPHERE")
print("Press 3 for CYLINDER")
print("Press ESC to quit")
main()
