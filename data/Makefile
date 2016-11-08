# Data Makefile

all: etopo1-northamerica.nc etopo1-cordillera.nc ice14k.shp lgm_simple.shp \
     era40.sat.day.5801.dev.monstd.nc

etopo1-northamerica.nc etopo1-cordillera.nc: get-etopo1.sh
	bash $<

ice14k.shp: get-dykeshp.sh
	bash $<

lgm_simple.shp: get-quatglac.sh
	bash $<

era40.sat.day.5801.dev.monstd.nc:
	scp scooter:data/era40/$@ .
