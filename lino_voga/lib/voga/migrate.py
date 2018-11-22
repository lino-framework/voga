# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Rumma & Ko Ltd
# This file is part of the Lino Voga project.
# Lino Voga is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino Voga is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino Voga; if not, see <http://www.gnu.org/licenses/>.

"""This defines the :class:`Migrator` class

is a real-world example of how the application developer
can provide automatic data migrations for :ref:`dpy`.
"""

import logging
logger = logging.getLogger(__name__)
from django.conf import settings

from lino.core.utils import resolve_model
from lino.api import dd, rt

from lino.utils.dpy import Migrator, override


class Migrator(Migrator):
    """
    This class is used because a :ref:`voga` Site has
    :attr:`ad.Site.migration_class` set to
    ``"lino_voga.migrate.Migrator"``.

    """
    def migrate_from_0_0_1(self, globals_dict):
        """
        - Renamed `countries.City` to `countries.Place`
        - removed field imode from contacts.Partner
        - renamed sales.PaymentTerm to vat.PaymentTerm
        """
        countries_Place = resolve_model("countries.Place")
        globals_dict.update(countries_City=countries_Place)

        globals_dict.update(
            sales_PaymentTerm=resolve_model("vat.PaymentTerm"))

        contacts_Partner = resolve_model("contacts.Partner")
        def create_contacts_partner(id, country_id, city_id, region_id, zip_code, name, addr1, street_prefix, street, street_no, street_box, addr2, language, email, url, phone, gsm, fax, remarks, invoicing_address_id, payment_term_id, vat_regime, imode_id):
            kw = dict()
            kw.update(id=id)
            kw.update(country_id=country_id)
            kw.update(city_id=city_id)
            kw.update(region_id=region_id)
            kw.update(zip_code=zip_code)
            kw.update(name=name)
            kw.update(addr1=addr1)
            kw.update(street_prefix=street_prefix)
            kw.update(street=street)
            kw.update(street_no=street_no)
            kw.update(street_box=street_box)
            kw.update(addr2=addr2)
            kw.update(language=language)
            kw.update(email=email)
            kw.update(url=url)
            kw.update(phone=phone)
            kw.update(gsm=gsm)
            kw.update(fax=fax)
            kw.update(remarks=remarks)
            kw.update(invoicing_address_id=invoicing_address_id)
            kw.update(payment_term_id=payment_term_id)
            kw.update(vat_regime=vat_regime)
            # kw.update(imode_id=imode_id)
            return contacts_Partner(**kw)
        globals_dict.update(create_contacts_partner=create_contacts_partner)

        return '0.0.2'

    def migrate_from_0_0_2(self, globals_dict):
        """\
- removed field `cal.Event.course`
        """
        return '0.0.3'

    def migrate_from_0_0_3(self, globals_dict):
        """
- `cal.EventType` : remove fields `build_method` and `template`
- `cal.Event` : remove field `course`
- `notes.NoteType` : remove field `body_template`
- `contacts.Partner` : rename field `invoicing_address` to `invoice_recipient`
- `system.SiteConfig` : remove field `farest_future`
- `system.TextFieldTemplate` : remove field `team`

        """
        bv2kw = globals_dict['bv2kw']
        new_content_type_id = globals_dict['new_content_type_id']
        cal_EventType = resolve_model("cal.EventType")
        def create_cal_eventtype(id, name, seqno, build_method, template, attach_to_email, email_template, description, is_appointment, all_rooms, locks_user, start_date, event_label):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            kw.update(seqno=seqno)
            # kw.update(build_method=build_method)
            # kw.update(template=template)
            kw.update(attach_to_email=attach_to_email)
            kw.update(email_template=email_template)
            kw.update(description=description)
            kw.update(is_appointment=is_appointment)
            kw.update(all_rooms=all_rooms)
            kw.update(locks_user=locks_user)
            kw.update(start_date=start_date)
            if event_label is not None: kw.update(bv2kw('event_label',event_label))
            return cal_EventType(**kw)
        globals_dict.update(create_cal_eventtype=create_cal_eventtype)

        notes_NoteType = resolve_model("notes.NoteType")
        def create_notes_notetype(id, name, build_method, template, attach_to_email, email_template, important, remark, body_template):
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            kw.update(build_method=build_method)
            kw.update(template=template)
            kw.update(attach_to_email=attach_to_email)
            kw.update(email_template=email_template)
            kw.update(important=important)
            kw.update(remark=remark)
            # kw.update(body_template=body_template)
            return notes_NoteType(**kw)
        globals_dict.update(create_notes_notetype=create_notes_notetype)


        contacts_Partner = resolve_model("contacts.Partner")
        def create_contacts_partner(id, country_id, city_id, region_id, zip_code, addr1, street_prefix, street, street_no, street_box, addr2, name, language, email, url, phone, gsm, fax, remarks, vat_regime, payment_term_id, invoicing_address_id):
            kw = dict()
            kw.update(id=id)
            kw.update(country_id=country_id)
            kw.update(city_id=city_id)
            kw.update(region_id=region_id)
            kw.update(zip_code=zip_code)
            kw.update(addr1=addr1)
            kw.update(street_prefix=street_prefix)
            kw.update(street=street)
            kw.update(street_no=street_no)
            kw.update(street_box=street_box)
            kw.update(addr2=addr2)
            kw.update(name=name)
            kw.update(language=language)
            kw.update(email=email)
            kw.update(url=url)
            kw.update(phone=phone)
            kw.update(gsm=gsm)
            kw.update(fax=fax)
            kw.update(remarks=remarks)
            kw.update(vat_regime=vat_regime)
            kw.update(payment_term_id=payment_term_id)
            kw.update(invoice_recipient_id=invoicing_address_id)
            return contacts_Partner(**kw)
        globals_dict.update(create_contacts_partner=create_contacts_partner)

        system_SiteConfig = resolve_model('system.SiteConfig')
        def create_system_siteconfig(id, default_build_method, next_partner_id, site_company_id, default_event_type_id, site_calendar_id, max_auto_events, farest_future, pupil_guestrole_id, system_note_type_id, clients_account_id, sales_vat_account_id, sales_account_id, suppliers_account_id, purchases_vat_account_id, purchases_account_id):
            kw = dict()
            kw.update(id=id)
            kw.update(default_build_method=default_build_method)
            kw.update(next_partner_id=next_partner_id)
            kw.update(site_company_id=site_company_id)
            kw.update(default_event_type_id=default_event_type_id)
            kw.update(site_calendar_id=site_calendar_id)
            kw.update(max_auto_events=max_auto_events)
            # kw.update(farest_future=farest_future)
            kw.update(pupil_guestrole_id=pupil_guestrole_id)
            kw.update(system_note_type_id=system_note_type_id)
            kw.update(clients_account_id=clients_account_id)
            kw.update(sales_vat_account_id=sales_vat_account_id)
            kw.update(sales_account_id=sales_account_id)
            kw.update(suppliers_account_id=suppliers_account_id)
            kw.update(purchases_vat_account_id=purchases_vat_account_id)
            kw.update(purchases_account_id=purchases_account_id)
            return system_SiteConfig(**kw)
        globals_dict.update(create_system_siteconfig=create_system_siteconfig)

        cal_Event = resolve_model('cal.Event')
        def create_cal_event(id, owner_type_id, owner_id, user_id, created, modified, build_time, build_method, start_date, start_time, end_date, end_time, summary, description, access_class, sequence, auto_type, event_type_id, transparent, room_id, priority_id, state, assigned_to_id, course_id):
            kw = dict()
            kw.update(id=id)
            owner_type_id = new_content_type_id(owner_type_id)
            kw.update(owner_type_id=owner_type_id)
            kw.update(owner_id=owner_id)
            kw.update(user_id=user_id)
            kw.update(created=created)
            kw.update(modified=modified)
            kw.update(build_time=build_time)
            kw.update(build_method=build_method)
            kw.update(start_date=start_date)
            kw.update(start_time=start_time)
            kw.update(end_date=end_date)
            kw.update(end_time=end_time)
            kw.update(summary=summary)
            kw.update(description=description)
            kw.update(access_class=access_class)
            kw.update(sequence=sequence)
            kw.update(auto_type=auto_type)
            kw.update(event_type_id=event_type_id)
            kw.update(transparent=transparent)
            kw.update(room_id=room_id)
            kw.update(priority_id=priority_id)
            kw.update(state=state)
            kw.update(assigned_to_id=assigned_to_id)
            # kw.update(course_id=course_id)
            return cal_Event(**kw)
        globals_dict.update(create_cal_event=create_cal_event)

        system_TextFieldTemplate = resolve_model('system.TextFieldTemplate')
        def create_system_textfieldtemplate(id, user_id, name, description, team_id, text):
            kw = dict()
            kw.update(id=id)
            kw.update(user_id=user_id)
            kw.update(name=name)
            kw.update(description=description)
            # kw.update(team_id=team_id)
            kw.update(text=text)
            return system_TextFieldTemplate(**kw)
        globals_dict.update(create_system_textfieldtemplate=create_system_textfieldtemplate)


        return '0.0.4'

    def migrate_from_0_0_4(self, globals_dict):
        """
        - removed field User.notifyme_mode
        
        """

        # bv2kw = globals_dict['bv2kw']
        # new_content_type_id = globals_dict['new_content_type_id']
        # cal_EventType = resolve_model("cal.EventType")
        users.User = resolve_model("users.User")
        
        @override(globals_dict)
        def create_users_user(id, modified, created, username, password, user_type, initials, first_name, last_name, email, remarks, language, partner_id, access_class, event_type_id, notifyme_mode):
            if user_type: user_type = settings.SITE.models.users.UserTypes.get_by_value(profile)
            if access_class: access_class = settings.SITE.models.cal.AccessClasses.get_by_value(access_class)
            kw = dict()
            kw.update(id=id)
            kw.update(modified=modified)
            kw.update(created=created)
            kw.update(username=username)
            kw.update(password=password)
            kw.update(user_type=user_type)
            kw.update(initials=initials)
            kw.update(first_name=first_name)
            kw.update(last_name=last_name)
            kw.update(email=email)
            kw.update(remarks=remarks)
            kw.update(language=language)
            kw.update(partner_id=partner_id)
            kw.update(access_class=access_class)
            kw.update(event_type_id=event_type_id)
            # kw.update(notifyme_mode=notifyme_mode)
            return users.User(**kw)
        
        return '2016.12.0'
    
