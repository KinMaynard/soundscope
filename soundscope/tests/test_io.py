import os
import unittest

import numpy as np
import soundfile as sf

from soundscope.io.import_array import import_array
from soundscope.io.export_array import export_array


class TestIO(unittest.TestCase):
    """Test io module."""
    def test_import_array(self):
        """Test import_array module."""
        sf.write('tmp.wav', np.arange(-1, 1, .5).reshape(2, 2), 44100,
                 'PCM_24')
        metadata = ('tmp.wav', '2', np.array([[-1., -0.5], [0., 0.5]]),
                    '[PCM_24]', 44100)
        name, channels, data, subtype, sample_rate = import_array('tmp.wav')
        self.assertTrue((data == metadata[2]).all())
        self.assertEqual(name, metadata[0])
        self.assertEqual(channels, metadata[1])
        self.assertEqual(subtype, metadata[3])
        self.assertEqual(sample_rate, metadata[4])

    def test_export_array(self):
        """Test export_array module."""
        export_array('tmp.wav', np.array([[-1. , -0.5], [0., 0.5]]), 48000,
                     'PCM_24')
        name, channels, data, subtype, sample_rate = import_array('tmp.wav')
        self.assertEqual(sample_rate, 48000)

    def tearDown(self):
        os.remove('tmp.wav')