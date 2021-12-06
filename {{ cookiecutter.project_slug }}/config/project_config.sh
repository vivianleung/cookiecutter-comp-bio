#!/usr/bin/env bash

# config/project_config.sh

# Config file for generating templates, etc


USER_FULL_NAME="{{ cookiecutter.full_name }}"
USER_EMAIL="{{ cookiecutter.email }}"
USER_GITHUB_USERNAME="{{ cookiecutter.github_username }}"
USER_INITIALS="{{ cookiecutter.initials }}"

PROJECT_NAME="{{ cookiecutter.project_name }}"
PROJECT_SLUG="{{ cookiecutter.project_slug }}"
HPC_TYPE="{{ cookiecutter.hpc_cluster }}"
