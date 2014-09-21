# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

SETUP_INFO = dict(
    name='lino-faggio',
    version='0.0.4',
    install_requires=['lino'],
    test_suite='tests',
    description="A Lino application for managing courses, "
    "participants and meeting rooms",

    long_description="""Lino Faggio is a `Lino <http://www.lino-framework.org>`_
application for managing courses, participants and meeting rooms.

""",
    author='Luc Saffre',
    author_email='luc.saffre@gmail.com',
    url="http://faggio.lino-framework.org",
    license='BSD License',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Development Status :: 1 - Planning
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Topic :: Office/Business :: Scheduling
""".splitlines())

SETUP_INFO.update(packages=[
    'lino_faggio',
    'lino_faggio.lib',
    'lino_faggio.lib.cal',
    'lino_faggio.lib.cal.fixtures',
    'lino_faggio.lib.contacts',
    'lino_faggio.lib.contacts.fixtures',
    'lino_faggio.lib.contacts.management',
    'lino_faggio.lib.contacts.management.commands',
    'lino_faggio.lib.courses',
    'lino_faggio.lib.courses.fixtures',
    'lino_faggio.lib.rooms',
    'lino_faggio.projects',
    'lino_faggio.projects.docs',
    'lino_faggio.projects.docs.settings',
    'lino_faggio.projects.docs.tests',
    'lino_faggio.projects.edmund',
    'lino_faggio.projects.edmund.settings',
    'lino_faggio.projects.edmund.settings.fixtures',
    'lino_faggio.projects.roger',
    'lino_faggio.projects.roger.settings',
    'lino_faggio.projects.roger.settings.fixtures',
    'lino_faggio.fixtures',
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
