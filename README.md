# Illusion of persistence in NBA 1995-2018 regular season data

In this repository we provide the code and the data behind the paper
"Illusion of persistence in NBA 1995-2018 regular season data" [1].

The order in which files should be run in order to reproduce (or obtain similar)
results:
1. Scrape the data with `data-get.py`
1. Transform the full regular season record into individual team record data
with `data-transform.py`
1. Explore Hurst exponents of the original data with `data-analyze-original.ipynb`
1. Explore the first passage times (streak lengths) of the original data in
comparison with some random models with `data-analyze-passage-times.ipynb`.
1. Run shuffle the original data to obtain 95% CIs for H with `data-shuffle-\*.py`
1. Explore the autocorrelation functions of the original data in comparison to the
autocorrelation fucntion of the shuffled data with `data-analyze-correlation.ipyb`
(total shuffle) and `data-analyze-correlation-inseason.ipynb` (in-season shuffle).

Note that we have also shared the `.csv` files we have obtained. These are stored
in the `data` folder.

The `stats` folder contains couple of custom functions taken from
[another repository](https://github.com/akononovicius/python-stats).

**Licensing:** The scripts, scraped and generated data are made available under
[CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## References

[1] A. Kononovicius. *Illusion of persistence in NBA 1995-2018 regular season data*.
Physica A **520**: 250-256 (2019). doi:
[10.1016/j.physa.2019.01.039](https://dx.doi.org/10.1016/j.physa.2019.01.039).
arXiv: [1810.03383 [physics.soc-ph]](https://arxiv.org/abs/1810.03383).
