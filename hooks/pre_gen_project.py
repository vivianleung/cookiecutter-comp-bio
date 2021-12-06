# #!/usr/bin/env python

# from cookiecutter.main import cookiecutter
# # from jinja2 import environment
# # import re
# import os
# import sys




# # initials = [ '{{ cookiecutter.full_name }}'.replace('-',' ').split()]

# # print(os.listdir(os.path.abspath(os.path.dirname(__file__))))
# # print(os.getcwd())
# # print("os.path.abspath(os.path.dirname(__file__))", os.path.abspath(os.path.dirname(__file__)))
# # print("os.path.abspath('.')", os.path.abspath('.'))

# # print(vars())
# # print(os.environ)
# # print(sys.argv)

# # # print("ENV VARS", *[f"{k}: {v}" for k, v in os.environ.items()], sep='\n')
# # # print("COOKIECUTTER", *[f"{k}: {v}" for k, v in vars(cookiecutter).items()], sep='\n')

# # try:
# #     cookiecutter(
# #         "cookiecutter-comp-bio/",
# #         # os.path.abspath(os.path.dirname(__file__)),
# #         extra_context={
# #             'name_initials': ''.join([s[0].upper() for s in initials])}
# #     )

# # except:
# #     sys.exit(1)




# # MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

# # module_name = '{{ cookiecutter.project_slug }}'

# # if not re.match(MODULE_REGEX, module_name):
# #     print('ERROR: The project slug (%s) is not a valid Python module name. Please do not use a - and use _ instead' % module_name)

# #     #Exit to cancel project
# #     sys.exit(1)


