# CENG 487 Assignment4 by
# Oğuzhan Özer
# StudentId: 260201039
# November 2021
# Runs in Python 3.10.0

import glhelper
import objparser as op
from obj3d import Obj3d


def main():
    # get filename
    filename = op.parse_cl()

    # parse file to lines
    lines = op.parse_lines(filename)

    # parse object from the lines
    vertices, faces = op.parse_obj(lines)

    # create object from vertices and faces lists
    obj3d = Obj3d(vertices, faces)

    # add object to glhelper class and start drawing
    glhelper.addobj(obj3d)
    glhelper.start()

    print("Hit ESC key to quit.")


main()
