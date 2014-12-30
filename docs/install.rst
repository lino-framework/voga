.. _faggio.install:

Installing Lino Faggio
=======================

Development server
------------------

If you need only a development server, 
just install Lino (the framework) as documented 
in :ref:`lino.dev.install`, then:

- Go to your :file:`repositories` directory and download also a copy
  of the Lino Faggio repository::

    $ cd ~/repositories
    $ git clone https://github.com/lsaffre/lino-faggio faggio
    
- Use pip to install this as editable package::

    $ pip install -e faggio

- In your project's :xfile:`settings.py`, make sure that you inherit
  from the :mod:`lino_faggio.settings` module::
    
    from lino_faggio.settings import *


