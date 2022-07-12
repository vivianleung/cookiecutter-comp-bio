#!/usr/bin/env python

# pdtools.py

# pandas helper tools

# Created 09 Sep 2021
# Vivian Leung

# some functions were moved from utils.py or previous pyhelpers pkg

#%%
import logging
import regex
from io import StringIO
from typing import Any, Annotated, Collection, Generic, NoReturn, TypeVar, Union

import numpy as np
import pandas as pd

from .utils import default

__all__ = ['IndexLabel', 'SeriesType', 'cast_dtypes', 'check_if_exists', 
           'check_if_redundant', 'dicts2df', 'drop_duplicates', 'parse_info',
           'reorder_cols']



#%%
IndexLabel = TypeVar('IndexLabel')

A = TypeVar('A')
class SeriesType(Generic[A]):
    """pandas.Series type"""
    def __init__(self, value: A):
        self.value = value
    def get(self) -> A:
        return self.value



def cast_dtypes(df: pd.DataFrame,
                dtypes: dict[IndexLabel, Union[str, type]],
                inplace: bool = False,
                verbose: bool = False) -> Union[NoReturn, pd.DataFrame]:
    """Type cast data"""
    def _cast_dtypes(_df: pd.DataFrame) -> list:
        casted = []
        for col, dtype in dtypes.items():
            try:
                _df[col] = _df[col].astype(dtype)
            except ValueError:
                print(f"Warning: '{col}' could not be cast as type",
                      (dtype.__name__ if isinstance(dtype, type) else dtype))
            except Exception as err:
                raise err
            else:
                casted.append(f"{col:15}: {dtype}")
        if verbose:
            print("Successfully casted:", *casted, sep='\n - ')
        return casted
    
    
    if inplace:
        _cast_dtypes(df)
    else:
        df_copy = df.copy()
        _cast_dtypes(df_copy)
        return df_copy
    
    
    
def check_if_redundant(df: pd.DataFrame, label1: IndexLabel, label2: IndexLabel
                       ) -> bool:
    
    is_redundant = (df[label1].astype(str) == df[label2].astype(str)).all()
    if not is_redundant:
        print(f"'{label1}' and '{label2}' differ for some entries")
    return is_redundant


def dicts2df(data: pd.DataFrame, *labels: IndexLabel,
             prefix: Annotated[Any, True, None] = None,
             append: bool = False, **kwargs) -> pd.DataFrame:
    """Convert dict values in given columns of input data into DataFrame
    
    Required:
        data:     pd.DataFrame 
        *labels:  column labels containing dicts to process 
    
    Optional:
        prefix:   constant value, True or None. Default Noneself.
            constant value (converted to str); use column names if True; or
            don't include prefix for new columns labels
            
        append:   bool, default False.
            If True, return input df with new cols appended and old cols
            dropped; else return only the new columns as dataframe
            (generated from dict values).
                  
        **kwargs: passed to pd.concat, excluding 'axis' kwarg
    
    Returns: pd.DataFrame
    """

    # def _applymap_pd_series(x: Any):
    #     if isinstance(x, str) or not isinstance(x, Collection):
    #         return pd.Series(None, dtype='object')
    #     elif len(x) == 0:
    #         return pd.Series(x, dtype='object')
    #     return pd.Series(x)

    # def _apply_pd_series(ser: pd.Series):
    #     _ser = ser.copy()        
    #     _ser.update(_ser.loc[_ser.isnull() \
    #         | _ser.astype(str).str.strip().str.len() == 0
    #         ].apply(lambda x: [x])
    #     )
    #     return _ser.apply(pd.Series)

    if len(labels) == 0:
        raise ValueError("No columns provided.")
    
    labels = list(labels)
    
    # replace null entries with [{}]
    cols = data[labels].applymap(lambda x: [{}] if pd.isnull(x) else x)
    
    
    # list of dicts converted to pd.Series objs
    dict_dfs = [cols[c].apply(pd.Series) for c in labels]
    
    if prefix == True:
        for p, df in zip(labels, dict_dfs):
            df.rename(lambda c: f"{p}_{c}", axis=1, inplace=True)
    
    elif prefix is not None:
        for df in dict_dfs:
            df.rename(lambda c: f"{prefix}_{c}", axis=1, inplace=True)
        
    kwargs['axis'] = 1
    return pd.concat(
        ([data.drop(labels, axis=1)] if append else []) + dict_dfs, **kwargs)


def check_if_exists(labels: list, index: pd.Index,
                    errors: Annotated[str, 'ignore', 'warn', 'raise'] = 'ignore'
                    ) -> list:
    """"check if label exists"""
    if min(len(labels), len(index)) == 0:
        return labels
    try:
        is_in_index = np.array([el in index for el in labels])
        assert all(is_in_index) or (errors == 'ignore'), \
            np.choose(np.where(~is_in_index), labels)[0]
                    
    except AssertionError as err:
        msg = f"Labels not in index: {list(err.args[0])}"
        if errors == 'warn':
            logging.warning(msg)
        elif errors == 'raise':
            raise ValueError(msg)
        else:
            raise ValueError(f"errors arg '{errors}' is invalid.")
    except:
        raise
    
    which_labels = np.where(is_in_index)
    
    return np.array(labels)[which_labels]

def drop_duplicates(df: pd.DataFrame, **kws) -> pd.DataFrame:
    """Nice way of dropping duplicates, handling complex objects like dicts
    
    **kws: passed to pd.DataFrame.drop_duplicates()
    """
    which_keep = df.reset_index().astype(str).drop_duplicates(**kws).index
    return df.iloc[which_keep, :]



def reorder_cols(df: pd.DataFrame,
                 first: Union[IndexLabel, Collection[IndexLabel], pd.Index] = None,
                 last: Union[IndexLabel, Collection[IndexLabel], pd.Index] = None,
                 inplace: bool = False,
                 ascending: bool = None,
                 sort_kws: dict = None,
                 errors: Annotated[str, 'ignore', 'warn', 'raise'] = 'ignore',
                 ) -> Union[pd.DataFrame, NoReturn]:
    """Reorders columns of dataframe.

    Arguments:
        df: pd.DataFrame
        first: column label, list of labels or pd.Index to put first
        last: column label, list of labels or pd.Index to put last
        inplace: bool, default False
        ascending: bool, default None
            how to sort remaining columns, where True is ascending, False is descending, and None is not sorted
        sort_kws: dict, default None
            kwargs to pass to pd.DataFrame.sort_index() func

    Returns: pd.DataFrame if inplace is False, else None.
    """
    if len(df.columns) == 0:
        if errors == 'raise':
            raise ValueError('Empty DataFrame')
        elif errors == 'warn':
            logging.warning('Warning: Empty DataFrame')
        return df
    
    if not isinstance(first, (pd.Index, list)):
        first = default(first, [], [first])
    if not isinstance(last, (pd.Index, list)):
        last = default(last, [], [last])
    
    first = check_if_exists(first, df.columns, errors=errors)
    last = check_if_exists(last, df.columns, errors=errors)
    
    mid = df.drop(first, axis=1).drop(last, axis=1)
        
    if isinstance(ascending, bool):
        mid = mid.sort_index(axis=1, ascending=ascending,
                             **default(sort_kws, {}))

    if inplace:
        left = pd.concat([df.loc[:, first], mid], axis=1)

        # reverse to insert at 0 during .apply
        left = left[list(reversed(left.columns))]

        # start with last columns
        df.drop([*first, *mid.columns], axis=1, inplace=True)
        left.apply(lambda col: df.insert(0, col.name, col))

    else:
        return pd.concat([df.loc[:, first], mid, df.loc[:, last]], axis=1) 
# %%


def parse_info(df: pd.DataFrame, other_metadata: dict = None) -> pd.DataFrame:
    """Get and parse dataframe info into a table, with metadata at top"""
    regex_table_border = regex.compile(r'^-[\s-]+$')
    regex_metadata = regex.compile(r'^([A-Za-z_][^:]*):(|(?:\s)(.+))$')
    regex_colsep = regex.compile(r'\s{2,}')

    # remove 'class' description line at start
    buffer = StringIO()
    df.info(verbose=True, buf=buffer)
    info_str = regex.sub(
        r'(?:^|\n)<class ["\']pandas\.[A-Za-z.]+["\']>(?:\n|$)', '',
        buffer.getvalue(), 1)


    metadata = default(other_metadata, [], lambda d: list(d.items()))
    header = None
    ncols = 1
    body = []
    prev_line = None

    for line in regex.splititer('\n', info_str):
        line = line.strip()
        if len(line) == 0:
            pass
        
        elif regex_table_border.match(line) is not None:  # tbl head line
            header = regex_colsep.split(prev_line)
            ncols = len(header)
            prev_line = None
        
        else:
            if prev_line is not None:  # add previous line to body
                first, right = regex_colsep.split(prev_line, maxsplit=1)
                other = [x[::-1] for x in 
                         regex_colsep.split(right[::-1], maxsplit=ncols - 2)]
                body.append([first, *other[::-1]])
                
            try:  # check if current line is metadata
                metadata.append(list(regex_metadata.match(line).groups()))
                prev_line = None
            except (AssertionError, AttributeError):
                prev_line = line
    
    # put together
    info = pd.DataFrame(body, columns=header)
    info.set_index(info.columns[0], inplace=True)
    info.columns = pd.MultiIndex.from_product(
        [*([m[1]] for m in metadata), info.columns],
        names=[*(m[0] for m in metadata), info.columns.name]
    )    
    return info
