# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The main module of :ref:`voga`.

.. autosummary::
   :toctree:

    lib
    projects

"""

import os

execfile(os.path.join(os.path.dirname(__file__), 'setup_info.py'))
__version__ = SETUP_INFO['version']

intersphinx_urls = dict(docs="http://voga.lino-framework.org")
srcref_url = 'https://github.com/lsaffre/lino-voga/blob/master/%s'
