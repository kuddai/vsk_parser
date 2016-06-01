import sys
sys.path.insert(0, '../src')
import unittest
import numpy as np

from vsk_parser.src.character import Transform

class TestTransform(unittest.TestCase):

    def arrayCheck(self, expected, answer):
        return self.assertTrue(np.allclose(expected, answer))

    def test_translation(self):
        transform = Transform(np.eye(4))
        self.arrayCheck(transform.translation, np.array([0, 0, 0]))

        transform.translation = np.array([1, 2, 3])
        self.arrayCheck(transform.translation, np.array([1, 2, 3]))
        self.arrayCheck(transform.m4x4,
                        np.array([[1, 0, 0, 1],
                                  [0, 1, 0, 2],
                                  [0, 0, 1, 3],
                                  [0, 0, 0, 1]]))

        transform.m4x4[1, 3] = 7
        self.arrayCheck(transform.translation, np.array([1, 7, 3]))

    def test_rotation(self):
        transform = Transform(np.eye(4))
        self.arrayCheck(transform)

    def test_from_euler(self):
        expected = Transform.from_euler( 90, 0, 0)
        answer = np.array([[ 1.,  0.,  0.],
                           [ 0.,  0., -1.],
                           [ 0.,  1.,  0.]])
        self.arrayCheck(expected, answer)

        expected = Transform.from_euler(180, 0, 0)
        answer = np.array([[ 1.,  0.,  0.],
                           [ 0., -1., -0.],
                           [ 0.,  0., -1.]])
        self.arrayCheck(expected, answer)

        expected = Transform.from_euler(0, 90, 0)
        answer = np.array([[ 0.,  0.,  1.],
                           [ 0.,  1.,  0.],
                           [-1.,  0.,  0.]])
        self.arrayCheck(expected, answer)

        expected = Transform.from_euler(0, 0, 90)
        answer = np.array([[ 0., -1.,  0.],
                           [ 1.,  0.,  0.],
                           [ 0.,  0.,  1.]])
        self.arrayCheck(expected, answer)

if __name__ == "__main__":
    unittest.main()