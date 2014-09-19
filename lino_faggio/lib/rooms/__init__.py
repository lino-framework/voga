# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.modlib.rooms import Plugin


class Plugin(Plugin):

    extends_models = ['Booking']
