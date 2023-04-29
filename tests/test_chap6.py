import pandas as pd
from . import DATA_DIR


def test_example():
    """Example"""

    df = pd.read_csv(DATA_DIR / "tab_6_4.csv")

    assert df.iloc[0,0] == 0.80
