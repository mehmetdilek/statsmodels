"""
Test functions for models.robust.scale
"""

import numpy as np
from numpy.random import standard_normal
from numpy.testing import *

# Example from Section 5.5, Venables & Ripley (2002)

import statsmodels.robust.scale as scale

DECIMAL = 4
#TODO: Can replicate these tests using stackloss data and R if this
# data is a problem
class TestChem(object):
    def __init__(self):
        self.chem = np.array([2.20, 2.20, 2.4, 2.4, 2.5, 2.7, 2.8, 2.9, 3.03,
            3.03, 3.10, 3.37, 3.4, 3.4, 3.4, 3.5, 3.6, 3.7, 3.7, 3.7, 3.7,
            3.77, 5.28, 28.95])

    def test_mean(self):
        assert_almost_equal(np.mean(self.chem), 4.2804, DECIMAL)

    def test_median(self):
        assert_almost_equal(np.median(self.chem), 3.385, DECIMAL)

    def test_stand_mad(self):
        assert_almost_equal(scale.stand_mad(self.chem), 0.52632, DECIMAL)

    def test_huber_scale(self):
        assert_almost_equal(scale.huber(self.chem)[0], 3.20549, DECIMAL)

    def test_huber_location(self):
        assert_almost_equal(scale.huber(self.chem)[1], 0.67365, DECIMAL)

    def test_huber_huberT(self):
        n = scale.norms.HuberT()
        n.t = 1.5
        h = scale.Huber(norm=n)
        assert_almost_equal(scale.huber(self.chem)[0], h(self.chem)[0], DECIMAL)
        assert_almost_equal(scale.huber(self.chem)[1], h(self.chem)[1], DECIMAL)

    def test_huber_Hampel(self):
        hh = scale.Huber(norm=scale.norms.Hampel())
        assert_almost_equal(hh(self.chem)[0], 3.17434, DECIMAL)
        assert_almost_equal(hh(self.chem)[1], 0.66782, DECIMAL)

class TestMad(object):
    def __init__(self):
        np.random.seed(54321)
        self.X = standard_normal((40,10))

    def test_stand_mad(self):
        m = scale.stand_mad(self.X)
        assert_equal(m.shape, (10,))

    def test_mad(self):
        n = scale.mad(self.X)
        assert_equal(n.shape, (10,))

class TestMadAxes():
    def __init__(self):
        np.random.seed(54321)
        self.X = standard_normal((40,10,30))

    def test_axis0(self):
        m = scale.stand_mad(self.X, axis=0)
        assert_equal(m.shape, (10,30))

    def test_axis1(self):
        m = scale.stand_mad(self.X, axis=1)
        assert_equal(m.shape, (40,30))

    def test_axis2(self):
        m = scale.stand_mad(self.X, axis=2)
        assert_equal(m.shape, (40,10))

    def test_axisneg1(self):
        m = scale.stand_mad(self.X, axis=-1)
        assert_equal(m.shape, (40,10))

class TestHuber():
    def __init__(self):
        np.random.seed(54321)
        self.X = standard_normal((40,10))

    def basic_functionality(self):
        h = scale.Huber(maxiter=100)
        m, s = h(self.X)
        assert_equal(m.shape, (10,))

class TestHuberAxes(object):
    def __init__(self):
        np.random.seed(54321)
        self.X = standard_normal((40,10,30))
        self.h = scale.Huber(maxiter=1000, tol=1.0e-05)

    def test_default(self):
        m, s = self.h(self.X, axis=0)
        assert_equal(m.shape, (10,30))

    def test_axis1(self):
        m, s = self.h(self.X, axis=1)
        assert_equal(m.shape, (40,30))

    def test_axis2(self):
        m, s = self.h(self.X, axis=2)
        assert_equal(m.shape, (40,10))

    def test_axisneg1(self):
        m, s = self.h(self.X, axis=-1)
        assert_equal(m.shape, (40,10))

if __name__=="__main__":
    run_module_suite()