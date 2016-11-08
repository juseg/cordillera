# Data Makefile
# =============


# Variables
# ---------

# Dyke (2003) deglaciation shapefiles
DYKE_AGES = 18 17 16 15 14
DYKE_FILES = $(foreach AGE, $(DYKE_AGES), external/ice$(AGE)k.shp)

# Ehlers et al. (2011) simplified LGM shapefile
EHLERS_FILES = external/lgm_simple.shp

# ETOPO1 Bed reprojected maps
ETOPO1_REGS = cordillera northamerica
ETOPO1_FILES = $(foreach REG, $(ETOPO1_REGS), external/etopo1-$(REG).nc)

# ERA40 temperature standard deviation
ERA40_FILES = external/era40.sat.mon.5801.std.nc


# Rules
# -----

all: $(DYKE_FILES) $(EHLERS_FILES) $(ETOPO1_FILES) $(ERA40_FILES)

# Dyke (2003) archive
external/dyke-2003.zip:
	mkdir -p external
	wget -nc http://ftp.geogratis.gc.ca/pub/nrcan_rncan/publications/ess_sst/\
	214/214399/of_1574.zip -O $@

# Dyke (2003) shapefiles
external/ice%k.shp: external/dyke-2003.zip
	unzip -DDju $< data/shp/$(notdir $(basename $@)).??? -d $(dir $@)
	chmod 644 $(basename $@).???

# Ehlers et al. (2011) archive
external/ehlers-etal-2011.zip:
	mkdir -p external
	wget -nc http://static.us.elsevierhealth.com/ehlers_digital_maps/\
	digital_maps_02_all_other_files.zip -O $@

# Ehlers et al. (2011) shapefile
external/lgm_simple.shp: external/ehlers-etal-2011.zip
	unzip -DDju $< lgm.??? -d $(dir $@)
	ogr2ogr -overwrite -where "OGR_GEOM_AREA > 1e-3" -simplify 0.1 \
	        $@ $(subst _simple,,$@)

# ETOPO1 Bed original cell-registered data
external/etopo1-world.tif:
	mkdir -p external
	wget -nc http://www.ngdc.noaa.gov/mgg/global/relief/ETOPO1/data/bedrock/\
	cell_registered/georeferenced_tiff/ETOPO1_Bed_c_geotiff.zip -O $@
	unzip -n $@
	rm $@

# ETOPO1 reprojected for North America
external/etopo1-northamerica.nc: external/etopo1-world.tif
	gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3979 -r bilinear \
	         -te -4250000 -1200000 4250000 3800000 -tr 5000 5000 \
	         -srcnodata -2147483648 -dstnodata -32768 \
	         -wm 512 -wo SOURCE_EXTRA=100 -of netcdf -overwrite \
	         $< $@

# ETOPO1 reprojected for the Cordillera (used -tr 3000 3000 in cycle paper)
external/etopo1-cordillera.nc: external/etopo1-world.tif
	gdalwarp -s_srs EPSG:4326 -r bilinear \
	         -t_srs '+proj=lcc +lon_0=-135 +lat_0=45 +lat_1=45 +lat_2=70' \
	         -te -2250000 000000 2250000 3000000 -tr 2500 2500 \
	         -srcnodata -2147483648 -dstnodata -32768 \
	         -wm 512 -wo SOURCE_EXTRA=100 -of netcdf -overwrite \
	         $< $@

# ERA40 temperature standard deviation
external/era40.sat.mon.5801.std.nc:
	mkdir -p external
	scp ogive:/scratch_net/ogive_second/juliens/geodata/reanalysis/era40/\
	$(notdir $@) $@

# clean external files
.PHONY: clean
clean:
	rm -rf external

