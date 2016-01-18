PAPER = cordillera-cycle

all: $(PAPER).pdf revisions-diff.pdf figures
	latexmk -pdf -dvi- -ps- $(PAPER).tex

%.pdf: %.tex
	latexmk -pdf -dvi- -ps- $<

revisions-diff.tex: typeset.tex $(PAPER).tex
	latexdiff --type=CULINECHBAR $^ > revisions-diff.tex

.PHONY : diff figures clean

figures:
	cd figures && $(MAKE)

rtf:
	latex2rtf -E0 -f0 -M4 -t2 $(PAPER).tex

clean:
	cd figures && $(MAKE) clean
	latexmk -CA
	rm $(PAPER).rtf
