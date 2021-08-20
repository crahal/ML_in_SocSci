import pandas as pd
import os
from dtypes_dict import dtypes_dict
from query_dict import query_dict
from data_dict import data_dict
from dateutil.relativedelta import relativedelta
import string
import numpy as np
from tqdm import tqdm
window_days = 14


def make_df_topics(search_path):
    print('Making Topics DataFrame')
    topics_list = ['is_ML', 'Basic ML', 'Deep Learning', 'Support Vector', 'Trees', 'Shrinkage',
                   'Recognition', 'Gradient Boost', 'ML Eval']
    df_topics = pd.DataFrame(columns=topics_list, index=data_dict.keys())
    for subj in data_dict.keys():
        df_clean = pd.read_csv(os.path.join(search_path, 'clean', subj + '.tsv'), sep='\t')
        for query in topics_list:
            df_topics.at[subj, query] = df_clean[query].sum() / len(df_clean)
    df_topics.to_csv(os.path.join(search_path, 'topics', 'topics_df.tsv'), sep='\t')


def make_time(df):
    import datetime
    day_delta = datetime.timedelta(days=window_days)
    start_date = datetime.date(1960, 1, 1)
    end_date = datetime.date(2020, 12, 31)
    df_time = pd.DataFrame(columns=['is_ML', 'Total'])
    print('Processing Temporal File')
    for i in tqdm(range(int((end_date - start_date).days/window_days))):
        new_date = start_date + i*day_delta
        df_temp = df[(df['prism:coverDate'].dt.date > new_date - relativedelta(years=1)) &
                     (df['prism:coverDate'].dt.date <= new_date)]
        df_time.at[new_date, 'Total'] = len(df_temp)
        df_time.at[new_date, 'is_ML'] = df_temp['is_ML'].sum()
    return df_time


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
    from datetime import datetime
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
    for query, value in query_dict.items():
        raw_file[query] = 0
        for val in value:
            raw_file[query] = np.where(raw_file['clean_abstract'].str.contains(val),
                                       1, raw_file[query])
            raw_file['is_ML'] = np.where(raw_file['clean_abstract'].str.contains(val),
                                         1, raw_file['is_ML'])
    raw_file_temporal = make_time(raw_file)
    raw_file_temporal.to_csv(os.path.join(search_path, 'temporal', subj+'.tsv'), sep='\t')
    raw_file.to_csv(os.path.join(search_path, 'clean', subj+'.tsv'), sep='\t', index=False)


def main_preprocessor(search_path):
    """
    Acts as main preprocessor func: calls subj_preprocessor
    for manually specified inputs.

            Parameters:
                    search_path: i.e. ./data/scopus/search
            Returns:
                    None
    """
    usecols_list = list(dtypes_dict.keys())
    usecols_list.append('prism:coverDate')
    for key, value in data_dict.items():
        df = pd.read_csv(os.path.join(search_path, 'raw',
                                      'scopus_search_' + key + '_' + value + '.zip'),
                         compression='zip', sep='\t',
                         usecols=list(usecols_list),
                         dtype=dtypes_dict,
                         parse_dates=['prism:coverDate'],
                         #nrows=1000000
                         )
        df['prism:coverDate'] = pd.to_datetime(df['prism:coverDate'], format='%Y-%d-%m', errors='coerce')
        subj_preprocessor(df, key, search_path)
    make_df_topics(search_path)


if __name__ == '__main__':
    search_path = os.path.join(os.getcwd(), '..', 'data',
                               'scopus', 'search')
    main_preprocessor(search_path)