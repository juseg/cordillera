# Data Makefile

all: etopo1.nc lgm_simple.shp

etopo1.nc: get-etopo1.sh
	bash $<

lgm_simple.shp: get_quatglac.sh
	bash $<
