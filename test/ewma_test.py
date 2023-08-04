import numpy as np
from numba import jit
from numba import float64
from numba import int64
from utils.fast_ewma import _ewma
import unittest

class TestFloatEquality(unittest.TestCase):
    a = np.array([1,2,3,4,5], dtype=np.float64)
    def test_almost_equal(self):
        self.assertAlmostEqual(_ewma(self.a,4,4), 3.095588, places=5)
    def test_almost_equal2(self):
        self.assertAlmostEqual(_ewma(self.a,4,3), 2.42857, places=5)
    def test_almost_equal3(self):
        self.assertAlmostEqual(_ewma(self.a,2,5), 4.75, places=5)
    def test_almost_equal4(self):
        self.assertAlmostEqual(_ewma(np.array([],dtype=np.float64),2,0), 0, places=5)

if __name__ == '__main__':
    unittest.main()