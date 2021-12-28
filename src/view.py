from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from vector import *
from matrix import *
from shapes import *
from scene import *
from defs import *

class Event:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.button = -1
        self.state = -1
        self.altPressed = False


class View:
    def __init__(self, camera, grid, scene = None):
        self.camera = camera
        self.grid = grid
        self.scene = scene
        self.bgColor = ColorRGBA(0.15, 0.15, 0.15, 1.0)
        self.cameraIsMoving = False
        self.objectAnimOn = False
        self.event = Event()
        self.mouseX = -1
        self.mouseY = -1

    def draw(self):
        # set color to scene background color
        glClearColor(self.bgColor.r, self.bgColor.g, self.bgColor.b, self.bgColor.a)
        
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw grid
        glUseProgram(self.grid.programID)
        # set uniform view matrix of the shader
        viewLocation = glGetUniformLocation( self.grid.programID, "view")
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE, self.camera.getViewMatrix())

        # set uniform projection matrix of the shader
        projLocation = glGetUniformLocation( self.grid.programID, "proj")
        glUniformMatrix4fv(projLocation, 1, GL_FALSE, self.camera.getProjMatrix())
        # self.grid.draw()

        # draw nodes
        for node in self.scene.nodes:
            # use the shader linked to the object
            glUseProgram(node.programID)
            
            # set uniform view matrix of the shader
            viewLocation = glGetUniformLocation( node.programID, "view")
            glUniformMatrix4fv(viewLocation, 1, GL_FALSE, self.camera.getViewMatrix())

            # set uniform projection matrix of the shader
            projLocation = glGetUniformLocation( node.programID, "proj")
            glUniformMatrix4fv(projLocation, 1, GL_FALSE, self.camera.getProjMatrix())
            
            # draw the object
            node.draw()
            
            # reset the shader
            glUseProgram(0)

        # swap the buffers to show it to screen
        glutSwapBuffers()


    def setScene(self, scene):
        self.scene = scene


    def setObjectAnim(self, onOff):
        self.objectAnimOn = onOff


    def isObjectAnim(self):
        return self.objectAnimOn


    def setCameraIsMoving(self, onOff):
        self.cameraIsMoving = onOff


    def isCameraMoving(self):
        return self.cameraIsMoving


    # The function called whenever a key is pressed.
    def keyPressed(self, key, x, y):
        # If escape is pressed, kill everything.
        # ord() is needed to get the keycode
        if ord(key) == 27:
            # Escape key = 27
            glutLeaveMainLoop()
            return

        if key == b'f':
            self.camera.reset()
            self.draw()

        if key == b'4':
            for node in self.scene.nodes:
                if not node.fixedDrawStyle:
                    node.drawStyle = DrawStyle.WIRE
                    node.wireOnShaded = False
                    self.draw()

        if key == b'5':
            for node in self.scene.nodes:
                if not node.fixedDrawStyle:
                    node.drawStyle = DrawStyle.SMOOTH
                    node.wireOnShaded = False
                    self.draw()

        if key == b'6':
            for node in self.scene.nodes:
                if not node.fixedDrawStyle and node.drawStyle != DrawStyle.WIRE:
                    node.wireOnShaded = True
                    self.draw()


    # The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
    def resizeView(self, width, height):
        if height == 0:						# Prevent A Divide By Zero If The Window Is Too Small
            height = 1

        glViewport(0, 0, width, height)		# Reset The Current Viewport And Perspective Transformation
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = float(width)/float(height)
        self.camera.aspect = aspect
        gluPerspective(self.camera.fov, aspect, self.camera.near, self.camera.far)
        glMatrixMode(GL_MODELVIEW)


    # The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
    def specialKeyPressed(self, *args):
        if args[0] == GLUT_KEY_LEFT:
            self.camera.eye.x -= .5
            self.camera.center.x -= .5
            self.camera.computeCamSpace()
            self.setCameraIsMoving( True )

        if args[0] == GLUT_KEY_RIGHT:
            self.camera.eye.x += .5
            self.camera.center.x += .5
            self.camera.computeCamSpace()
            self.setCameraIsMoving( True )

        


    def mousePressed(self, button, state, x, y):
        self.event.x = x
        self.event.y = y
        self.event.state = state
        self.event.button = button

        # get status of alt key
        m = glutGetModifiers()
        self.event.altPressed = m & GLUT_ACTIVE_ALT

        self.mouseX = x
        self.mouseY = y

        if state == 0:
            if self.event.altPressed > 0:
                self.setCameraIsMoving( True )
        else:
            self.setCameraIsMoving( False )


    def mouseMove(self, x, y):
        if self.event.altPressed == False:
            return

        xSpeed = 0.02
        ySpeed = 0.02
        xOffset = (x - self.mouseX) * xSpeed
        yOffset = (y -self.mouseY) * ySpeed

        if ( self.event.button == GLUT_RIGHT_BUTTON ):
            self.camera.zoom(xOffset)
            #self.camera.roll(yOffset)
        elif ( self.event.button == GLUT_MIDDLE_BUTTON ):
            self.camera.dolly(-xOffset, yOffset, 0)
        elif ( self.event.button == GLUT_LEFT_BUTTON ):
            self.camera.yaw(xOffset)
            self.camera.pitch(yOffset)
            #self.camera.dollyCamera(-xOffset, yOffset, 0)

        # store last positions
        self.mouseX = x
        self.mouseY = y

        # remember this point
        self.event.x = x
        self.event.y = y


    # The main drawing function
    def idleFunction(self):
        if self.isObjectAnim() or self.isCameraMoving():
            self.draw()


class Grid(_Shape):
    def __init__(self, name, xSize, zSize):
        vertices = []
        for x in range(-xSize, xSize + 1, 2):
            for z in range(-zSize, zSize + 1, 2):
                vertices.append( Point3f(x, 0, z) )

        faces = []
        for x in range(0, xSize * zSize):
            indexX = x % xSize
            indexZ = x // zSize
            id1 = indexZ * (xSize + 1) + indexX
            id2 = (indexZ + 1) * (xSize + 1) + indexX
            faces.append([id1, id1 + 1, id2 + 1, id2])

        colors = []
        for _ in range(len(vertices)):
            colors.append(ColorRGBA(0.3, 0.3, 0.3, 1.0))

        UVs = []

        _Shape.__init__(self, name, vertices, faces, colors, UVs)

        self.fixedDrawStyle = True

        self.setWireColor(0.3, 0.3, 0.3, 1.0)
        self.xAxisColor = ColorRGBA(0.4, 0.0, 0.0, 1.0)
        self.zAxisColor = ColorRGBA(0.0, 0.4, 0.0, 1.0)
        self.yAxisColor = ColorRGBA(0.0, 0.0, 0.4, 1.0)
        self.axisWidth = 2

        self.originColor = ColorRGBA(0.4, 0.4, 0.4, 1.0)
        self.originRadius = 4

        self.xSize = xSize
        self.zSize = zSize


    def setXAxisColor(self, r, g, b, a):
        self.xAxisColor = ColorRGBA(r, g, b, a)


    def setYAxisColor(self, r, g, b, a):
        self.yAxisColor = ColorRGBA(r, g, b, a)


    def setZAxisColor(self, r, g, b, a):
        self.zAxisColor = ColorRGBA(r, g, b, a)


    def setMainAxisWidth(self, width):
        self.mainAxisWidth = width


    def draw(self):
        _Shape.draw(self)
