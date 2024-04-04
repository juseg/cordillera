# Figures Makefile
# ================


# Variables
# ---------

# default figure extension
EXT = pdf

# python executable
PY = python

# old python 2 figures
PY_FIGS = $(addprefix cisbed_, relaxtime timeseries \
            $(addprefix lr_, glacareas)) \
          $(addprefix ciscyc_, locmap \
            $(addprefix hr_, atm basedispl deglacage deglacshots duration \
                             lastflow mis2 mis3 mis4 pfepica pfgrip puget \
                             thompson timeseries warmbase warmfrac) \
            $(addprefix lr_, snapshots misareas timeseries violins) \
            $(addprefix sens_, plot_ntil plot_rheo plot_tauc \
                               misareas snapshots timeseries veldist)) \
          $(addprefix cisghf_, sublakes timestamps \
            $(addprefix cumu_, bmelt bwat) \
            $(addprefix diff_, bmelt bwat) \
            $(addprefix maps_, bmelt bwat bwatvel gflx)) \
          $(addprefix ciskap_, \
            $(addprefix map_, cordillera northamerica) \
            $(addprefix paleo_, glaciation timeseries) \
            $(addprefix plot_, atm cover erosion lastflow lgm sdmap snapshots))

# broken python 3 figures
PY_FIGS = $(addprefix cisbed_, pugetsound relaxtime)

# new python 3 figures
PY_FIGS = $(addprefix cisbed_, iodp341 massbalance timestamps timeseries) \
          $(addprefix ciscyc_, \
            $(addprefix hr_, deglacshots ))
PY_FIGS := $(addsuffix .$(EXT), $(PY_FIGS))

# tex executable
TEX = latexmk -quiet -pdf -dvi- -ps-

# all tex figures
TEX_FIGS = $(addprefix ciskap_, \
             $(addprefix model_, interfaces pdd siassa variables workflow))
TEX_FIGS := $(addsuffix .$(EXT), $(TEX_FIGS))

# all python-latex figures
PYTEX_FIGS := $(addprefix ciscyc_tab_, hr lr sens)
PYTEX_FIGS := $(addsuffix .$(EXT), $(PYTEX_FIGS))

# all figures
ALL_FIGS = $(PY_FIGS) $(PYTEX_FIGS) $(TEX_FIGS)

# tex and pytex figures are broken
ALL_FIGS = $(PY_FIGS)


# Rules
# -----

# default rule
all: $(ALL_FIGS)

# rules and dependencies for python figures
$(PY_FIGS): %.pdf : %.py matplotlibrc util
	$(PY) $<

# rules and dependencies for python-latex figures
$(PYTEX_FIGS): %.pdf : %.py util
	$(PY) $<
	$(TEX) $*.tex

# rules and dependencies for latex figures
$(TEX_FIGS): %.pdf : %.tex
	$(TEX) $<

# clean up
.PHONY: clean
clean:
	rm -f $(ALL_FIGS)
	rm -f *.aux *.log *.fdb_latexmk *.fls
