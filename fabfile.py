from atelier.fablib import *
setup_from_fabfile(globals(), 'lino_faggio')

add_demo_project('lino_faggio/projects/docs')
add_demo_project('lino_faggio/projects/roger')
add_demo_project('lino_faggio/projects/edmund')

env.tolerate_sphinx_warnings = False
env.languages = 'en de fr et'.split()
env.revision_control_system = 'git'
