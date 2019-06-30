# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""

Loads :mod:`lino_voga.lib.roger.courses.management.commands.eiche2lino`


"""
import os
from django.conf import settings
from lino_voga.lib.roger.courses.management.commands.eiche2lino \
    import MyBook2016


def objects():

    p = settings.SITE.legacy_data_path or settings.SITE.project_dir
    # book = MyBook(os.path.join(p, "Eiche 2013.xls"))
    book = MyBook2016(os.path.join(p, "Eiche2016.xls"))
    yield book.objects()

