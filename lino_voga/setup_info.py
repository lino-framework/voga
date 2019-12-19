# -*- coding: UTF-8 -*-
# Copyright 2013-2019 Rumma & Ko Ltd

# This file may not have a docstring because it is being `exec`ed from
# the __init__.py file.
# How to test just this file:
#   $ python setup.py test -s tests.PackagesTests


SETUP_INFO = dict(
    name='lino-voga',
    version='19.12.0',
    install_requires=[
        'lino_xl'
        # 'lino_cosi',  # TODO: remove dependency from cosi
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
    license='BSD-2-Clause',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Development Status :: 5 - Production/Stable
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
Intended Audience :: Education
License :: OSI Approved :: BSD License
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
])

SETUP_INFO.update(message_extractors={
    'lino_voga': [
        ('**/cache/**', 'ignore', None),
        ('**.py', 'python', None),
        ('**.js', 'javascript', None),
        ('**.html', 'jinja2', None),
        ('**/config/**.html', 'jinja2', None),
        ('**/config/**/**.html', 'jinja2', None),
        ('lino_voga/lib/voga/config/courses/Enrolment/**.html',
         'jinja2', None),

    ],
})

SETUP_INFO.update(include_package_data=True)

# SETUP_INFO.update(package_data=dict())
#
#
# def add_package_data(package, *patterns):
#     l = SETUP_INFO['package_data'].setdefault(package, [])
#     l.extend(patterns)
#     return l
#
#
# ~ add_package_data('lino_voga',
# ~ 'config/patrols/Patrol/*.odt',
# ~ 'config/patrols/Overview/*.odt')
# add_package_data('lino_voga.lib.voga', 'config/logo.jpg')
# add_package_data('lino_voga.lib.voga', 'config/courses/Course/*.*')
# add_package_data('lino_voga.lib.voga', 'config/courses/Enrolment/*.*')
# add_package_data('lino_voga.lib.voga', 'config/courses/Topic/*.*')
# add_package_data('lino_voga.lib.voga', 'config/excerpts/*.*')
# add_package_data('lino_voga.lib.voga', 'config/sales/Invoice/*.*')
#
# l = add_package_data('lino_voga')
# for lng in 'de fr'.split():
#     l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
