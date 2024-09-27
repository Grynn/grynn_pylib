import subprocess
import tempfile
from loguru import logger
import pandas as pd

def bcompare_indices(a: pd.Index, b: pd.Index):
    """
    Diff two indices (a and b) using Beyond Compare (wait for user to close the window)
    """
    bcompare_frames(a.to_series(), b.to_series())


def bcompare_frames(a: pd.Series|pd.DataFrame, b: pd.Series|pd.DataFrame):
    """
    Diff two series (a and b) using Beyond Compare (wait for user to close the window)
    """
    aname = a.name if a.name is not None else "a"
    bname = b.name if b.name is not None else "b"

    with tempfile.NamedTemporaryFile(suffix=".csv", prefix=aname, delete=True) as temp1:
        with tempfile.NamedTemporaryFile(suffix=".csv", prefix=bname, delete=True) as temp2:
            a.to_csv(temp1.name)
            b.to_csv(temp2.name)
            print(f"Temp files: {aname}: {temp1.name},\n{bname}: {temp2.name}")
            subprocess.run(["bcomp", temp1.name, temp2.name])
            # subprocess.run waits for the process to complete
            # bcomp in turn waits for the user to close the comparison window

def bcompare(a: pd.Series|pd.DataFrame|pd.Index, b: pd.Series|pd.DataFrame|pd.Index):
    """
    Diff two series or dataframes using Beyond Compare (wait for user to close the window)
    """
    if isinstance(a, pd.Index): a = a.to_series()        
    if isinstance(b, pd.Index): b = b.to_series()
    bcompare_frames(a, b)
