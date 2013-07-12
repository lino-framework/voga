from lino_faggio.settings import *
SITE = Site(globals(),title="Lino-Faggio demo",is_demo_site=True) 
# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'

