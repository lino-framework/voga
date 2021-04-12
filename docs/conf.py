# -*- coding: utf-8 -*-

from lino.sphinxcontrib import configure; configure(globals())

# from atelier.sphinxconf import interproject
# interproject.configure(globals(), 'atelier lino_cosi')

extensions += ['lino.sphinxcontrib.logo']

html_context.update(public_url='https://voga.lino-framework.org')

project = 'Lino Voga'
copyright = '2012-2021 Rumma & Ko Ltd'
