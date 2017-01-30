# Figures Makefile
# ================


# Variables
# ---------

# default figure extension
EXT = pdf

# python executable
PY = PYTHONPATH=iceplotlib python2

# all python figures (broken: lr_ts_diff lr_ts_scaling plot-sdeffect)
PY_FIGS = atm locmap \
          $(addprefix lr_, maps misareas ts violins) \
          $(addprefix hr_, \
            $(addprefix geom_, basedispl deglacage duration lastflow \
                               warmbase warmfrac) \
            $(addprefix maps_, deglac mis2 mis3 mis4 puget) \
            ts_deglac pf_epica pf_grip) \
          $(addprefix sens_, plot_ntil plot_rheo plot_tauc \
                             dist_vel maps misareas ts) \
          $(addprefix ghf_, \
            $(addprefix cumu_, bmelt bwat) \
            $(addprefix diff_, bmelt bwat) \
            $(addprefix maps_, bmelt bwat bwatvel gflx) \
            sublakes) \
          $(addprefix map-, cordillera northamerica) \
          $(addprefix paleo-, glaciation timeseries) \
          $(addprefix plot-, atm cover erosion lastflow lgm sdmap snapshots)
PY_FIGS := $(addsuffix .$(EXT), $(PY_FIGS))

# tex executable
TEX = latexmk -pdf -dvi- -ps-

# all tex figures
TEX_FIGS = $(addprefix model-, pdd siassa variables interfaces) \
           soft-workflow
TEX_FIGS := $(addsuffix .$(EXT), $(TEX_FIGS))

# all python-latex figures
PYTEX_FIGS := tab_hr tab_lr tab_sens
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
