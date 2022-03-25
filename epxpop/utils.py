"""
"""

import subprocess
import pandas as pd

__all__ = ["read_csv"]
__author__ = ["Duncan Campbell"]


def read_csv(fname, cols, header=None, converters={}) -> pd.DataFrame:
    """
    A customized reader for loading comma-separated value (csv) files into
    Pandas DataFrames.

    Parameters
    ----------
    fname : str, path object or file-like object
        Any valid string path is acceptable. The string could be a URL.
        Valid URL schemes include http, ftp, s3, gs, and file. For file URLs, a
        host is expected. A local file could be:
        file://localhost/path/to/table.csv. If you want to pass in a path
        object, this function accepts any os.PathLike. By file-like object, we
        refer to objects with a read() method, such as a file handle (e.g. via
        builtin open function) or StringIO.

    cols : dict
        a dictionary of column names, poitions, and data types,
        e.g. {‘a’: (0, np.float64), ‘b’: (1, np.int32), ‘c’: (2, ‘Int64’)}

    header : int, list of int, None
        Row number(s) to use as the column names, and the start of the data.
        Default behavior is to infer the column names: if no names are passed
        the behavior is identical to header=0 and column names are inferred
        from the first line of the file, if column names are passed explicitly
        then the behavior is identical to header=None. Explicitly pass header=0
        to be able to replace existing names. The header can be a list of
        integers that specify row locations for a multi-index on the columns
        e.g. [0,1,3]. Intervening rows that are not specified will be skipped
        (e.g. 2 in this example is skipped).

    Returns
    -------
    df : pandas.DataFrame
        A comma-separated values (csv) file is returned as two-dimensional data
        structure with labeled axes.

    Notes
    -----
    This is a wrapper around the pandas.read_csv function. See that function
    for more details.
    """

    usecols = []
    names = []
    for key in cols.keys():
        usecols.append(cols[key][0])
        names.append(key)

    # column dtypes
    dtypes = {key: cols[key][1] for key in cols.keys()}
    # if a converter for a column is specified, do not pass a dtype
    for key in cols.keys():
        if cols[key][0] in converters.keys():
            del dtypes[key]

    return pd.read_csv(
        fname,
        sep="\t",
        header=header,
        names=names,
        usecols=usecols,
        dtype=dtypes,
        converters=converters,
    )


def line_count(fname) -> int:
    """
    return the number of lines in `fname`

    Parameters
    ----------
    fname : path-like
        the file for which lines will be counted
    """
    return int(subprocess.check_output(f"wc -l {fname}", shell=True).split()[0])
