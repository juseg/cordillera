PAPER=cordillera-cycle

all: figures $(PAPER).texgit 
	latexmk -pdf -dvi- -ps- $(PAPER).tex

figures: figures/*.pdf

figures/%.pdf: figures/%.py
	cd figures && python2 $*.py

clean:
	rm -f figures/$(PAPER)-*.pdf
	latexmk -CA
