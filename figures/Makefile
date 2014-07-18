# Figures Makefile

INK_FIGS = model-interfaces.pdf
TEX_FIGS = model-pdd.pdf model-siassa.pdf model-variables.pdf soft-workflow.pdf
PY_FIGS = map-cordillera.png map-northamerica.png \
          paleo-glaciation.png paleo-timeseries.png \
          plot-atm.png plot-lgm.png plot-sdmap.png plot-sdeffect.png \
          plot-snapshots.png
ALL_FIGS = $(INK_FIGS) $(TEX_FIGS) $(PY_FIGS)

all: data $(ALL_FIGS)

$(INK_FIGS): %.pdf: %.svg
	inkscape $< --export-pdf=$@

$(TEX_FIGS): %.pdf : %.tex
	latexmk -pdf -dvi- -ps- $<

$(PY_FIGS): %.png : %.py
	python2 $<

.PHONY : data clean

data:
	cd data && $(MAKE)

clean:
	rm $(ALL_FIGS)
	rm -f *.{aux,log,fdb_latexmk,fls}
