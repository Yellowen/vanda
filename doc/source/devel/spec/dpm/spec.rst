DPM Specification
=================
DPM have some units that works together and build a functional package manager. In this document i will explain these units in more details.

Package
-------
A package is the smallest part of a DPM system. A package is a tarball that contains an application, template or modules. DPM use packages for installing
any DPM units and each package contains only one Dina Component, for example one application or one template.

A DPM package contains two sets of files: a set of files to install on the system when the package is installed, and a set of files that provide additional metadata
about the package or which are executed when the package is installed or removed. 

The package name
^^^^^^^^^^^^^^^^
Every package must have a name that's unique within the Dina archive.
The package name is included in the :ref:`control` field Package, the format of which is described in Package. The package name is also included as a part of the file name of the package file. 

