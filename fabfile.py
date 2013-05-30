from atelier.fablib import *
setup_from_project('lino_faggio')

#~ env.demo_database = 'lino_welfare.demo.settings'

env.demo_databases.append('lino_faggio.settings.demo')
#~ env.django_databases.append('userdocs')
#~ env.tolerate_sphinx_warnings = True

env.languages = 'de fr'.split()
