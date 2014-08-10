# Figures Makefile

INK_FIGS =
TEX_FIGS = model-pdd.pdf model-siassa.pdf model-variables.pdf \
           model-interfaces.pdf soft-workflow.pdf
PY_FIGS = map-cordillera.pdf map-northamerica.pdf \
          paleo-glaciation.pdf paleo-timeseries.pdf \
          plot-atm.pdf plot-sdmap.pdf plot-sdeffect.pdf \
          plot-snapshots.pdf
ALL_FIGS = $(INK_FIGS) $(TEX_FIGS) $(PY_FIGS) plot-lgm.jpg

all: data $(ALL_FIGS)

$(INK_FIGS): %.pdf: %.svg
	inkscape $< --export-pdf=$@

$(TEX_FIGS): %.pdf : %.tex
	latexmk -pdf -dvi- -ps- $<

$(PY_FIGS): %.pdf : %.py
	python2 $<

plot-lgm.jpg: plot-lgm.png
	convert -quality 85 $< $@

plot-lgm.png: plot-lgm.py
	python2 $<

.PHONY : data clean

data:
	cd data && $(MAKE)

clean:
	rm $(ALL_FIGS)
	rm -f *.{aux,log,fdb_latexmk,fls}
