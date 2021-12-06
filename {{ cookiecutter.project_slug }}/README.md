{{cookiecutter.project_name}}
==============================

{{cookiecutter.description}}

__{{cookiecutter.full_name}}__

Created: {% now 'utc' '%d %j %Y' %}
Last updated: {% now 'utc' '%d %j %Y' %}

{% set full_name_list = cookiecutter.full_name.split(' ') %}


Project Organization
------------
.
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
├── bin/                    <-- Shell scripts and other executables
│   └── init_subproject.sh  
├── config/                 <-- Config files
{%- if cookiecutter.init_snakemake == "y" -%}
│   └── config.smk.yaml     <-- Snakemake config YAML
{% endif %}
├── docs/
{%- if cookiecutter.hpc_cluster == 'Slurm' -%}
├── slurm/                  <-- Job submission scripts
│   └── slurm_template.sh
{%- elif cookiecutter.hpc_cluster in {'Torque', 'Torque-D24H'} -%}
├── pbs/                    <-- Job submission scripts
│   └── template.pbs
{% endif %}
├── notebooks/              <-- Jupyter notebooks
│   └── 0_1-{{ cookiecutter.name_initials }}-dummy.py  <-- example notebook
├── notes/                  <-- Miscellaneous notes and observations
├── references/             <-- Third-party references, guides, etc.
├── scripts/                <-- Ad-hoc scripts
│
│── {{\ cookiecutter.repo_pkg_name\ }}  <-- local Python package to import into notebooks and scripts
├── subprojects
│   ├── subprojects.txt
│   └── my_subproject       <-- Example subproject
│       ├── about.txt       <-- Metadata and description of project
│       ├── data            <-- Your data
│       │   ├── external/       <-- Third-party data
│       │   ├── raw/            <-- Original/basic data dump
│       │   ├── interim/        <-- Transformed data 
{%- if cookiecutter.hpc_cluster != 'None' -%}
│       │   ├── processed/      <-- Final data ready for analysis or modelling
│       │   └── jobs/           <-- Job submission scripts and logs
{% else %}
│       │   └── processed/      <-- Final data ready for analysis or modelling
{% endif %}
│       └── analysis/        <-- Generated analysis in documents and figures
│           └── figures/        <-- Exported figures
│           └── tables/         <-- Exported tables
{%- if cookiecutter.init_snakemake == "y" -%}
├── Snakefile               
├── workflow                <-- Snakemake workflow files
│   ├── README.md
│   ├── envs
│   ├── report
│   ├── resources
│   ├── rules
│   │   └── common.smk
│   └── schemas
│       └── common.schema.smk
{% endif %}
{%- if cookiecutter.create_env == './venv' -%}
├ venv/                     <-- virtual environment
{% endif %}
├── environment.yml
├── requirements.txt
└── setup.py

