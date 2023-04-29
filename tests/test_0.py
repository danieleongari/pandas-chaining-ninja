import pandas as pd
from . import DATA_DIR

from IPython.display import display

def test_01():
    """Read a CSV file and create a new column with 3 different methods"""
    print("\n>> Output from test_01:")

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
    
    
    display(df.head(3))
    
    assert "OpenCloseRange" in df.columns

    
def test_02():
    """Display the dataframe within the chaining."""
    print("\n>> Output from test_02:")
    
    df = (
        pd.read_csv(DATA_DIR / "table_1.csv")
        .pipe(lambda dfx: print("DataFrame before...") or dfx) # Note you need to use "or df" to return the dataframe instead of a None
        .pipe(lambda dfx: display(dfx.head(3)) or dfx)
        .assign(OpenCloseRange=lambda dfx: dfx["Open"] - dfx["Close"])
        .pipe(lambda dfx: display("\nDataFrame after...\n", dfx.head(3)) or dfx) # You can also pass multiple arguments to display
    )
    
    assert "OpenCloseRange" in df.columns