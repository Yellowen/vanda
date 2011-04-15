Master/Slave Communication
**************************
.. py:currentmodule:: debbox.core.servers

As you read before in this document Master and Slave process can not communicate with each other directly, so they have to use other ways to communicate.
We found unix socket as the best way to connect Master and Slave process together. Master process will create a unix domain socket or unxi socket for short
and change the ownership of socket to Debbox Slave process owner (default is ``debbox`` user), so no one else except of Salve process user can not access to
socket. Also unix sockets are not easy to sniff, you need the root permission to sniff a unix socket. Master process use the :py:class:`MasterServer` to create 
the socket. :py:class:`MasterServer` is a :py:class:`UnixStream` application.

Slave process connect to unix socket using :py:class:`MasterClient`.

MasterServer
============

.. py:class:: MasterServer(logger_instance, [debug=False]):
   
   MasterServer will use logger_instance as its default logger. if debug option is True then MasterServer will output more results and logs.

.. py:method:: MasterServer._dumpmsg(status, msg, [extra=None]):

   return a json form data message to communicate via the unix socket.

.. py:method:: MasterServer.handler(socket, address):

   Unix stream server handler, this method will receive all the data from unix socket. address is an emtry variable. and *socket* is a :py:class:`socket` instance.

.. py:attribute:: MasterServer.commands

   This dictionary will contains all the commands that Master process should response to them as its keys and their responsible methods or functions as its values.

.. seealso:: for more information about :py:class:`MasterServer` take a look at its source code.


MasterClient
============

.. py:class:: MasterClient()

   Client class for communicating with :py:class:`MasterServer`.

.. py:method:: MasterClient.connect()

   establish the connection to master socket. you call this method before sending any command.

.. py:method:: MasterClient.command(command, **kwargs)

   send a command to master process. use it like::

       masterclient_instance.command(command='command_name',
                                     arg1='value', arg2=...)

   each argument that you provide for command method will pass to remote command, (Note: you should use arguments in keyword type
   not list type). This method will return an object that have three attribute

   .. py:attribute:: status
      
      return code of remote command, 0 means ok.

   .. py:attribute:: message
      
      return result of remote command.
 
   .. py:attribute:: extra

      extra flag of Communication Protocol


    also command method will raise remote exception in :py:class:`MasterClient`.


.. py:method:: MasterClient.disconnect()

   This method will close the connection.

.. py:exception:: MasterClient.CantFindConfigFile

   This exception will raise in case of MasterClient could not find the debbox.conf

.. py:exception:: MasterClient.CantConnectToSocket

   This exception will raise in case of MasterClient could not connect to unix socket.

.. py:exception:: MasterClient.EmptyCommand

   This exception will raise in case of your provide an empty command to :py:meth:`connect`.

Communication Protocol version 1.0
==================================
Debbox Master/Slave Communication Protocol or **DMSCP** for short is a very simple protocol that allow Master and Slave process
communicate with each other over a unix socket. **DMSCP** send and receive data based on line indicator('\n'), so **DMSCP** treats
to incoming or outgoing line as a request or response data. **DMSCP** requests and responses transport in a JSON string format. 

**DMSCP** you can think about request as a python dictionary like::

	  {"command":  COMMAND,
	  "args" : {"arg1": value1, "arg2": value2, ....],
	  }


.. option:: COMMAND

   This is the name of a remote (Master) command that may be a function or method

.. option:: {"arg1": value1, "arg2": value2, ....}

    Each pair of key/value in this dictionary will send to remote COMMAND as keyword arguments

Also you can think about **DMSCP** responses as dictionary too. like::

     {"status": STATUS,
     "message": MSG,
     "extra": EXTRA,
     }

.. option:: STATUS

   Hold the status code of response, any none zero value means failed and zero means success.

.. option:: MSG

   This key contain the remote COMMAND result. result will be a python pickled string   

.. option:: EXTRA

   This variable is an extra flag, each command will use it for its own goals.
