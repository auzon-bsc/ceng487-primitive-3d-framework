from OpenGL.GL import *
import numpy

class DirectionalLight():
    
    def __init__(self, dir, color, intensity) -> None:
        self.dir = numpy.array(dir, dtype='float32')
        self.color = numpy.array(color, dtype='float32')
        self.intensity = float(intensity)

    def bindToProgram(self, programID):
        # we need to bind to the program to set lighting related params
        glUseProgram(programID)

        lightDirLocation = glGetUniformLocation(programID, "lightDir")
        glUniform3f(lightDirLocation, self.dir[0], self.dir[1], self.dir[2])
        lightColorLocation = glGetUniformLocation(programID, "lightColor")
        glUniform4f(lightColorLocation, self.color[0], self.color[1], self.color[2], self.color[3])
        lightIntensityLocation = glGetUniformLocation(programID, "lightIntensity")
        glUniform1f(lightIntensityLocation, self.intensity)

        glUseProgram(0)


class PointLight():

    def __init__(self, pos, color, intensity) -> None:
        self.pos = numpy.array(pos, dtype='float32')
        self.color = numpy.array(color, dtype='float32')
        self.intensity = float(intensity)

class Spotlight():

    pass