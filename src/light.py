from OpenGL.GL import *
import numpy

class DirectionalLight():
    
    def __init__(self, dir, color, intensity) -> None:
        self.dir = numpy.array(dir, dtype='float32')
        self.color = numpy.array(color, dtype='float32')
        self.intensity = float(intensity)
        self.isOn = 1.0

    def bindToProgram(self, programID):
        # we need to bind to the program to set lighting related params
        glUseProgram(programID)

        lightDirLocation = glGetUniformLocation(programID, "dLightDir")
        glUniform3f(lightDirLocation, self.dir[0], self.dir[1], self.dir[2])
        lightColorLocation = glGetUniformLocation(programID, "dLightColor")
        glUniform4f(lightColorLocation, self.color[0], self.color[1], self.color[2], self.color[3])
        lightIntensityLocation = glGetUniformLocation(programID, "dLightIntensity")
        glUniform1f(lightIntensityLocation, self.intensity)
        lightIsOnLocation = glGetUniformLocation(programID, "dLightIsOn")
        glUniform1f(lightIsOnLocation, self.isOn)

        glUseProgram(0)
        

class PointLight():

    def __init__(self, pos, color, intensity) -> None:
        self.pos = numpy.array(pos, dtype='float32')
        self.color = numpy.array(color, dtype='float32')
        self.intensity = float(intensity)
        self.isOn = 1.0

    def bindToProgram(self, programID):
        # we need to bind to the program to set lighting related params
        glUseProgram(programID)

        lightDirLocation = glGetUniformLocation(programID, "pLightPos")
        glUniform3f(lightDirLocation, self.pos[0], self.pos[1], self.pos[2])
        lightColorLocation = glGetUniformLocation(programID, "pLightColor")
        glUniform4f(lightColorLocation, self.color[0], self.color[1], self.color[2], self.color[3])
        lightIntensityLocation = glGetUniformLocation(programID, "pLightIntensity")
        glUniform1f(lightIntensityLocation, self.intensity)
        lightIsOnLocation = glGetUniformLocation(programID, "pLightIsOn")
        glUniform1f(lightIsOnLocation, self.isOn)

        glUseProgram(0)


class Spotlight():

    def __init__(self, pos, cutoff, color, intensity, dir) -> None:
        self.pos = pos
        self.cutoff = cutoff
        self.color = color
        self.intensity = intensity
        self.dir = dir
        self.isOn = 1.0

    def bindToProgram(self, programID):
        # we need to bind to the program to set lighting related params
        glUseProgram(programID)

        lightDirLocation = glGetUniformLocation(programID, "sLightPos")
        glUniform3f(lightDirLocation, self.pos[0], self.pos[1], self.pos[2])
        lightColorLocation = glGetUniformLocation(programID, "sLightColor")
        glUniform4f(lightColorLocation, self.color[0], self.color[1], self.color[2], self.color[3])
        lightCutoffLocation = glGetUniformLocation(programID, "sLightCutoff")
        glUniform1f(lightCutoffLocation, self.cutoff)
        lightIntensityLocation = glGetUniformLocation(programID, "sLightIntensity")
        glUniform1f(lightIntensityLocation, self.intensity)
        lightDirLocation = glGetUniformLocation(programID, "sDir")
        glUniform3f(lightDirLocation, self.dir[0], self.dir[1], self.dir[2])
        lightIsOnLocation = glGetUniformLocation(programID, "sLightIsOn")
        glUniform1f(lightIsOnLocation, self.isOn)

        glUseProgram(0)
    