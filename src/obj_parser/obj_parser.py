# CENG 487 Assignment4 by
# Oğuzhan Özer
# StudentId: 260201039
# November 2021
# Runs in Python 3.8.6

from abc import ABC, abstractmethod
import sys

from vec3d import Vec3d


class Parser(ABC):
    def __init__(self):
        filename = None
        lines = None

    def parse_command_line(self):
        # total arguments
        n = len(sys.argv)

        # if total number of arguments is wrong
        if n != 2:
            print("This program only takes 1 additional argument, which is the object file")
            exit()

        # assign filename
        filename = sys.argv[1]
        self.filename = filename

    def parse_lines(self):
        # open file in read mode
        f = open(self.filename, 'r')

        # read all the lines
        lines = f.readlines()

        # close the file
        f.close()

        # return all the lines
        self.lines = lines

class ObjParser(Parser):
    def __init__(self):
        super().__init__()
    
    def parse_obj3d(self):
        # vertex and face lists to be filled
        vertices = []
        faces = []

        # for each line in the file
        for line in self.lines:
            # split lines by whitespace
            splitted_line = line.split()
            # pop first char from the line
            try:
                first_char = splitted_line.pop(0)
            # if line is empty pop raises error
            # continue loop if error raises
            except Exception as exc:
                continue
            # look the first char
            # line represents name
            if first_char == "o":
                name = line[2:-1]
            # line represents single vertex
            elif first_char == "v":
                # convert each string in the line to float list and add that list to vertex list
                vertices.append([float(x) for x in splitted_line])
            # line represents single face
            elif first_char == "f":
                # convert each string in the line to int list and add that list to face list
                faces.append([int(x) - 1 for x in splitted_line])
        [vertex.append(1.0) for vertex in vertices]

        for vertexIndex in range(len(vertices)):
            vertices[vertexIndex] = Vec3d(vertices[vertexIndex])
            
        # find the edges of the object
        return vertices, faces

    