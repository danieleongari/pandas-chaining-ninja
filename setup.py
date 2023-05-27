#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

if __name__ == '__main__':
    setup(packages=find_packages(),
          long_description=LONG_DESCRIPTION,
          long_description_content_type='text/markdown',
          name="pandas-chaining-ninja",
          author="Daniele Ongari",
          author_email="daniele.ongari@gmail.com",
          description="Pandas Chaining Ninja is a library that helps you to writing pandas code in a more readable way.",
          url="https://github.com/danieleongari/pandas-chaining-ninja",
          license="Creative Commons",
          classifiers=["Programming Language :: Python"],
          version="0.1.0",
          install_requires=[
              "pandas>=2.0",
              "ipython==8.13.2"
          ],
          extras_require={
              "testing": [
                  "pytest==7.3.1", 
                  "pytest-cov==2.12.1"
            ],
              "pre-commit": [
                  "pre-commit==3.2.2",
                  "yapf==0.33.0",
                  "prospector==1.9.0"
            ]
          })
