.. _faggio.contacts:

=========
Contacts
=========

In Lino you register any physical or moral person as a 
:ref:`Partner <faggio.contacts.Partners>`.

Lino-Faggio différencie les types de Partenaires suivants:

.. django2rst:: contacts.Partner.print_subclasses_graph()

.. _faggio.contacts.Partner.obsolete:

Veraltete Partner
-----------------

Das Attribut "veraltet" bedeutet : 

- die Daten dieses Partners werden nicht mehr gepflegt, 
- alle Angaben verstehen sich als "so war es, bevor dieser Partner 
  aufhörte, uns zu interessieren".

Veraltete Partner werden normalerweise in Listen ignoriert,
als wären sie gelöscht.
Um sie trotzdem zu sehen, 
muss das Ankreuzfeld `Auch veraltete Klienten`
(bzw. `Auch veraltete Partner`)
im Parameter-Panel der Liste angekreuzt werden.


.. actor:: contacts.Partners

.. actor:: contacts.Persons

.. actor:: contacts.Companies

.. actor:: contacts.Roles

.. actor:: contacts.RoleTypes

.. actor:: contacts.CompanyTypes


