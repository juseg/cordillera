PAPER = kappa

all: $(PAPER).tex figures
	latexmk -pdf -dvi- -ps- $(PAPER).tex

.PHONY : figures clean
figures:
	cd figures && $(MAKE)

clean:
	cd figures && make clean
	latexmk -CA
