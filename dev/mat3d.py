# CENG 487 Assignment1 by
# Oğuzhan Özer
# StudentId: 260201039
# October 2021

class Mat3d:
  def __init__(self, m = 1, n = 1) -> None:
      self.m = m
      self.n = n
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
        for num in row:
          s += " " + str(num)
        s += " |"
      return s
  
  def set_num(self, num, row, col):
    if (row - 1) > self.m or (col - 1) > self.n:
      print("Error: Invalid row and column locations")
    else:
      self.matrix[row - 1][col - 1] = num

  def multipy(self, other):
    if(self.n != other.m):
      print("Error: You cannot multiply %d column matrix with %d row matrix" % (self.n, other.m))
    else:
      tmp_m = self.m
      tmp_n = other.n
      tmp_mat = Mat3d(tmp_m, tmp_n)
      for i in range(0, tmp_m):
        for j in range(0, tmp_n):
          for k in range(0, self.n):
            tmp_mat.matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
      return tmp_mat

def main():
  pass

main()