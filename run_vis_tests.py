"""Visual tests requiring user interaction and viewing."""

import os
import unittest

import numpy as np
import matplotlib as mpl
import soundfile as sf
import inquirer

from soundscope.io.import_array import import_array
from soundscope.vis.bins import bins
from soundscope.vis.waveform import waveform
from soundscope.vis.magnitude import magnitude
from soundscope.vis.spectrogram import spectrogram
from soundscope.vis.vectorscope import vectorscope
from soundscope.vis.visualizer import visualizer


if __name__ == '__main__':
    # Test selector
    questions = [inquirer.Checkbox('tests', message='Which tests to run?',
        choices=['Mono', 'Stereo', 'Downsample', 'Bins', 'Waveform',
                 'Magnitude', 'Spectrogram', 'Vectorscope', 'Visualizer'],),]

    answers = inquirer.prompt(questions)

    if 'Mono' in answers['tests']:
        # Create test files
        # Random to simulate dither
        sf.write('silence.aiff', (2*np.random.default_rng(42).random((4410))
                 - 1) / 10000, 44100, 'PCM_16')
        sf.write('white.aiff', 2 * np.random.default_rng(42).random((4410))
                 - 1, 88200, 'PCM_16')
        sf.write('sin.aiff', np.sin(np.linspace(-np.pi, np.pi, 4410)), 44100,
                 'PCM_16')

        # Waveform to perform tests on
        questions2 = [inquirer.List('waves', message='Which test wave?',
            choices=[('Silence', 'silence.aiff'),
                     ('White Noise', 'white.aiff'),
                     ('Sin', 'sin.aiff')],
            default=('Sin', 'sin.aiff')),]

        answers2 = inquirer.prompt(questions2)

        mono = answers2['waves']

        name, channels, data, subtype, sample_rate = import_array(mono)

        if 'Bins' in answers['tests']:
            # Downsampling test mono
            binned, bin_sample_rate = bins(data, channels, sample_rate)
            print(binned, bin_sample_rate)

        if 'Downsample' in answers['tests']:
            # Downsampling for visualization
            data, sample_rate = bins(data, channels, sample_rate)

        if 'Waveform' in answers['tests']:
            # Waveform plot test case mono file
            waveform(data, name, channels, sample_rate)

        if 'Magnitude' in answers['tests']:
            # Magnitude test mono file
            magnitude(data, name, channels, sample_rate)

        if 'Spectrogram' in answers['tests']:
            # Spectrogram test case mono file
            spectrogram(data, name, channels, sample_rate)

        if 'Vectorscope' in answers['tests']:
            # Vectorscope mono test
            vectorscope(data, name, channels, sample_rate)

        if 'Visualizer' in answers['tests']:
            # Visualizer mono plot
            visualizer(data, name, channels, sample_rate)

        # Delete Test Files
        os.remove('silence.aiff')
        os.remove('white.aiff')
        os.remove('sin.aiff')

    if 'Stereo' in answers['tests']:
        # Create test files
        sf.write('silence2d.aiff', (2*np.random.default_rng(42).random((4410,
                 2)) - 1) / 10000, 44100, 'PCM_16')
        sf.write('white2d.aiff', 2 * np.random.default_rng(42).random((4410,
                 2)) - 1, 44100, 'PCM_16')
        sf.write('sin2d.aiff', np.sin(np.linspace([-np.pi, -np.pi], [np.pi,
                 np.pi], 4410)), 44100, 'PCM_16')
        sf.write('sin_out_phase.aiff', np.sin(np.linspace([-np.pi, np.pi
                 ], [np.pi, -np.pi], 4410)), 44100, 'PCM_24')

        # Waveform to perform tests on
        questions2 = [inquirer.List('waves', message='Which test wave?',
            choices=[
            ('Silence', 'silence2d.aiff'),
            ('White Noise', 'white2d.aiff'),
            ('Sin', 'sin2d.aiff'),
            ('Sin Out Phase', 'sin_out_phase.aiff')],
            default=('White Noise', 'white2d.aiff')),]

        answers2 = inquirer.prompt(questions2)

        stereo = answers2['waves']

        name, channels, data, subtype, sample_rate = import_array(stereo)

        if 'Bins' in answers['tests']:
            # Downsampling test stereo
            binned, bin_sample_rate = bins(data, channels, sample_rate)
            print(binned, bin_sample_rate)

        if 'Downsample' in answers['tests']:
            # Downsampling for visualization
            data, sample_rate = bins(data, channels, sample_rate)

        if 'Waveform' in answers['tests']:
            # Waveform plot test case stereo file
            waveform(data, name, channels, sample_rate)

        if 'Magnitude' in answers['tests']:
            # Magnitude test stereo file
            magnitude(data, name, channels, sample_rate)

        if 'Spectrogram' in answers['tests']:
            # Spectrogram test case stereo file
            spectrogram(data, name, channels, sample_rate)

        if 'Vectorscope' in answers['tests']:
            # Vectorscope stereo test
            vectorscope(data, name, channels, sample_rate)

        if 'Visualizer' in answers['tests']:
            # Visualizer stereo plot
            visualizer(data, name, channels, sample_rate)

        # Delete Test Files
        os.remove('silence2d.aiff')
        os.remove('white2d.aiff')
        os.remove('sin2d.aiff')
        os.remove('sin_out_phase.aiff')