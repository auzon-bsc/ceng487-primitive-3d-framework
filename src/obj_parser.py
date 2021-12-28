# CENG 487 Assignment4 by
# Oğuzhan Özer
# StudentId: 260201039
# November 2021
# Runs in Python 3.8.6

import sys

class ObjParser():
    
    def __init__(self):
        self.fileNames = []
        self.filesLines = []

    def parseCL(self):
        for arg in sys.argv[1:]:
            self.fileNames.append(arg)

    def parseFilesLines(self):
        for fileName in self.fileNames:
            fileStream = open(fileName, 'r')
            lines = fileStream.readlines()
            fileStream.close()
            self.filesLines.append(lines)
    
    def parseWavefrontObjFiles(self):
        objsData = []
        for fileLines in self.filesLines:
            objData = {
                'vertices': [],
                'UVs': [],
                'normals': [],
                'faces': []
            }            
            for fileLine in fileLines:
                tokens = fileLine.split()
                if len(tokens) == 0:
                    continue
                if tokens[0] == "v":
                    x = float(tokens[1])
                    y = float(tokens[2])
                    z = float(tokens[3])
                    vertex = [x, y, z]
                    objData['vertices'].append(vertex)
                if tokens[0] == "vt":
                    u = float(tokens[1])
                    v = float(tokens[2])
                    UV = [u, v]
                    objData['UVs'].append(UV)
                if tokens[0] == "vn":
                    x = float(tokens[1])
                    y = float(tokens[2])
                    z = float(tokens[3])
                    normal = [x, y, z]
                    objData['normals'].append(normal)
                if tokens[0] == "f":
                    face = []
                    for token in tokens[1:]:
                        indicesString = token.split("/")
                        indices = []
                        for indexString in indicesString:
                            indices.append(int(indexString) - 1)
                        face.append(indices)
                    objData['faces'].append(face)
            objsData.append(objData)
        return objsData

