.. _voga.install:

Installing Lino Voga
=======================

Development server
------------------

If you need only a development server, 
just install Lino (the framework) as documented 
in :ref:`lino.dev.install`, then:

- Go to your :file:`repositories` directory and download also a copy
  of the Lino Voga repository::

    $ cd ~/repositories
    $ git clone https://github.com/lsaffre/voga
    
- Use pip to install this as editable package::

    $ pip install -e voga

- In your project's :xfile:`settings.py`, make sure that you inherit
  from the :mod:`lino_voga.settings` module::
    
    from lino_voga.settings import *


