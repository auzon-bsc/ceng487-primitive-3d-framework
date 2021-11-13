# CENG 487 Assignment4 by
# Oğuzhan Özer
# StudentId: 260201039
# November 2021
# Runs in Python 3.10.0

from matrix import Matrix
import parser
import glhelper

from obj3d import Obj3d

def main():
    # get filename
    filename = parser.parse_cl()

    # parse file to lines
    lines = parser.parse_lines(filename)

    # parse object from the lines
    vertices, faces = parser.parse_obj(lines)

    # create object from vertices and faces lists
    obj3d = Obj3d(vertices, faces)

    print(vertices, faces)

    glhelper.AddObject(obj3d)
    glhelper.start()



main()