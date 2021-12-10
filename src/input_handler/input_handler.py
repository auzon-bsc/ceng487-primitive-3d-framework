from OpenGL.GLUT import *

class InputHandler:

    def __init__(self) -> None:
        self._linkedScene = None

    def linkScene(self, scene):
        self._linkedScene = scene

    def asciiKey(self, key, x, y):
        """The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
        Args:
            key (byte): byte value of the pressed key
            x (?): ?
            y (?): ?
        """   
        asciiValue = ord(key)
        # ESC
        if asciiValue == 27:
            # leave opengl
            glutLeaveMainLoop()

        elif 48 <= asciiValue <= 57:
            topRowNumber = asciiValue - 48
            linkedScene = self._linkedScene
            linkedScene.selectObject(topRowNumber)
    
        # Minus
        elif asciiValue == 45:
            linkedScene = self._linkedScene
            linkedScene.decrementSubdivision()
        
        # Plus
        elif asciiValue == 43:
            linkedScene = self._linkedScene
            linkedScene.incrementSubdivision()

        else:
            print(f"Pressed key doesn't do anything!(value is: {key})")
    
    def nonAsciiKey(self, key, x, y):

        # Left and right arrow keys
        if key == 100 or key == 102:
            arrowKeyFactor = 101 - key
            linkedScene = self._linkedScene
            firstObject = linkedScene.getObj3D(0)
            # Rotate counter clockwise
            rotationSpeed = 5
            rotationAxis = "y"
            rotatonDegree = rotationSpeed * arrowKeyFactor
            firstObject.rotate(rotationAxis, rotatonDegree)

        # Up and down arrow keys
        elif key == 101 or key == 103:
            arrowKeyFactor = 102 - key
            linkedScene = self._linkedScene
            firstObject = linkedScene.getObj3D(0)
            rotationSpeed = -5
            rotationAxis = "x"
            rotatonDegree = rotationSpeed * arrowKeyFactor
            firstObject.rotate(rotationAxis, rotatonDegree)

        else:
            print(f"Pressed key doesn't do anything!(value is: {key})")