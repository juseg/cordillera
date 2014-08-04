# Figures Makefile

INK_FIGS = model-interfaces.pdf
TEX_FIGS = model-pdd.pdf model-siassa.pdf model-variables.pdf soft-workflow.pdf
PY_FIGS = map-cordillera.pdf map-northamerica.pdf \
          paleo-glaciation.pdf paleo-timeseries.pdf \
          plot-atm.pdf plot-lgm.pdf plot-sdmap.pdf plot-sdeffect.pdf \
          plot-snapshots.pdf
ALL_FIGS = $(INK_FIGS) $(TEX_FIGS) $(PY_FIGS)

all: data $(ALL_FIGS)

$(INK_FIGS): %.pdf: %.svg
	inkscape $< --export-pdf=$@

$(TEX_FIGS): %.pdf : %.tex
	latexmk -pdf -dvi- -ps- $<

$(PY_FIGS): %.pdf : %.py
	python2 $<

.PHONY : data clean

data:
	cd data && $(MAKE)

clean:
	rm $(ALL_FIGS)
	rm -f *.{aux,log,fdb_latexmk,fls}
