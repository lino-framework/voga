from atelier.fablib import *
setup_from_fabfile(globals(), 'lino_voga')

add_demo_project('lino_voga.projects.docs.settings.demo')
add_demo_project('lino_voga.projects.roger.settings.demo')
add_demo_project('lino_voga.projects.edmund.settings.demo')

env.tolerate_sphinx_warnings = False
env.languages = 'en de fr et'.split()
env.revision_control_system = 'git'
env.cleanable_files = ['docs/api/lino_voga.*']
env.locale_dir = 'lino_voga/lib/voga/locale'
