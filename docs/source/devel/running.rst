Running Debbox
**************
In this section you will learn about running Debbox using its build-in server and more about it.

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
