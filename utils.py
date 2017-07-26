#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:03:52 2017

@author: pramod
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import time

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed



@timeit
def display_col_type(data):
    '''See column type distribution
       Parameters
       ----------
       data: pandas dataframe
       Return
       ------
       dataframe
    '''
    column_type = data.dtypes.reset_index()
    column_type.columns = ["count", "column type"]
    return column_type.groupby(["column type"]).agg('count').reset_index()


@timeit
def get_NC_col_names(data):
    '''Get column names of category and numeric
        Parameters
        ----------
        data: dataframe
        Return:
        ----------
        numerics_cols: numeric column names
        category_cols: category column names
    '''
    numerics_cols = data.select_dtypes(exclude=['O']).columns.tolist()
    category_cols = data.select_dtypes(include=['O']).columns.tolist()
    return numerics_cols, category_cols


@timeit
def missing_columns(data):
    '''show missing information
        Parameters
        ----------
        data: pandas dataframe
        Return
        ------
        df: pandas dataframe
    '''
    df_missing = data.isnull().sum().sort_values(ascending=False)
    df = pd.concat([pd.Series(df_missing.index.tolist()), pd.Series(df_missing.values),
                    pd.Series(data[df_missing.index].dtypes.apply(lambda x: str(x)).values),
                    pd.Series((df_missing / data.shape[0]).values)], axis=1, ignore_index=True)
    df.columns = ['col_name', 'missing_count', 'col_type', 'missing_rate']

    return df


