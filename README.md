<img src="./figures/ML_Over_Time_1400dpi.png" width="1100"/>

# The Rise of Machine Learning in the Academic Social Sciences

![coverage](https://img.shields.io/badge/Purpose-Commentary-yellow)
[![Generic badge](https://img.shields.io/badge/License-GNU3.0-purple.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Maintained-Yes-brightgreen.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/BuildPassing-Yes-orange.svg)](https://shields.io/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5918226.svg)](https://doi.org/10.5281/zenodo.5918226)
---

A short bit of code to accompany the commentary entitled: "The Rise of Machine Learning in the Academic Social Sciences" with [Mark Verhagen](https://github.com/MarkDVerhagen) and [Dave Kirk](https://www.nuffield.ox.ac.uk/people/profiles/david-kirk/). A preprint of the short commentary can be found [here](https://osf.io/preprints/socarxiv/gydve/).

It's part of a larger strand of work entitled 'The Evolution of Science', in this case made possible (with permission) through the [Scopus API](https://dev.elsevier.com/sc_apis.html). To replicate, interested researchers will need to query the Scopus API for three subject areas as detailed in the note(`['SOCI', 'BUSI', 'ECON']` for the main figure, and `['COMP', 'DECI', 'ENGI', 'ENER', 'ARTS', 'BIOC', 'AGRI']` for the inset. Alternatively, you could request access to the [International Centre for the Study of Research](https://www.elsevier.com/icsr) platform. A link to the Scopus definition of the subject areas can be found [here](https://dev.elsevier.com/documentation/ScopusSearchAPI.wadl). Then, `src/preprocessor.py` takes the dictionary of terms for regular expression based searches in `src/query_dict.py`, cleans the raw individual subject areas (in `data/scopus/search/raw/`), and creates temporal rolling windows, topics for the scatter inset, and scalar summary statistics (output to `data/scopus/search/clean`, `data/scopus/search/temporal`, `data/scopus/search/topics`, and `data/scopus/search/scalars/`). The `src/query_dict.py` file is important: it maps various lists of terms onto our directionary of 'broader' terms for the regular expression exercises which essentially power the inset figure but also as a total composite create our main index over time.  Naturally, `make_figure.py` creates the visualisation.

The main requirements are all covered by an [Anaconda](https://www.anaconda.com/) installation. The requirements more generally can be found in `requirements.txt`, and as noted there, the project makes specific use of pandas (1.0.4) and matplotlib (3.5.1).

The data which is used to create the visualisations can be found at `./data/scopus/search`.

This work is made available under a GNU General Public License v3.0. The authors are grateful of support from the Leverhulme Trust, the Leverhulme Centre for Demographic Science (LCDS) and Nuffield College. Comments gratefully received from Felix Tropf, Per Engzell, Saul Newman and Kyla Chasalow and members of the LCDS more broadly, but all errors remain our own. Please raise all issues on this repository and do feel free to get in touch with any queries or comments more generally!
