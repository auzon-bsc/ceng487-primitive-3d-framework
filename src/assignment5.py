# CENG 487 Assignment5 by
# Oğuzhan Özer
# StudentId: 260201039
# November 2021
# Runs in Python 3.8.6
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

from obj3d import Obj3d
from vec3d import Vec3d
from window.window import Window
from scene.scene import Scene
from input_handler.input_handler import InputHandler
from obj_parser.obj_parser import *

def main():
    # parse object from the file
    parser = ObjParser()
    parser.parse_command_line()
    parser.parse_lines()
    vertices, faces = parser.parse_obj3d()

    # create object from vertices and faces lists
    obj3D = Obj3d(vertices, faces)

    # Scene
    scene = Scene()
    scene.addObj3D(obj3D)
    scene.addText("Press 'ESC' to quit.")
    scene.addText("Press '+' to increase subdivisions.")
    scene.addText("Press '-' to decrease subdivisions.")
    scene.addText("Press 'Arrow Keys' to rotate the objects.")

    # Initialize glut
    glutInit(sys.argv)

    # Initialize 800x600 window
    windowObject = Window()
    windowObject.createWindow()
    windowObject.initGL()
    
    # Registering draw function
    glutDisplayFunc(scene.drawScene)
    glutIdleFunc(scene.drawScene)
    
    # Input operations
    inputHandler = InputHandler()
    inputHandler.linkScene(scene)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(inputHandler.asciiKey)
    glutSpecialFunc(inputHandler.nonAsciiKey)

    # Start Event Processing Engine
    glutMainLoop()

if __name__ == '__main__':
    main()
