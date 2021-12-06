#!/usr/bin/env bash

# mkproject.sh
#
# generate data directory for a new project
# 
# Vivian Leung
# Created 01 Dec 2021
# Updated 01 Dec 2021
#

USAGE="""
Generate directory structure for a new sub project.

Usage: init_subproject.sh [-h|--help] [-d ROOT_DIR] [-g <0,1>] [-j] [-c CONFIG_FILE] SUBPROJECT

Arguments:
  SUBPROJECT <str>  Name of project (used as main dir)

Optional:
  -d  ROOT_DIR         Generate project dir structure in ROOT DIR. Default './'
  -c  CONFIG_FILE      Config file for params. Default PROJECT_DIR/config/project_config.sh
  -g  <0,1>            Init directories with .gitkeep. 0: yes; 1: no. Default 0
  -j                   Add jobs/ directory (for HPCs). Default uses hpc_template* in bin/
  -h                   Display usage message and exit.
  --help               Display usage and generated structure, and exit.
"""
  # -p    YAML   YAML file containing overall params, i.e. user's name, email,
  #                 to fall back on. Default ../config/project_params.yaml
DATA_STRUCTURE="""
Structure
---------
(ROOT_DIR)
  └── SUBPROJECT/
      ├── .gitkeep 
      ├── about.txt       <-- Metadata and description of project
      ├── data            <-- Your data
      │ ├── .gitkeep    
      │ ├── external/         <-- Third-party data
      │ │   └── .gitkeep 
      │ ├── raw/              <-- Original/basic data dump
      │ │   └── .gitkeep 
      │ ├── interim/          <-- Transformed data 
      │ │   └── .gitkeep 
      │ ├── processed/        <-- Final data ready for analysis or modelling
      │ │   └── .gitkeep 
      │ └── jobs/         <-- Job submission scripts and logs (if -j)
      │     └── .gitkeep 
      └── analysis/       <-- Generated analysis in documents and figures
          └── figures/        <-- Exported figures
          └── tables/         <-- Exported tables
"""
declare root_dir main_dir subproject config_file job_template  # params_yaml
declare -i gitkeep=0 mk_jobs=1

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
    -c)      config_file="$2" && shift ;;
    -d)      root_dir="$2" && shift ;;
    -g)      init_git=$2 && shift ;;
    -j)      child_dirs+=("jobs") ;;
        # mk_jobs=0
        # [[ "$2" =~ ^[^-] && -n "$3" ]] && { job_template="$2" && shift ; }
        # ;;
    *)       [[ -z "${subproject}" ]] && subproject="$1" \
                || { echo "Too many arguments" && exit 1 ; } ;;
  esac
  shift
done

# make directories

main_dir="${root_dir:-.}/${subproject}"

mkdir -p "${main_dir}"

# make directories
for d in "${child_dirs[@]}" ; do mkdir -p "${main_dir}/$d" ; done

if (( ${gitkeep} == 0 )) ; then
  touch "${main_dir}/.gitkeep"
  for d in "${child_dirs[@]}" ; do touch "${main_dir}/$d/.gitkeep" ; done
fi

get_cfg_value () {
  # Usage get_cfg_value VARIABLE CONFIG_FILE
  grep -E "^$1=" $2 | head -n 1 | sed -E "s/^$1=(.*)$/\1/ ; s/(^['\"]|['\"]$)//g"
}

default_user_name="$(get_cfg_value USER_FULL_NAME ${config_file:=$(dirname "$0")/../config/project_config.sh})"
default_user_email="$(get_cfg_value USER_EMAIL ${config_file})"



echo -n "Your name: [${default_user_name:-Press ENTER to skip}] " ; read -r user_name
echo -n "Email: [${default_user_email:-Press ENTER to skip}] " ; read -r user_email
echo -n "Description: [Press Enter to skip] " ; read -r description

cat <<ABOUT >"${main_dir}/about.txt"
# ${subproject}

${user_name:=${default_user_name}}
${user_email:=${default_user_email}}

Created:      $(date +'%d %h %Y')
Last updated: $(date +'%d %h %Y')

${description}

ABOUT

echo "Finished making subproject dir: ${main_dir}"




# # find template
# find_templates () {
#   # Usage find_templates DIRNAME
#   local -a templates

#   case "${OSTYPE}" in
#     darwin*) templates=($(find -E "$1" -type f -regex '^.*/hpc_template.*')) ;;
#     *)       templates=($(find "$1" -type f -regextype posix-extended '^.*/hpc_template.*')) ;;
#   esac
#   if (( ${#templates[@]} == 0 )) ; then
#     echo "Warning: No template found."
#   elif (( ${#templates[@]} > 1 )) ; then
#     echo "Multiple templates found:"
#     awk '{ printf "[%d] %s\n" NR $0 ; }' <(printf '%s\n' "${templates[@]}")
#     echo "Select a template [1]: "
#     read -r which_template
#     job_template="${templates[${which_template:=1}]}"
#   else
#     job_template="${templates[1]}"
#   fi

# }

# if (( ${mk_jobs} == 0 )) ; then
#   if [[ -z "${job_template:=$(get_cfg_value HPC_TEMPLATE "${config_file}")}" ]] ; then
#     find_templates "$(dirname "$0"))"
#   fi
#   sed -E "s/^(#SBATCH|#PBS) (-J |--job-name=|-N ).+$/\1 \2${subproject}/1" "${job_template}" > "${main_dir}/jobs"

