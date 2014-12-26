from atelier.fablib import *
setup_from_fabfile(globals(), 'lino_faggio')

add_demo_database('lino_faggio.projects.docs.settings.demo')
add_demo_database('lino_faggio.projects.roger.settings.demo')
add_demo_database('lino_faggio.projects.edmund.settings.demo')

env.tolerate_sphinx_warnings = False
env.languages = 'en de fr et'.split()
env.revision_control_system = 'git'
