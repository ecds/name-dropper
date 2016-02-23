name-dropper
************

Scripts and utilities for identifying and tagging names and named entities (persons, places, organizations) in XML.

Developed as part of the `Emory Center for Digital Scholarship`_ (previously Digital Scholarship Commons) project `Networking the Belfast Group`_.

.. _Emory Center for Digital Scholarship: http://digitalscholarship.emory.edu/
.. _Networking the Belfast Group: http://digitalscholarship.emory.edu/projects/project-networking-belfast.html


Components
==========

Currently **name-dropper** consists of two distinct code bases, which are stored in separate git repositories
and linked here as submodules:

* `namedropper-py`_ contains a Python module with code for interacting with
  `DBpedia Spotlight`_ and `VIAF`_ (Virtual International Authority File), and
  a command line script for identifying names in text or xml (EAD or TEI) content using
  those services.

  .. image:: https://travis-ci.org/emory-libraries-ecds/namedropper-py.svg?branch=develop
    :alt: current build status for namedropper-py
    :target: https://travis-ci.org/emory-libraries-ecds/namedropper-py

* `namedropper-oxygen`_ contains Java code for a plugin for the `Oxygen XML editor`_
  to expedite the process of tagging names and linking them to authoritative identifiers
  in EAD or TEI XML documents.

  .. image:: https://travis-ci.org/emory-libraries-ecds/namedropper-oxygen.svg?branch=develop
    :alt: current build status for namedropper-oxygen
    :target: https://travis-ci.org/emory-libraries-ecds/namedropper-oxygen

.. _namedropper-py: https://github.com/emory-libraries-ecds/namedropper-py
.. _DBpedia Spotlight: http://spotlight.dbpedia.org/
.. _VIAf: http://viaf.org
.. _Oxygen XML editor: http://oxygenxml.com/
.. _namedropper-oxygen: https://github.com/emory-libraries-ecds/namedropper-oxygen

See **README** files in the individual modules for more details about dependencies and installation.

XML conventions
===============

Both the Java and Python code bases assume the following XML encoding conventions for tagging personal,
corporate, and geogaphic names:

In EAD documents, names will be tagged with ``persname``, ``orgname``, or ``corpname`` and linked to VIAF records using the ``source`` and ``authfilenumber`` attributes, as follows:

* personal names::

    <persname source="viaf" authfilenumber="39398205">Michael Longley</persname>

* corporate or organizational name::

   <corpname source="viaf" authfilenumber="129928623">Arts Council of Northern Ireland</corpname>

* geographic names::

   <geogname source="viaf" authfilenumber="179000908">Belfast</geogname>


In TEI documents, names will be tagged with ``name``; the ``type`` attribute will be used to differentiate the type of name, and the ``ref`` attribute will be used to link to an authority record, for example:

* personal names::

    <name type="person" ref="http://viaf.org/viaf/39398205">Michael Longley</name>

* corporate or organizational name::

   <name type="org" ref="http://viaf.org/viaf/129928623">Arts Council of Northern Ireland</name>

* geographic names::

   <name type="place" ref="http://viaf.org/viaf/179000908">Belfast</name>

Note that the ``ref`` value could also be a DBpedia resource or other appropriate URI.

License
=======
NameDropper Python scripts and Oxygen plugin are distributed under the
`Apache 2.0 License <http://www.apache.org/licenses/LICENSE-2.0>`_.
