PAPER=cordillera-cycle

all: data figures $(PAPER).tex
	latexmk -pdf -dvi- -ps- $(PAPER).tex

data: data/ice145k.shp

data/%.shp: data/of_1574.zip
	cd data && unzip -j of_1574.zip data/shp/$*.{dbf,shp,shx}  && touch $*.{dbf,shp,shx}

data/deglac.zip:
	cd data && wget http://ftp2.cits.rncan.gc.ca/pub/geott/ess_pubs/214/214399/of_1574.zip

figures: figures/*.pdf

figures/%.pdf: figures/%.py
	cd figures && python2 $*.py

clean:
	rm -f figures/$(PAPER)-*.pdf
	latexmk -CA
