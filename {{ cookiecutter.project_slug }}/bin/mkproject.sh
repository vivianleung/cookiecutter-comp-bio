#!/usr/bin/env bash

# mkproject.sh
#
# generate data directory for a new project
# 
# Usage: mkproject.sh [-h|--help] PROJECT_NAME [ROOT_DIR]
#
# By: Vivian Leung (vivianleung19@gmail.com)
# Created 01 Dec 2021
# Updated 12 Jul 2022
#

USAGE="""
Generate data directory for a new project.

Usage: mkproject.sh [-h|--help] [-d ROOT_DIR] [-s] [PROJECT_NAME]

Arguments:
  PROJECT_NAME <str>  Name of project (used as main dir)

Optional:
  -d    <str>  Generate project dir structure in ROOT DIR. Default './'
  -s           Set up Snakemake directories and files [NOTE: NOT IN USE]
  -h|--help    Display help message and exit.
"""

DATA_STRUCTURE="""
Structure
---------
(ROOT_DIR)
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

"""
  # (NOT IN USE)
  #     └── workflow/         <-- Snakemake workflow (see Snakemake docs)
  #         ├── envs/
  #         ├── rules/
  #         │   └── common.smk
  #         ├── schemas/
  #         │   └── config.schema.yaml
  #         ├── scripts/
  #         │   └── __init__.py
  #         ├── report/
  #         └── Snakefile

declare root_dir proj_dir project mk_smk

while [[ -n "$1" ]] ; do
  case "$1" in
    -h)      printf "%s\n" "${USAGE}" && exit 0 ;;
    --help)  printf "%s\n" "${USAGE}" "${DATA_STRUCTURE}" && exit 0 ;;
    -d)      root_dir="$2" && shift ;;
    -s)      mk_smk=0 ;;
    *)       [[ -z "${project}" ]] && project="$1" \
                || { echo "Too many arguments" && exit 1 ; } ;;
  esac
  shift
done

# get general project input configs
if [[ -n "$(which git)" ]] ; then
  default_user_name="$(git config --get user.name)"
  default_user_email="$(git config --get user.email)"
fi

if [[ -z "${project}" ]] ; then
  echo -n "Project name (required): "
  read -r project
fi

echo -n "Your name: [${default_user_name:-Press ENTER to skip}] "
read -r user_name

echo -n "Email: [${default_user_email:-Press ENTER to skip}] "
read -r user_email

echo -n "Description: [Press Enter to skip] "
read -r description

# get snakemake configs 
# if [[ "${mk_smk}" = 0 ]] ; then
#   if [[ -n "$(which snakemake)" ]] ; then 
#     default_smk_version="$(snakemake --version)"
#     # default_smk_version="$(snakemake --version | sed -E 's/^([0-9]+\.[0-9]+).*$/\1/')"
#   else
#     echo "Snakemake: Note: no snakemake installed!"
#   echo -n "Snakemake: min version: [${default_smk_version:-None}]) "
#   read -r smk_version
# fi


# ####  Do stuff  ####
proj_dir="${root_dir:-.}/${project}"


# ####  Make directories  ####

# general dirs
mkdir -pv "${proj_dir}/"{analysis,config/rosters,exports/figures,exports/tables,jobs,logs,notes,resources,scripts}

# touch "${proj_dir}"/{data,jobs}/.gitkeep

cat <<GITIGNORE | tee "${proj_dir}/data/.gitignore" > "${proj_dir}/jobs/.gitignore"
*
*/
!.gitignore
!.gitkeep

GITIGNORE


cat <<-SNIPPETS_SH > "${proj_dir}/snippets.sh"
#!/usr/bin/env bash

# ${project}/snippets.sh

# Miscellaneous and ad-hoc snippets

# ${user_name}
# Created:      $(date +'%d %b %Y')
# Last updated: $(date +'%d %b %Y')

##########################

# purpose
# $(date +'%d %b %Y')

PROJECT_DIR="${proj_dir}"

##########################

SNIPPETS_SH

cat <<-SNIPPETS_PY > "${proj_dir}/snippets.py"
#!/usr/bin/env python3

# ${project}/snippets.py

# Miscellaneous and ad-hoc snippets

# ${user_name}
# Created:      $(date +'%d %b %Y')
# Last updated: $(date +'%d %b %Y')

##########################

# purpose
# $(date +'%d %b %Y')

PROJECT_DIR="${proj_dir}"

##########################

SNIPPETS_PY


# # set up Snakemake stuff
# if [[ "${mk_smk}" = 0 ]] ; then  

#   workflow_dir="${proj_dir}/workflow/"
#   # make Snakemake files and folders
#   mkdir -p "${workflow_dir}/"{envs,rules,schemas,scripts,report}

#   touch "${workflow_dir}/scripts/__init__.py"

#   touch "${proj_dir}/config/config.yaml"

#   "workflow/rules/common.smk"
#   "workflow/schemas/config.schema.yaml"
#   "workflow/Snakefile"


# # make config/config.yaml
# cat <<CONFIG_YAML >"${proj_dir}/config/config.yaml"
# # config.yaml

# # TODO

# # TODO
# params:
#   MYPARAM: ""

# CONFIG_YAML

# # make workflow/rules/common.smk
# cat <<COMMON_SMK >"${proj_dir}/workflow/rules/common.smk"
# # common.smk

# from snakemake.utils import validate

# validate(config, schema="../schemas/config.schema.yaml")

# ####  Functions  ####

# COMMON_SMK

# # make workflow/schemas/config.schema.yaml
# cat <<CONFIG_SCHEMA_YAML >"${proj_dir}/workflow/schemas/config.schema.yaml"
# # config.schema.yaml
# $schema: "http://json-schema.org/draft-06/schema#"

# description: "snakemake config file"

# type: object

# # TODO
# properties:
#   PROP1:
#     type: string
  

# # TODO
# required:
#   - PROP1

# CONFIG_SCHEMA_YAML


# # make workflow/Snakefile
# cat <<SNAKEFILE >"${proj_dir}/workflow/Snakefile"

# import pandas as pd
# from snakemake.utils import min_version

# $([[ -z "${smk_version:-${default_smk_version}}"]] && echo "# ")min_version("${smk_version:-${default_smk_version}}")

# configfile: "config/config.yaml"

# #####  load rules  #####

# include: "rules/common.smk"

# #####  target rule  #####

# # TODO
# rule all:
#     input:
#         ""

# SNAKEFILE


# make ./about.txt
cat <<-ABOUT_TXT >"${proj_dir}/about.txt"
# ${project}/about.txt

${user_name:=${default_user_name}}
${user_email:=${default_user_email}}

Created:      $(date +'%d %b %Y')
Last updated: $(date +'%d %b %Y')

${description}

ABOUT_TXT








echo "Finished making project dir: ${proj_dir}"

# end of script
