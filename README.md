# Pandas Chaining Ninja

## What is the *Pandas Chaining* method?

The concept behind this method is to write the full pipeline that you need to transform your data in one stream of code:
in such a way you are not creating multiple versions of the dataframes or some slices of them.
The result is that you data pipeline is:
- easier to read
- easier to maintain
- easier to debug
- more efficient

But there are also some downsides:
- more pandas and numpy expertise is requres
- you need to run all the operations every time, which may be time consuming when working on a particular operation but you need to run the whole pipeline

## How to use this repository
1. Search what you need in this readme file
2. Look for working examples in the `tests/` folders: you can get the output on your computer with `pytest -s`, or checking *Actions > Last Commit > Build > Run tests with pytest*
3. Use GitHub search in repository to find the code you need: I'll try to use many keywords to make it easier to find
3. Explore further `REFERENCES.md`
4. Open an issue or a pull request if you want to add any technique it was useful for you, to share

The idea behind this repository is to share chunks of code that is easy to browse, and it is running tests via GitHub Actions 
to make sure the code is working with the lasest pandas version.

## Chunks of code

