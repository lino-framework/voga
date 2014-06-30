from ..settings.demo import *
SITE = Site(globals(),  # no_local=True,
            remote_user_header='REMOTE_USER',
            hidden_languages='de fr')
SITE.appy_params.update(raiseOnError=True)
#~ hidden_languages is for tested docs
# DEBUG = True
