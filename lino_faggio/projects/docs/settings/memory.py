from ..settings import *
SITE = Site(globals(), title="Lino Faggio (:memory:)")
DATABASES['default']['NAME'] = ':memory:'
