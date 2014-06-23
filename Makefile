PAPER = kappa

all: $(PAPER).tex
	latexmk -pdf -dvi- -ps- $(PAPER).tex

clean:
	latexmk -CA
