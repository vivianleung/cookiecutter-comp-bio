from snakemake.utils import validate


validate(config, "../schemas/config.schema.yaml")

def get_input(wildcards):
    inputs = []
    return inputs

