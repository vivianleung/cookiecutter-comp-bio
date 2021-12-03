from setuptools import find_packages, setup

{% set license_names = {
    "MIT": "MIT License",
    "Apache 2.0": "Apache License 2.0",
    "BSD 3-Clause": "BSD 3-Clause \"New\" or \"Revised\" License",
    "GPL-3.0": "GNU General Public License v3.0"
} %}

setup(
    name='{{ cookiecutter.repo_pkg_name }}',
    author='{{ cookiecutter.full_name }}',
    author_email='{{ cookiecutter.email }}',
    project_name='{{ cookiecutter.project_name }}',
    description='{{ cookiecutter.description }}',
    version='{{ cookiecutter.version }}',
    include_package_data=True,
    packages=find_packages(include=['{{ cookiecutter.repo_pkg_name }}', '{{ cookiecutter.repo_pkg_name }}.*']),
{%- if cookiecutter.license in license_names -%}
    license="{{ license_names[cookiecutter.license.strip()] }}",
{% endif %}
{%- if cookiecutter.github_username -%}
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}',
{% endif %}
)
