PAPER = cordillera-cycle
FIGS = atm.png deglac.png duration.png lgm.png locmap.png \
       snapshots.png timeseries.png

all: $(PAPER).tex figures
	latexmk -pdf -dvi- -ps- $(PAPER).tex

figures: $(addprefix figures/,$(FIGS))

figures/%.png: figures/%.py data
	cd $(<D) && python2 $(<F)

data: data/etopo1.nc data/ice18k.shp

data/etopo1.nc:
	cd data && bash get-etopo1.nc

data/ice18k.shp:
	cd data && bash get-dykeshp.sh

clean:
	rm -f data/ice*k.{dbf,shp,shx}
	rm -f $(addprefix figures/,$(FIGS))
	latexmk -CA
