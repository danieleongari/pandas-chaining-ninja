# Pandas Chaining Ninja
![](header_image.jpg)

🔥 [Posted on Reddit r/datascience](https://www.reddit.com/r/datascience/comments/1h7j7ry/the_method_chaining_is_the_best_way_to_write/): 100k+ views

## What is the *Pandas Method Chaining* approach?
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
    .drop_duplicates(subset=["columnSum"]) # Drop rows having the same sum
    .pipe(lambda dfx: display(dfx) or dfx) # DEBUG: display the dataframe
    .assign(column3 = lambda x: x["column3"].apply(mycustomfunc)) # Apply a custom function
    .melt(id_vars=["column1", "column2"], value_vars=["column3", "column4"]) # Melt the dataframe
)
```

The concept behind this approach is to write the full pipeline that you need to transform your data, in one stream of code.

You don't need any particular extra library, it is just a philosophy of how to write your pandas code. 

As a result, you data pipeline will be:
- **easier to read** - you can see all operations line-by-line, in a compact format, and you can comment them on the side
- **easier to maintain** - no copies nor slices around (maybe even in different cells of a Jupyter notebook... you know what I mean!) 
- **easier to make modular** - you will elegantly define before the functions that you will use in the pipeline
- **easier to debug** - you can display the dataframe at any point of the pipeline (with `.pipe()`) or comment out (with `#`) all operations you are not focusing on
- **more *memory* efficient** - you don't waste memory in copies and slices

In the era of Large Language Models (LLMs) copilots, I believe that these advantages are more important than ever, 
to better synergize with the AI that is helping us to write code.

But let's be honest, there are also a few downsides:
- more pandas and numpy expertise is required (but LLMs like GPT-4o reached a level that can help you with that)
- it may be time consuming when you are debugging one singular operation that depends on the previous ones, as there are no checkpoints saved (but you can comment out later operations)

## How to use this repository

1. Search what you need in this README file, or read it all to have a flavor of what you can do
2. Look for working examples in the `tests/` folders: you can get the output on your computer with `pytest -s`, or checking *Actions > Last Commit > Build > Run tests with pytest*
3. Use GitHub search in repository to find the code you need: I'll try to use many keywords to make it easier to find
3. Explore further [REFERENCES](https://github.com/danieleongari/pandas-chaining-ninja/blob/master/REFERENCES.md)
4. Open an issue or a pull request if you want to add any technique it was useful for you, to share

The idea behind this repository is to share chunks of code that are easy to browse, and running tests via GitHub Actions 
to make sure the code is working with the lasest pandas version as well as some older versions.

With the method chaining you will use `numpy` and `pandas` functions that you may not be familiar with (e.g., `where`, `select`, `query`, `pipe`, `filter`, ...),
because you could do equivalent operations that are more intuitive when you are allowed to save-and-modify the dataframe multiple times.
Therefore the purpose of this repository is to provide a reference for the most common operations that are key to perform the data
manipulation under the method chaining.

You may wonder: *"Why didn't I use a Jupyter notebooks?"* 
Here a few reasons:
(1) to maintain the commits clean, 
(2) to split README's metacode to running code,
(3) to perform testing on the pandas version, having the possibility to run a chunk at a time,
(4) to more easily accept your PR contributions,
(5) to run [dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates) and check if the new releases of pandas are breaking any code snippets.

## Tested on different Pandas versions
The code in the `tests/` is run on all pandas version from 1.1 to the latest. The latest version is bumped by [dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates),
while for previous versions all the minor releases are tested to the latest bug fix, e.g., `1.1.5`, `1.2.5`, etc.

Earlier versions of `pandas<1.1` (July 28, 2020) are not tested because they don't support anymore what I believe are basic functionalities for the method chaining,
and I don't want to downgrade some useful functionalities to maintain compatibility with a 4+ years old version of the code.

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

# Calling the split function twice: easier to read, but less efficient
(
    df
    .assign(
        column1 = lambda x: x["column"].str.split(" ", expand=True)[0],
        column2 = lambda x: x["column"].str.split(" ", expand=True)[1]
    )
)

# Most efficient solution, but maybe less readable for a non-expert
(
    df
    .pipe(lambda x: x.assign(
        **x["column"].str.split(" ", expand=True)
        .rename(columns={0: "column1", 1: "column2"}))
    )
)

```

Note what is going on here: you first create an expanded dataframe with the two splitted columns named `0` and `1`.
Then you rename the columns to the desired names, and use `assign` to add them to the main dataframe.

See [`test_05`](https://github.com/danieleongari/pandas-chaining-ninja/blob/master/tests/test_0.py).

Another equivalent alternative to the latest variant:

```python
(
    df
    .pipe(lambda x: x.assign(
        **pd.DataFrame(
            x["column"].str.split(" ").tolist(), 
            columns=["column1", "column2"]),
            index=x.index
        )
    )
)
```
In this case you generate a DataFrame with the splitted columns, you assign the name of the columns you prefer,
and then you assign it to the main DataFrame with the same index.

Such alternative, is more generalizable, and you can use it with any custom function that returns multiple outputs:

```python
def mycustomfuncmultioutput(x):
    """Simple function where you can pass an array and return two arrays."""
    return x/1e3, x/1e6

(
    df
    .pipe(lambda x: x.assign(
        **pd.DataFrame(
            x["column"].apply(mycustomfuncmultioutput).tolist(), 
            columns=["column1", "column2"]),
            index=x.index
        )
    )
)
```

See [`test_06`](https://github.com/danieleongari/pandas-chaining-ninja/blob/master/tests/test_0.py).

> **Note**: in this example we saw a very interesting tradeoff between readability and efficiency, worth to be discussed.
> In any case, it is possible to make some clean chaining-rule readable code, but you will need to call the multi-output
> function as many times as the number of outputs you have. 
> If you want to be efficient, you need to write a more complex code that looks more like an IQ test than everyday code.
> Unless the DataFrame is very large, or the function is very slow, I would personally go with the first solution.
> The scope is to make the code readable and maintainable, not to make it a puzzle for the next developer!


### Operate on certain subset of columns

Practical example: sum columns whose column name starts with a certain string.

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

See [`test_07`](https://github.com/danieleongari/pandas-chaining-ninja/blob/master/tests/test_0.py).


### Keep specific columns based on their values

When you have many columns, you may want to keep only a few ones based on some logic applied to the content of their cells.

```python
(
    df
    .loc[:, lambda dfx: (dfx != 0).any(axis=0)] # Drop all columns that contain only zeros 
    .loc[:, lambda dfx: (dfx > 200).any(axis=0)] # Drop all columns that contain only values below 200 (working only if all columns are numeric)
    .loc[:, lambda dfx: (
        dfx.select_dtypes(exclude="number").columns.tolist() + 
        dfx.select_dtypes(include="number").columns[dfx.select_dtypes(include="number").mean() >= 200].tolist()
    )] # Keep all non-numeric columns and all numeric columns with mean >= 200
)
```

See [`test_08`](https://github.com/danieleongari/pandas-chaining-ninja/blob/master/tests/test_0.py).


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

Remember: life is to short to learn Regex, ask help to some Large Language Model!

