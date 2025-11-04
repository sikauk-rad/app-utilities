from decimal import Decimal
from os import PathLike
from io import BytesIO

import numpy as np

type FileLike = PathLike[str] | BytesIO
type CompatibleNumber = int | float | np.integer | np.floating | Decimal
type CompatibleInt = int | np.integer
type CompatibleFloat = float | np.floating | Decimal
type JSONable = dict[str, JSONable] | list[JSONable] | str | int | float | bool | None