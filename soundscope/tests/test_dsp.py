'''
Audio processing & visualization library

Unit Tests
'''

import unittest
import numpy as np
from soundscope.dsp.normalize import normalize
from soundscope.dsp.midside import midside

encoded = np.array([[ 0.5,  0.5], [ 0.5, -0.5]])

class TestDsp(unittest.TestCase):
	
	def test_midside(self):
		self.assertEqual(midside(np.arange(2), '1'), np.array([[0., 0.], [1., 0.]]), True)
		self.assertEqual(midside(np.identity(2), '2'), encoded, True)
		self.assertEqual(midside(encoded, '2', False), np.identity(2), False)

	def test_normalize(self):
		array, normal = normalize(np.arange(-50, 75, 25))
		self.assertTrue((array == np.array([-1., -0.5, 0., 0.5, 1.])).all())
		self.assertEqual(normal, True)