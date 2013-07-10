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
    school = dd.resolve_app('school')
    
    Room = dd.resolve_model('cal.Room')
    Event = dd.resolve_model('cal.Event')
    Company = dd.resolve_model('contacts.Company')
    Teacher = dd.resolve_model('school.Teacher')
    TeacherType = dd.resolve_model('school.TeacherType')
    Pupil = dd.resolve_model('school.Pupil')
    PupilType = dd.resolve_model('school.PupilType')
    Enrolment = dd.resolve_model('school.Enrolment')
    Course = dd.resolve_model('school.Course')
    Product = dd.resolve_model('products.Product')
    CourseStates = school.CourseStates
    EnrolmentStates = school.EnrolmentStates
    
    we = Company(name="Buche V.o.G.",prefix="Die")
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
    
        
    product = Instantiator('products.Product',"price cat name").build
    yield product("20",tariffs,"20€")
    yield product("50",tariffs,"50€")
    yield product("80",tariffs,"80€")
    yield product("20",rent,**babelkw('name',
        en="Spiegelraum Eupen",et="Spiegelraum Eupen",de="Spiegelraum Eupen",
        fr="Spiegelraum Eupen"))

    
    
    
    calendar = Instantiator('cal.Calendar').build
    yield calendar(color=1,**dd.babelkw('name',
          de=u"Kurse",
          fr=u"Cours",
          en=u"Courses",
          ))
    
    yield calendar(color=4,**dd.babelkw('name',
          de=u"Seminare",
          fr=u"Séminaires",
          en=u"Seminars",
          ))
    
    yield calendar(color=8,**dd.babelkw('name',
          de="Ausflüge",
          fr="Excursions",
          en="Excursions",
          ))
    yield calendar(color=12,**dd.babelkw('name',
          de="Wanderungen",
          fr="Randonnées",
          en="Hikes",
          ))
          
    yield calendar(color=16,
        email_template='Team.eml.html',
        **dd.babelkw('name',
          de="Team-Besprechungen",
          fr="Coordinations en équipe",
          en="Team Meetings",
          ))
          
    
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
    
    
    room = Instantiator('cal.Room').build
    kw = dict(company=eupen)
    kw.update(babelkw('name',
          de="Spiegelsaal",
          fr="Salle mirroitée",
          en="Mirrored room",
          ))
    spiegel = room(**kw)
    yield spiegel
    
    kw.update(babelkw('name',
          de="Computerraum",
          fr="Salle ordinateurs",
          en="Computer room",
          ))
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
    
    
    
    topic = Instantiator('school.Topic').build
    line = Instantiator('school.Line','topic').build
    course = Instantiator('school.Course','line room start_time end_time').build
    
    TEACHERS = Cycler(Teacher.objects.all())
    USERS = Cycler(settings.SITE.user_model.objects.all())
    PLACES = Cycler(Room.objects.all())
    #~ PRICES = Cycler(20,30,40,50)
    PRICES = Cycler(Product.objects.filter(cat=tariffs))
    
    def add_course(*args,**kw):
        kw.update(user=USERS.pop())
        kw.update(teacher=TEACHERS.pop())
        #~ kw.update(price=PRICES.pop())
        kw.update(tariff=PRICES.pop())
        kw.update(every=1)
        kw.update(company=we)
        kw.update(every_unit=cal.Recurrencies.per_weekday)
        return course(*args,**kw)
    
    comp = topic(**dd.babelkw('name',de="Computer"))
    yield comp
    sport = topic(**dd.babelkw('name',de="Sport"))
    yield sport
    medit = topic(**dd.babelkw('name',de="Meditation"))
    yield medit
    
    obj = line(comp,**dd.babelkw('name',de="Erste Schritte"))
    yield obj
    kw = dict(max_events=8)
    kw.update(max_places=20)
    kw.update(start_date=settings.SITE.demo_date(-30))
    kw.update(state=school.CourseStates.started)
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
    obj = line(comp,description=desc,**dd.babelkw('name',de="Internet: World Wide Web für Anfänger"))
    yield obj
    kw = dict(max_events=8)
    kw.update(start_date=settings.SITE.demo_date(10))
    kw.update(state=school.CourseStates.scheduled)
    yield add_course(obj,pc_bbach,"13:30","15:00",monday=True,**kw)
    yield add_course(obj,pc_eupen,"17:30","19:00",wednesday=True,**kw)
    yield add_course(obj,pc_kelmis,"13:30","15:00",friday=True,**kw)
    
    obj = line(sport,**dd.babelkw('name',de="Bauchtanz"))
    yield obj
    kw = dict(max_events=8)
    kw.update(max_places=10)
    kw.update(start_date=settings.SITE.demo_date(-20))
    kw.update(state=CourseStates.started)
    yield add_course(obj,spiegel,"19:00","20:00",wednesday=True,**kw)
    
    obj = line(sport,**dd.babelkw('name',de="Funktionsgymnastik"))
    yield obj
    kw = dict(max_events=10,state=CourseStates.started)
    kw.update(start_date=settings.SITE.demo_date(-10))
    yield add_course(obj,spiegel,"11:00","12:00",monday=True,**kw)
    yield add_course(obj,spiegel,"13:30","14:30",monday=True,**kw)
    
    obj = line(sport,**dd.babelkw('name',de="Rücken fit durch Schwimmen"))
    yield obj
    kw = dict(max_events=10,state=CourseStates.ended)
    kw.update(start_date=settings.SITE.demo_date(-100))
    yield add_course(obj,spiegel,"11:00","12:00",monday=True,**kw)
    yield add_course(obj,spiegel,"13:30","14:30",monday=True,**kw)
    yield add_course(obj,pc_stvith,"11:00","12:00",tuesday=True,**kw)
    yield add_course(obj,pc_stvith,"13:30","14:30",tuesday=True,**kw)
    yield add_course(obj,pc_kelmis,"11:00","12:00",thursday=True,**kw)
    yield add_course(obj,pc_kelmis,"13:30","14:30",thursday=True,**kw)
    

    obj = line(sport,**dd.babelkw('name',de="Selbstverteidigung im Alltag"))
    yield obj
    kw = dict(max_events=6)
    kw.update(max_places=12)
    kw.update(start_date=settings.SITE.demo_date(-80))
    kw.update(state=CourseStates.ended)
    yield add_course(obj,spiegel,"18:00","19:00",friday=True,**kw)
    yield add_course(obj,spiegel,"19:00","20:00",friday=True,**kw)

    obj = line(medit,**dd.babelkw('name',de="GuoLin-Qigong"))
    yield obj
    kw = dict(max_events=10)
    kw.update(start_date=settings.SITE.demo_date(-10))
    kw.update(state=CourseStates.started)
    yield add_course(obj,spiegel,"18:00","19:30",monday=True,**kw)
    yield add_course(obj,spiegel,"19:00","20:30",friday=True,**kw)

    obj = line(medit,**dd.babelkw('name',de="Den Kopf frei machen - zur inneren Ruhe finden"))
    yield obj
    kw = dict(max_events=10)
    kw.update(max_places=30)
    kw.update(start_date=settings.SITE.demo_date(-10))
    kw.update(state=CourseStates.started)
    yield add_course(obj,konf,"18:00","19:30",monday=True,**kw)
    yield add_course(obj,konf,"19:00","20:30",friday=True,**kw)

    obj = line(medit,**dd.babelkw('name',de="Yoga"))
    yield obj
    kw = dict(max_events=10)
    kw.update(start_date=settings.SITE.demo_date(60))
    kw.update(state=CourseStates.scheduled)
    yield add_course(obj,konf,"18:00","19:30",monday=True,**kw)
    yield add_course(obj,konf,"19:00","20:30",friday=True,**kw)


    PUPILS = Cycler(Pupil.objects.all())
    COURSES = Cycler(Course.objects.all())
    STATES = Cycler(EnrolmentStates.objects())
    
    for i in range(100):
        kw = dict(
            user=USERS.pop(),course=COURSES.pop(),
            pupil=PUPILS.pop())
        kw.update(request_date=settings.SITE.demo_date(-i))
        kw.update(state=STATES.pop())
        yield Enrolment(**kw)
        
    for feast in (
        (6,1,"Kinderschutztag"),
        (12,25,"Weihnachten"),
        (6,24,"Saint-Jean"),
        (7,21,"Nationalfeiertag"),
        ):
        d = settings.SITE.demo_date().replace(month=feast[0],day=feast[1])
        yield Event(start_date=d,summary=feast[2],user=USERS.pop())



        
