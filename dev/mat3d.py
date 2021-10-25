# CENG 487 Assignment1 by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

class Mat3d:
  def __init__(self, m, n) -> None:
      self.matrix = []
      for i in range(0, m):
        row = []
        for j in range(0, n):
          row.append(0)
        self.matrix.append(row)
  
  def __str__(self) -> str:
      s = ""
      for row in self.matrix:
        s += "\n|"
        for number in row:
          s += " " + str(number)
        s += " |"
      return s
      

def main():
  
  pass

main()