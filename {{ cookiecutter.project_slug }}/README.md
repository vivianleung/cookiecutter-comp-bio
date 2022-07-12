{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}

__{{cookiecutter.full_name}}__

Created:      {% now 'utc', '%d %b %Y' %}

Last updated: {% now 'utc', '%d %b %Y' %}

{% set full_name_list = cookiecutter.full_name.split(' ') %}


Project Organization
------------

    ├── .gitignore
    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── bin/               <- Shell scripts and other executables
    │   └── mkproject.sh   <- generate data directory for a new project
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── environment.yaml         <- virtual env specs (bare requirements called with conda)
    ├── environment_mamba.yaml   <- virtual env specs (called with mamba)
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │   │                     the creator's initials, and a short `-` delimited description, e.g.
    │   │                     `01_00-{{ cookiecutter.initials }}-initial-data-exploration`.
    │   └── 00_01-{{ cookiecutter.initials }}-dummy.py      <- Template
    │
{%- if cookiecutter.hpc == 'Slurm' -%}
    ├── slurm/                  <-- Job submission scripts
    │   └── _template.sh
{%- elif cookiecutter.hpc == 'Torque' -%}
    ├── pbs/                    <-- Job submission scripts
    │   └── _template.pbs{% endif %}
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    │
    ├── scripts/           <- General Python and other scripts
    │
    ├── src                <- Source code for use in this project.
    │   └── __init__.py    <- Makes src a Python module
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


For project directories
-----------------------
projects/

  └── PROJECT_NAME/
      ├── about.txt     <-- Metadata and description of project
      │
      ├── analysis/     <-- Analyzed data that can be used to make figures
      │
      ├── config/       <-- Config files
      │   └── rosters/  <-- Roster tables used as input for jobs
      │
      ├── data/         <-- Raw/intermediate files
      │   ├── .gitignore
      │   └── .../
      │
      ├── exports/      <-- Finished figures and tables exported from analysis
      │   ├── figures/  <-- figures
      │   └── tables/   <-- formatted tables
      │
      ├── logs/         <-- Job log files
      │
      ├── notes/        <-- Notes written by user
      │
      ├── resources/    <-- (meta)data or supplementary/accessory external info 
      │
      ├── jobs/         <-- Parent directory for running jobs
      │   ├── .gitignore
      │   └── JOB_NAME-DATE-JID/
      │
      ├── scripts/      <-- ad-hoc scripts used in this particular project
      │
      ├── snippets.py
      └── snippets.sh

--------
<p><small>Cookiecutter project created from vivianleung/cookiecutter-comp-bio</small></p>

<!-- <p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p> -->
