#!/bin/bash

#SBATCH -J JOB_NAME
#SBATCH -o=slurm-%J.o
#SBATCH -e=slurm-%J.e


#### TODO: CHANGE AS NECESSARY ###
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=16G
#SBATCH --time=06:00:00
#SBATCH --qos=6hours

#SBATCH --array=1-409%20

{%- if cookiecutter.email != '' -%}
#SBATCH --mail-type=END,FAIL,TIME_LIMIT
#SBATCH --mail-user={{ cookiecutter.email }}
{% endif %}

#### TODO: CHANGE AS NECESSARY
COMMAND
