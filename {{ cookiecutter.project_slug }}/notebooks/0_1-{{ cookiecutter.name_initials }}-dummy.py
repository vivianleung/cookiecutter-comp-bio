#!/usr/bin/env python

# 0_1-{{ cookiecutter.name_initials }}-dummy.py

# This is a dummy template that does dumb stuff. [MAIN DESCRIPTION]

# Input:
#   Files:
#       - some file (output from another script/notebook)
#   Params:
#       Required: out_dir
#       Optional: suffix, default DATE-TIME, e.g. 2021-09-20-1610

# Output (files):
#   - Gibberish in format .txt
#       "foo-{suffix}.txt"

# {{ cookiecutter.full_name }}
# Created: {%- now 'utc' '%d %j %Y' -%} 
# 
# NOTE: ex. ("this script does not work or is deprecated",
#            "this script is complete/has been tested", caveats, etc.
#            )

#%%
# #####  IMPORTS  #####

# built-ins
import os
from typing import Annotated, Any, Union # see Python doc on 'typing' module

# third-party
# import pandas as pd

# custom (i.e. from {{ cookiecutter.repo_pkg_name }}/)
# from {{ cookiecutter.repo_pkg_name }} import modules

#%%
# #####  USER PARAMS  #####  (for notebooks)

OUT_DIR = '../subprojects/my_subproject/data/raw'
SUFFIX = None             # default DATE (e.g. 2021-09-20-1610)

#%%
# #####  FUNCTIONS  #####

# Helpers
def helper_foo(x: str) -> Union[str, Annotated[bool, False]]:
    """Tries to convert x to lowercase, else returns False"""
    try:
        return x.lower()
    except AttributeError:
        return False
    except:
        raise


# Core functions
def main_foo(*values: Any, n: int = 5) -> list:
    """Returns list of lowercase (string) values, each repeated n times
    
    Arguments:
        Required:
            *values: Any. Values to be repeated
        Optional:
            n: int, default 5. Repeat value this number of times.
    
    Returns:
        list of length n of string-type values. See helper_foo(x) doc.
    """
    assert len(values) > 0, "No values provided."
    converted = [helper_foo(v) for v in values]
    
    lst = []  # output list
    for val in filter(lambda x: x != False, converted):
        lst.extend([val for _ in range(n)])
    
    return lst

#%%
# #####  SCRIPT  #####

# check/set defaults for inputs
assert OUT_DIR is not None, "No OUT_DIR provided!"

out_dir = OUT_DIR
suffix = default(SUFFIX, now(time=True))


#%%
# actually do things

res_1 = main_foo('a', 'b')
res_2 = main_foo('a', 1, 'b', n=5)

try:
    res_3 = main_foo()
except AssertionError:
    res_3 = None
except:
    raise
    
    
#%%
# ## SAVE FILES

# make output dir
if not os.path.exists(out_dir):
    print("Making dir", out_dir)
    os.makedirs(out_dir, exist_ok=True)

# or simply
os.makedirs(out_dir, exist_ok=True)

# write file
out_fname = "foo.txt"
with open(os.path.join(out_dir, out_fname), 'w') as fout:
    lines = [strjoin(*x) for x in [res_1, res_2, res_3] if x is not None]    
    fout.write('\n'.join(lines))

# confirm (if you like to be verbose)
print(f'Files saved to dir: "{out_dir}"',
      '- Gibberish lines as txt', f'   "{out_fname}"',
      sep='\n')


#%%

# for scripts in src/
# if __name__ == '__main__':
#    run(*args, **kwargs)