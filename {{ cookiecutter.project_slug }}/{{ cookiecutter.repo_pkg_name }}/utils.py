#!/usr/bin/env python

# utils.py

# General helper functions

#%%
### NOTE TO SELF: DO NOT IMPORT ANYTHING FROM src! (circular)
import json
import logging
import os
import pickle
from datetime import datetime
from typing import Annotated, Any, Callable, Collection, Iterable, Union

import numpy as np
import pandas as pd

from .config import NoneType
#%%

__all__ = ['now', 'default', 'dropna', 'strjoin', 'makedirs', 'ordered_set',
           'savefile', 'setdefaults', 'logging_defaults', 'init_logging']

_LOGGING_DEFAULTS = dict(
    format= "[ %(asctime)s %(name)s - %(funcName)12s():%(lineno)s ] %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO,
)


#%%
def now(time: bool = False, fmt: str = None) -> str:
    """Returns current date as YYYY-mm-dd, plus HHMM if time==True, or fmt"""
    if fmt is None:
        fmt = f"%Y-%m-%d{'-%H%M' if time else ''}"
    return datetime.now().strftime(fmt)
    


def default(x: Any, default_value: Any = None, has_value: Any = lambda x: x,
            null: Annotated[Union[Any, Collection[Any], str], 'null'] = None,
            *args, **kwargs):
    """General function for checking/returning null/non-null objects.
    
    x: Any
        object to test
        
    default_value: Any, default None
        Value to return if x is null

    has_value: Any, default lambda x: x
        if x is not null, then return this. if has_value is a function, then
        it should take x as the first arg and any *args, **kwargs

    null: value or list of values considered as null, or 'null'. default None.
        If null='null', then any null-like value is considered,
            i.e. None, np.nan, empty strings or 0-length collections. can't
            handle generators.
        If the literal value 'null' or non-str collections (e.g. tuple()) are
            to considered as null values, they should be wrapped in a list-like
            (e.g. [tuple()] or ['null', tuple()]).

    *args, **kwargs passed to has_value (if it is a function)
    """
    
    none_objs = [None, np.nan]
    try:
        if null == 'null':
            if hasattr(x, '__len__'):
                assert len(x) > 0
            assert x not in none_objs
                    
        else:
            if isinstance(null, str) or not isinstance(null, Collection):
                null = [null]
            
            for n in null:
                # np.nan == np.nan is False, but np.nan is np.nan is True
                assert not ((x in none_objs) and (n in none_objs))
                assert x != n
            
    except AssertionError:
        return default_value
    
    except:
        raise
    else:
        if isinstance(has_value, Callable):
            return has_value(x, *args, **kwargs)
        else:
            return has_value


def dropna(obj: Any, simplify: bool = False
           ) -> Union[Any, list[Any], NoneType]:
    """Nice way of dropping null values from potential list"""
    try:
        assert not isinstance(obj, (str, bytes))
        nonnull = []
        for x in obj:
            try:
                if pd.notnull(x):
                    nonnull.append(x)
            except ValueError:
                if pd.notnull(x).any():
                    nonnull.append(x)
        if len(nonnull) == 0:
            return None
        if (len(nonnull) == 1) and simplify:
            return nonnull[0]
        return nonnull
    except (AssertionError, TypeError):
        return obj



def ordered_set(lst: Iterable) -> list:
    seen = set()
    ordered = []
    for x in lst:
        try:
            is_seen = x in seen or seen.add(x)
        except TypeError:
            is_seen = str(x) in seen or seen.add(str(x))
        if not is_seen:
            ordered.append(x)     
    # ordered = [x for x in lst if not (x in seen or seen.add(x))]
    return ordered

def suffixize_fpath(fpath: str, suffix: str) -> str:
    """Inserts suffix before extension of a filepath"""
    fname, sep, ext = os.path.basename(fpath).rpartition('.')
    return f"{fname}-{suffix}{sep}{ext}"


def strjoin(*args: Any, sep: str = ',') -> str:
    return str(sep).join([str(a) for a in args])


def makedirs(name: str, **kws):
    """Wrapper for os.makedirs with extra error reporting.
    
    **kws passed to os.makedirs
    """
    try:
        os.makedirs(name)
    except FileExistsError:
        assert os.path.isdir(name), f"'{name}' exists but is not a directory!"
    else:
        print("Created directory:", name)


def savefile(obj: Any, name: str, savedir: str = None,
             path: str = None, ftype: str = None,
             overwrite: Annotated[Union[bool, str], True, False, 'ask', 'warn'
                                  ] = 'warn', **kws):
    """
    ftype: str, default 'infer' from name of file ('name' or in 'path')
        for pd objects: default csv.
            csv|tsv, html, json, latex|tex, md|markdown, pkl|pickle,
            string|txt|text, excel|xls|xlsx, xml
        other objects: default raw (text)
            pkl|pickle, json, txt|text|raw

    """
    assert (savedir is not None) or (path is not None), \
        "Neither savedir nor path were provided"
    
    if path is None:
        path = os.path.join(savedir, name)

    try:
        assert not os.path.exists(path)
    except AssertionError:
        if overwrite == True:
            pass
        elif overwrite == 'warn':
            print(f"Overwriting existing file {path}")
        elif overwrite == 'warn':
            msg = f"File {path} exists! Continue? [Y|n] "
            do_continue = input(msg)
            while do_continue.lower() not in [' ', 'y', 'n']:
                do_continue = input(msg)
            if do_continue == 'n':
                return
        elif overwrite == False:
            raise FileExistsError(path)
        else:
            raise ValueError(f"'overwrite' value '{overwrite}' is invalid.")

    ftype = default(ftype, os.path.splitext(path)[1][1:]).lower()
    
    if isinstance(obj, (pd.DataFrame, pd.Series)):
        
        if ftype in ['excel', 'xls', 'xlsx']:
            kws.set_default('writer', pd.ExcelWriter(path))
            obj.to_excel(**kws)
            
        elif ftype == 'html':
            obj.to_html(path, **kws)
            
        elif ftype == 'json':
            obj.to_json(path, **kws)
            
        elif ftype in ['latex', 'tex']:
            obj.to_latex(path, **kws)
            
        elif ftype in ['md', 'markdown']:
            obj.to_markdown(path, **kws)
            
        elif ftype in ['string', 'text', 'txt']:
            obj.to_string(path, **kws)
            
        elif ftype in ['pkl', 'pickle']:
            obj.to_pickle(path, **kws)
            
        elif ftype == 'xml':
            obj.to_xml(path, **kws)
            
        else:  # default csv
            if ftype == 'tsv':
                kws.setdefault('sep', '\t')
            obj.to_csv(path, **kws)
            
    elif ftype in ['pkl', 'pickle']:
        with open(path, 'wb') as fout:
            pickle.dump(obj, fout, **kws)
            
    elif ftype == 'json':
        with open(path, 'w') as fout:
            json.dump(obj, fout, **kws)
            
    else:
        with open(path, 'w') as fout:
            fout.write(str(obj))

    print(f"-  Saved file {os.path.basename(path)} as {ftype}",
          f"at {os.path.dirname(path)}.")

    


# def expand_dict(data: pd.DataFrame, *columns: IndexLabel,
#                 prefix: Annotated[str, True, None],
#                 **kwargs) -> pd.DataFrame:
#     """kwargs passed to pd.concat, excluding axis kwarg"""
    
#     columns = list(columns)
    
#     # list of dicts converted to pd.Series objs
#     dict_dfs = [data[c].apply(pd.Series) for c in columns]
    
#     if prefix == True:
#         for p, df in zip(columns, dict_dfs):
#             df.rename(lambda c: f"{p}_{c}", axis=1, inplace=True)
    
#     elif prefix is not None:
#         for df in dict_dfs:
#             df.rename(lambda c: f"{prefix}_{c}", axis=1, inplace=True)
        
#     kwargs['axis'] = 1
#     return pd.concat([data.drop(columns, axis=1)] + dict_dfs, **kwargs)

def setdefaults(dct: dict, defaults: dict) -> None:
    """Set multiple defaults at once"""
    for k, v in defaults.items():
        dct.setdefault(k, v)
    
def logging_defaults():
    return _LOGGING_DEFAULTS

def init_logging(log_file: str = None, log_dir: str = None, suffix: str = None,
                 name: str = None, **kws) -> str:
    """Inits logging config and file, with custom defaults (see description)
    
    Keyword arguments:
        log_file:   str, default None
                Name of log file, if provided. Else, will use log_dir, 
                project_name (or script name), and suffix to make new log file
        log_dir:    str, default None
                directory to place new log file
        suffix:     str, default current time
                suffix for log file
        name: str, default this script name
                Name as file root name for new log file
        
        **kws: passed to logging.basicConfig, with the following defaults:
            filemode:   str, default 'w+'
            format:     str, default "[ %(asctime)s %(name)s - %(funcName)12s():%(lineno)s ] %(message)s"
            datefmt:    str, default '%d-%b-%y %H:%M:%S'
            level:      str or logging Level, default INFO
            
            Call utils.logging_defaults() to see defaults
    
    Return:  str, log file path
    """
    
    if log_file is None:
        assert log_dir is not None, "No LOG_FILE or LOG_DIR provided"
        suffix = default(suffix, now(time=True), null='')
        log_file = os.path.join(
            log_dir,  f"{default(name, '', f'{name}-')}{suffix}.log")
        
    makedirs(os.path.dirname(log_file), exists_ok=True)

    # for LOGGING_DEFAULTS
    setdefaults(kws, _LOGGING_DEFAULTS)
    logging.basicConfig(filename=log_file, **kws)
    logging.info("Project name: %s", name)
    logging.info("Log filepath: %s", os.path.abspath(log_file))

    print(f"Log at {log_file}.", flush=True)
    return log_file
