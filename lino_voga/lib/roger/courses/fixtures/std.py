# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from lino.api import dd, rt, _

def objects():

    ContentType = rt.models.contenttypes.ContentType
    ExcerptType = rt.models.excerpts.ExcerptType
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

