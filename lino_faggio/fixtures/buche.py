# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""

demo data specific for :ref:`faggio`.
"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


from lino.utils.instantiator import Instantiator, i2d
from lino.utils import Cycler
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from atelier.utils import date_offset
from lino.api import dd, rt

DEMO_REF_DATE = i2d(20140101)


cal = dd.resolve_app('cal')
courses = dd.resolve_app('courses')
rooms = dd.resolve_app('rooms')

Booking = dd.resolve_model('rooms.Booking')
Room = dd.resolve_model('cal.Room')
Event = dd.resolve_model('cal.Event')
Partner = dd.resolve_model('contacts.Partner')
Company = dd.resolve_model('contacts.Company')
Teacher = dd.resolve_model('courses.Teacher')
TeacherType = dd.resolve_model('courses.TeacherType')
Pupil = dd.resolve_model('courses.Pupil')
PupilType = dd.resolve_model('courses.PupilType')
Enrolment = dd.resolve_model('courses.Enrolment')
Course = dd.resolve_model('courses.Course')
Product = dd.resolve_model('products.Product')
CourseStates = courses.CourseStates
EnrolmentStates = courses.EnrolmentStates
BookingStates = rooms.BookingStates
Calendar = dd.resolve_model('cal.Calendar')


def demo_date(*args, **kw):
    return date_offset(DEMO_REF_DATE, *args, **kw)


class Loader1(object):

    def objects(self):

        yield PupilType(ref="M", name="Mitglied")
        yield PupilType(ref="H", name="Helfer")
        yield PupilType(ref="L", name="LFV")
        yield PupilType(ref="C", name="COK")
        #~ yield PupilType(ref="E",name="Extern")

        yield TeacherType(ref="S", **dd.str2kw('name', _("Independant")))
        yield TeacherType(ref="EP", **dd.babelkw('name', de="Ehrenamtlich pauschal", fr="Volontaire (forfait)", en="Voluntary (flat)"))
        yield TeacherType(ref="ER", **dd.babelkw('name', de="Ehrenamtlich real", fr="Volontaire (réel)", en="Voluntary (real)"))
        yield TeacherType(ref="LBA", **dd.babelkw('name', de="LBA", fr="ALE", en="LEA"))
        #~ yield TeacherType(ref="A",**dd.babelkw('name',de="Andere",fr="Autre",en="Other"))

        company = Instantiator('contacts.Company', 'name city:name').build

        we = company("Die Buche V.o.G.", "Eupen",
                     street="Birkenweg", street_no=5)
        yield we
        settings.SITE.site_config.site_company = we
        yield settings.SITE.site_config

        ProductCat = rt.modules.products.ProductCat
        # productcat = Instantiator('products.ProductCat').build

        course_fees = ProductCat(**dd.str2kw('name', _("Participation fees")))
        yield course_fees

        trips = ProductCat(**dd.str2kw('name', _("Trips")))
        # et="Väljasõidud", de="Ausflüge", fr="Excursions"))
        yield trips

        kw = dd.str2kw('name', _("Journeys"))
        self.journeys_cat = ProductCat(**kw)
        yield self.journeys_cat

        self.journey_tariff = Product(cat=self.journeys_cat, **kw)
        yield self.journey_tariff

        rent = ProductCat(**dd.str2kw('name', _("Room renting")))
        # et="Ruumiüür", de="Raummiete", fr="Loyer"))
        yield rent
        # other = ProductCat(**dd.str2kw('name', _("Other")))
        # et="Muud", de="Sonstige", fr="Autres"))
        # yield other

        product = Instantiator(
            'products.Product', "sales_price cat name").build
        yield product("20", course_fees, "20€")
        yield product("50", course_fees, "50€")
        yield product("80", course_fees, "80€")

        rent20 = product("20", rent, "Spiegelraum Eupen")
        yield rent20
        rent10 = product("10", rent, **dd.babelkw(
            'name',
            en="Rent per meeting", et="Ruumi üürimine",
            de="Raummiete pro Versammlung",
            fr="Loyer par réunion"))
        yield rent10

        self.PRICES = Cycler(Product.objects.filter(cat=course_fees))

        event_type = Instantiator('cal.EventType').build
        kw = dd.str2kw('name', _("Courses"))
        kw.update(dd.str2kw('event_label', _("Hour")))
        self.kurse = event_type(**kw)
        yield self.kurse
        settings.SITE.site_config.default_event_type = self.kurse
        yield settings.SITE.site_config

        self.seminare = event_type(**dd.str2kw('name', _("Seminars")))
        yield self.seminare

        yield event_type(**dd.str2kw('name', _("Excursions")))
                                     # de="Ausflüge",
                                     #  fr="Excursions",
                                     #  en="Excursions",
        yield event_type(**dd.str2kw('name', _("Hikes")))
                                      # de="Wanderungen",
                                      # fr="Randonnées",
                                      # en="Hikes",

        yield event_type(**dd.str2kw('name', _("Meetings")))
                                      # de="Versammlungen",
                                      # fr="Réunions",
                                      # en="Meetings",

        yield event_type(
            email_template='Team.eml.html',
            **dd.str2kw('name', _("Team Meetings")))
                         # de="Team-Besprechungen",
                         # fr="Coordinations en équipe",
                         # en="Team Meetings",

        #~ yield event_type(**dd.babelkw('name',
              #~ de="Feiertage",
              #~ fr="Jours fériés",
              #~ en="Holidays",
              #~ ))
        #~

        company = Instantiator('contacts.Company', 'name city:name').build
        eupen = company("Lern- und Begegnungszentrum", "Eupen",
                        street="Kirchstraße", street_no=39, street_box="/B2")
        yield eupen
        bbach = company("Lern- und Begegnungszentrum", "Butgenbach")
        yield bbach
        kelmis = company("Zur Klüüs", "Kelmis")
        yield kelmis
        stvith = company("Sport- und Freizeitzentrum", "Sankt Vith")
        yield stvith

        self.ext1 = company("AA Neudorf", "Raeren")
        yield self.ext1
        self.ext2 = company("Nisperter Schützenverein", "Eupen")
        yield self.ext2

        room = Instantiator('cal.Room').build
        kw = dict(company=eupen)
        kw.update(dd.str2kw('name', _("Mirrored room")))
        kw.update(tariff=rent20)
        self.spiegel = room(**kw)
        yield self.spiegel

        kw.update(dd.str2kw('name', _("Computer room")))
        kw.update(tariff=rent10)
        self.pc_eupen = room(**kw)
        yield self.pc_eupen

        kw = dict(company=bbach)
        kw.update(dd.str2kw('name', _("Conferences room")))
        self.konf = room(**kw)
        yield self.konf

        kw.update(dd.str2kw('name', _("Computer room")))
        self.pc_bbach = room(**kw)
        yield self.pc_bbach

        kw = dict(company=kelmis)
        kw.update(dd.str2kw('name', _("Computer room")))
        self.pc_kelmis = room(**kw)
        yield self.pc_kelmis

        kw = dict(company=stvith)
        kw.update(dd.str2kw('name', _("Computer room")))
        self.pc_stvith = room(**kw)
        yield self.pc_stvith

        # a room without company
        kw = dict()
        kw.update(dd.str2kw('name', _("Outside")))
        self.outside = room(**kw)
        yield self.outside

        COLORS = Cycler(Calendar.COLOR_CHOICES)

        for u in Room.objects.all():
            obj = Calendar(name=unicode(u), color=COLORS.pop())
            yield obj
            #~ logger.info("20131018 %s", obj)
            u.calendar = obj
            u.save()


class Loader2(Loader1):

    def objects(self):

        yield super(Loader2, self).objects()

        topic = Instantiator('courses.Topic').build
        line = Instantiator('courses.Line', 'topic event_type tariff').build
        course = Instantiator(
            'courses.Course', 'line room start_time end_time').build
        booking = Instantiator(
            'rooms.Booking', 'room start_time end_time').build

        TEACHERS = Cycler(Teacher.objects.all())
        COMPANIES = Cycler(Company.objects.all())
        USERS = Cycler(settings.SITE.user_model.objects.all())

        def add_course(*args, **kw):
            kw.update(user=USERS.pop())
            kw.update(teacher=TEACHERS.pop())
            #~ kw.update(price=PRICES.pop())
            return course(*args, **kw)

        Product = rt.modules.products.Product
        ProductCat = rt.modules.products.ProductCat

        journey_options = ProductCat(**dd.str2kw(
            'name', _("Hotel options")))
        yield journey_options
        option = Instantiator(Product, cat=journey_options).build
        yield option(**dd.str2kw('name', _("Single room")))
        yield option(**dd.str2kw('name', _("Double room")))
        yield option(**dd.str2kw('name', _("Triple room")))
        # yield option(**dd.str2kw('name', _("Shower")))
        # yield option(**dd.str2kw('name', _("Night club")))

        # trip_options = ProductCat(**dd.str2kw('name', _("Trip options")))
        # yield trip_options
        # option = Instantiator(Product, cat=trip_options).build
        # yield option(name="Eupen Oberstadt")
        # yield option(name="Eupen Unterstadt")
        # yield option(name="Raeren")
        # yield option(name="Kelmis")
        # yield option(name="Büllingen")

        journey = Instantiator(
            'courses.Course', 'line name start_date end_date').build

        def add_journey(*args, **kw):
            kw.update(user=USERS.pop())
            kw.update(teacher=TEACHERS.pop())
            return journey(*args, **kw)

        self.journeys_topic = topic(**dd.str2kw('name', _("Journeys")))
        yield self.journeys_topic
        europe = line(self.journeys_topic, None, self.journey_tariff,
                      options_cat=journey_options,
                      **dd.str2kw('name', _("Europe")))

        yield europe
        yield add_journey(europe, "Griechenland 2014",
                          i2d(20140814), i2d(20140820))
        yield add_journey(europe, "London 2014",
                          i2d(20140714), i2d(20140720))

        comp = topic(name="Computer")
        yield comp
        sport = topic(name="Sport")
        yield sport
        medit = topic(name="Meditation")
        yield medit
        externe = topic(name="Externe")
        yield externe

        obj = line(comp, self.kurse, self.PRICES.pop(),
                   ref="comp",
                   **dd.babelkw('name', de="Erste Schritte", en="First Steps"))
        yield obj
        kw = dict(max_events=8)
        kw.update(max_places=20)
        kw.update(start_date=demo_date(-30))
        kw.update(state=courses.CourseStates.registered)
        kw.update(every=1)
        kw.update(every_unit=cal.Recurrencies.per_weekday)

        yield add_course(obj, self.pc_bbach, "13:30", "15:00",
                         monday=True, **kw)
        yield add_course(obj, self.pc_eupen, "17:30", "19:00",
                         wednesday=True, **kw)
        yield add_course(obj, self.pc_kelmis, "13:30", "15:00",
                         friday=True, **kw)

        desc = """
    Behandelte Themengebiete:

    - Grundlagen, Voraussetzungen
    - Arbeiten im WWW unter Verwendung eines Browsers
    - Navigieren im WWW
    - Links in die Linkleiste legen
    - aus Webseiten heraus drucken
    - Favoriten bzw. Lesezeichen verwenden
    - Aufgabe und Funktionsweise von Suchmaschinen
    - Elektronische Post: E-Mails verfassen, senden, empfangen, beantworten
    - E-Mails mit Anlagen
    - E-mail Sicherheit
    - Tipps und Tricks
    """
        obj = line(
            comp, self.kurse, self.PRICES.pop(),
            ref="WWW",
            description=desc, **dd.babelkw(
                'name',
                de="Internet: World Wide Web für Anfänger",
                en="Internet for beginners"))
        yield obj
        kw = dict(max_events=8)
        kw.update(start_date=demo_date(10))
        kw.update(state=courses.CourseStates.registered)
        yield add_course(obj, self.pc_bbach, "13:30", "15:00",
                         monday=True, **kw)
        yield add_course(obj, self.pc_eupen, "17:30", "19:00",
                         wednesday=True, **kw)
        yield add_course(obj, self.pc_kelmis, "13:30", "15:00",
                         friday=True, **kw)

        obj = line(sport, self.kurse, self.PRICES.pop(),
                   ref="BT",
                   **dd.babelkw('name', de="Bauchtanz", en="Belly dancing"))
        yield obj
        kw = dict(max_events=8)
        kw.update(max_places=10)
        kw.update(start_date=demo_date(20))
        kw.update(state=CourseStates.registered)
        yield add_course(obj, self.spiegel, "19:00", "20:00",
                         wednesday=True, **kw)

        obj = line(sport, self.kurse, self.PRICES.pop(),
                   ref="FG",
                   **dd.babelkw('name',
                                de="Funktionsgymnastik",
                                en="Functional gymnastics"))
        yield obj
        kw = dict(max_events=10, state=CourseStates.registered)
        kw.update(start_date=demo_date(-10))
        yield add_course(obj, self.spiegel, "11:00", "12:00", monday=True, **kw)
        yield add_course(obj, self.spiegel, "13:30", "14:30", monday=True, **kw)

        obj = line(sport, self.kurse, self.PRICES.pop(),
                   ref="Rücken",
                   **dd.babelkw('name', de="Rücken fit durch Schwimmen", en="Swimming"))
        yield obj
        kw = dict(max_events=10, state=CourseStates.registered)
        kw.update(start_date=demo_date(-100))
        yield add_course(obj, self.spiegel, "11:00", "12:00", monday=True, **kw)
        yield add_course(obj, self.spiegel, "13:30", "14:30", monday=True, **kw)
        yield add_course(obj, self.pc_stvith, "11:00", "12:00", tuesday=True, **kw)
        yield add_course(obj, self.pc_stvith, "13:30", "14:30", tuesday=True, **kw)
        yield add_course(obj, self.pc_kelmis, "11:00", "12:00", thursday=True, **kw)
        yield add_course(obj, self.pc_kelmis, "13:30", "14:30", thursday=True, **kw)

        obj = line(sport, self.kurse, self.PRICES.pop(),
                   ref="SV",
                   **dd.babelkw('name', de="Selbstverteidigung im Alltag", en="Self-defence"))
        yield obj
        kw = dict(max_events=6)
        kw.update(max_places=12)
        kw.update(start_date=demo_date(-80))
        kw.update(state=CourseStates.registered)
        yield add_course(obj, self.spiegel, "18:00", "19:00", friday=True, **kw)
        yield add_course(obj, self.spiegel, "19:00", "20:00", friday=True, **kw)

        obj = line(medit, self.kurse, self.PRICES.pop(),
                   ref="GLQ",
                   name="GuoLin-Qigong")
        yield obj
        kw = dict(max_events=10)
        kw.update(start_date=demo_date(-10))
        kw.update(state=CourseStates.registered)
        yield add_course(obj, self.spiegel, "18:00", "19:30",
                         monday=True, **kw)
        yield add_course(obj, self.spiegel, "19:00", "20:30",
                         friday=True, **kw)

        obj = line(medit, self.kurse, self.PRICES.pop(),
                   ref="MED",
                   **dd.babelkw(
                       'name',
                       de="Den Kopf frei machen - zur inneren Ruhe finden",
                       en="Finding your inner peace"))
        yield obj
        kw = dict(max_events=10)
        kw.update(max_places=30)
        kw.update(start_date=demo_date(-10))
        kw.update(state=CourseStates.registered)
        yield add_course(obj, self.konf, "18:00", "19:30", monday=True, **kw)
        yield add_course(obj, self.konf, "19:00", "20:30", friday=True, **kw)

        obj = line(medit, self.kurse, self.PRICES.pop(), name="Yoga")
        yield obj
        kw = dict(max_events=10)
        kw.update(start_date=demo_date(60))
        kw.update(state=CourseStates.registered)
        yield add_course(obj, self.konf, "18:00", "19:30", monday=True, **kw)
        yield add_course(obj, self.konf, "19:00", "20:30", friday=True, **kw)

        EXTS = Cycler(self.ext1, self.ext2)

        def add_booking(*args, **kw):
            kw.update(user=USERS.pop())
            kw.update(event_type=self.seminare)
            #~ kw.update(price=PRICES.pop())
            #~ kw.update(tariff=PRICES.pop())
            #~ kw.update(calendar=self.kurse)
            kw.update(every=1)
            kw.update(company=EXTS.pop())
            return booking(*args, **kw)

        #~ obj = line(externe,self.kurse,PRICES.pop(),**dd.babelkw('name',
            #~ de="Raumbuchung",en="Room booking"))
        #~ yield obj
        kw = dict(max_events=10)
        kw.update(every_unit=cal.Recurrencies.per_weekday)
        kw.update(start_date=demo_date(60))
        kw.update(state=BookingStates.registered)
        kw.update(company=COMPANIES.pop())
        yield add_booking(self.konf, "20:00", "22:00", tuesday=True, **kw)
        kw.update(company=COMPANIES.pop())
        yield add_booking(self.konf, "20:00", "22:00", thursday=True, **kw)

        kw = dict(max_events=1)
        kw.update(every_unit=cal.Recurrencies.once)
        kw.update(company=COMPANIES.pop())
        kw.update(every_unit=cal.Recurrencies.once)
        yield add_booking(self.konf, "10:00", "14:00", **kw)

        PUPILS = Cycler(Pupil.objects.all())
        #~ print 20130712, Pupil.objects.all()
        COURSES = Cycler(Course.objects.filter(line__tariff__isnull=False))
        STATES = Cycler(EnrolmentStates.objects())

        for i in range(100):
            kw = dict(
                user=USERS.pop(), course=COURSES.pop(),
                pupil=PUPILS.pop())
            kw.update(request_date=demo_date(-i))
            kw.update(state=STATES.pop())
            #~ print 20130712, kw
            yield Enrolment(**kw)

        #~ ses = settings.SITE.login('rolf')
        ses = settings.SITE.login()

        for model in (Course, Booking):
            for obj in model.objects.all():
                rc = ses.run(obj.do_update_events)
                if not rc.get('success', False):
                    raise Exception("update_reminders on %s returned %s" %
                                    (obj, rc))

        n = 0
        for p in Partner.objects.all():
            if n > 10:
                break
            try:
                rc = ses.run(p.create_invoice)
                #~ print 20130802, rc
                if rc.get('success', True):
                    n += 1
            except Warning:
                pass


objects = Loader2().objects
