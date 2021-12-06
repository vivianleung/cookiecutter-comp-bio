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

Usage: init_subproject.sh [-h|--help] [-d ROOT_DIR] [-g <0,1>] 
    [-j [<pbs|pbs_d24h|slurm>]] [-c CONFIG_FILE] SUBPROJECT

Arguments:
  SUBPROJECT <str>  Name of project (used as main dir)

Optional:
  -d  ROOT_DIR      Generate project dir structure in ROOT DIR. Default './'
  -c  CONFIG_FILE   Config file for params. Default PROJECT_DIR/config/project_config.sh
  -g  <0,1>         Init directories with .gitkeep. 0: yes; 1: no. Default 0
  -j  [<pbs|pbs_d24h|slurm>]   Add jobs/ directory (for HPCs). Default uses HPC_TYPE in CONFIG_FILE
  -h                Display usage message and exit.
  --help            Display usage and generated structure, and exit.
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
      │     ├── .gitkeep        <-- Final data ready for analysis or modelling
      │     └──  
      └── analysis/       <-- Generated analysis in documents and figures
          └── figures/        <-- Exported figures
          └── tables/         <-- Exported tables
"""
declare root_dir main_dir subproject hpc  # params_yaml
declare -i gitkeep=0

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
    -j)      child_dirs+=("jobs") && hpc="$2" && shift ;;
    # -p)      params_yaml="$2" && shift ;;
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

get_cfg_value () {
  grep -E "^$1=" $2 | head -n 1 | sed -E "s/^$1=(.*)$/\1/ ; s/(^['\"]|['\"]$)//g"
}

if (( ${gitkeep:=$(get_cfg_value "${GITKEEP}")} == 0 )) ; then
  touch "${main_dir}/.gitkeep"
  for d in "${child_dirs[@]}" ; do touch "${main_dir}/$d/.gitkeep" ; done
fi


# "s/^(#SBATCH|#PBS) (-J |--job-name=|-N ).+$/\1 \2${subproject}/1"


cp_template () {
  # Usage: cp_template NAME TEMPLATE_FPATH DEST_FPATH 
  # Accepts only default directive prefixed, i.e. #SBATCH or #PBS
  if [[ -f "$2" ]] ; then
    sed -E "s/^(#SBATCH|#PBS) (-J |--job-name=|-N ).+$/\1 \2$1/1" $2 > "$3"
  else
    echo "Skipping job template as file not found: $2" 
  fi
}

# PBS -N <NAME>

case "${hpc}" in
  pbs)      cp_template "${subproject}" "hpc_templates/template.pbs" \
              "${main_dir}/jobs/template.pbs" ;;
  pbs_d24h) cp_template "${subproject}" "hpc_templates/template_d24h.pbs" \
              "${main_dir}/jobs/template.pbs" ;;
  slurm)    cp_template "${subproject}" "hpc_templates/template_slurm.sh" \
              "${main_dir}/jobs/template.sh"
  *) echo "Unrecognized HPC type. Continuing without template." ;;
esac


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

cat <<ABOUT >"${main_dir}/about.txt"
# ${project}

${user_name:=${default_user_name}}
${user_email:=${default_user_email}}

Created:      $(date +'%d %h %Y')
Last updated: $(date +'%d %h %Y')

${description}

ABOUT

echo "Finished making subproject dir: ${main_dir}"

