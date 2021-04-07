# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from lino.utils.instantiator import Instantiator

from lino.api import dd, rt


def objects():

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
