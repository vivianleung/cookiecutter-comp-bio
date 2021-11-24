{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}

__{{cookiecutter.full_name}}__

Project Organization
------------
.gitignore
LICENSE
MakeFile
README.md
environment.yml  <-- packages required for dev
<!-- requirements.txt -->
bin/    <- shell scripts and executables
data/
    external/
    raw/
    interim/
    processed/

venv/  <-- virtual environment for dev
notebooks/
notes/
resources/
requirements.txt  <-- requirements for reproducing analyses
scripts/  <-- miscellaneous scripts
setup.py  <-- make project (`src`) installable
src/  <-- useful scripts to import into notebooks
    __init__.py
config/  <-- config files for `snakemake`
workflow/  <-- for `snakemake`
    envs/
    reports/
    rules/
    schemas/
    Snakefile
references/