Debbox Daemon
*************
.. py:currentmodule:: debbox.core.daemon

Debbox daemon is the most important unit in Debbox execution process. It runs the :py:class:`MasterServer` and :py:class:`WebServer` and
configure the logger for *Master Process*. *server.py* script runs :py:class:`Debbox` and by doing that runs the whole system

*Debbox Daemon* should run under the root user because it fork a Master process and Master process is responsible for executing Slave
process requests under the root user, if Debbox daemon runs under non-root user it can not fork the Master process under root user.

How deos Debbox daemon works?
=============================

Debbox daemon runs in to state foreground and background. In the background state :py:class:`Debbox` class will fork a child process
and terminate the parent process (why? to release from current user session) then child process continue its work and establish a new
session and redirect all the outputs to ``/dev/null`` because it does not want to user see any IO. At last it will fork again and run
:py:class:`MasterServer` in the master process (itself) and writes the pid files in the :ref:`piddir` and runs :py:class:`WebServer` in
the slave process (second child). both of the :py:class:`MasterServer` and :py:class:`WebServer` will go to their own blocking loop and
cause their process to block and wait for an event such as new request from user in case of slave process and new request from slave process
in case of master process.

Debbox Class
============

.. autoclass:: Debbox 
   :members:
