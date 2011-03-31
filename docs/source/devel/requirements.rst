Requirements
************
Before jumping in the Debbox development process make sure that you have enough knowledge to use
Python programming language and Django framework. These two are the most important requirements
for Debbox development.
.. cn: jumping into the ...
 
Required packages
=================
Debbox will use an isolated environment in the deployed state, to prevent unwanted changes in the
Host OS. Here is a list of required packages with their details for building a Debbox virtual environment:

* **python-virtualenv**: Debbox use this script to create e virtual environments.
* **libevent-1.4.2**: This packages is required if you want to use GEvent as the web server backed for Debbox.
* **libevent-dev**: This packages is required if you want to use GEvent as the web server backed for Debbox.
* **sphinx** (>=1.0): if you want to build Debbox document you will need this package. 

.. note:: *envcreator.sh* script will install **sphinx** package too.

.. note:: If you use .deb package for installing **Debbox**, then above package already installed on your Debian box.

Debbox user
===========
Debbox run its webserver under a system user called ``debbox``, so you should build the system user before using debbox. for creating linux user you can do like::

       # adduser debbox --system --no-create-home

You can change the defualt user in ``debbox.conf`` under the *User* section.

.. note:: If you use .deb package for installing **Debbox**, then the default user and group already created in your Debian box.

Building virtual environment
============================
After installing required packages, you can easily build a environment using ``debbox/bin/envcreator.sh`` script. ``envcreator.sh`` will build a environment in the current working directory with the name of *env*, and install Django, GEvent and PIL in created virtualenv directory.

.. note:: should we add sphinx here ? ^


so if you don't want tu install one of them, just comment the corresponding code in ``envcreator.sh``.

Virtual environment will simulate a naked linux environment with minimal dependencies installed. To activating provided virtualenv you can do like thise::

	$ . env/bin/activate

and for exit the virtual environment use **deactivate** command.

.. note:: if you already have a *env* directory ``envcreator.sh`` will not clean that environment just installs new packages. But if you want to clean the exists environment up, just use *--clean* parameter with ``envcreator.sh`` .

.. warning:: Do not commit you comments (see above note) in ``envcreator.sh`` on the main Repository.

Debbox database
===============
According to Debian database policy the universal place for storing database is in ``/var/lib/``, so you should create a folder called *debbox* under the ``/var/lib/``.
so the final path will be ``/var/lib/debbox/``. then you should change the ownership of that folder to Debbox default user and group (defined in config file).

After creating the directory you should sync your Django database. Since Debbox web server runs under default user, you should sync your database using default
user, so you can do that like::

      # cd debbox
      # sudo -u debbox python manage.py syncdb


.. note:: If you use .deb package for installing **Debbox**, then above action take effect automatically.


