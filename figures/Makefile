# Figures Makefile
# ================


# Variables
# ---------

# default figure extension
EXT = pdf

# python executable
PY = PYTHONPATH=iceplotlib python2

# all python figures (broken: ciscyc_lr_ts_diff ciscyc_lr_ts_scaling ciskap_plot_sdeffect)
PY_FIGS = $(addprefix ciscyc_, locmap \
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
