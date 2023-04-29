import pandas as pd
from . import DATA_DIR

def test_01():
    """Read a CSV file and create a new column with 3 different methods"""

    # Method 1: traditional
    df = pd.read_csv(DATA_DIR / "table_1.csv")
    df["OpenCloseRange"] = df["Open"] - df["Close"]
    
    assert "OpenCloseRange" in df.columns
    
    # Method 2: load the CSV file and then use chaining
    df = pd.read_csv(DATA_DIR / "table_1.csv")
    df = (
        df
        .assign(OpenCloseRange=df["Open"] - df["Close"])
    )
    
    assert "OpenCloseRange" in df.columns
    
    # Method 3: load CSV whithin the chaining
    df = (
        pd.read_csv(DATA_DIR / "table_1.csv")
        .assign(OpenCloseRange=lambda dfx: dfx["Open"] - dfx["Close"])
    )
    
    print()
    print(df.head(3))
    
    assert "OpenCloseRange" in df.columns

    
