# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Rumma & Ko Ltd
# This file is part of Lino Voga.
#
# Lino Voga is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Voga is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Voga.  If not, see
# <http://www.gnu.org/licenses/>.

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

