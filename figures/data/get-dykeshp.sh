#!/bin/bash

url='http://ftp2.cits.rncan.gc.ca/pub/geott/ess_pubs/214/214399/of_1574.zip'
archive=$(basename $url)

[ -f $archive ] || wget $url
unzip -j $archive data/shp/ice??k.{dbf,shp,shx}
touch ice??k.{dbf,shp,shx}
