DOCS := response-editor response-jarosch response-stumpf response-marshall
DOCS := $(addsuffix .pdf, $(DOCS))

all: $(DOCS)

%.pdf: %.tex response-header.tex
	latexmk -pdf -dvi- -ps- $<

.PHONY : clean

clean:
	latexmk -C
