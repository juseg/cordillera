# Data Makefile

all: etopo1.nc ice14k.shp lgm_simple.shp

etopo1.nc: get-etopo1.sh
	bash $<

ice14k.shp: get-dykeshp.sh
	bash $<

lgm_simple.shp: get_quatglac.sh
	bash $<
