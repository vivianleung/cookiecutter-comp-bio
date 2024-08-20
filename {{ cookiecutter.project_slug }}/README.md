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
└── PROJECT\_NAME
    ├── about.txt
    ├── bin            <-- Shell scripts
    │   └── .gitkeep
    ├── config         <-- Rosters, input params, etc.
    │   └── .gitkeep
    ├── data           <-- Raw and intermediate data files
    │   └── .gitkeep
    ├── docs           <-- Notes and other docs
    │   └── .gitkeep
    ├── .gitignore
    ├── logs           <-- PBS job logs
    │   └── .gitkeep
    ├── pbs            <-- PBS scripts
    │   └── .gitkeep
    ├── scripts        <-- Structured Python scripts
    │   └── .gitkeep
    ├── snippets.py    <-- Miscellaneous and ad-hoc python snippets
    └── snippets.sh    <-- Miscellaneous and ad-hoc shell snippets


--------
<p><small>Cookiecutter project created from vivianleung/cookiecutter-comp-bio</small></p>

<!-- <p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p> -->
