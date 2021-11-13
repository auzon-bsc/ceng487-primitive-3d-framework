# CENG 487 Assignment4 by
# Oğuzhan Özer
# StudentId: 260201039
# November 2021
# Runs in Python 3.10.0

import sys
import logging

from OpenGL import error

from obj3d import Obj3d

def parse_cl():
    # total arguments
    n = len(sys.argv)
    print("Total arguments passed:", n)

    # if total number of arguments is wrong
    if n != 2:
        raise ValueError("This program only takes 1 additional argument, which is the object file")

    # assign filename
    filename = sys.argv[1]
    print(f"Filename: {filename}")

    # return filename
    return filename

def parse_lines(filename: str):
    # open file in read mode
    f = open(filename, "r")

    # read all the lines
    lines = f.readlines()
    
    # close the file
    f.close()

    # return all the lines
    return lines

def parse_obj(lines: list[str]):
    # vertex and face lists to be filled
    vertices = []
    faces = []

    # for each line in the file
    for line in lines:
        # split lines by whitespace
        splitted_line = line.split()
        
        # print(splitted_line)
        
        # pop first char from the line
        try:
            first_char = splitted_line.pop(0)
        # if line is empty pop raises error
        # continue loop if error raises
        except:
            continue
        # look the first char
        match first_char:
            # line represents name
            case "o":
                name = line[2:-1]

                # print(f"Name of the object: '{name}'")

            # line represents single vertex
            case "v":
                # convert each string in the line to float list and add that list to vertex list
                vertices.append([float(x) for x in splitted_line])
            # line represents single face
            case "f":
                # convert each string in the line to int list and add that list to face list
                faces.append([int(x) for x in splitted_line]) 
    
    # print(f"vertices: {vertices}")
    # print(f"faces: {faces}")

    return vertices, faces

def main():
    # get filename
    filename = parse_cl()

    # parse file to lines
    lines = parse_lines(filename)

    # parse object from the lines
    vertices, faces = parse_obj(lines)
    
    # create object from vertices and faces lists
    obj = Obj3d(vertices, faces)
    

main()