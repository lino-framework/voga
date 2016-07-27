# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
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

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from lino.utils.instantiator import Instantiator

from lino.api import dd, rt


def excerpt_types():

    etype = Instantiator('excerpts.ExcerptType').build
    # email_template='Default.eml.html').build

    yield etype(
        build_method='appypdf',
        template='Confirmation.odt',
        backward_compat=True,
        content_type=ContentType.objects.get_for_model(
            rt.models.courses.Enrolment),
        **dd.str2kw('name', _("Confirmation")))

    yield etype(
        build_method='appypdf',
        template='Certificate.odt',
        backward_compat=True,
        content_type=ContentType.objects.get_for_model(
            rt.models.courses.Enrolment),
        **dd.str2kw('name', _("Certificate")))

    yield etype(
        build_method='appypdf',
        template='Default.odt',
        body_template='payment_list.body.html',
        certifying=True,
        content_type=ContentType.objects.get_for_model(
            rt.models.courses.Course),
        **dd.str2kw('name', _("Payment list")))


def objects():

    # mailType = Instantiator('notes.NoteType').build

    # yield mailType(**dd.str2kw('name', _("Enrolment")))
    # yield mailType(**dd.str2kw('name', _("Timetable")))
    # yield mailType(**dd.str2kw('name', _("Letter")))

    yield excerpt_types()
