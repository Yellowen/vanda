Requirements
************
Before jumping in the Debbox development process make sure that you have enough knowledge to use
Python programming language and Django framework. These two are the most important requirements
for Debbox development.

Required packages
=================
Debbox will use an isolated environment in the deployed state, to prevent unwanted changes in the
Host OS. Here is a list of required packages with their details for building a Debbox virtual environment:

* **python-virtualenv**: Debbox use this script to create e virtual environments.
* **libevent-1.4.2**: This packages is required if you want to use GEvent as the web server backed for Debbox.
* **libevent-dev**: This packages is required if you want to use GEvent as the web server backed for Debbox.

.. note:: If you use .deb package for installing **Debbox**, then above package already installed on your Debian box.

Building virtual environment
============================
After installing required packages, you can easily build a environment using ``debbox/bin/envcreator.sh`` script. ``envcreator.sh`` will build a environment in the current working directory with the name of *env*, and install Django, GEvent and PIL in created virtualenv directory.

so if you don't want tu install one of them, just comment the corresponding code in ``envcreator.sh`` .

Virtual environment will simulate a naked *nix environment with minimal dependencies installed. To activating provided virtualenv you can do like thise::

	$ . env/bin/activate

and for exit the virtual environment use **deactivate** command.

.. note:: if you already have a *env* directory ``envcreator.sh`` will not clean that environment just installs new packages. But if you want to clean the exists environment up, just use *--clean* parameter with ``envcreator.sh`` .

.. warning:: Do not commit you comments (see above note) in ``envcreator.sh`` on the main Repository.

Running Debbox server
=====================
By installing requirement and building a virtual environment, now its time to run Server of Debbox. There is a python script called **server.py** in the
root of Debbox source tree. you should use **server.py** to run Debbox, you can do that like this::
     
     $ python server.py -k start

But above command will run Debbox in daemon mode. Debbox daemon mode is for deployment not for development. So **server.py** provide some arguments that 
allow developers to overrid the default action on **server.py**.

For example, you run the Debbox server in foreground by executing **server.py** like this::

    $ python server.py -f

But if you want to run Debbox server for developing Debbox, the best choice whould be::

    $ python server.py -f --debug -c <path_to_develoment_conf_file>

as you can see in the above example you should pass a config file address to **server.py**, thats because Debbox expect default config file in ``/etc/debbox/debbox.conf``
and since you want to run a development environment you should copy ``debbox.conf`` file exists in root directory of Debbox source tree some where you like and change that
for you box (specially SSL configuration) then pass the conf file address tp *-c* option of **server.py**.

.. seealso:: For more information take a loot at --help option of **server.py**


