PAPER = cordillera-cycle

all: $(PAPER).tex figures
	latexmk -pdf -dvi- -ps- $(PAPER).tex

.PHONY : figures clean

figures:
	cd figures && $(MAKE)

rtf:
	latex2rtf -E0 -f0 -M4 -t2 $(PAPER).tex

clean:
	cd figures && $(MAKE) clean
	latexmk -CA
	rm $(PAPER).rtf
