from lino_voga.projects.docs.settings import *

SITE = Site(globals(), is_demo_site=True)  #, use_java=False)

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
