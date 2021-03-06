import sys

import numpy as np


def mask(array):
    """
    Calculate boolean mask of non-zeros: -epsilon > non0's > epsilon.

    array: numpy array of audio data.
    returns: boolean mask of nonzeros (values greater than epsilon)
    in array.
    """

    epsilon = sys.float_info.epsilon
    mask = abs(array) > epsilon
    return mask


def first_nonzero(array, axis, mask, invalid_val=-1):
    """
    Get index of the first non_zero element in an array.

    array: 1d or 2d numpy array of audio data.
    axis: generic axis specifier along which to access elements.
    mask: boolean array of non zeros (non epsilon) values in array.
    invalid_value: marker for dimensions of only zeros.
    returns: index of first non zero value in array.

    argmax returns indicies of first matches (True values) in cases
    where max occurs multiple times, using where() given any() as the
    condition we can return the index from argmax for any true value in
    the mask and the invalid value marker otherwise.

    Column major order access.
    """

    # Boolean array of True where element of original array is nonzero
    # false otherwise (if zero)
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)


def last_nonzero(array, axis, mask, invalid_val=-1):
    """
    Get index of the last non_zero element in an array.

    array: 1d or 2d numpy array of audio data.
    axis: generic axis specifier axis along which to access elements.
    mask: boolean array of non zeros (non epsilon) values in array.
    invalid_value: marker for dimensions of only zeros, default argument
    is -1.
    returns: index of last non zero value in array.

    Similar behavior to first_nonzero however we flip along the axis
    to access and use argmax again for the behavior of finding indicies
    of first occurence in tie cases we compensate for the flipping by
    offsetting from the axis length.

    Accessing the array here in column major order.
    """

    # Boolean array of True where element of original array is nonzero
    # false otherwise (if zero)
    dex_last_occur = array.shape[axis] - np.flip(
        mask, axis=axis).argmax(axis=axis) - 1
    return np.where(mask.any(axis=axis), dex_last_occur, invalid_val)


def trim(array):
    """
    Truncates leading and trailing silence (0's) from array.

    array: numpy array created from an audio file.
    returns: array without leading and trailing silence.

    Want min index of any channel from first non zero and max index of
    any channel from last non zero to avoid 2 different sized channels.
    """

    # Mask of absolute value of values > epsilon
    mask1 = mask(array)
    # Return a copy of array sliced from first nonzero element to
    # last nonzero element
    # Adds 1 to compensate for indexing from zero
    return array[np.amin(first_nonzero(array, 0, mask1)):np.amax(last_nonzero(
        array, 0, mask1)) + 1].copy()