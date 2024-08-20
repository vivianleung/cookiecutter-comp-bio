{% raw %}#!/usr/bin/env bash

# mkproject.sh
#
# Generates project directory for a new project
# 
# Usage: mkproject.sh [-h|--help] [-d DIRPATH] PROJECT_NAME

# Vivian Leung (vivianleung19@gmail.com) 2022

set -e

declare project_dir project_name

declare USAGE="""
Generates project directory for a new project

Usage: mkproject.sh [-h|--help] [-d DIRPATH] PROJECT_NAME

ARGUMENTS:
  PROJECT_NAME  Name of project. Used in auto-generated files and naming 
                project directory (if -d not provided)

Optional:
  -d  DIRPATH   Init contents in this directory. Default ./<PROJECT_NAME>.
  -h|--help     Display short|long help message and exit.

2022 Vivian Leung
"""

declare DESCRIPTION="""Structure
---------
PROJECT_DIR
   ├── .gitignore
   ├── about.txt
   ├── bin            <-- Shell scripts
   │   └── .gitkeep
   ├── config         <-- Rosters, input params, etc.
   │   └── .gitkeep
   ├── data           <-- Raw and intermediate data files
   │   └── .gitkeep
   ├── docs           <-- Notes and other docs
   │   └── .gitkeep
   ├── logs           <-- Running jobs
   │   └── .gitkeep
   ├── logs           <-- PBS job logs
   │   └── .gitkeep
   ├── pbs            <-- PBS scripts
   │   └── .gitkeep
   ├── scripts        <-- Structured Python scripts
   │   └── .gitkeep
   ├── snippets.py    <-- Miscellaneous and ad-hoc python snippets
   └── snippets.sh    <-- Miscellaneous and ad-hoc shell snippets
"""

while [[ -n "$1" ]] ; do
  case "$1" in
    -h)     printf '%s\n' "${USAGE}" && exit 0 ;;
    --help) printf '%s\n' "${USAGE}" "${DESCRIPTION}" && exit 0 ;;
    -d)     project_dir="$2" && shift ;;
    *)      [[ -z "${project_name}" ]] && project_name="$1" \
              || { echo "Extra argument \'$1\' given." && exit 1 ; } ;;
  esac
  shift
done


declare default_user_name default_user_email

# get general project input configs
if [[ -n "$(which git)" ]] ; then
  default_user_name="$(git config --get user.name)"
  default_user_email="$(git config --get user.email)"
fi

if [[ -z "${project_name}" ]] ; then
  echo -n "Project name (required): "
  read -r project_name
fi

echo -n "Your name: [${default_user_name:-Press ENTER to skip}] "
read -r user_name

echo -n "Email: [${default_user_email:-Press ENTER to skip}] "
read -r user_email

echo -n "Description: [Press Enter to skip] "
read -r description

echo -n "Python version: [PYTHON3|python] "
read -r python_version

[[ -z "${project_dir}" ]] && project_dir="./${project_name}"

# Make directories
for d in 'bin' 'config' 'data' 'docs' 'jobs' 'logs' 'pbs' 'scripts' ; do
  echo "$d" && mkdir -p "${project_dir}/$d"
  echo "$d/.gitkeep" && touch "${project_dir}/$d/.gitkeep"
done

echo "about.txt"
# make about.txt
cat <<-ABOUT_TXT >"${project_dir}/about.txt"
	# about.txt

	Project: ${project_name}
  
	${user_name:=${default_user_name}}
	${user_email:=${default_user_email}}
	
	Created:      $(date +'%d %b %Y')
	Last updated: $(date +'%d %b %Y')
	
	${description}
	
ABOUT_TXT

# make snippets.py
echo "snippets.py"
cat <<-SNIPPETS_PY > "${project_dir}/snippets.py"
	#!/usr/bin/env ${python_version}
	
	# snippets.py
	
	# ${project_name} project miscellaneous and ad-hoc snippets
	
	# ${user_name:=${default_user_name}}
	# ${user_email:=${default_user_email}}
	
	# Created:      $(date +'%d %b %Y')
	# Last updated: $(date +'%d %b %Y')
	
	##########################
	
	import os
	
	import pandas as pd
	
	##########################
	
	# Purpose
	# $(date +'%d %b %Y')
	
	PROJECT_DIR = "${project_dir}"
	
	##########################

SNIPPETS_PY

# make snippets.sh
echo "snippets.sh"
cat <<-SNIPPETS_SH > "${project_dir}/snippets.sh"
	#!/usr/bin/env bash
	
	# snippets.sh
	
	# ${project_name} project miscellaneous and ad-hoc snippets
	
	# ${user_name:=${default_user_name}}
	# ${user_email:=${default_user_email}}
	
	# Created:      $(date +'%d %b %Y')
	# Last updated: $(date +'%d %b %Y')
	
	##########################
	
	# Purpose
	# $(date +'%d %b %Y')
	
	PROJECT_DIR="${project_dir}"
	
	##########################

SNIPPETS_SH

# make .gitignore
echo ".gitignore"
cat <<-GITIGNORE > "${project_dir}/.gitignore"
# .gitignore for project ${project_name}
data/**
jobs/**

!.gitkeep

GITIGNORE

cat <<-EPILOGUE
	Done.
	Project directory: ${project_dir}
EPILOGUE

{% endraw %}
# end of script
