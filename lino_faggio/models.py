# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` for the :mod:`lino_faggio` app.
"""

from django.db import models
from django.db.models import loading
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat


from lino.api import dd

#~ print 20130607, loading.cache.postponed

from lino.modlib.courses import workflows



if False:
    # 20131025 fails because MergeAction.__init__ tries to use _lino_ddh
    # which hasn't yet been installed

    @dd.when_prepared('contacts.Person', 'contacts.Company')
    def add_merge_action(model):
        model.define_action(merge_row=dd.MergeAction(model))

else:

    @dd.receiver(dd.pre_analyze)
    def add_merge_action(sender, **kw):
        apps = sender.modules
        for m in (apps.contacts.Person, apps.contacts.Company):
            m.define_action(merge_row=dd.MergeAction(m))


def site_setup(site):
    site.modules.accounts.Accounts.set_detail_layout(
        """
        ref:10 name id:5
        seqno chart group type clearable
        ledger.MovementsByAccount
        """)

    site.modules.system.SiteConfigs.set_detail_layout(
        """
        site_company next_partner_id:10
        default_build_method
        clients_account   sales_account     sales_vat_account
        suppliers_account purchases_account purchases_vat_account
        pupil_guestrole
        max_auto_events default_event_type site_calendar
        """)
