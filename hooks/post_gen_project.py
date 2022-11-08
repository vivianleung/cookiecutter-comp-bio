# #!/usr/bin/env python

# post_gen_project.py

from typing import NoReturn
import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
{% raw %}
PBS_TEMPLATE = """#!/usr/bin/env bash

# _template.pbs

# TODO (template) << PURPOSE >>

# By Vivian Leung (vivianleung19@gmail.com)
# Created:       14 Jun 2022
# Last updated:  30 Jun 2022

# Todo
### Job name
### Queue name (qaussian): stdq1, medq1, fatq1 or gpuq1
### Wall time required (between 00:00:01 to 336:00:00).
### Number of CPUs: ppn: up to 40 for stdq1, 48 for gpuq1, 64 for medq1 and fatq1
### Memory: up to 750gb for stdq1, 1000gb for medq1 and gpuq1, 3000gb for fatq1
#__PBS -N <<#TODO>>
#__PBS -q stdq1
#__PBS -l walltime=150:00:00 
#__PBS -l select=1:ncpus=40:mem=750gb

#PBS -N dry_run-<<#TODO>>
#PBS -q quickq1
#PBS -l walltime=0:05:00
#PBS -l select=1:ncpus=1


## Generally fixed settings
#PBS -M {% endraw %}{{ cookiecutter.hpc_mail_name }}{% raw %}
#PBS -v CONDA_PREFIX,MODULEPATH

### Declare job non-rerunable
#PBS -r n
#PBS -k oed


#######
set -o nounset
set -o errtrace

declare -i start_time=${SECONDS}
declare DRY_RUN= TEST_RUN=

# todo: indicate DRY_RUN or TEST_RUN
DRY_RUN='y'
# TEST_RUN='y'

# NOTE: get_mem_info MUST BE DECLARED BEFORE METASPADES_PARAMS! (in GB)
# NOTE: use with caution if not using all cpus
get_mem_info() {
  case "${PBS_QUEUE}" in
    stdq1|quickq1) echo 750 ;;
    medq1|gpuq1) echo 1500 ;;
    fatq) echo 3000 ;;
    *)
      local -i memfree=$(grep "MemFree:" /proc/meminfo \\\
                         | sed -E 's/^MemFree:\\s+([0-9]+)\\s+kB$/\\1/')
      echo $(( memfree / 10**6-1 * 3 / 4 ))
      ;;
  esac
}

############ SPECS AND PARAMS ############

# common/universal
declare PROJECT_DIR ROSTER OUT_DIR CONDA_ENV=
declare -i MAX_FAILS START_ROW END_ROW
declare -a MODULES=() OUT_DIRS_TO_MAKE=()

# todo: project directory
PROJECT_DIR={% endraw %}'{{ cookiecutter.project_slug }}'{% raw %}

# todo: input roster
# TODO (template): roster input description, e.g TSV of ACCESSION [OTHER ARGS..]
ROSTER="${PROJECT_DIR}/config/rosters/roster.tsv"

# Job output dir
OUT_DIR="${PROJECT_DIR}/${PBS_JOBNAME}-$(date +'%Y-%m-%d')-${PBS_JOBID%%.*}"

# todo: start/end rows
# START_ROW=7
# END_ROW=8

# CONDA_ENV=''
MODULES=()
MAX_FAILS=3

# Autogen sub-dirs
# TODO (template) << SUB-DIRS >>

# TODO (template)
OUT_DIRS_TO_MAKE=("${OUT_DIR}")

# #####  Params  #####
#TODO (template): << PARAMS >>
declare MIN_CONTIG_LENGTH=1500

declare -a PARAMS=(
  "--minContig ${MIN_CONTIG_LENGTH}"  # min contig len allowed
  "--numThreads ${OMP_NUM_THREADS}"
  "--unbinned"
  "--seed 42"
)


############ UTILS AND FUNCTIONS  ############

# TODO (template) << OUT PATHS >>
# File naming conventions
# Usage: path_bins_dirpath ACCESSION
path_outpath () { echo "${OUT_DIR}/$1/metabat2/$1" ; }

# ############ >>>>>>>>>>  STANDARD/FIXED STUFF  >>>>>>>> ############
declare tmpdir=
declare -i n_entries= n_entries_in_roster= retcode= i=0
declare -a passed=() failed=() remaining=()

# Usage: join_by SEP VAL [...]. From https://stackoverflow.com/a/17841619
join_by () {
  local d=${1-} f="${2-}" ; if shift 2 ; then printf '%s' "$f" "${@/#/$d}" ; fi
}

is_dry_run () { [[ "${DRY_RUN:-n}" =~ ^y|Y$ ]] && return 0 || return 1 ; }

printf_eval_cmd () { 
  join_by ' ' '$' "$@" && printf '\\n'
  if is_dry_run ; then return 0 ; else eval "$@" ; return $? ; fi
}

# Usage: check_passed_failed RETCODE NAME
check_passed_failed () {
  if [[ $1 -eq 0 ]] ; then
    passed+=("$2")
    return 0
  else
    failed+=("$2 (exit code: $1)")
    if [ ! -f "${failed_log}" ] ; then
      cat <<-FAILED_RUNS > "${failed_log}"
				FAILED RUNS
				==================
				Job ID:       ${JID}
				Script:       $(basename "$0")
				Script path:  $0
				
				Failed:
			FAILED_RUNS
    fi
    printf "\\n>> [$2] STOPPING: ERROR: exit status %s\\n" $1 | tee -a /dev/stderr
    printf '> %s (exit code: %s)\\n' "$2" "$1" >> "${failed_log}"
  fi
}
# USAGE printf_list HEADER LIST
printf_list () { printf '\\n%s\\n' "$1" ; shift ; printf "> %s\\n" "$@" ; }

# Trap
epilogue () {
  
  if [ ${retcode} -ne 0 ] ; then
    printf '\\n\n>>>>> REACHED MAX FAILS! Exited with status %d <<<<<\\n' \\
      ${retcode} | tee -a /dev/stderr
  fi

  [ -n "${tmpdir}" ] && rm -rf "${tmpdir}"

  cat <<-EPILOGUE_STDOUT

		------------------------------
		Processed ${i} of $n_entries entries, with
		  ${#passed[@]} passed 
		  ${#failed[@]} failed
		  ${#remaining[@]} remaining (not processed)
		  $([[ -n ${START_ROW:-} || -n ${END_ROW:-} ]] && echo "Start row: ${START_ROW:-}; end row: ${END_ROW:-}")
	EPILOGUE_STDOUT
  
  [ ${#failed[@]} -gt 0 ] && printf_list "Failed:" "${failed[@]}"
	[ ${#remaining[@]} -gt 0 ] && printf_list "Entries not processed:" \\\
    "${remaining[@]}" | tee -a "${failed_log}"
	
  cat <<-EPILOGUE_TIME | tee -a /dev/stderr

		Duration: $(date -u -d @"$((${SECONDS}-${start_time}))" +'%-Hh %-Mmin %-Ssec')
		Job Finish Time is $(date +'%c')
	EPILOGUE_TIME
}

trap epilogue EXIT

############  STUFF FOR PBS  ############

declare PATH NPROCS NNODES NCORES JID failed_log roster

PATH=$PBS_O_PATH
cd $PBS_O_WORKDIR

# Define number of processors
NPROCS=$(wc -l < $PBS_NODEFILE)
NNODES=$(uniq $PBS_NODEFILE | wc -l)
NCORES=$((NPROCS / NNODES))
JID="${PBS_JOBID%%.*}"

# Save this pbs job script to jobs dir
cp "$0" "${PBS_O_WORKDIR}/${PBS_JOBNAME}-${JID}.pbs"

# fpath for list of failed runs
failed_log="${PBS_O_WORKDIR}/${PBS_JOBNAME}-${JID}-failed.txt"


# #######  Prep environment  #####
module load anaconda3
if [[ -n "${CONDA_ENV:-}" ]] ; then
  set +o nounset
  set +o errtrace
  source activate "${CONDA_ENV}"
  set -o nounset
  set -o errtrace
fi
for mod in "${MODULES[@]}" ; do module load "${mod}" ; done

# Check input files
[[ -f "${ROSTER}" ]] || { echo "File does not exist: ${ROSTER}" >&2 && exit 1 ; }

# count up entries
n_entries_in_roster=$(grep -cvxE "^\\s*$" "${ROSTER}")

# make a blank-line-free copy of roster
roster="${PBS_O_WORKDIR}/${PBS_JOBNAME}-$(basename "${ROSTER%.*}")-roster-${JID}.${ROSTER##*.}"

head -n ${END_ROW:-${n_entries_in_roster}} "${ROSTER}" | tail -n $(( ${END_ROW:-${n_entries_in_roster}}-${START_ROW:-1}+1 )) \\
  | grep -vE "^\\s*$" > "${roster}"


n_entries=$(wc -l "${roster}" | cut -d ' ' -f1)

cat <<-STANDARD_PROLOGUE
	================  ${PBS_JOBNAME} : Job ID : ${JID}  ================
	${NNODES} nodes.
	${NPROCS} CPUs allocated: $(cat $PBS_NODEFILE)
	${OMP_NUM_THREADS} threads.
	This PBS script is running on host $(hostname)
	Working directory is ${PBS_O_WORKDIR}

	Date is $(date +'%c')

	Environment: ${CONDA_PREFIX}

	$(module list 2>&1)

	Dry run:  ${DRY_RUN:-N}
	Test run: ${TEST_RUN:-N}
STANDARD_PROLOGUE

# ########## <<<<<<<<<<  END OF STANDARD/FIXED STUFF  <<<<<<<< #########


####################  DO STUFF  ####################


# Report standard prologue
cat <<-PROLOGUE
	============== Programs in Use ==============
	
	<< #TODO (template): << PROGRAMS >>
	PROGRAM: $(PROGRAM -v)
	$(which PROGRAM)

	================  Input/Output  ================

	Input paths
	-------------------
	File list:              ${ROSTER}

	Number of entries (list):     ${n_entries_in_roster}
	Start row:                    ${START_ROW:-}
	End row:                      ${END_ROW:-}
	Number of entries to process: ${n_entries}

	Copy of roster (of entries to be processed): 
	${roster}

	Output directories
	-------------------
	Main data dir:         ${OUT_DIR}

	#TODO (template) << AUTOGEN SUBDIRS >>
	SUB_DIR:               ${SUB_DIR}
	
	============ Common Command Params ============
	
	#TODO (template): << PARAMS >>
	STEP: PROGRAM
	-----------------
	$(printf '%s\\n' "${PARAMS[@]}")

PROLOGUE


####################  CORE  ####################

#TODO: (template) << THE ACTUAL WORK >>
# Usage: process_entry ACCESSION [OTHER ARGS]
process_entry () {
  
  local outpath="$(path_outpath "$1")"

  printf_eval_cmd 'mkdir' '-pv' "$(dirname "${outpath}")"
  
  printf_eval_cmd 'echo' "$@"
                
  # needs to be this way or else will return 1 due to if
  if ! is_dry_run ; then return $? ; else return 0 ; fi
}


####################  EXECUTE  ####################

printf "============== EXECUTING..... ==============\\n"

if ! is_dry_run ; then
  mkdir -pv "${OUT_DIRS_TO_MAKE[@]}"
  tmpdir="$(mktemp -d -p ${OUT_DIR})"
else
  tmpdir="DRY_RUN_TMPDIR"
fi

# run through entries
i=0
declare -a args  # TODO (template) << ACCESSION [OTHER ARGS...] >>

while IFS=$'\\n' read -r line ; do

  IFS=$'\\t' read -d $'\\n' -r -a args <<<"${line}"

  if [ ${#failed[@]} -ge ${MAX_FAILS} ] ; then 
    remaining+=("${args[0]}")
  else
    i=$((i+1))
    printf '\\n[%s - %2d of %d] %s\\n' "$(date +'%Y-%m-%d %H:%M')" \\
      $i ${n_entries} "${args[0]}" | tee -a /dev/stderr
    (
      set -e
      set -o nounset
      set -o errtrace
      process_entry "${args[@]}"
    )
    retcode=$?
    check_passed_failed ${retcode} "${args[0]}"
    [[ "${TEST_RUN:-n}" =~ ^y|Y$ ]] && break
  fi
done < "${roster}"


# exit 0

# End of script
{% endraw %}
"""

SLURM_TEMPLATE = """{% raw %}#!/bin/bash

#SBATCH -J JOB_NAME
#SBATCH -o=slurm-%J.o
#SBATCH -e=slurm-%J.e


#### TODO: CHANGE AS NECESSARY ###
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=16G
#SBATCH --time=06:00:00
#SBATCH --qos=6hours

#SBATCH --array=1-409%20
{% endraw %}
{%- if cookiecutter.email != '' -%}
{% raw %}#SBATCH --mail-type=END,FAIL,TIME_LIMIT{% endraw %}
{% raw %}#SBATCH --mail-user={{ cookiecutter.email }}{% endraw %}
{% endif %}

#### TODO: CHANGE AS NECESSARY
COMMAND

"""
{% raw %}
GITIGNORE = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover

# Translations
*.mo
*.pot

# Django stuff:
*.log

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# DotEnv configuration
.env

# Database
*.db
*.rdb

# Pycharm
.idea

# VS Code
.vscode/

# Spyder
.spyproject/

# Jupyter NB Checkpoints
.ipynb_checkpoints/

# MS temp files
~$*.ppt*
~$*.doc*
~$*.xls*

# LaTeX temp files
*.acn
*.acr
*.alg
*.aux
*.bbl
*.bcf
*.blg
*.fdb_latexmk
*.fls
*.glg
*.glo
*.gls
*.idx
*.ind
*.ist
*.lof
*.log
*.lot
*.nav
*.out
*.run.xml
*.snm
*.synctex.gz
*.synctex.gz(busy)
*.synctex(busy)
*.toc
*.vrb
__latexindent_temp.tex

# exclude data from source control by default
/projects/**/data*/**
/projects/**/jobs/
!/projects/**/data*/**/  # keep dir struct

!*.log
!log
!*.py
!*.pbs
!*.[oej][0-9]*  # job logs
!*.job[0-9]*
# from kmergenie
# /projects/**/*.histo
# /projects/**/*.histo.pdf

# Mac OS-specific storage files
.DS_Store

# vim
*.swp
*.swo

# Mypy cache
.mypy_cache/

# virtual env
/venv/
/env/
/venv/**

!.gitkeep

/workflow/analysis
/workflow/analysis/*

/tmp/

.snakemake/

"""
{% endraw %}

###### FUNCTIONS AND DOING THINGS ######

def cp_hpc_template(hpc_name: str, template: str) -> NoReturn:
    hpc_dir = os.path.join(PROJECT_DIRECTORY, hpc_name)
    os.makedirs(hpc_dir)
    with open(os.path.join(hpc_dir, f"_template.{hpc_name}"), 'w') as fout:
        fout.write(template)
        
if __name__ == '__main__':
  
  with open(os.path.join(PROJECT_DIRECTORY, '.gitignore'), 'w') as fout:
    fout.write(GITIGNORE)
  
    if "{{ cookiecutter.hpc }}" == "Slurm":
        cp_hpc_template("slurm", SLURM_TEMPLATE)

    elif "{{ cookiecutter.hpc }}" == "Torque":
        cp_hpc_template("pbs", PBS_TEMPLATE)
    