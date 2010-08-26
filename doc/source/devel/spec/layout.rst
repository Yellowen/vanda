Layout Manager
==============

Dina have a powerful and flexible mechanism that provide dynamic template rendering. By using
:mod:`Layout Manager` you can define your own section in the template code easily. for example
``top`` or ``side`` section and then choose to render which components in which section. 

Dina provide a simple to use UI to fill the template section with template components such as
``news`` , ``blog`` , ``menu system`` and what ever your installed in you Dina package.

How does Layout Manager works? --- Concepts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Dina use a collection of tools and modules in order to manage the front-end layouts as a unigue 
system that is called ``Layout manager``. Layout manager is not an application or an isolated 
python package by itself, it use some other parts of Dina such as template loader template 
cache system and etc to manage dynamic template rendering.


