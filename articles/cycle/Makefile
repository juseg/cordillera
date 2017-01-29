# Article Makefile
# ================


# Variables
# ---------

# default paper extension
EXT = pdf

# main paper
PAPER = cordillera-cycle

# responses
RESPS = $(addprefix response-, editor jarosch stumpf marshall)

# revisions diff
REVIS = $(PAPER)-revisions

# all documents
ALL = $(addsuffix .$(EXT), $(PAPER) $(RESPS) $(REVIS))


# Rules
# -----

# default rule
all: $(ALL)

# patterned rule for pdfs
%.pdf: %.tex
	latexmk -pdf -dvi- -ps- $<

# additional dependence for responses
$(RESPS): response-header.tex

# latexdiff rule for revisions
$(REVIS).tex: $(PAPER)-typeset.tex $(PAPER).tex
	latexdiff $^ > $@

# rich text format
$(PAPER).rtf:
	latex2rtf -E0 -f0 -M4 -t2 $(PAPER).tex

# clean up
.PHONY: clean
clean:
	latexmk -CA
	rm -f $(REVIS).tex
	rm -f $(PAPER).rtf
