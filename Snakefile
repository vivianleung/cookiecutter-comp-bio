configfile: config/config.smk.yaml

include: workflow/rules/common.smk

rule all:
    get_input,
    