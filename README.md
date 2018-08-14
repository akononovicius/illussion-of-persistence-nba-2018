# Illusion of persistence in NBA 1995-2018 regular season data

In this repository we provide the code and the data behind the forthcoming paper
"Illusion of persistence in NBA 1995-2018 regular season data" (by A. Kononovicius).
The link to the paper will be soon.

The order in which files should be run in order to reproduce (or obtain similar)
results:
1. Scrape the data with `data-get.py`
1. Transform the full regular season record into individual team record data
with `data-transform.py`
1. Explore Hurst exponents of the original data with `data-analyze-original.ipynb`
1. Explore the first passage times (streak lengths) of the original data in
comparison with some random models with `data-analyze-passage-times.ipynb`.
1. Run shuffle the original data to obtain 95% CIs for H with `data-shuffle-\*.py`

Note that we have also shared the `.csv` files we have obtained. These are stored
in the `data` folder.

The `stats` folder contains couple of custom functions taken from
[another repository](https://github.com/akononovicius/python-stats).

**Licensing:** The scripts, scraped and generated data are made available under
[CC0](https://creativecommons.org/publicdomain/zero/1.0/).
