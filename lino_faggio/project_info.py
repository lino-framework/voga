# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# This file is part of the Lino-Faggio project.
# Lino-Faggio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino-Faggio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino-Faggio; if not, see <http://www.gnu.org/licenses/>.

SETUP_INFO = dict(name='lino-faggio',
                  version='0.0.1',
                  install_requires=['lino'],
                  test_suite='tests',
                  description="A Lino application for managing courses, participants and meeting rooms",
      long_description="""\
Lino-Faggio is a `Lino <http://www.lino-framework.org>`_ 
application for managing courses, participants and meeting rooms.

""",
                  author='Luc Saffre',
                  author_email='luc.saffre@gmail.com',
                  url="http://faggio.lino-framework.org",
                  license='GPL',
      classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Development Status :: 1 - Planning
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: GNU General Public License (GPL)
Operating System :: OS Independent
Topic :: Office/Business :: Scheduling
""".splitlines())

SETUP_INFO.update(packages=[
    'lino_faggio',
    'lino_faggio.cal',
    'lino_faggio.cal.fixtures',
    'lino_faggio.contacts',
    'lino_faggio.contacts.fixtures',
    'lino_faggio.courses',
    'lino_faggio.courses.fixtures',
    'lino_faggio.rooms',
    'lino_faggio.settings',
    'lino_faggio.fixtures',
    'lino_faggio.tests',
])

SETUP_INFO.update(message_extractors={
    'lino_faggio': [
        ('**/cache/**',          'ignore', None),
        ('**.py',                'python', None),
        ('**.js',                'javascript', None),
        ('**/templates_jinja/**.html', 'jinja2', None),
    ],
})

SETUP_INFO.update(package_data=dict())


def add_package_data(package, *patterns):
    l = SETUP_INFO['package_data'].setdefault(package, [])
    l.extend(patterns)
    return l

#~ add_package_data('lino_faggio',
  #~ 'config/patrols/Patrol/*.odt',
  #~ 'config/patrols/Overview/*.odt')

l = add_package_data('lino_faggio')
for lng in 'de fr'.split():
    l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
