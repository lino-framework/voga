# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
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

from __future__ import unicode_literals

from lino.api import dd, rt, _


def objects():

    ContentType = rt.modules.contenttypes.ContentType
    ExcerptType = rt.modules.excerpts.ExcerptType
    Course = rt.models.courses.Course

    yield ExcerptType(
        template='presence_sheet.wk.html',
        primary=True,
        build_method='wkhtmltopdf',
        content_type=ContentType.objects.get_for_model(Course),
        **dd.str2kw('name', _("Presence sheet")))

    yield ExcerptType(
        template='overview.wk.html',
        build_method='wkhtmltopdf',
        content_type=ContentType.objects.get_for_model(Course),
        **dd.str2kw('name', _("Overview")))

