<img src="./figures/ML_Over_Time.png" width="1100"/>

# Machine Learning in the Academic Social Sciences: a quintessential case of Amara’s Law?

![coverage](https://img.shields.io/badge/Purpose-Commentary-yellow)
[![Generic badge](https://img.shields.io/badge/Python-3.8-red.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/License-GNU3.0-purple.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Maintained-Yes-brightgreen.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/BuildPassing-Yes-orange.svg)](https://shields.io/)
---

A short bit of code to accompany the commentary entitled: "Machine Learning in the Academic Social Sciences: a quintessential case of Amara’s Law?" with [Mark Verhagen](https://github.com/MarkDVerhagen). 

It's part of a larger strand of work entitled 'The Evolution of Science' all made possible through the [Scopus API](https://dev.elsevier.com/sc_apis.html). To replicate, interested researchers will need to query the Scopus API for entire subject areas as detailed in the note. Then, `src/preprocessor.py` takes the dictionary of terms for regular expression based searches in `src/query_dict.py`, cleans the raw individual subject areas (in `data/scopus/search/raw/`), and creates temporal rolling windows, topics for the scatter inset, and scalar summary statistics (output to `data/scopus/search/clean`, `data/scopus/search/temporal` and `data/scopus/search/scalars/`).

This work is made available under a GNU General Public License v3.0. Please raise all issues on this repository and do feel free to get in touch with any queries or comments more generally!
