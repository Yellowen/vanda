Loggin System specification
===========================

Dina use logging system to provide useful informations at the runtime that allow better 
and faster debugging. Also privent developers to use `print` statement in there code
that could break Dina code under WSGI and mod_python.

How does Logging system work ?
------------------------------

Logging subsystem code live under ``dina/log/__init__.py`` at this time. It lookup for 
the logging configuration in settings.py and provide a class called :class:`Logger`. Each 
part of Dina that need logging system should build an instance from the Logger class,
and use the instance for produce some logs. Dina initialize its logging system configuration 
in the settings.py file. So each time that web server runs the settings.py script logging
configuration initialized once. for more detail take a look at code comments.


How to use logging system ?
---------------------------

Using the logger system is so simple, you can make an instance from the :class:`Logger` class
and use that to produce logs. Here is the explaination for :class:`Logger` class.

.. note:: Parameter names are just for better understanding and not exactly the same as real ones.

.. class:: Logger (logger_name)
Logger class use ``logger_name`` as the name of log producer, for example::
    
    [2010-08-25 11:54:42] [Template cache class], line:64-> DEBUG    : "TemplateQueryCache class inti."

The above log snippet taken from Dina log. You can see that ``Template cache class`` procude a :attr:`DEBUG`
log in line ``64`` of its module. In this example ``Template cache class`` used as ``logger_name`` parameter
for :class:`Logger` class.

.. method:: Logger.debug (log_string)
This method produce a log with the priority level of DEBUG and ``log_string`` data.

.. method:: Logger.info (log_string)
This method produce a log with the priority level of INFO and ``log_string`` data.

.. method:: Logger.warning (log_string)
This method produce a log with the priority level of WARNING and ``log_string`` data.

.. method:: Logger.error (log_string)
This method produce a log with the priority level of ERROR and ``log_string`` data.

.. method:: Logger.critical (log_string)
This method produce a log with the priority level of CRITICAL and ``log_string`` data.

A simple example::
  
   from dina.log import Logger
   
   logger = Logger ("test module")
   logger.info ("Some log")

This code snippet will produce a log entry like::

    [2010-08-25 11:54:42] [test module], line:4-> INFO    : "Some log"

.. seealso:: Please read the official python documentation for logging module, current logging system use the python logging module.
