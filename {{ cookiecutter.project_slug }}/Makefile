.PHONY hpc_cluster_dir example_subproject create_env rm_smk mk_repo_pkg_dir
# check_pkg_name

###############################################################################
# GLOBALS                                                                     #
###############################################################################

# PROJECT_DIR := "$(shell $(realpath ./{{ cookiecutter.project_slug }})"
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME := {{ cookiecutter.project_slug }}
PYTHON_INTERPRETER := {{ cookiecutter.python_interpreter }}
REPO_PKG_NAME = {{ cookiecutter.repo_pkg_name }}

ifeq ('',PYTHON_VERSION)
	PYTHON_VERSION = 2.7
endif

ifeq (,$(shell which conda))
	HAS_CONDA=False
else
	HAS_CONDA=True
endif


define select_python_version
	sed -E '^python//'
endef 



###############################################################################
# COMMANDS                                                                    #
###############################################################################

# ## Install Python Dependencies
# requirements: test_environment
# 	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
# 	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

# do :
#     @echo "What is your age?: "; \
#     read AGE; \
#     echo "Your age is ", $$(AGE)

define check_pkg_name
	test_env_name=_foo
	while [[ "$(conda env list | grep -E '^$(test_env_name)\s+')" != "" ]] ; do \
		test_env_name=$(test_env_name)_ ; \
	done

	ifneq $(,$(shell $(1) env create -d -n __foo__ -f $(2) | grep -E '::$(REPO_PKG_NAME)='))
		@echo ">>> Repo package name $(2) exists in environment! Revert to name 'src'? [Y/n]" / 
			read -r do_revert ; ifeq(n,$$(do_revert)) @echo "Cancelling" && exit 1 \
			else @echo "src"
	else
		@echo "$(1)"
	endif

endef

create_env:
	ifneq (Do not create,{{ cookiecutter.create_env }})
		ifeq (True,$(HAS_CONDA))
			@echo ">>> Detected conda, creating conda environment."
			env_arg = ""
			ifeq (./venv,{{ cookiecutter.create_env }})
				env_arg = $(PROJECT_DIR)/{{ cookiecutter.create_env }}
			else
				env_arg = {{ cookie.create_env }}
			endif

			REPO_PKG_NAME = $(call check_pkg_name conda '${PROJECT_DIR}/environment.yml')
			
			ifeq (y,{{ cookiecutter.init_snakemake }})
				REPO_PKG_NAME = $(call check_pkg_name mamba '${PROJECT_DIR}/environment_mamba.yml')
			endif

			conda env create $(env_arg) -f '$(PROJECT_DIR)/environment.yml'
			
			ifeq (y,{{ cookiecutter.init_snakemake }})
				mamba env update $(env_arg) -f '$(PROJECT_DIR)/environment_mamba.yml'
			endif
			@echo ">>> New conda env created. Activate with:\nconda activate {{ cookiecutter.create_env }}"
		else
			@echo ">>> No conda detected. Please install requirements manually."
		endif
	endif

mk_repo_pkg_dir:
	$(shell mkdir "$(PROJECT_DIR)/$(REPO_PKG_NAME)")


hpc_cluster_dir:

	hpc_template_dir := $(PROJECT_DIR)/bin/hpc_templates/
	ifeq (Slurm,{{ cookiecutter.hpc_cluster }})
		cp -p $(hpc_template_dir)/template_slurm.sh $(PROJECT_DIR)/bin/template_slurm.pbs
	else ifeq (Torque,{{ cookiecutter.hpc_cluster }})	
		cp -p $(hpc_template_dir)/template.pbs $(PROJECT_DIR)/bin/template.pbs
	else ifeq (Torque-D24H,{{ cookiecutter.hpc_cluster }}) 
		cp -p $(hpc_template_dir)/template_d24h.pbs $(PROJECT_DIR)/bin/template.pbs
	endif
	rm -r $(hpc_template_dir)



example_subproject:
	$(shell $(PROJECT_DIR)/bin/init_subproject.sh -d '$(PROJECT_DIR)/subprojects/' my_subproject)




rm_smk:
	ifneq (y,{{ cookiecutter.init_snakemake }})
		rm -r $(PROJECT_DIR)/config/config.smk.yaml $(PROJECT_DIR)/workflow/ $(PROJECT_DIR)/Snakefile $(PROJECT_DIR)/environment_mamba.yml
	endif

