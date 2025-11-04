from pathlib import Path
import re
from zipfile import ZipFile

from beartype import beartype

from .datatypes import FileLike


@beartype
def prevent_directory_override(
    new_directory_path: Path,
) -> Path:

    """
    Create a new directory, avoiding name collisions by appending a counter if necessary.

    If the specified directory already exists, appends an incrementing integer to the 
    directory name until a unique name is found, then creates the directory.

    Parameters
    ----------
    new_directory_path : Path
        The desired path for the new directory.

    Returns
    -------
    Path
        The path to the newly created directory, guaranteed to be unique.

    Examples
    --------
    >>> prevent_directory_override(Path("output"))
    PosixPath('output')
    >>> prevent_directory_override(Path("output"))
    PosixPath('output 0')
    """

    n = 0
    while new_directory_path.exists():
        new_directory_path = new_directory_path.with_stem(f'{new_directory_path.name} {n}')
        n += 1
    new_directory_path.mkdir(parents = True)
    return new_directory_path


@beartype
def get_excel_sheet_names(file: FileLike) -> list[str]:

    """
    Extract the names of all sheets from an Excel (.xlsx) file.

    Opens the given Excel file (as a path or file-like object), reads the workbook 
    metadata, and returns a list of sheet names.

    Parameters
    ----------
    file : FileLike
        The Excel file to read, as a path or file-like object.

    Returns
    -------
    list of str
        A list containing the names of all sheets in the workbook.

    Examples
    --------
    >>> get_excel_sheet_names(Path("workbook.xlsx"))
    ['Sheet1', 'Sheet2']
    """

    with ZipFile(file, 'r') as zip_ref: 
        xml = zip_ref.read('xl/workbook.xml').decode('utf-8')
    return [re.search(
        'name="[^"]*', 
        s_tag,
    ).group(0)[6:] for s_tag in filter(None, re.findall("<sheet [^>]*", xml))]