from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class Window:
    _title: str
    _width: float
    _height: float

    def __init__(self) -> None:
        self._title = ""
        self._width = 800
        self._height = 600

        glutInitWindowSize(self._width, self._height)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowPosition(0, 0)

    def setTitle(self, string):
        self._title = string
        glutSetWindowTitle(string)

    def setWidth(self, width):
        self._width = width

    def setHeight(self, height):
        self._height = height

    def setResolution(self, width, height):
        self.setWidth(width)
        self.setHeight(height)
        glutReshapeWindow(self._width, self._height)

    def fullscreen(self):
        glutFullScreen()

    def createWindow(self):
        title = self._title
        glutReshapeFunc(self.resizeGLScene)
        return glutCreateWindow(title)

    # The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
    def resizeGLScene(self, width, height):
        if width == 0:  # Prevent A Divide By Zero If The Window Is Too Small
            height = 1

        # Reset The Current Viewport And Perspective Transformation
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        fovY = 45.0
        aspectRatio = float(width) / float(height)
        zNear = 0.1
        zFar = 100.0
        gluPerspective(fovY, aspectRatio, zNear, zFar)
        glMatrixMode(GL_MODELVIEW)

    def initGL(self):
        """A general OpenGL initialization function.  Sets all of the initial parameters.
        We call this right after our OpenGL window is created.

        Args:
            Width ([type]): [description]
            Height ([type]): [description]
        """
        # This Will Clear The Background Color To Black
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)  # Enables Clearing Of The Depth Buffer
        glDepthFunc(GL_LESS)  # The Type Of Depth Test To Do
        glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
        glShadeModel(GL_SMOOTH)  # Enables Smooth Color Shading

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()  # Reset The Projection Matrix
        fovY = 45.0
        aspectRatio = float(self._width) / float(self._height)
        zNear = 0.1
        zFar = 100.0
        gluPerspective(fovY, aspectRatio, zNear, zFar)

        glMatrixMode(GL_MODELVIEW)