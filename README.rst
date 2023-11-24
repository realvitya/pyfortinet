Fortinet Python library
=======================
This project implement easy way of handling Fortinet device management from Python.

Quick example
-------------
FMG
~~~
.. code-block:: Python

        config = {
            "base_url": "https://myfmg.com",
            "username": "myuser",
            "password": "verysecret",
            "adom": "root",
            "verify": False
        }
        settings = FMGSettings(**config)
        with FMG(settings) as conn:
            ver = conn.get_version()


Installation
------------
TBD

Setup
-----
TBD
