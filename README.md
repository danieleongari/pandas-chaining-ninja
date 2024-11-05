# Pandas Chaining Ninja
![](header_image.jpg)

## What is the *Pandas Chaining* method?
```python
def mycustomfunc(xxx):
    # turn xxx value into xxy
    return xxy

df = (
    pd.read_csv("data.csv") # Load the data
    .pipe(lambda dfx: print(f"Number of rows BEFORE query: {len(dfx)}") or dfx)
    .query("column1 > 0")
#    .query("column2 > 0") # DEBUG: filter rows on stricter condition
    .pipe(lambda dfx: print(f"Number of rows AFTER query: {len(dfx)}") or dfx)
    .assign(columnSum = lambda x: x["column1"] + x["column2"]) # Create new column
    .drop_duplicated(subset=["columnSum"]) # Drop rows having the same sum
    .pipe(lambda dfx: display(dfx) or dfx) # DEBUG: display the dataframe
    .assign(column3 = lambda x: x["column3"].apply(mycustomfunc)) # Apply a custom function
    .melt(id_vars=["column1", "column2"], value_vars=["column3", "column4"]) # Melt the dataframe
)
```

The concept behind this method is to write the full pipeline that you need to transform your data in one stream of code:
in such a way you are not creating multiple versions of the dataframes or some slices of them.
The result is that you data pipeline is:
- easier to read, as you can see all operations line-by-line and also comment them on the side
- easier to maintain, no copies nor slices around
- easier to make modular, as you elegantly define before the functions that you will use in the pipeline
- easier to debug, you can display the dataframe at any point of the pipeline and comment out some operations to see the result
- more *memory* efficient, you don't waste memory in copies and slices

But there are also some downsides:
- more pandas and numpy expertise is requres
- you need to run all the operations every time, which may be time consuming when working on a particular single operation (i.e., line) but you need to run the whole pipeline

## How to use this repository
1. Search what you need in this readme file
2. Look for working examples in the `tests/` folders: you can get the output on your computer with `pytest -s`, or checking *Actions > Last Commit > Build > Run tests with pytest*
3. Use GitHub search in repository to find the code you need: I'll try to use many keywords to make it easier to find
3. Explore further [REFERENCES](https://github.com/danieleongari/pandas-chaining-ninja/blob/master/REFERENCES.md)
4. Open an issue or a pull request if you want to add any technique it was useful for you, to share

The idea behind this repository is to share chunks of code that is easy to browse, and it is running tests via GitHub Actions 
to make sure the code is working with the lasest pandas version.

Using the chaining method you will use nupy and pandas functions that you may not be familiar with (e.g., `where`, `select`, `query`, `pipe`, `filter`, ...),
because you could do equivalent operations that are more intuitive when you are allowed to save-and-modify the dataframe multiple times.
Therefore the purpose of this repository is to provide a reference for the most common operations that are key to perform the data
manipulation under the chaining method.

Why didn't I use Jupyter notebooks? Multiple reasons: 
(1) to maintain the commits clean, 
(2) to split REAME's metacode to running code,
(3) to perform testing on the pandas version, having the possibility to run a chunk at a time,
(4) to more easily accept your PR contributions,
(5) to run [dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates) and check if the new releases of pandas are breaking the code snippets.
Anyway, I will maybe add a Jupyter notebook in the future.

## Tested on different Pandas versions
The code in the `tests/` is run on all pandas version from 1.1 to the latest. The latest version is bumped by [dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates),
while for previous versions all the minor releases are tested to the latest bug fix, e.g., `1.1.5`, `1.2.5`, etc.

Note: earlier versions of pandas are not tested because they are not supported anymore for the code in test.

## Chunks of code

### Read CSV
You can start reading the CSV file already inside the chaining:
```python
df = (
    pd.read_csv("data.csv")
    .dosomeoperation()
    .dosomeotheroperation()
)
```
See [`test_01`](https://github.com/danieleongari/pandas-chaining-ninja/blob/master/tests/test_0.py).

### Add new columns
You can add new columns to the dataframe with `assign`:
```python
(
    df
    .assign(new_column = lambda x: x["column1"] + x["column2"])
    .assign(
        new_column2 = lambda x: x["column3"] * 2,
        new_column3 = lambda x: x["new_column2"] / 2 # You can use the new column in the same assign
    )
)
```


If you need to create a column with spaces in the name, you can use `assign` with a dictionary:
```python
(
    df
    .assign(**{"new column": lambda x: x["column1"] + x["column2"]})
)
```
See [`test_01`](https://github.com/danieleongari/pandas-chaining-ninja/blob/master/tests/test_0.py).

### Display the dataframe within the chaining
You can display the dataframe within the chaining with `pipe`:
```python
(
    df
    .pipe(lambda x: display(x) or df)
    .dosomeoperation()
    .dosomeotheroperation()
)
```
See [`test_02`](https://github.com/danieleongari/pandas-chaining-ninja/blob/master/tests/test_0.py).

### Query rows by conditions
Instead of using `df[df.column1>0]` you can query rows by condition with `query`:
```python
(
    df
    .query("column1 > 0")
    .query("`column 2` > 0") # use backticks for columns with spaces
    .query("column3 > @myvalue") # use @ for local variables
    .query("column4 > 0 | column5 > 0") # use | for OR
    .query("column6 > 0 & column7 > 0") # use & for AND ...but note thta this is the same as using multiple lines of query!
    .query("column9.isna()") # Select rows with NaN value for column9 
    .loc[(lambda dfx: dfx["column8"] > 0)] # You can also use a lambda function with .loc as alternative to .query
)
```
See [`test_03`](https://github.com/danieleongari/pandas-chaining-ninja/blob/master/tests/test_0.py).

### Use numpy functions to create a new column based on other columns
Create a new column with the result of a [numpy `where`](https://numpy.org/doc/stable/reference/generated/numpy.where.html) function:
```python
(
    df
    .assign(val2ifPos_val3ifNeg = lambda x: np.where(x["column1"] > 0, x["column2"], x["column3"]))
)
```
or using [`np.select`](https://numpy.org/doc/stable/reference/generated/numpy.select.html) for multiple conditions:
```python
(
    df
    .assign(SelectedColValue = lambda x: np.select(
        condlist = [
            x["colSel"] == "A", 
            x["colSel"] == "B", 
            x["colSel"] == "C"],
        choicelist = [x["colA"], x["colB"], x["colC"]],
        default = x["colX"] # If non of the conditions are met, use this value
    ))
)
``` 
See [`test_04`](https://github.com/danieleongari/pandas-chaining-ninja/blob/master/tests/test_0.py).

### Split one column into two (or more) in a single operation
You have a column with strings like `AAA BBB` and you want to split `AAA` and `BBB` into two separated columns.
You want to be eficient and not call the `split` function twice to do the same operation.

```python
# Not Chaining: N00B!
df[["column1", "column2"]] = df["column"].str.split(" ", expand=True)

# Calling the split function twice: NOT EFFICIENT!
(
    df
    .assign(
        column1 = lambda x: x["column"].str.split(" ", expand=True)[0],
        column2 = lambda x: x["column"].str.split(" ", expand=True)[1]
    )
)

# GOD solution
(
    df
    .pipe(lambda x: x.assign(
        **x["column"].str.split(" ", expand=True)
        .rename(columns={0: "column1", 1: "column2"}))
    )
)
```
See [`test_05`](https://github.com/danieleongari/pandas-chaining-ninja/blob/master/tests/test_0.py).


### Operate on certain subset of columns
Practical example: sum columns that start with a certain string.

Rational: since it is somewhat impractical to use MultiIndex columns in pandas (IMHO), if you want to specify a subset of columns
it is usually more convenient to pre/post-pend a string and use [pandas `filter`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.filter.html) to select them.

Here, we want to sum the attributes `attr` of `df.columns = ["ID", "attr_1", "attr_2", "attr_3", "value", "notes"]`:
```python
(
    df
    .assign(
        attr_sum_alt1 = lambda x: x.filter(like="attr_").sum(axis=1), # filter if "attr_" is in the column name
        attr_sum_alt2 = lambda x: x.filter(regex="^attr_").sum(axis=1), # filter if "attr_" is at the start of the column name, using regex (see CheatSheet at the end of this README)
    )
)
```
See [`test_06`](https://github.com/danieleongari/pandas-chaining-ninja/blob/master/tests/test_0.py).


### Drop specific columns based on their values
```python
(
    df
    .loc[:, lambda dfx: (dfx != 0).any(axis=0)] # Drop all columns that contain only zeros
    .loc[:, lambda dfx: dfx.select_dtypes(include="number").sum() >= 0] # Drop all columns whose sum is negative, ignoring non-numeric columns
)
```

## Regex Cheat Sheet
- `^` start of string
- `$` end of string
- `.` any character
- `*` zero or more repetitions
- `+` one or more repetitions
- `?` zero or one repetitions
- `[]` any character inside the brackets
- `[^]` any character not inside the brackets
- `|` OR
- `()` group
- `\` escape character
- `\d` digit
- `\D` non-digit
- `\s` whitespace
- `\S` non-whitespace
- `\w` alphanumeric
- `\W` non-alphanumeric

