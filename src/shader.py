from OpenGL.GL import *

programID = None

class Shader:

    def __init__(self):
        self.vertName = "default.vert"
        self.fragName = "default.frag"
        self.programID = None
        # self.initProgram()

    def __repr__(self):
        return f"Shader(vert={self.vert}, frag={self.frag})"

    def _read(self, filename):
        with open(filename, 'r') as file:
            content = file.read()
        return content

    # Set up the list of shaders, and call functions to compile them
    def initProgram(self):
        
        if self.programID is not None:
            glDeleteProgram(self.programID)
        
        shaderList = []

        vertStr = self._read(self.vertName)
        fragStr = self._read(self.fragName)

        shaderList.append(self._createShader(GL_VERTEX_SHADER, vertStr))
        shaderList.append(self._createShader(GL_FRAGMENT_SHADER, fragStr))

        self.programID = self._createProgram(shaderList)

        for shaderID in shaderList:
            glDeleteShader(shaderID)

    # Function that accepts a list of shaders, compiles them, and returns a handle to the compiled program
    def _createProgram(self, shaderList):
        programID = glCreateProgram()

        for shaderID in shaderList:
            glAttachShader(programID, shaderID)

        glLinkProgram(programID)

        status = glGetProgramiv(programID, GL_LINK_STATUS)
        if status == GL_FALSE:
            strInfoLog = glGetProgramInfoLog(programID)
            print(b"Linker failure: \n" + strInfoLog)

        # important for cleanup
        for shaderID in shaderList:
            glDetachShader(programID, shaderID)

        return programID


    # Function that creates and compiles shaders according to the given type (a GL enum value) and
    # shader program (a string containing a GLSL program).
    def _createShader(self, shaderType, shaderCode):
        shaderID = glCreateShader(shaderType)
        glShaderSource(shaderID, shaderCode)
        glCompileShader(shaderID)

        status = None
        glGetShaderiv(shaderID, GL_COMPILE_STATUS, status)
        if status == GL_FALSE:
            # Note that getting the error log is much simpler in Python than in C/C++
            # and does not require explicit handling of the string buffer
            strInfoLog = glGetShaderInfoLog(shaderID)
            strShaderType = ""
            if shaderType is GL_VERTEX_SHADER:
                strShaderType = "vertex"
            elif shaderType is GL_GEOMETRY_SHADER:
                strShaderType = "geometry"
            elif shaderType is GL_FRAGMENT_SHADER:
                strShaderType = "fragment"

            print(b"Compilation failure for " + strShaderType + b" shader:\n" + strInfoLog)

        return shaderID