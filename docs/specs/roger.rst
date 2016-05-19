.. _voga.specs.roger:

=================================
Specific for Lino Voga à la Roger
=================================

.. to test only this doc:

    $ python setup.py test -s tests.SpecsTests.test_roger

    >>> from lino import startup
    >>> startup('lino_voga.projects.roger.settings.doctests')
    >>> from lino.api.doctest import *
    
    
>>> dd.demo_date()
datetime.date(2014, 5, 22)

>>> rt.show(courses.Pupils)
======================================== ================================= ================== ============ ===== ===== ======== ==============
 Name                                     Address                           Participant Type   Section      LFV   CKK   Raviva   Mitglied bis
---------------------------------------- --------------------------------- ------------------ ------------ ----- ----- -------- --------------
 Hans Altenberg (MEC)                     Aachener Straße, 4700 Eupen                                       No    Yes   No       31/12/2014
 Annette Arens (ME)                       Alter Malmedyer Weg, 4700 Eupen                                   No    No    No       31/12/2014
 Laurent Bastiaensen (MS)                 Am Berg, 4700 Eupen                                  Eupen        No    No    No
 Bernd Brecht (MS)                        Germany                                              Nidrum       No    No    No
 Ulrike Charlier (ME)                     Auenweg, 4700 Eupen                                               No    No    No       31/12/2014
 Dorothée Demeulenaere (ME)               Auf'm Rain, 4700 Eupen                                            No    No    No       31/12/2014
 Daniel Dericum (MCLS)                    August-Thonnar-Str., 4700 Eupen                      Nidrum       Yes   Yes   No
 Dorothée Dobbelstein-Demeulenaere (ME)   Bahnhofstraße, 4700 Eupen                                         No    No    No       31/12/2014
 Jean Dupont (ML)                         4031 Angleur                                                      Yes   No    No
 Daniel Emonts (ME)                       Bellmerin, 4700 Eupen                                             No    No    No       31/12/2014
 Erna Emonts-Gast (ME)                    4730 Raeren                                                       No    No    No       31/12/2014
 Edgar Engels (MS)                        Bennetsborn, 4700 Eupen                              Walhorn      No    No    No
 Eberhart Evers (MEC)                     Bergstraße, 4700 Eupen                                            No    Yes   No       31/12/2014
 Luc Faymonville (ME)                     Brabantstraße, 4700 Eupen                                         No    No    No       31/12/2014
 Gregory Groteclaes (ME)                  Edelstraße, 4700 Eupen                                            No    No    No       31/12/2014
 Hildegard Hilgers (MCS)                  Favrunpark, 4700 Eupen                               Herresbach   No    Yes   No
 Jacqueline Jacobs (MS)                   Fränzel, 4700 Eupen                                  Eynatten     No    No    No
 Jérôme Jeanémart (MCLS)                  France                                               Walhorn      Yes   Yes   No
 Josef Jonas (MEC)                        Gülcherstraße, 4700 Eupen                                         No    Yes   No       31/12/2014
 Karl Kaivers (MLS)                       Haasberg, 4700 Eupen                                 Kelmis       Yes   No    No
 Lisa Lahm (MEL)                          Germany                                                           Yes   No    No       31/12/2014
 Laura Laschet (ME)                       Habsburgerweg, 4700 Eupen                                         No    No    No       31/12/2014
 Josefine Leffin (MCS)                    Heidgasse, 4700 Eupen                                Hergenrath   No    Yes   No
 Mark Martelaer (ME)                      Amsterdam, Netherlands                                            No    No    No       31/12/2014
 Marie-Louise Meier (MS)                  Hisselsgasse, 4700 Eupen                             Hauset       No    No    No
 Alfons Radermacher (MS)                  4730 Raeren                                          Elsenborn    No    No    No
 Christian Radermacher (ME)               4730 Raeren                                                       No    No    No       31/12/2014
 Edgard Radermacher (MCS)                 4730 Raeren                                          Weywertz     No    Yes   No
 Guido Radermacher (ME)                   4730 Raeren                                                       No    No    No       31/12/2014
 Hedi Radermacher (MLS)                   4730 Raeren                                          Sonstige     Yes   No    No
 Jean Radermacher (MEC)                   4730 Raeren                                                       No    Yes   No       31/12/2014
 Marie-Louise Vandenmeulenbos (ME)        Amsterdam, Netherlands                                            No    No    No       31/12/2014
 Didier di Rupo (ME)                      4730 Raeren                                                       No    No    No       31/12/2014
 Erna Ärgerlich (MCS)                     4730 Raeren                                          Eupen        No    Yes   No
 Otto Östges (ME)                         4730 Raeren                                                       No    No    No       31/12/2014
======================================== ================================= ================== ============ ===== ===== ======== ==============
<BLANKLINE>
