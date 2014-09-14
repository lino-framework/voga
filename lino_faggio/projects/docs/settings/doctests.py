from ..settings import *
SITE = Site(globals(), no_local=True, remote_user_header='REMOTE_USER')
SITE.appy_params.update(raiseOnError=True)
DEBUG = True
