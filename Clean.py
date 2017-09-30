import sys
import os
import errno


def main():
    g.run_command("v.in.ogr", flags="oe", input_=options["input"],
        output="w", overwrite=flags["o"])
    g.run_command("v.clean", tool="break", input_="w",
        output="w_break", overwrite=flags["o"])
    g.run_command("v.clean", tool="snap", input_="w_break",
        thresh=options["snap_t"], output="w_snap", overwrite=flags["o"])
    g.run_command("v.clean", tool="rmdangle", input_="w_snap",
        thresh=options["dangle_t"], output="w_rmdangles", overwrite=flags["o"])
    g.run_command("v.clean", tool="rmline", input_="w_rmdangles",
        output="w_rmline", overwrite=flags["o"])
    g.run_command("v.clean", flags="c", tool="rmsa", input_="w_rmline",
        output="w_rmsa", overwrite=flags["o"])
    g.run_command("v.type", input_="w_rmsa", output="w_boundaries",
        from_type="line", to_type="boundary", overwrite=flags["o"])
    g.run_command("v.clean", tool="rmbridge", input_="w_boundaries", output="w_no_bridges",
        overwrite=flags["o"])
    g.run_command("v.clean", tool="rmarea", input_="w_no_bridges",
        thresh="0.01", output="w_no_zombies", overwrite=flags["o"])
    g.run_command("v.centroids", input_="w_no_zombies", output="w_centroids",
        overwrite=flags["o"])
    g.run_command("v.db.addcolumn", map_="w_centroids", columns="sqm double precision")
    g.run_command("v.to.db", map_="w_centroids", type_="centroid",
        option="area", columns="sqm", unit="meters")
    g.run_command("v.extract", input_="w_centroids", output="w_xsareas",
        where="sqm < 0.3", overwrite=flags["o"])
    print("=======================================================")
    print("Listing polygons smaller than 0.3 sqm (check w_xsareas)")
    print("=======================================================")
    g.run_command("db.select", sql="select cat, sqm from w_xsareas order by sqm asc", separator="tab")
    if flags["o"]:
        try:
            noext = os.path.splitext(options["output"])[0]
            os.remove("{0}.shp".format(noext))
            os.remove("{0}.dbf".format(noext))
            os.remove("{0}.shx".format(noext))
            os.remove("{0}.prj".format(noext))
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
    g.run_command("v.out.ogr", input_="w_centroids",
        output=options["output"], type_="area")


if __name__ == "__main__":
    options, flags = g.parser()
    sys.exit(main())