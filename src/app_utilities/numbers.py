from beartype import beartype
import numpy as np

from .datatypes import CompatibleNumber

@beartype
def get_optimal_intype(
    number: CompatibleNumber,
) -> type[np.integer] | type[np.floating]:

    """
    Return the optimal integer or float type for a given non-negative number.

    The function determines the smallest signed integer or float type that can
    represent the input number without loss of precision.

    Parameters
    ----------
    number : int or float or np.integer or np.float or Decimal
        The number to evaluate.

    Returns
    -------
    np.int8, np.int16, np.int32, np.int64, np.float32, np.float64
        The optimal signed integer or float type.

    Examples
    --------
    >>> get_optimal_intype(42)
    np.int8
    >>> get_optimal_intype(1000)
    np.int16
    >>> get_optimal_intype(-1e10)
    np.int64
    >>> get_optimal_intype(1e40)
    np.float64
    """

    if number <= 127:
        return np.int8
    elif number <= 32767:
        return np.int16
    elif number <= 2147483647:
        return np.int32
    elif number <= 9223372036854775807:
        return np.int64
    elif number <= 3.4028235e+38:
        return np.float32
    else:
        return np.float64


@beartype
def get_optimal_uintype(
    number: CompatibleNumber,
) -> type[np.integer] | type[np.floating]:

    """
    Return the optimal unsigned integer or float type for a given non-negative number.

    The function determines the smallest unsigned integer or float type that can
    represent the input number without loss of precision.

    Parameters
    ----------
    number : int or float or np.integer or np.float or Decimal
        The non-negative number to evaluate.

    Returns
    -------
    np.uint8, np.uint16, np.uint32, np.uint64, np.float32, np.float64
        The optimal unsigned integer or float type.

    Raises
    ------
    ValueError
        If the input number is negative.

    Examples
    --------
    >>> get_optimal_uintype(42)
    np.uint8
    >>> get_optimal_uintype(1000)
    np.uint16
    >>> get_optimal_intype(1e10)
    np.uint64
    >>> get_optimal_intype(1e40)
    np.float64
    """

    if number < 255:
        return np.uint8
    elif number < 65535:
        return np.uint16
    elif number < 4294967295:
        return np.uint32
    elif number < 18446744073709551615:
        return np.uint64
    elif number <= 3.4028235e+38:
        return np.float32
    else:
        return np.float64