import numpy as np


def reverse(array, channels, subdivision=1):
    """
    Reverses subdivisions of an array of audio data.

    Reverses every nth subdivision of an array in place. The default
    subdivision argument reverses the whole array. Any greater number
    will reverse a subdivision of the array (eg. 2 will halve array,
    reverse the halves and combine them).

    array: a numpy array of audio data, numbers not empty
    channels: mono (1) or stereo (2) file
    subdivision: int, amount of subarrays to create default: 1
    returns: a reversed version of array by subdivision
    """

    # Check if array.shape divisible by subdivision
    # if not error
    if len(array) % subdivision != 0:
        print('Error: array size not divisible by subdivision.')
    
    # Subdivide array
    else:
        # Reverse every nth subarray
        rev_array = np.row_stack(np.flip(np.split(array, subdivision), axis=1))

        # Mono case for removing extra dimension from np.split
        # on mono arrays
        if channels == '1':
            rev_array = rev_array.reshape(array.size)
        
        # Return combined array
        return rev_array