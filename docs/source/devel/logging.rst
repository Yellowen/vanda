Logging
*******
Debbox have two Logger that fill two different logging needs. one for Master Server and one for Web application.

Master Server Loggin System
===========================

Web Application Logging System
==============================
Debbox use the original python logging facility, but with some configuration and changes. logging configuration live at ``settings.py``
You should use logging facility in you code, it is very important to collect information about current process, Log outputs are very useful and
valuable debug time informations.

Logging configuration
^^^^^^^^^^^^^^^^^^^^^
There is no need to configuring Debbox logger by default. In any case you can configure logger by changing its configuration variables in 
``settings.py``. Here is the list of logger configurations:

.. option:: VERBOSE

   This option allow you to choose a level for Debbox Logger. for example if you set this option to *WARNING*, only logs 
   higher than *WARNING* level will be appear in logger output. default value of this option is **0**, so logger ouput will contains all the logs in all logger levels.

.. option:: LOG_FORMAT
   
    This option indicate the format of logger output string.
.. option:: LOG_MAX_BYTES

    Numbers of bytes that will put in the Debbox log files. If logger reache this limit, it will create an archive from current log file in the same directory.

.. option:: LOG_BACKUP_COUNT 

   Numbers of backups for log file. also you can think of it as current log file archives.

.. option:: LOG_FILENAME
   
   Where to store log recordes.

For the list of complete options of logger take a look at @file{settings.py}.

Logger usage
^^^^^^^^^^^^
For using Debbox logger all you need it to import it and use it. for example::

    from core.log import logger

    def someview(request):
        logger.debug("Hello logger")


Above example will produce::

      [2011-01-22 05:50:02] [views.py-someview], line:5-> DEBUG     : "Hello logger"

As you can see in Debbox logger record, default configuration of Debbox logger have some interesting information in the log record like where log produced (in this example views.py module at someview function in line 5) and the time of record.

.. seealso:: For more information about logger take a look at official python logger documentation.
