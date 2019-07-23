=========
btmonitor
=========


.. image:: https://img.shields.io/travis/uudisaru/btmonitor.svg
        :target: https://travis-ci.org/uudisaru/btmonitor

.. image:: https://ci.appveyor.com/api/projects/status/uudisaru/branch/master?svg=true
    :target: https://ci.appveyor.com/project/uudisaru/btmonitor/branch/master
    :alt: Build status on Appveyor



Real-time bus traffic monitor. Includes scraper for monitoring bus traffing in Tallinn, Estonia.


* Free software: MIT license

* Demo: https://btmonitor.trtd.eu


Installation using docker:
--------------------------

Docker scripts build UI, create API key, download letsencrypt certificate and build Docker image for the btmonitor.

.. code-block:: console

    $ git clone https://github.com/uudisaru/btmonitor.git
    $ cd btmonitor/docker
    $ ./build.sh
    $ ./start.sh


Running backend server locally:
-------------------------------

.. code-block:: console

    $ git clone https://github.com/uudisaru/btmonitor.git
    $ cd btmonitor/docker
    $ poetry install
    $ btmonitor server

Features
--------

* Server fetches periodically (in every 5 seconds) the real time locations of buses in Tallinn.
* Web server exposes websockets API that pushes location changes to the clients.
* Web endpoints are optionally exposed over https if certificate file is provided.
* Frontend https://github.com/uudisaru/btmonitor-ui displays the bus locations on the map.

Technology
----------

* Python-based Sanic web framework with async actions for:
    * Fetching the data
    * Serving web content
    * Pushing data over websockets
* Frontend written in React, map components based on Openlayers


Credits
-------

This package was created with Cookiecutter_ and the `wboxx1/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`wboxx1/cookiecutter-pypackage`: https://github.com/wboxx1/cookiecutter-pypackage-poetry
