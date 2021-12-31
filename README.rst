==================================
python-anyconfig-fit-backend
==================================

.. image:: https://img.shields.io/pypi/v/anyconfig-fit-backend.svg
   :target: https://pypi.python.org/pypi/anyconfig-fit-backend/
   :alt: [Latest Version]

.. image:: https://img.shields.io/pypi/pyversions/anyconfig-fit-backend.svg
   :target: https://pypi.python.org/pypi/anyconfig-fit-backend/
   :alt: [Python versions]

.. image:: https://img.shields.io/pypi/l/anyconfig-fit-backend.svg
   :target: https://pypi.python.org/pypi/anyconfig-fit-backend/
   :alt: MIT License

.. image:: https://github.com/ssato/python-anyconfig-fit-backend/workflows/Tests/badge.svg
   :target: https://github.com/ssato/python-anyconfig-fit-backend/actions?query=workflow%3ATests
   :alt: [Github Actions: Test status]

.. .. image:: https://img.shields.io/coveralls/ssato/python-anyconfig-fit-backend.svg
   :target: https://coveralls.io/r/ssato/python-anyconfig-fit-backend
   :alt: Coverage Status

.. image:: https://img.shields.io/lgtm/alerts/g/ssato/python-anyconfig-fit-backend.svg
   :target: https://lgtm.com/projects/g/ssato/python-anyconfig-fit-backend/alerts/
   :alt: [Total Alerts by LGTM]

.. image:: https://img.shields.io/lgtm/grade/python/g/ssato/python-anyconfig-fit-backend.svg
   :target: https://lgtm.com/projects/g/ssato/python-anyconfig-fit-backend/context:python
   :alt: [Code Quality by LGTM]

This is a backend module for python-anyconfig to support to load and parse
FIT (Flexible and Interoperable Data Transfer) data files.

- Author: Satoru SATOH
- License: MIT

SEE ALSO:

- python-anyconfig: https://pypi.python.org/pypi/anyconfig
- Flexible and Interoperable Data Transfer (FIT) Protocol: https://developer.garmin.com/fit/protocol/

Requirements
===============

It utilizes a great library fitdecode [#]_ to load and parse FIT data files.

.. [#] https://github.com/polyvertex/fitdecode

Build & Install
================

- From PyPI: anyconfig-fit-backend (package name) [#]_ 
- Pre-built RPMs are available from my copr repo, ssato/python-anyconfig [#]_

If you're Fedora or Red Hat Enterprise Linux user, try::

  $ python setup.py srpm && mock dist/<package>-<ver_dist>.src.rpm
  
or::

  $ python setup.py rpm

and install built RPMs. 

Otherwise, try usual ways to build and/or install python modules such like
'python setup.py bdist', etc.

.. [#] https://pypi.org/project/anyconfig-fit-backend/
.. [#]  https://copr.fedorainfracloud.org/coprs/ssato/python-anyconfig/packages/

.. vim:sw=2:ts=2:et:
