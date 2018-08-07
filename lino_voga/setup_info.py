# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd
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

# This file may not have a docstring because it is being `exec`ed from
# the __init__.py file.
# How to test just this file:
#   $ python setup.py test -s tests.PackagesTests


SETUP_INFO = dict(
    name='lino-voga',
    # version='0.0.4',
    version='18.04.0',
    install_requires=[
        'lino_xl',
        'lino_cosi',  # TODO: remove dependency from cosi
        ],
    test_suite='tests',
    # tests_require=['pytest'],
    description="A Lino application for managing courses, "
    "participants and meeting rooms",

    long_description="""\

Lino Voga is a `Lino <http://www.lino-framework.org>`__ application
for managing courses, participants and meeting rooms.

- The central project homepage is http://voga.lino-framework.org

- For *introductions* and *commercial information* about Lino Voga
  please see `www.saffre-rumma.net
  <http://www.saffre-rumma.net/voga/>`__.

- Online demo site at http://roger.lino-framework.org (English, German, French)
  and  http://vtp2014.lino-framework.org (English, Estonian)

""",
    author='Luc Saffre',
    author_email='luc.saffre@gmail.com',
    url="http://voga.lino-framework.org",
    license='GNU Affero General Public License v3',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Development Status :: 5 - Production/Stable
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
Intended Audience :: Education
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: OS Independent
Topic :: Office/Business :: Financial :: Accounting
Topic :: Office/Business :: Scheduling
""".splitlines())

SETUP_INFO.update(packages=[
    'lino_voga',
    'lino_voga.lib',
    'lino_voga.lib.cal',
    'lino_voga.lib.cal.fixtures',
    'lino_voga.lib.contacts',
    'lino_voga.lib.contacts.fixtures',
    'lino_voga.lib.contacts.management',
    'lino_voga.lib.contacts.management.commands',
    'lino_voga.lib.courses',
    'lino_voga.lib.courses.fixtures',
    'lino_voga.lib.products',
    'lino_voga.lib.invoicing',
    'lino_voga.lib.invoicing.fixtures',
    'lino_voga.lib.roger',
    'lino_voga.lib.roger.courses',
    'lino_voga.lib.roger.courses.fixtures',
    'lino_voga.lib.roger.courses.management',
    'lino_voga.lib.roger.courses.management.commands',
    'lino_voga.lib.rooms',
    'lino_voga.lib.sales',
    'lino_voga.lib.sales.fixtures',
    'lino_voga.lib.voga',
    'lino_voga.lib.voga.fixtures',
    'lino_voga.lib.voga.config',
    'lino_voga.lib.voga.config.courses',
    'lino_voga.lib.voga.config.courses.Course',
    'lino_voga.lib.voga.config.courses.Enrolment',
    'lino_voga.lib.voga.config.courses.Topic',
    'lino_voga.lib.voga.config.excerpts',
    'lino_voga.lib.voga.config.sales',
    'lino_voga.lib.voga.config.sales.Invoice',
])

SETUP_INFO.update(message_extractors={
    'lino_voga': [
        ('**/cache/**',          'ignore', None),
        ('**.py',                'python', None),
        ('**.js',                'javascript', None),
        ('**.html', 'jinja2', None),
        # ('**/config/**.html', 'jinja2', None),
        # ('**/config/**/**.html', 'jinja2', None),
        # ('lino_voga/lib/voga/config/courses/Enrolment/**.html',
        #  'jinja2', None),

    ],
})

SETUP_INFO.update(package_data=dict())


def add_package_data(package, *patterns):
    l = SETUP_INFO['package_data'].setdefault(package, [])
    l.extend(patterns)
    return l

#~ add_package_data('lino_voga',
  #~ 'config/patrols/Patrol/*.odt',
  #~ 'config/patrols/Overview/*.odt')

l = add_package_data('lino_voga')
for lng in 'de fr'.split():
    l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
