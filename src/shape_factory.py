import numpy
from vector import ColorRGBA, Point3f
from shapes import _Shape

class ShapeFactory:

    def __init__(self, objsData) -> None:
        self.objsData = objsData

    def createAll(self):
        shapes = []
        for objData in self.objsData:
            vertices = []
            colors = []
            UVs = []
            normals = []
            for face in objData['faces']:
                for vertexIndices in face:
                    v = vertexIndices[0]
                    vt = vertexIndices[1]
                    vn = vertexIndices[2]
                    x = (objData['vertices'][v])[0]
                    y = (objData['vertices'][v])[1]
                    z = (objData['vertices'][v])[2]
                    vertices.append(Point3f(x, y, z))
                    r = (objData['vertices'][v])[0]
                    g = (objData['vertices'][v])[1]
                    b = (objData['vertices'][v])[2]
                    colors.append(ColorRGBA(r, g, b, 1.0))
                    u = (objData['UVs'][vt])[0]
                    v = (objData['UVs'][vt])[1]
                    UVs.append([u, v])
                    x = (objData['normals'][vn])[0]
                    y = (objData['normals'][vn])[1]
                    z = (objData['normals'][vn])[2]
                    normals.append([x, y, z])            
            shapes.append(_Shape('Shape', vertices, colors, UVs, normals))
        return shapes
