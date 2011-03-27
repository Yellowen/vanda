Master/Slave Processes
**********************
Debbox use a Master/Slave process schema to provide a safe and easy to use communication layer between normal users environment and root user environment.
Since wide range of administration jobs only allowed under root user, Debbox needs to run some of its code under root user, but running a web server and 
application under root user is bad security risk. So the best choice is to have two different process, one of them will handle the administration issues that
should runs under root user and another one will communicate with user as the Web application user interface.

Master Process
==============
The process that run under root user will be Master Process. The main objective of master process is to run the Slave process request under the root user privilege and 
return the request result as a response to Slave Process. but beside this objective master process have some other tasks like forking the Slave process.

Master Process will be runs with **server.py** script on the Starting time of Debbox, then it will fork a process from itself and change the ownership of the child process
to ``debbox`` user (the default user of Debbox is ``debbox`` but user may change that from Debbox configuration file in ``/etc/debbox/debbox.conf``), so new process will
continue its work under non-root user, 

.. TODO: check the references in this page ..

Master Process will run the :ref:`Master Server` and wait for Slave process requests.

