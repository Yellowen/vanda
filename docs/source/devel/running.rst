Running Debbox
**************
In this section you will learn about running Debbox using its built-in server and more about it.

Running Debbox server
=====================
By installing requirement and building a virtual environment, now its time to run Server of Debbox. There is a python script called **server.py** in the
root of Debbox source tree. you should use **server.py** to run Debbox, you can do that like this::
     
     $ python server.py -k start

But above command will run Debbox in daemon mode. Debbox daemon mode is for deployment not for development. So **server.py** provide some arguments that 
allow developers to overrid the default action on **server.py**.
.. cn : override	
For example, you run the Debbox server in foreground by executing **server.py** like this::

    $ python server.py -f

But if you want to run Debbox server for developing Debbox, the best choice whould be::

    $ python server.py -f --debug -c <path_to_develoment_conf_file>

as you can see in the above example you should pass a config file address to **server.py**, thats because Debbox expect default config file in ``/etc/debbox/debbox.conf``
and since you want to run a development environment you should copy ``debbox.conf`` file exists in root directory of Debbox source tree some where you like and change that
for you box (specially SSL configuration) then pass the conf file address tp *-c* option of **server.py**.

Now here is a complete list of **server.py** options explanation.

.. option:: -k <action> 

   Execute the ``action`` on **server.py**, available options are

   * **start**: Starting the Debbox server in daemon mode.
   * **stop**: Stop the Debbox daemon.
   * **status**: print out the current status of Debbox daemon.


.. option:: -f

   Run the Debbox server in foreground, so there whould be no IO redirection and no daemon. It's a good option for development.

.. option:: --debug

   Run the Debbox server in debug mode. Debbox server redirect logs to log files and IOs to ``/dev/null`` but with this option all the mentioned outputs redirect to STDIO.

.. option:: -c <configfile>

   Use provided ``configfile`` instead of default one in ``/etc/debbox/debbox.conf``

.. option:: --port=<PORT>

   Run Debbox server on PORT instead of default port that is 8000. Debbox will use a different port number on deployment state.

.. option:: --shell

   Run an Ipython interactive shell on the Debbox environment

.. option:: --syncdb

   Sync the Debbox web application (Django project).

.. option:: --syncdb-new

   Remove the old database and resync it again.

.. option:: --host=<HOST>

   Run Debbox on given HOST. Default is ``localhost``

.. piddir:

.. option:: --piddir=<pid_folder>

   Store the pid files in ``pid_folder``, Default value for this option is ``/var/run/`` according to LBS standard.

.. option:: --settings=<SETTINGS>
   
   Use provided SETTINGS file as the Django application main settings. Default is ``debbox.settings``.

.. option:: --pythonpath=<PATH>

   This option will add the given PATH to current python path.

.. note:: Sometimes, when you run the **server.py** script you may experience an ``Address in already in use``. if this situation happened to you just find the server.py
   process that is running (by ``ps aux| grep server.py``) and kill it, and report the issue to lxsameer@gnu.org.
.. cn:Using development mailing list for contact is better that personal.
