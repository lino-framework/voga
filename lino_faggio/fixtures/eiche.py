# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino-Faggio project.
## Lino-Faggio is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-Faggio is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-Faggio; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

#~ from lino import dd
from lino.utils.instantiator import Instantiator, i2d
from lino.utils  import Cycler
#~ from lino.core.dbutils import resolve_model
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from north.dbutils import babelkw

from lino import dd


def objects():
    
    cal = dd.resolve_app('cal')
    courses = dd.resolve_app('courses')
    
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
    
    yield PupilType(ref="M",name="Mitglied")
    yield PupilType(ref="H",name="Helfer")
    yield PupilType(ref="L",name="LFV")
    yield PupilType(ref="C",name="COK")
    #~ yield PupilType(ref="E",name="Extern")
    
    yield TeacherType(ref="S",**babelkw('name',de="Selbstständig",fr="Indépendant",en="Independant"))
    yield TeacherType(ref="EP",**babelkw('name',de="Ehrenamtlich pauschal",fr="Volontaire (forfait)",en="Voluntary (flat)"))
    yield TeacherType(ref="ER",**babelkw('name',de="Ehrenamtlich real",fr="Volontaire (réel)",en="Voluntary (real)"))
    yield TeacherType(ref="LBA",**babelkw('name',de="LBA",fr="ALE",en="LEA"))
    #~ yield TeacherType(ref="A",**babelkw('name',de="Andere",fr="Autre",en="Other"))
    
    
    company = Instantiator('contacts.Company','name city:name').build
    
    we = company("Die Buche V.o.G.","Eupen",street="Birkenweg",street_no=5)
    yield we
    settings.SITE.site_config.site_company = we
    yield settings.SITE.site_config
    
    
    productcat = Instantiator('products.ProductCat').build

    tariffs = productcat(**babelkw('name',
        en="Courses",et="Kursused",de="Kurse",fr="Cours"))
    yield tariffs
    rent = productcat(**babelkw('name',
        en="Room renting",et="Ruumiüür",de="Raummiete",fr="Loyer"))
    yield rent
    other = productcat(**babelkw('name',
        en="Other",
        et="Muud",
        de="Sonstige",
        fr="Autres"))
    yield other
    
        
    product = Instantiator('products.Product',"sales_price cat name").build
    yield product("20",tariffs,"20€")
    yield product("50",tariffs,"50€")
    yield product("80",tariffs,"80€")
    rent20 = product("20",rent,"Spiegelraum Eupen")
    yield rent20
    rent10 = product("10",rent,**babelkw('name',
        en="Rent per meeting",et="Ruumi üürimine",de="Raummiete pro Versammlung",
        fr="Loyer par réunion"))
    yield rent10

    
    event_type = Instantiator('cal.EventType').build
    kw = dd.babelkw('name',
          de="Kurse",
          fr="Cours",
          en="Courses",
          )
    kw.update(dd.babelkw('event_label',
          de="Stunde",
          fr="Heure",
          en="Hour",
          ))
    kurse = event_type(**kw)
    yield kurse
    settings.SITE.site_config.default_event_type = kurse
    yield settings.SITE.site_config
    
    yield event_type(**dd.babelkw('name',
          de="Seminare",
          fr="Séminaires",
          en="Seminars",
          ))
    
    yield event_type(**dd.babelkw('name',
          de="Ausflüge",
          fr="Excursions",
          en="Excursions",
          ))
    yield event_type(**dd.babelkw('name',
          de="Wanderungen",
          fr="Randonnées",
          en="Hikes",
          ))
          
    yield event_type(
        email_template='Team.eml.html',
        **dd.babelkw('name',
          de="Team-Besprechungen",
          fr="Coordinations en équipe",
          en="Team Meetings",
          ))
          
    #~ yield event_type(**dd.babelkw('name',
          #~ de="Feiertage",
          #~ fr="Jours fériés",
          #~ en="Holidays",
          #~ ))
    #~ 
    
    company = Instantiator('contacts.Company','name city:name').build
    eupen = company("Lern- und Begegnungszentrum","Eupen",
      street="Kirchstraße",street_no=39,street_box="/B2")
    yield eupen
    bbach = company("Lern- und Begegnungszentrum","Bütgenbach")
    yield bbach
    kelmis = company("Zur Klüüs","Kelmis")
    yield kelmis
    stvith = company("Sport- und Freizeitzentrum","Sankt Vith")
    yield stvith
    ext1 = company("AA Neudorf","Raeren")
    yield ext1
    ext2 = company("Nisperter Schützenverein","Eupen")
    yield ext2
    
    
    room = Instantiator('cal.Room').build
    kw = dict(company=eupen)
    kw.update(babelkw('name',
          de="Spiegelsaal",
          fr="Salle mirroitée",
          en="Mirrored room",
          ))
    kw.update(tariff=rent20)
    spiegel = room(**kw)
    yield spiegel
    
    kw.update(babelkw('name',
          de="Computerraum",
          fr="Salle ordinateurs",
          en="Computer room",
          ))
    kw.update(tariff=rent10)
    pc_eupen = room(**kw)
    yield pc_eupen
    
    kw = dict(company=bbach)
    kw.update(babelkw('name',
          de="Konferenzraum",
          fr="Salle conférences",
          en="Conferences room",
          ))
    konf = room(**kw)
    yield konf
    
    kw.update(babelkw('name',
          de="Informatikraum",
          fr="Salle informatique",
          en="Computerroom",
          ))
    pc_bbach = room(**kw)
    yield pc_bbach
    
    kw = dict(company=kelmis)
    kw.update(babelkw('name',
          de="Computerraum",
          fr="Salle ordinateurs",
          en="Computer room",
          ))
    pc_kelmis = room(**kw)
    yield pc_kelmis
    
    kw = dict(company=stvith)
    kw.update(babelkw('name',
          de="Computerraum",
          fr="Salle ordinateurs",
          en="Computer room",
          ))
    pc_stvith = room(**kw)
    yield pc_stvith
    
    
    
    topic = Instantiator('courses.Topic').build
    line = Instantiator('courses.Line','topic event_type tariff').build
    course = Instantiator('courses.Course','line room start_time end_time').build
    
    TEACHERS = Cycler(Teacher.objects.all())
    USERS = Cycler(settings.SITE.user_model.objects.all())
    PLACES = Cycler(Room.objects.all())
    #~ PRICES = Cycler(20,30,40,50)
    PRICES = Cycler(Product.objects.filter(cat=tariffs))
    
    def add_course(*args,**kw):
        kw.update(user=USERS.pop())
        kw.update(teacher=TEACHERS.pop())
        #~ kw.update(price=PRICES.pop())
        kw.update(every=1)
        kw.update(company=we)
        kw.update(every_unit=cal.Recurrencies.per_weekday)
        return course(*args,**kw)
    
    comp = topic(name="Computer")
    yield comp
    sport = topic(name="Sport")
    yield sport
    medit = topic(name="Meditation")
    yield medit
    externe = topic(name="Externe")
    yield externe
    
    obj = line(comp,kurse,PRICES.pop(),**dd.babelkw('name',de="Erste Schritte",en="First Steps"))
    yield obj
    kw = dict(max_events=8)
    kw.update(max_places=20)
    kw.update(start_date=settings.SITE.demo_date(-30))
    kw.update(state=courses.CourseStates.started)
    yield add_course(obj,pc_bbach,"13:30","15:00",monday=True,**kw)
    yield add_course(obj,pc_eupen,"17:30","19:00",wednesday=True,**kw)
    yield add_course(obj,pc_kelmis,"13:30","15:00",friday=True,**kw)
    

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
    obj = line(comp,kurse,PRICES.pop(),description=desc,**dd.babelkw('name',
        de="Internet: World Wide Web für Anfänger",
        en="Internet for beginners"))
    yield obj
    kw = dict(max_events=8)
    kw.update(start_date=settings.SITE.demo_date(10))
    kw.update(state=courses.CourseStates.published)
    yield add_course(obj,pc_bbach,"13:30","15:00",monday=True,**kw)
    yield add_course(obj,pc_eupen,"17:30","19:00",wednesday=True,**kw)
    yield add_course(obj,pc_kelmis,"13:30","15:00",friday=True,**kw)
    
    obj = line(sport,kurse,PRICES.pop(),**dd.babelkw('name',de="Bauchtanz",en="Belly dancing"))
    yield obj
    kw = dict(max_events=8)
    kw.update(max_places=10)
    kw.update(start_date=settings.SITE.demo_date(-20))
    kw.update(state=CourseStates.started)
    yield add_course(obj,spiegel,"19:00","20:00",wednesday=True,**kw)
    
    obj = line(sport,kurse,PRICES.pop(),**dd.babelkw('name',de="Funktionsgymnastik",en="Functional gymnastics"))
    yield obj
    kw = dict(max_events=10,state=CourseStates.started)
    kw.update(start_date=settings.SITE.demo_date(-10))
    yield add_course(obj,spiegel,"11:00","12:00",monday=True,**kw)
    yield add_course(obj,spiegel,"13:30","14:30",monday=True,**kw)
    
    obj = line(sport,kurse,PRICES.pop(),**dd.babelkw('name',de="Rücken fit durch Schwimmen",en="Swimming"))
    yield obj
    kw = dict(max_events=10,state=CourseStates.ended)
    kw.update(start_date=settings.SITE.demo_date(-100))
    yield add_course(obj,spiegel,"11:00","12:00",monday=True,**kw)
    yield add_course(obj,spiegel,"13:30","14:30",monday=True,**kw)
    yield add_course(obj,pc_stvith,"11:00","12:00",tuesday=True,**kw)
    yield add_course(obj,pc_stvith,"13:30","14:30",tuesday=True,**kw)
    yield add_course(obj,pc_kelmis,"11:00","12:00",thursday=True,**kw)
    yield add_course(obj,pc_kelmis,"13:30","14:30",thursday=True,**kw)
    

    obj = line(sport,kurse,PRICES.pop(),**dd.babelkw('name',de="Selbstverteidigung im Alltag",en="Self-defence"))
    yield obj
    kw = dict(max_events=6)
    kw.update(max_places=12)
    kw.update(start_date=settings.SITE.demo_date(-80))
    kw.update(state=CourseStates.ended)
    yield add_course(obj,spiegel,"18:00","19:00",friday=True,**kw)
    yield add_course(obj,spiegel,"19:00","20:00",friday=True,**kw)

    obj = line(medit,kurse,PRICES.pop(),name="GuoLin-Qigong")
    yield obj
    kw = dict(max_events=10)
    kw.update(start_date=settings.SITE.demo_date(-10))
    kw.update(state=CourseStates.started)
    yield add_course(obj,spiegel,"18:00","19:30",monday=True,**kw)
    yield add_course(obj,spiegel,"19:00","20:30",friday=True,**kw)

    obj = line(medit,kurse,PRICES.pop(),**dd.babelkw('name',
        de="Den Kopf frei machen - zur inneren Ruhe finden",
        en="Finding your inner peace"))
    yield obj
    kw = dict(max_events=10)
    kw.update(max_places=30)
    kw.update(start_date=settings.SITE.demo_date(-10))
    kw.update(state=CourseStates.started)
    yield add_course(obj,konf,"18:00","19:30",monday=True,**kw)
    yield add_course(obj,konf,"19:00","20:30",friday=True,**kw)

    obj = line(medit,kurse,PRICES.pop(),name="Yoga")
    yield obj
    kw = dict(max_events=10)
    kw.update(start_date=settings.SITE.demo_date(60))
    kw.update(state=CourseStates.published)
    yield add_course(obj,konf,"18:00","19:30",monday=True,**kw)
    yield add_course(obj,konf,"19:00","20:30",friday=True,**kw)
    
    EXTS = Cycler(ext1,ext2)
    def add_course(*args,**kw):
        kw.update(user=USERS.pop())
        #~ kw.update(teacher=TEACHERS.pop())
        #~ kw.update(price=PRICES.pop())
        #~ kw.update(tariff=PRICES.pop())
        #~ kw.update(calendar=kurse)
        kw.update(every=1)
        kw.update(company=EXTS.pop())
        kw.update(every_unit=cal.Recurrencies.per_weekday)
        return course(*args,**kw)
        
    obj = line(externe,kurse,PRICES.pop(),**dd.babelkw('name',de="Treffen",en="Meeting"))
    yield obj
    kw = dict(max_events=30)
    kw.update(start_date=settings.SITE.demo_date(60))
    kw.update(state=CourseStates.published)
    yield add_course(obj,konf,"20:00","22:00",tuesday=True,**kw)
    yield add_course(obj,konf,"20:00","22:00",thursday=True,**kw)


    PUPILS = Cycler(Pupil.objects.all())
    #~ print 20130712, Pupil.objects.all()
    COURSES = Cycler(Course.objects.filter(line__tariff__isnull=False))
    STATES = Cycler(EnrolmentStates.objects())
    
    for i in range(100):
        kw = dict(
            user=USERS.pop(),course=COURSES.pop(),
            pupil=PUPILS.pop())
        kw.update(request_date=settings.SITE.demo_date(-i))
        kw.update(state=STATES.pop())
        #~ print 20130712, kw
        yield Enrolment(**kw)
        
    #~ for feast in (
        #~ (6,1,"Kinderschutztag"),
        #~ (12,25,"Weihnachten"),
        #~ (6,24,"Saint-Jean"),
        #~ (7,21,"Nationalfeiertag"),
        #~ ):
        #~ d = settings.SITE.demo_date().replace(month=feast[0],day=feast[1])
        #~ yield Event(start_date=d,summary=feast[2],user=USERS.pop())

    n = 0
    ses = settings.SITE.login('rolf')
    for p in Partner.objects.all():
        if n > 10:
            break
        try:
            rc = ses.run(p.create_invoice)
            #~ print 20130802, rc
            if rc.get('success',True):
                n += 1
        except Warning:
            pass
        
        
