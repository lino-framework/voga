# Copyright 2013-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
The :xfile:`models.py` for the :mod:`lino_voga` app.
"""

from lino.api import dd

from lino_xl.lib.courses import workflows


# if False:
#     # 20131025 fails because MergeAction.__init__ tries to use _lino_ddh
#     # which hasn't yet been installed

#     @dd.when_prepared('contacts.Person', 'contacts.Company')
#     def add_merge_action(model):
#         model.define_action(merge_row=dd.MergeAction(model))

# else:

#     @dd.receiver(dd.pre_analyze)
#     def add_merge_action(sender, **kw):
#         apps = sender.modules
#         # for m in (apps.contacts.Person, apps.contacts.Company):
#         for m in (apps.courses.Pupil, apps.contacts.Company):
#             m.define_action(merge_row=dd.MergeAction(m))


# def site_setup(site):

#     site.actors.system.SiteConfigs.set_detail_layout(
#         """
#         site_company next_partner_id:10
#         default_build_method simulate_today
#         clients_account   sales_account
#         suppliers_account purchases_account
#         site_calendar default_event_type pupil_guestrole
#         max_auto_events hide_events_before
#         """)

