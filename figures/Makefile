# Figures Makefile

INK_FIGS = model-interfaces.pdf
TEX_FIGS = model-pdd.pdf soft-workflow.pdf
ALL_FIGS = $(INK_FIGS) $(TEX_FIGS)

all: $(ALL_FIGS)

$(INK_FIGS): %.pdf: %.svg
	inkscape $< --export-pdf=$@

$(TEX_FIGS): %.pdf : %.tex
	latexmk -pdf -dvi- -ps- $<

clean:
	rm $(ALL_FIGS)
	rm -f *.{aux,log,fdb_latexmk,fls}
