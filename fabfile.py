from atelier.fablib import *
setup_from_project('lino_faggio', 'lino_faggio.projects.docs.settings.demo')

env.demo_databases.append('lino_faggio.projects.roger.settings.demo')
env.demo_databases.append('lino_faggio.projects.edmund.settings.demo')
#~ env.django_databases.append('userdocs')
env.tolerate_sphinx_warnings = False

#~ env.languages = 'en de fr'.split()
env.use_mercurial = False
