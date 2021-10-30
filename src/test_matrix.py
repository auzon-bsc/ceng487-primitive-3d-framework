import unittest
from matrix import Matrix

class TestMatrix(unittest.TestCase):

    def test_init(self):
        l1 = [[1,2,3],[4,5,6],[7,8,9]]
        self.assertEqual(Matrix(l1).matrix, l1)

        # check if unbalanced list raises error
        with self.assertRaises(IndexError):
            l2 = [[1,2],[4,5,6],[7,8,9]]
            Matrix(l2)

    def test_fill(self):
        m1 = Matrix([[0,0,0],[0,0,0],[0,0,0]])
        l2 = [[-1,2,3],[4,15,6],[7,8,-9]]
        m1.fill(l2)
        self.assertEqual(m1.matrix, l2)

    def test_set_num(self):
        m1 = Matrix([[0,0,0],[0,0,0],[0,0,0]])
        m1.set_num(3, 1, 2)
        self.assertEqual(m1.matrix[1][2], 3)

        with self.assertRaises(IndexError):
            m1.set_num(3, 5, 6)

    def test_multiply(self):
        m1 = Matrix([[1,2,3],[4,5,6]])
        m2 = Matrix([[7,8],[9,10],[11,12]])
        m3 = m1.multiply(m2)
        self.assertEqual(m3.matrix, [[58,64],[139,154]])

    def test_transpose(self):
        m1 = Matrix([[1,2,3],[4,5,6],[7,8,9]])
        m2 = m1.transpose()
        self.assertEqual(m2.matrix, [[1,4,7],[2,5,8],[3,6,9]])

if __name__ == '__main__':
    unittest.main()