PAPER=cordillera-cycle

all :
	latexmk -pdf -dvi- -ps- $(PAPER).tex
	
clean:
	latexmk -CA
