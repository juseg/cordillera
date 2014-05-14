PAPER = cordillera-cycle
FIGS = locmap.png atm.png multirec-snapshots.png multirec-timeseries.png

all: data figures $(PAPER).tex
	latexmk -pdf -dvi- -ps- $(PAPER).tex

data: data/ice145k.shp

data/%.shp: data/of_1574.zip
	cd data && unzip -j of_1574.zip data/shp/$*.{dbf,shp,shx}  && touch $*.{dbf,shp,shx}

data/deglac.zip:
	cd data && wget http://ftp2.cits.rncan.gc.ca/pub/geott/ess_pubs/214/214399/of_1574.zip

figures: $(addprefix figures/$(PAPER)-,$(FIGS))

figures/$(PAPER)-locmap.png: figures/$(PAPER)-locmap.py
	cd $(<D) && python2 $(<F)

figures/$(PAPER)-atm.png: figures/$(PAPER)-atm.py
	cd $(<D) && python2 $(<F)

figures/$(PAPER)-multirec-snapshots.png: figures/$(PAPER)-multirec.py
	cd $(<D) && python2 $(<F)

figures/$(PAPER)-multirec-timeseries.png: figures/$(PAPER)-multirec.py
	cd $(<D) && python2 $(<F)

clean:
	rm -f figures/$(PAPER)-*.{pdf,png}
	latexmk -CA
