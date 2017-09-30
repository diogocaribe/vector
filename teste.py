import sys
import os

if 'LD_LIBRARY_PATH' not in os.environ:
    os.environ['GISBASE'] = "/usr/lib/grass70"
    sys.path.append(os.environ['GISBASE'] + "/etc/python/")
    os.environ["LD_LIBRARY_PATH"] = os.environ['GISBASE'] + "/lib"
    os.environ['GIS_LOCK'] = "$$"
    os.environ['GISRC'] = os.environ["HOME"] + "/.grass7/rc"
    try:
        os.execv(sys.argv[0], sys.argv)
    except Exception as exc:
        print('Failed re-exec:', exc, sys.exit(1))

import grass.script as g

g.run_command("v.in.ogr", flags="oe", input_=options["input"],
              output="w", overwrite=flags["o"])