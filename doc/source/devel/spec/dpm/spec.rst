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

The version of a package
^^^^^^^^^^^^^^^^^^^^^^^^
Every package has a version number recorded in its :ref:`Version` :ref:`control` file field, described in Version.

The package management system imposes an ordering on version numbers, so that it can tell whether packages are being up- or downgraded and so that package system front end applications can tell whether a package it finds available is newer than the one installed on the system. The version number format has the most significant parts (as far as comparison is concerned) at the beginning.

If an upstream package has problematic version numbers they should be converted to a sane form for use in the Version field. 

The maintainer of a package
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Every package must have a Dina maintainer (the maintainer may be one person or a group of people reachable from a common email address, such as a mailing list). The maintainer is responsible for ensuring that the package is placed in the appropriate distributions.

The maintainer must be specified in the :ref:`Maintainer` :ref:`control` field with their correct name and a working email address. If one person maintains several packages, they should try to avoid having different forms of their name and email address in the Maintainer fields of those packages.

The format of the Maintainer control field is described in :ref:`Maintainer`.

If the maintainer of a package quits from the Dina project,  qpm@dina-project.com takes over the maintainer-ship of the package until someone else volunteers for that task. These packages are called orphaned packages.

The description of a package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Every Dina package must have a Description control field which contains a synopsis and extended description of the package. Technical information about the format of the Description field is in Description.

The description should describe the package (the application) to a user (system administrator) who has never met it before so that they have enough information to decide whether they want to install it. This description should not just be copied verbatim from the program's documentation.

Put important information first, both in the synopsis and extended description. Sometimes only the first part of the synopsis or of the description will be displayed. You can assume that there will usually be a way to see the whole extended description.

The description should also give information about the significant dependencies and conflicts between this package and others, so that the user knows why these dependencies and conflicts have been declared.

Instructions for configuring or using the package should not be included (that is what installation scripts). Copyright statements and other administrivia should not be included either (that is what the copyright file is for). 

The single line synopsis
^^^^^^^^^^^^^^^^^^^^^^^^
The single line synopsis should be kept brief - certainly under 80 characters.

Do not include the package name in the synopsis line. The display software knows how to display this already, and you do not need to state it. Remember that in many situations the user may only see the synopsis line - make it as informative as you can. 

Dependencies
^^^^^^^^^^^^
Every package must specify the dependency information about other packages that are required for the first to work correctly.

Sometimes, a package requires another package to be installed and configured before it can be installed. In this case, you must specify a Pre-Depends entry for the package.

You should not specify a Pre-Depends entry for a package before this has been discussed on the dina-devel mailing list and a consensus about doing that has been reached. 

Virtual packages
^^^^^^^^^^^^^^^^
Sometimes, there are several packages which offer more-or-less the same functionality. In this case, it's useful to define a virtual package whose name describes that common functionality. (The virtual packages only exist logically, not physically; that's why they are called virtual.) The packages with this particular function will then provide the virtual package. Thus, any other package requiring that function can simply depend on the virtual package without having to specify all possible packages individually.

All packages should use virtual package names where appropriate, and arrange to create new ones if necessary. They should not use virtual package names (except privately, amongst a cooperating group of packages) unless they have been agreed upon and appear in the list of virtual package names.

The procedure for updating the list is described in the preface to the list. 
