#!/usr/bin/env bash

# mkproject.sh
#
# generate data directory for a new project
# 
# Usage: init_subproject.sh [-h|--help] [-d ROOT_DIR] [-g <0,1>] [-j] [-p PARAMS_YAML] SUBPROJECT
#
# Vivian Leung
# Created 01 Dec 2021
# Updated 01 Dec 2021
#

USAGE="""
Generate directory structure for a new sub project.

Usage: init_subproject.sh [-h|--help] [-d ROOT_DIR] [-g <0,1>] SUBPROJECT

Arguments:
  SUBPROJECT <str>  Name of project (used as main dir)

Optional:
  -d    <str>  Generate project dir structure in ROOT DIR. Default './'
  -g    <0,1>  Init directories with .gitkeep. 0: yes; 1: no. Default 0
  -j           Add jobs/ directory (for HPCs)
  -h           Display usage message and exit.
  --help       Display usage and generated structure, and exit.
"""
  # -p    YAML   YAML file containing overall params, i.e. user's name, email,
  #                 to fall back on. Default ../config/project_params.yaml

DATA_STRUCTURE="""
Structure
---------
(ROOT_DIR)
  └── SUBPROJECT/
      ├── about.txt       <-- Metadata and description of project
      ├── data            <-- Your data
      │ ├── external/         <-- Third-party data
      │ ├── raw/              <-- Original/basic data dump
      │ ├── interim/          <-- Transformed data 
      │ ├── processed/        <-- Final data ready for analysis or modelling
      │ └── jobs/         <-- Job submission scripts and logs (if -j)
      └── analysis/        <-- Generated analysis in documents and figures
          └── figures/        <-- Exported figures
          └── tables/         <-- Exported tables
"""
declare root_dir parent_dir subproject  # params_yaml
declare -i init_git=0

declare -a child_dirs=(
  "external"
  "raw"
  "interim"
  "processed"
  "analysis/figures"
  "analysis/tables"
)

[[ -z "$1" ]] && { printf "%s" "${USAGE}" && exit 0 ; }

while [[ -n "$1" ]] ; do
  case "$1" in
    -h)      printf "%s\n" "${USAGE}" && exit 0 ;;
    --help)  printf "%s\n" "${USAGE}" "${DATA_STRUCTURE}" && exit 0 ;;
    -d)      root_dir="$2" && shift ;;
    -g)      init_git=$2 && shift ;;
    -j)      child_dirs+=("jobs") ;;
    # -p)      params_yaml="$2" && shift ;;
    *)       [[ -z "${subproject}" ]] && subproject="$1" \
                || { echo "Too many arguments" && exit 1 ; } ;;
  esac
  shift
done

# make directories

parent_dir="${root_dir:-.}/${subproject}"


# make directories
for d in "${child_dirs[@]}" ; do mkdir -p "${parent_dir}/$d" ; done

if (( ${init_git} == 0 )) ; then
  touch "${parent_dir}/.gitkeep"
  for d in "${child_dirs[@]}" ; do touch "${parent_dir}/$d/.gitkeep" ; done
fi



if [[ -n "$(which git)" ]] ; then
  default_user_name="$(git config --get user.name)"
  default_user_email="$(git config --get user.email)"
  echo -n "Your name: [${default_user_name}] " ; read -r user_name
  echo -n "Email: [${default_user_email}] " ; read -r user_email

else
  default_user_name=""
  default_user_email=""
  echo -n "Your name: [${default_user_name:-Press ENTER to skip}] " ; read -r user_name
  echo -n "Email: [${default_user_email:-Press ENTER to skip}] " ; read -r user_email
fi

echo -n "Description: [Press Enter to skip] " ; read -r description

cat <<ABOUT >"${parent_dir}/about.txt"
# ${project}

${user_name:=${default_user_name}}
${user_email:=${default_user_email}}

Created:      $(date +'%d %h %Y')
Last updated: $(date +'%d %h %Y')

${description}

ABOUT

echo "Finished making subproject dir: ${parent_dir}"

