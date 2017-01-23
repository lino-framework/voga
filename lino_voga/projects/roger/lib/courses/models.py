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

"""
Adds some specific fields for managing the member fee.

"""

from __future__ import unicode_literals
from __future__ import print_function

from django.db.models import Q

from lino.api import dd, rt, _


from lino.modlib.plausibility.choicelists import Checker

from lino_voga.lib.courses.models import *


class Sections(dd.ChoiceList):
    verbose_name = _("Section")
    verbose_name_plural = _("Sections")

add = Sections.add_item

names = """Eupen Nidrum Walhorn Herresbach Eynatten Kelmis Hergenrath
Hauset Elsenborn Weywertz"""

for i, name in enumerate(names.split()):
    add(name.lower(), name, name.lower())
# add("01", "Eupen", "eupen")
# add("02", "Nidrum", "nidrum")
# add("03", "Walhorn", "walhorn")
add("etc", "Sonstige", "etc")


class Pupil(Pupil):
    """The Roger variant of Lino Voga adds a few very specific fields
    which are being used for filtering, and they may influence the
    price of an enrolment.

    .. attribute:: legacy_id
    .. attribute:: section
    .. attribute:: is_lfv
    .. attribute:: is_ckk
    .. attribute:: is_raviva
    .. attribute:: member_until

    """
    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Pupil')
        verbose_name = _("Participant")
        verbose_name_plural = _('Participants')

    legacy_id = models.CharField(
        _("Legacy ID"), max_length=12, blank=True)

    section = Sections.field(blank=True)

    is_lfv = models.BooleanField(_("LFV"), default=False)
    is_ckk = models.BooleanField(_("CKK"), default=False)
    is_raviva = models.BooleanField(_("Raviva"), default=False)
    is_member = models.BooleanField(_("Member"), default=False)
    member_until = models.DateField(_("Mitglied bis"), blank=True, null=True)

    def get_enrolment_info(self):
        """Return a short text to be displayed between parentheses
        in `lino_xl.lib.courses.ui.EnrolmentsByCourse.pupil_info`.
        """
        s = ""
        if self.member_until is None:
            pass
        elif self.member_until >= dd.demo_date():
            s = "E"
        if self.is_ckk:
            s += "C"
        if self.is_lfv:
            s += "L"
        # if self.is_raviva:
        #     s += "R"
        if self.section:
            s += "S"
            # s += " {0}".format(self.section)
        if s:
            return "M{0}".format(s)
        return "N"

    @classmethod
    def get_parameter_fields(cls, **fields):
        fields.update(
            show_members=dd.YesNo.field(
                _("Members"), blank=True,
                help_text=_(
                    "Show those whose 'Member until' is after today.")),
            show_ckk=dd.YesNo.field(_("CKK"), blank=True),
            show_lfv=dd.YesNo.field(_("LFV"), blank=True),
            show_raviva=dd.YesNo.field(_("Raviva"), blank=True))

        return super(Pupil, cls).get_parameter_fields(**fields)

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(Pupil, cls).get_request_queryset(ar)
        pv = ar.param_values
        if pv.show_members == dd.YesNo.no:
            qs = qs.filter(
                Q(member_until__isnull=True) | Q(member_until__lt=dd.today()))
        elif pv.show_members == dd.YesNo.yes:
            qs = qs.filter(Q(member_until__gte=dd.today()))
        for k in ('ckk', 'raviva', 'lfv'):
            v = pv['show_' + k]
            if v:
                qs = qs.filter(**{'is_' + k: v == dd.YesNo.yes})
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Pupil, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.show_members:
            yield "{0}:{1}".format(_("Members"), pv.show_members)
        if pv.show_ckk:
            yield "{0}:{1}".format(_("CKK"), pv.show_ckk)


class Line(Line):
    # this is here just because is_abstract_model() does not yet work
    # as expected: if you subclass a plugin which extends a given
    # model then you must also extend all other models in your plugin.

    class Meta(Line.Meta):
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Line')


class MemberChecker(Checker):
    """Check membership payments.

    If :attr:`force_cleared_until
    <lino_cosi.lib.ledger.Plugin.force_cleared_until>` is set, then
    :attr:`member_until` dates before that date are tolerated.

    """
    verbose_name = _("Check membership payments")
    model = Pupil
    messages = dict(
        no_payment=_("Member until {0}, but no payment."),
        wrong_until=_("Member until {0} (expected {1})."),
    )

    def get_plausibility_problems(self, obj, fix=False):
        qs = rt.models.ledger.Movement.objects.filter(
            partner=obj,
            account__ref=dd.plugins.courses.membership_fee_account)
        qs = qs.order_by('-value_date')
        until = obj.member_until
        fcu = dd.plugins.ledger.force_cleared_until
        if qs.count() == 0:
            if until:
                if fcu and until > fcu:
                    return
                yield (False, self.messages['no_payment'].format(until))
            return
        
        def expected_until(mvt):
            pd = mvt.value_date
            if pd.month > 8:
                return pd.replace(year=pd.year+1, month=12, day=31)
            return pd.replace(month=12, day=31)

        eu = expected_until(qs[0])
        if until != eu:
            msg = self.messages['wrong_until'].format(until, eu)
            if until is None or until < eu:
                if fix:
                    obj.member_until = eu
                    obj.full_clean()
                    obj.save()
                else:
                    yield (True, msg)
            else:
                yield (False, msg)


MemberChecker.activate()

from lino_cosi.lib.ledger.utils import on_ledger_movement


@dd.receiver(on_ledger_movement)
def check_member_until(sender=None, instance=None, **kwargs):
    MemberChecker.self.get_plausibility_problems(instance, fix=True)
