import math
import unittest

from matrix import Matrix
from mat3d import Mat3d

class TestMatrix(unittest.TestCase):

    def test_init(self):
        l1 = [[1,2,3],[4,5,6],[7,8,9]]
        self.assertEqual(Matrix(l1).matrix_arr, l1)

        # check if unbalanced list raises error
        with self.assertRaises(IndexError):
            l2 = [[1,2],[4,5,6],[7,8,9]]
            Matrix(l2)

    def test_fill(self):
        m1 = Matrix([[0,0,0],[0,0,0],[0,0,0]])
        l2 = [[-1,2,3],[4,15,6],[7,8,-9]]
        m1.fill(l2)
        self.assertEqual(m1.matrix_arr, l2)

    def test_set_num(self):
        m1 = Matrix([[0,0,0],[0,0,0],[0,0,0]])
        m1.set_num(3, 1, 2)
        self.assertEqual(m1.matrix_arr[1][2], 3)

        with self.assertRaises(IndexError):
            m1.set_num(3, 5, 6)

    def test_multiply(self):
        m1 = Matrix([[1,2,3],[4,5,6]])
        m2 = Matrix([[7,8],[9,10],[11,12]])
        m3 = m1.multiply(m2)
        self.assertEqual(m3.matrix_arr, [[58,64],[139,154]])

    def test_transpose(self):
        m1 = Matrix([[1,2,3],[4,5,6],[7,8,9]])
        m2 = m1.transpose()
        self.assertEqual(m2.matrix_arr, [[1,4,7],[2,5,8],[3,6,9]])

class TestMat3d(unittest.TestCase):

    def test_translation(self):
        test_arr = [[1, 0, 0, 2],
                    [0, 1, 0, 3],
                    [0, 0, 1, 4],
                    [0, 0, 0, 1]]
        tr_mat = Mat3d.translation(2, 3, 4)
        self.assertEqual(tr_mat.matrix.matrix_arr, test_arr)
    
    def test_inverse_translation(self):
        test_arr = [[1, 0, 0, -2],
                    [0, 1, 0, -3],
                    [0, 0, 1, -4],
                    [0, 0, 0, 1]]
        tr_mat = Mat3d.inverse_translation(2, 3, 4)
        self.assertEqual(tr_mat.matrix.matrix_arr, test_arr)
    
    def test_scale(self):
        test_arr = [[2, 0, 0, 0],
                    [0, 3, 0, 0],
                    [0, 0, 4, 0],
                    [0, 0, 0, 1]]
        tr_mat = Mat3d.scale(2, 3, 4)
        self.assertEqual(tr_mat.matrix.matrix_arr, test_arr)

    def test_inverse_scale(self):
        test_arr = [[1/2, 0, 0, 0],
                    [0, 1/3, 0, 0],
                    [0, 0, 1/4, 0],
                    [0, 0, 0, 1]]
        tr_mat = Mat3d.inverse_scale(2, 3, 4)
        self.assertEqual(tr_mat.matrix.matrix_arr, test_arr)
    
    def test_rotation(self):
        test_arr = [[1, 0, 0, 0],
                    [0, 6.123233995736766e-17, -1, 0],
                    [0, 1, 6.123233995736766e-17, 0],
                    [0, 0, 0, 1]]
        tr_mat = Mat3d.rotation("x", 90)
        self.assertEqual(tr_mat.matrix.matrix_arr, test_arr)

        with self.assertRaises(ValueError):
            Mat3d.rotation("w", 90)
    
    def test_inverse_rotation(self):
        test_arr = [[1, 0, 0, 0],
                    [0, 6.123233995736766e-17, 1, 0],
                    [0, -1, 6.123233995736766e-17, 0],
                    [0, 0, 0, 1]]
        tr_mat = Mat3d.inverse_rotation("x", 90)
        self.assertEqual(tr_mat.matrix.matrix_arr, test_arr)

        with self.assertRaises(ValueError):
            Mat3d.rotation("w", 90)

if __name__ == '__main__':
    unittest.main()