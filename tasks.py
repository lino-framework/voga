from atelier.tasks import ns, setup_from_tasks

setup_from_tasks(globals(), "lino_voga")

ns.configure(dict(languages="en de fr et".split()))

