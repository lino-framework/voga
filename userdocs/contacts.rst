.. _faggio.contacts:

=========
Contacts
=========

.. contents:: 
   :local:
   :depth: 1


.. actor:: contacts.Partner

    A Partner is any physical or moral person for which you want to 
    keep contact data (address, phone numbers, ...).

    :ref:`faggio` differentiates the following subclasses of Partner:

    .. django2rst:: contacts.Partner.print_subclasses_graph()
    
    That is: 
    :ref:`faggio.contacts.Partner`
    can be also a
    :ref:`faggio.contacts.Person`
    or a 
    :ref:`faggio.contacts.Company`
    (or both).
    A :ref:`faggio.contacts.Person`
    can be also a
    :ref:`faggio.courses.Pupil`
    or
    :ref:`faggio.courses.Teacher`
    (or both).
    
    
    


.. _faggio.contacts.Partner.obsolete:

**Veraltete Partner**

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


.. actor:: contacts.Person

    A Person is a :ref:`faggio.contacts.Partner` which corresponds to 
    a physical person or human being.


.. actor:: contacts.Company

    A Company is a :ref:`faggio.contacts.Partner` which corresponds to 
    a company or any other type of organization.

.. actor:: contacts.Role

    A Role is when a given 
    :ref:`faggio.contacts.Person`
    plays a given 
    :ref:`faggio.contacts.RoleType`
    in a given 
    :ref:`faggio.contacts.Company`.

.. actor:: contacts.RoleType

    A :ref:`faggio.contacts.RoleType` is 
    "what a given :ref:`faggio.contacts.Person` can be for a given 
    :ref:`faggio.contacts.Company`".

    The default database comes with the following list of 
    :ddref:`contacts.RoleTypes`:
    
    .. django2rst:: settings.SITE.login('robin').show(contacts.RoleTypes)
    
.. actor:: contacts.CompanyType

    The default database comes with the following list of 
    organization types:
    
    .. django2rst:: settings.SITE.login('robin').show(contacts.CompanyTypes)
    


