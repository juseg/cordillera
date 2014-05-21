PAPER = cordillera-cycle
FIGS = atm.png deglac.png duration.png locmap.png snapshots.png timeseries.png

all: $(PAPER).tex figures
	latexmk -pdf -dvi- -ps- $(PAPER).tex

figures: $(addprefix figures/,$(FIGS))

figures/%.png: figures/%.py data
	cd $(<D) && python2 $(<F)

data: data/ice18k.shp

data/ice18k.shp:
	cd data && bash get.sh

clean:
	rm -f data/ice*k.{dbf,shp,shx}
	rm -f $(addprefix figures/,$(FIGS))
	latexmk -CA
