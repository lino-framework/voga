from .demo import *
SITE = Site(globals(), title="Lino Voga (:memory:)")
DATABASES['default']['NAME'] = ':memory:'
