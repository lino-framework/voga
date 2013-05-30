# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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

from lino import dd


def objects():
    
    cal = dd.resolve_app('cal')
    school = dd.resolve_app('school')
    Company = dd.resolve_model('contacts.Company')
    Teacher = dd.resolve_model('school.Teacher')
    
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
    bbach = company("Seniorenheim","Bütgenbach")
    yield bbach
    kelmis = company("Zur Klüüs","Kelmis")
    yield kelmis
    stvith = company("Sport- und Freizeitzentrum","Sankt Vith")
    yield stvith
    
    topic = Instantiator('school.Topic').build
    line = Instantiator('school.Line','topic').build
    course = Instantiator('school.Course','line company start_time end_time').build
    
    if Teacher.objects.all().count() == 0:
        raise Exception(str(settings.INSTALLED_APPS))
    TEACHERS = Cycler(Teacher.objects.all())
    USERS = Cycler(settings.SITE.user_model.objects.all())
    PLACES = Cycler(cal.Place.objects.all())
    
    def add_course(*args,**kw):
        kw.update(user=USERS.pop())
        kw.update(teacher=TEACHERS.pop())
        kw.update(every=1)
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
    kw = dict(max_occurences=8)
    kw.update(start_date=settings.SITE.demo_date(-30))
    kw.update(state=school.CourseStates.started)
    yield add_course(obj,bbach,"13:30","15:00",monday=True,**kw)
    yield add_course(obj,eupen,"17:30","19:00",wednesday=True,**kw)
    yield add_course(obj,kelmis,"13:30","15:00",friday=True,**kw)
    
    obj = line(comp,**dd.babelkw('name',de="Internet"))
    yield obj
    kw = dict(max_occurences=8)
    kw.update(start_date=settings.SITE.demo_date().replace(month=1,day=29))
    kw.update(state=school.CourseStates.scheduled)
    yield add_course(obj,bbach,"13:30","15:00",monday=True,**kw)
    yield add_course(obj,eupen,"17:30","19:00",wednesday=True,**kw)
    yield add_course(obj,kelmis,"13:30","15:00",friday=True,**kw)
    
    obj = line(sport,**dd.babelkw('name',de="Bauchtanz"))
    yield obj
    kw = dict(max_occurences=8)
    kw.update(start_date=settings.SITE.demo_date().replace(month=9,day=1))
    yield add_course(obj,eupen,"19:00","20:00",wednesday=True,**kw)
    
    obj = line(sport,**dd.babelkw('name',de="Funktionsgymnastik"))
    yield obj
    kw = dict(max_occurences=10)
    kw.update(start_date=settings.SITE.demo_date().replace(month=9,day=9))
    yield add_course(obj,eupen,"11:00","12:00",monday=True,**kw)
    yield add_course(obj,eupen,"13:30","14:30",monday=True,**kw)
    
    obj = line(sport,**dd.babelkw('name',de="Rücken fit durch Schwimmen"))
    yield obj
    kw = dict(max_occurences=10)
    kw.update(start_date=settings.SITE.demo_date().replace(month=9,day=1))
    yield add_course(obj,eupen,"11:00","12:00",monday=True,**kw)
    yield add_course(obj,eupen,"13:30","14:30",monday=True,**kw)
    yield add_course(obj,stvith,"11:00","12:00",tuesday=True,**kw)
    yield add_course(obj,stvith,"13:30","14:30",tuesday=True,**kw)
    yield add_course(obj,kelmis,"11:00","12:00",thursday=True,**kw)
    yield add_course(obj,kelmis,"13:30","14:30",thursday=True,**kw)
    

    obj = line(sport,**dd.babelkw('name',de="Selbstverteidigung im Alltag"))
    yield obj
    kw = dict(max_occurences=10)
    kw.update(start_date=settings.SITE.demo_date().replace(month=9,day=1))
    yield add_course(obj,eupen,"18:00","19:00",friday=True,**kw)
    yield add_course(obj,eupen,"19:00","20:00",friday=True,**kw)

    obj = line(medit,**dd.babelkw('name',de="GuoLin-Qigong"))
    yield obj
    kw = dict(max_occurences=10)
    kw.update(start_date=settings.SITE.demo_date().replace(month=3,day=1))
    yield add_course(obj,eupen,"18:00","19:30",monday=True,**kw)
    yield add_course(obj,eupen,"19:00","20:30",friday=True,**kw)

    obj = line(medit,**dd.babelkw('name',de="Den Kopf frei machen - zur inneren Ruhe finden"))
    yield obj
    kw = dict(max_occurences=10)
    kw.update(start_date=settings.SITE.demo_date().replace(month=3,day=1))
    yield add_course(obj,bbach,"18:00","19:30",monday=True,**kw)
    yield add_course(obj,bbach,"19:00","20:30",friday=True,**kw)

    obj = line(medit,**dd.babelkw('name',de="Yoga"))
    yield obj
    kw = dict(max_occurences=10)
    kw.update(start_date=settings.SITE.demo_date().replace(month=3,day=1))
    yield add_course(obj,kelmis,"18:00","19:30",monday=True,**kw)
    yield add_course(obj,kelmis,"19:00","20:30",friday=True,**kw)

