.. _faggio.install:

Installing Lino-Faggio
=======================

Development server
------------------

If you need only a development server, 
just install Lino (the framework) as documented 
in :ref:`lino.dev.install`, then:

- Go to your `hgwork` directory and 
  download also a copy of the Lino-Faggio repository::

    cd ~/hgwork
    hg clone https://code.google.com/p/lino-faggio/ faggio
    
- Use pip to install this as editable package::

    pip install -e faggio

- In your project's `settings.py`, make sure that you inherit from 
  the right `settings` module::
    
    from lino_faggio.settings import *


