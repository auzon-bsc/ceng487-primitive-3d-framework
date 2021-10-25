# CENG 487 Assignment1 by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

class Mat3d:
  def __init__(self) -> None:
      self.matrix = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
  
  def __str__(self) -> str:
      s = ""
      for row in self.matrix:
        s += "\n| %d %d %d %d |" % (row[0], row[1], row[2], row[3])
      return s
      

def main():
  
  pass

main()