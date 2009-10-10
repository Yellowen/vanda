import os
import shutil
import tarfile as tf
import sys

if len (sys.argv) > 1:
    if os.path.isdir ( os.path.join (os.path.dirname (sys.argv[1]) , sys.argv[1]).replace ('\\' , '/')):
        target = sys.argv[1]
    else:
        print "Check first argument for a valid directory."
        sys.exit (1)
