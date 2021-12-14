from OpenGL.GL import *

programID = None

class Shader:

    def __init__(self):
        self.vertName = "default.vert"
        self.fragName = "default.frag"
        self.programID = None

    def __repr__(self):
        return f"Shader(vert={self.vert}, frag={self.frag})"

    def _read(self, filename):
        with open(filename, 'r') as file:
            content = file.read()
        return content

    # Set up the list of shaders, and call functions to compile them
    def initProgram(self):

        # if it's initialized before delete to reinitialize
        if self.programID is not None:
            glDeleteProgram(self.programID)
        
        # create shaders
        shaderList = []

        vertStr = self._read(self.vertName)
        fragStr = self._read(self.fragName)

        shaderList.append(self._createShader(GL_VERTEX_SHADER, vertStr))
        shaderList.append(self._createShader(GL_FRAGMENT_SHADER, fragStr))

        # create the program and set the programID
        self.programID = self._createProgram(shaderList)

        # delete shaders after creation
        for shaderID in shaderList:
            glDeleteShader(shaderID)


    def _createProgram(self, shaderList):
        
        # create an empty program and get its ID
        programID = glCreateProgram()

        # attach our shaders to our ID
        for shaderID in shaderList:
            glAttachShader(programID, shaderID)

        # link our program to the gl
        glLinkProgram(programID)

        # check linking status
        status = glGetProgramiv(programID, GL_LINK_STATUS)
        if status == GL_FALSE:
            strInfoLog = glGetProgramInfoLog(programID)
            print(b"Linker failure: \n" + strInfoLog)

        # to delete shader we must detach them first
        for shaderID in shaderList:
            glDetachShader(programID, shaderID)

        return programID


    def _createShader(self, shaderType, shaderCode):
        # create and compile the shader from source code as string
        shaderID = glCreateShader(shaderType)
        glShaderSource(shaderID, shaderCode)
        glCompileShader(shaderID)

        # check compilation status
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