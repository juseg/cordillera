PAPER = cordillera-cycle
  FIGS = locmap.png atm.png deglac.png duration.png \
		multirec-snapshots.png multirec-timeseries.png

all: data figures $(PAPER).tex
	latexmk -pdf -dvi- -ps- $(PAPER).tex

data: data/ice145k.shp

data/%.shp: data/of_1574.zip
	cd data && unzip -j of_1574.zip data/shp/$*.{dbf,shp,shx}  && touch $*.{dbf,shp,shx}

data/of_1574.zip:
	cd data && wget http://ftp2.cits.rncan.gc.ca/pub/geott/ess_pubs/214/214399/of_1574.zip

figures: $(addprefix figures/,$(FIGS))

figures/locmap.png: figures/locmap.py
	cd $(<D) && python2 $(<F)

figures/atm.png: figures/atm.py
	cd $(<D) && python2 $(<F)

figures/deglac.png: figures/deglac.py
	cd $(<D) && python2 $(<F)

figures/duration.png: figures/duration.py
	cd $(<D) && python2 $(<F)

figures/hires-snapshots.png: figures/hires.py
	cd $(<D) && python2 $(<F)

figures/hires-timeseries.png: figures/hires.py
	cd $(<D) && python2 $(<F)

figures/multirec-snapshots.png: figures/multirec.py
	cd $(<D) && python2 $(<F)

figures/multirec-timeseries.png: figures/multirec.py
	cd $(<D) && python2 $(<F)

clean:
	rm -f $(addprefix figures/,$(FIGS))
	latexmk -CA
