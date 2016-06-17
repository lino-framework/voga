# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
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

from __future__ import unicode_literals

from django.conf import settings

from lino.api import dd, rt


def objects():
    Person = rt.models.contacts.Person
    User = rt.models.users.User
    Place = rt.models.countries.Place
    eupen = Place.objects.get(name__exact='Eupen')

    person = Person(first_name="Marianne", last_name="Martin",
                    email=settings.SITE.demo_email,
                    city=eupen, gender=dd.Genders.female)
    yield person
    yield User(username=person.first_name.lower(),
               partner=person, profile='100')

    person = Person(first_name="Monique", last_name="Mommer",
                    email=settings.SITE.demo_email,
                    city=eupen, gender=dd.Genders.female)
    yield person
    yield User(username=person.first_name.lower(),
               partner=person, profile='200')

