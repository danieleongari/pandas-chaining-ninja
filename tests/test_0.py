"""To be run as `pytest -s` to display the print statements"""

import pandas as pd
import numpy as np
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
    
    # Extra: use multiple assign variables
    df = (
        pd.read_csv(DATA_DIR / "table_1.csv")
        .assign(
            OpenCloseRange=lambda dfx: dfx["Open"] - dfx["Close"],
            # Use the column just created above, in the same assign
            OpenCloseRangeAbs=lambda dfx: dfx["OpenCloseRange"].abs() 
        )
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
    

def test_03():
    """Query rows by conditions."""
    print("\n>> Output from test_03:")
    
    MIN_VOLUME = 50000000
    
    df = (
        pd.read_csv(DATA_DIR / "table_1.csv")
        .query("Open > 160")
        .query("Close > 160")
        .query("Volume > @MIN_VOLUME")
        .query("Open > 165 | Close > 165")
        .query("Low > 160 & Close > 160")
        .loc[(lambda dfx: dfx["Volume"] > 0)]
        .query("MixedTypes.isna()")
    )
    
    display(df)
    
    assert len(df) < 20
    
def test_04():
    """Use numpy functions to create a new column based on other columns."""
    print("\n>> Output from test_04:")
    
    df = (
        pd.read_csv(DATA_DIR / "table_1.csv")
        .assign(
            OpenAbove165 = lambda dfx: np.where(dfx["Open"] > 165, True, False),
            OpenRange = lambda x: np.select(
                condlist = [
                    x["Open"] > 165,
                    x["Open"] >= 164, 
                    x["Open"] >= 162
                ],
                choicelist=[
                    "above 165", 
                    "range 164-165", 
                    "range 162-164"
                ],
                default="below 162"
            )
        )
    )
    
    display(df.head(5))
    
    assert "OpenAbove165" in df.columns and "OpenRange" in df.columns
    

def test_05():
    """Split one column into two (or more) in a single operation."""
    print("\n>> Output from test_05:")
    
    df = (
        pd.read_csv(DATA_DIR / "table_1.csv")
        .loc[lambda dfx: dfx["MixedTypes"].str.contains(" ", na=False)]
        # for this test are keept only rows where MixedTypes contains a " "
        .pipe(lambda x: x.assign(
            **x["MixedTypes"].str.split(" ", expand=True)
            .rename(columns={0: "FirstWord_alt1", 1: "SecondWord_alt1"}))
        )
        .pipe(lambda x: x.assign(
            **pd.DataFrame(
                x["MixedTypes"].str.split(" ").tolist(), 
                columns=["FirstWord_alt2", "SecondWord_alt2"],
                index=x.index
                )
            )
        )
    )
    
    display(df.head(5))
    
    assert "FirstWord_alt1" in df.columns and "SecondWord_alt2" in df.columns
    assert all(df["FirstWord_alt1"] == df["FirstWord_alt2"])
    
def test_06():
    """Use a custom multioutput function to create two new columns."""
    print("\n>> Output from test_06:")
    
    def mycustomfuncmultioutput(x):
        """Simple function where you can pass an array and return two arrays."""
        return x/1e3, x/1e6
    
    # Example with numpy
    example_array = np.array([2,4,6])
    assert (mycustomfuncmultioutput(example_array)[1] == example_array/1e6).all()
    
    df = (
        pd.read_csv(DATA_DIR / "table_1.csv")
        .query("Volume > 50000000")
        .pipe(lambda x: x.assign(
            **pd.DataFrame(
                x["Volume"].apply(mycustomfuncmultioutput).tolist(), 
                columns=["VolumeK", "VolumeM"],
                index=x.index #without this the index will be inconsitent: VERY TRICKY!
                )
            )
        )
    )
    
    display(df.head(5))
    
    assert "VolumeK" in df.columns and "VolumeM" in df.columns
    

def test_07():
    """Operate on certain subset of columns."""
    print("\n>> Output from test_07:")
    
    df = (
        pd.read_csv(DATA_DIR / "table_1.csv")
        .assign(
            Close1=lambda x: x["Close"] + 1,
            Close2=lambda x: x["Close"] + 2,
            Close3=lambda x: x["Close"] + 3,
            OpenNotClose=lambda x: x["Open"],
        )
        # After creating the new columns, we want to sum Close, Close1, Close2, Close3
        # but not OpenNotClose
        .assign(
            WrongSum0123 = lambda x: x.filter(like="Close").sum(axis=1), # will include OpenNotClose
            CloseSum0123 = lambda x: x.filter(regex="^Close").sum(axis=1) # Correct
        )
    )
    
    display(df.head(5))
    
    firstrow = df.iloc[0]
    assert firstrow["CloseSum0123"] == firstrow["Close"] + firstrow["Close1"] + firstrow["Close2"] + firstrow["Close3"]


def test_08():
    """Keep specific columns based on their values."""
    print("\n>> Output from test_08:")
    
    df = (
        pd.read_csv(DATA_DIR / "table_1.csv")
        # keep only columns that are non-numeric or have a mean >= 200
        .loc[:, lambda dfx: (
            dfx.select_dtypes(exclude="number").columns.tolist() + 
            dfx.select_dtypes(include="number").columns[dfx.select_dtypes(include="number").mean() >= 200].tolist()
        )]
    )
    
    display(df.head(3))
    
    assert all([ col not in df.columns for col in ["Open", "Low", "Close"]])