# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
from __future__ import unicode_literals

from django.conf import settings

from lino.api import dd, rt


def objects():
    Person = rt.models.contacts.Person
    Teacher = rt.models.courses.Teacher
    User = rt.models.users.User
    from lino.modlib.users.choicelists import UserTypes
    Place = rt.models.countries.Place
    eupen = Place.objects.get(name__exact='Eupen')

    person = Person(first_name="Marianne", last_name="Martin",
                    email=settings.SITE.demo_email,
                    city=eupen, gender=dd.Genders.female)
    yield person
    yield User(username=person.first_name.lower(),
               partner=person, user_type='100')

    person = Person(first_name="Monique", last_name="Mommer",
                    email=settings.SITE.demo_email,
                    city=eupen, gender=dd.Genders.female)
    yield person
    yield User(username=person.first_name.lower(),
               partner=person, user_type='200')

    person = Teacher(first_name="Tom", last_name="Thess",
                    email=settings.SITE.demo_email,
                    city=eupen, gender=dd.Genders.male)
    yield person
    yield User(username=person.first_name.lower(),
               partner=person, user_type=UserTypes.teacher)

