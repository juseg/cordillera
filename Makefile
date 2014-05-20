PAPER = cordillera-cycle
FIGS = atm.png deglac.png duration.png locmap.png multirec.png timeseries.png

all: data figures $(PAPER).tex
	latexmk -pdf -dvi- -ps- $(PAPER).tex

data: data/ice145k.shp

data/%.shp: data/of_1574.zip
	cd data && unzip -j of_1574.zip data/shp/$*.{dbf,shp,shx}  && touch $*.{dbf,shp,shx}

data/of_1574.zip:
	mkdir data
	cd data && wget http://ftp2.cits.rncan.gc.ca/pub/geott/ess_pubs/214/214399/of_1574.zip

figures: $(addprefix figures/,$(FIGS))

figures/%.png: figures/%.py
	cd $(<D) && python2 $(<F)

clean:
	rm -f $(addprefix figures/,$(FIGS))
	latexmk -CA
