from lino_voga.projects.docs.settings import *


class Site(Site):

    use_java = False
    is_demo_site = True


SITE = Site(globals())

DEBUG = True

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'

APPEND_SLASH = True
