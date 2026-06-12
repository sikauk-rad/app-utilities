from decimal import Decimal
from os import PathLike
from io import BytesIO

import numpy as np

# type 
FileLike = PathLike[str] | BytesIO
CompatibleNumber = int | float | np.integer | np.floating | Decimal
CompatibleInt = int | np.integer
CompatibleFloat = float | np.floating | Decimal

JSONable = dict[str, "JSONable"] | list["JSONable"] | str | int | float | bool | None
