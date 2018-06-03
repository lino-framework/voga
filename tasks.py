from atelier.invlib import setup_from_tasks
ns = setup_from_tasks(
    globals(), "lino_voga",
    languages="en de fr et".split(),
    tolerate_sphinx_warnings= False,
    blogref_url='http://luc.lino-framework.org',
    revision_control_system='git',
    locale_dir= 'lino_voga/lib/voga/locale')
