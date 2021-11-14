# CENG 487 Assignment4 by
# Oğuzhan Özer
# StudentId: 260201039
# November 2021
# Runs in Python 3.10.0

# default libraries
import sys

# opengl
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# my files
from obj3d import Obj3d
from vec3d import Vec3d

# Number of the glut window.
window = 0

# rotation angle and rotation speed
# rotation speed determines the rotation angle
rangle = 5

# objects list to store Obj3d instances
objects: list[Obj3d] = []
# object index determines which object to be drawn
oindex = 0
# subdivision number determines subdivision amount for the objects
sdnum = 0

# vertices and faces to be drawn
# initially nothing will be drawn
vertices = []
faces = []


def addobj(obj3d: Obj3d):
    """Add the object to the end of the objects list

    Args:
        obj3d (Obj3d): 3D object to be added
    """
    objects.append(obj3d)


def InitGL(Width, Height):
    """A general OpenGL initialization function.  Sets all of the initial parameters.
    We call this right after our OpenGL window is created.

    Args:
        Width ([type]): [description]
        Height ([type]): [description]
    """
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


def ReSizeGLScene(Width, Height):
    """The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)

    Args:
        Width ([type]): [description]
        Height ([type]): [description]
    """
    if Height == 0:  # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    # Reset The Current Viewport And Perspective Transformation
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def DrawGLScene():
    """The main drawing function
    """
    global objects

    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Reset The View
    glLoadIdentity()

    # Move Left And Into The Screen
    glTranslatef(0.0, 0.0, -10.0)

    # calculate vertices and faces of the object and draw it
    vertices, faces = recalculate()
    drawobj(vertices, faces)
    rendertext(f"Subdivision number: {sdnum}")

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()


def recalculate():
    """Recalculate vertices and faces when necessary instead of every time

    Returns:
        tuple[list[Vec3d], list[list[int]]]: vertices, faces
    """
    return subdivision(objects[oindex].transform(),
                       objects[oindex].getfaces(), sdnum)


def drawobj(vertices: list[Vec3d], faces: list[list[int]]):
    """Draw quads and lines for each face

    Args:
        vertices (list[Vec3d]): Vertices of the object
        faces (list[list[int]]): Faces of the object
    """
    for face in faces:
        drawquads(vertices, face)
        drawlines(vertices, face)


def drawquads(vertices: list[Vec3d], face: list[int]):
    """Draw quads for given vertices and face

    Args:
        vertices (list[Vec3d]): vertices of the object
        face (list[int]): a list contains index of vertices for a face
    """
    # begin drawing quads
    glBegin(GL_QUADS)
    # for every vertex index in list face
    for vi in face:
        # determine color with coordinates
        glColor3f(1, 1, 1)
        # send a vertex of the face to opengl
        glVertex3f(vertices[vi].x,
                   vertices[vi].y,
                   vertices[vi].z)
    # end drawing quads
    glEnd()


def drawlines(vertices: list[Vec3d], face: list[int]):
    """Draw lines for given vertices and face

    Args:
        vertices (list[Vec3d]): vertices of the object
        face (list[int]): a list contains index of vertices for a face
    """
    # begin drawing lines
    glBegin(GL_LINES)
    for i in range(len(face)):
        # set line color to black
        glColor3f(0, 0, 0)
        # starting point of the line
        glVertex3f(
            vertices[face[i-1]].x,
            vertices[face[i-1]].y,
            vertices[face[i-1]].z+0.01)    # +0.01 for better visibility for lines
        # ending point of the line
        glVertex3f(
            vertices[face[i]].x,
            vertices[face[i]].y,
            vertices[face[i]].z+0.01)    # +0.01 for better visibility for lines
    # end drawing lines
    glEnd()


def rendertext(text: str):
    glColor3f(1, 0, 0.3)
    glRasterPos3f(-2, -1.5, 6)
    for c in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))


def keyPressed(key, x, y):
    """The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)

    Args:
        key (byte): byte value of the pressed key
        x (?): ?
        y (?): ?
    """
    # this variables will change with user input
    global oindex
    global sdnum
    global rangle
    global vertices
    global faces

    match key:
        # ESC
        case b'\x1b':
            # leave opengl
            glutLeaveMainLoop()
            return
        case b'1':
            oindex = 0
            vertices, faces = recalculate()
        # +
        case b'+':
            # increase subdivision number
            sdnum += 1
            vertices, faces = recalculate()
        # -
        case b'-':
            # decrease subdivision number
            sdnum -= 1
            vertices, faces = recalculate()
        # Left arrow key
        case 100:
            objects[oindex].rotate("y", Vec3d([0, 0, 0, 1]), rangle)
            vertices, faces = recalculate()
        # Right arrow key
        case 102:
            objects[oindex].rotate("y", Vec3d([0, 0, 0, 1]), -rangle)
            vertices, faces = recalculate()
        case _:
            print(f"Pressed key doesn't do anything!(value is: {key})")


def subdivision(vertices: list[Vec3d], faces: list[list[int]], sdnum: int):
    """Calculate the subdivided vertices and faces with respect to subdivision number

    Args:
        vertices (list[Vec3d]): Vertices of the object
        faces (list[list[int]]): Faces of the object
        sdnum (int): Subdivision number

    Returns:
        tuple[list[Vec3d], list[list[int]]]: divided vertices and faces as a tuple
    """
    # copy faces and vertices so algorithm won't mess up originals
    sdfaces = copy_faces(faces)
    sdvertices = copy_vertices(vertices)

    # repeat the division algorithm sdnum times
    for sdstep in range(sdnum):    # subdivisionstep

        # loop all faces to calculate all subdivision vertices and faces
        for facestep in range(len(sdfaces)):

            # remove first face since it'll be divided and become invalid
            sdface = sdfaces.pop(0)

            # vertices size is required for indexing newly added vertices
            vs = len(sdvertices)      # size of the vertices list

            # initialize a vertex for midvertex of the face
            midvertex = Vec3d([0, 0, 0, 1])
            # loop all vertices in the face to find middle vertices
            for vi in range(len(sdface)):
                # add next vertex of the face to current sum
                midvertex += sdvertices[sdface[vi]]
                # calculate the point between two vertex
                # sum the vertices and divide the summation by 2
                edgevertex = sdvertices[sdface[vi-1]] + sdvertices[sdface[vi]]
                edgevertex.scale(0.5)
                # since this is a new vertex add it to the vertex list
                sdvertices.append(edgevertex)
            # to find middle vertex
            # divide the sum of the all vertexes in the face to number of face
            midvertex.scale(1/len(sdface))
            # add the vertex that will be in the middle of the face
            sdvertices.append(midvertex)

            # add the new faces to end of the faces list
            sdfaces += [[sdface[0], vs+1, vs+4, vs],
                        [vs+1, sdface[1], vs+2, vs+4],
                        [vs+4, vs+2, sdface[2], vs+3],
                        [vs, vs+4, vs+3, sdface[3]]
                        ]
    return sdvertices, sdfaces


def copy_faces(faces: list[list[int]]):
    """Deep copy faces of an object

    Args:
        faces (list[list[int]]): Faces of the object

    Returns:
        list[list[int]]: Newly created deepcopy of original faces
    """
    copy = []
    for face in faces:
        sdface = []
        for val in face:
            sdface.append(val)
        copy.append(sdface)
    return copy


def copy_vertices(vertices: list[Vec3d]):
    """Copy vertices of an object

    Args:
        vertices (list[Vec3d]): Vertices of the object

    Returns:
        list[Vec3d]: Deepcopy of vertices of the object
    """
    return [vertex.clone() for vertex in vertices]


def start():
    """Driver function for this module
    """
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

    # for special keys like arrow keys glutSpecialFunc can be used
    glutSpecialFunc(keyPressed)

    # Initialize our window.
    InitGL(640, 480)

    # Start Event Processing Engine
    glutMainLoop()


# Print message to console, and kick off the main to get it rolling.
print("Hit ESC key to quit.")
