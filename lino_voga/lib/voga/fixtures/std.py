# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from lino.utils.instantiator import Instantiator

from lino.api import dd, rt


def excerpt_types():

    etype = Instantiator('excerpts.ExcerptType',
                         # build_method='appypdf',
                         email_template='Default.eml.html').build

    yield etype(
        build_method='appypdf',
        template='Confirmation.odt',
        backward_compat=True,
        content_type=ContentType.objects.get_for_model(
            rt.modules.courses.Enrolment),
        **dd.str2kw('name', _("Confirmation")))

    yield etype(
        build_method='appypdf',
        template='Certificate.odt',
        backward_compat=True,
        content_type=ContentType.objects.get_for_model(
            rt.modules.courses.Enrolment),
        **dd.str2kw('name', _("Certificate")))


def objects():

    # mailType = Instantiator('notes.NoteType').build

    # yield mailType(**dd.str2kw('name', _("Enrolment")))
    # yield mailType(**dd.str2kw('name', _("Timetable")))
    # yield mailType(**dd.str2kw('name', _("Letter")))

    yield excerpt_types()
