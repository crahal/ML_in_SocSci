import pandas as pd
import os
from dtypes_dict import dtypes_dict
from query_dict import query_dict
from datetime import datetime
import string
import numpy as np


def subj_preprocessor(raw_file, subj, search_path):
    """
    Acts as main preprocessor file after loading data.

            Parameters:
                    raw_file: the preloaded raw corpus df
                    subj: the subject area abbreviation
                    search_path: i.e. ./data/scopus/search
            Returns:
                    None
    """
    print(f'{len(raw_file)} rows in the raw {subj}.')
    raw_file = raw_file.drop_duplicates(subset=['dc:identifier', 'dc:title'])
    print(f'{len(raw_file)} rows are unique.')
    raw_file = raw_file[(raw_file['dc:description'].notnull()) &
                        (raw_file['dc:description'].str.len() >= 5)]
    print(f'{len(raw_file)} rows have abstracts.')
    raw_file = raw_file[(raw_file['prism:coverDate'] > datetime.strptime('1960-01-01', '%Y-%d-%m')) &
                        (raw_file['prism:coverDate'] <= datetime.strptime('2020-31-12', '%Y-%d-%m'))]
    print(f'{len(raw_file)} rows remain within our date range.')
    raw_file['clean_abstract'] = raw_file['dc:description'].str.\
        replace('[{}]'.format(string.punctuation), '', regex=True)
    raw_file['clean_abstract'] = raw_file['clean_abstract'].str.lower()
    raw_file['is_ML'] = 0
    for query in query_dict.keys():
        raw_file[query] = 0
    for query, term in query_dict.items():
        raw_file[query] = np.where(raw_file['clean_abstract'].str.contains(term),
                                   1, raw_file[query])
        raw_file['is_ML'] = np.where(raw_file['clean_abstract'].str.contains(term),
                                     1, raw_file['is_ML'])
    raw_file.to_csv(os.path.join(search_path, 'clean', subj+'.tsv'), sep='\t')


def main_preprocessor(search_path):
    """
    Acts as main preprocessor func: calls subj_preprocessor
    for manually specified inputs.

            Parameters:
                    search_path: i.e. ./data/scopus/search
            Returns:
                    None
    """
    subj_dict = {'ECON': '20210501',
                 'SOCI': '20210518',
                 'BIOC': '20210620',
                 'BUSI': '20210501'}
    usecols_list = list(dtypes_dict.keys())
    usecols_list.append('prism:coverDate')
    for key, value in subj_dict.items():
        df = pd.read_csv(os.path.join(search_path, 'raw',
                                      'scopus_search_' + key + '_' + value + '.zip'),
                         compression='zip', sep='\t',
                         usecols=list(usecols_list),
                         dtype=dtypes_dict,
                         parse_dates=['prism:coverDate'],
                         nrows=100000,
                         )
        df['prism:coverDate'] = pd.to_datetime(df['prism:coverDate'], format='%Y-%d-%m')
        subj_preprocessor(df, key, search_path)


