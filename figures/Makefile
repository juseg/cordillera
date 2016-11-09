# Figures Makefile
# ================


# Variables
# ---------

# default figure extension
EXT = pdf

# figures without dependencies
BASE_FIGS := atm locmap
BASE_FIGS := $(addsuffix .$(EXT), $(BASE_FIGS))

# lo-res runs figures
LR_FIGS := lr_maps lr_misareas lr_ts lr_violins  # broken: lr_ts_diff lr_ts_scaling
LR_FIGS := $(addsuffix .$(EXT), $(LR_FIGS))

# hi-res runs figures
HR_FIGS := hr_geom_basedispl hr_geom_deglacage hr_geom_duration \
           hr_geom_lastflow hr_geom_warmbase hr_geom_warmfrac \
           hr_maps_deglac hr_maps_mis2 hr_maps_mis3 hr_maps_mis4 \
           hr_maps_puget hr_ts_deglac \
           hr_pf_epica hr_pf_grip
HR_FIGS := $(addsuffix .$(EXT), $(HR_FIGS))

# sensitivity tests figures
SENS_FIGS := sens_plot_ntil sens_plot_rheo sens_plot_tauc \
             sens_dist_vel sens_maps sens_misareas sens_ts
SENS_FIGS := $(addsuffix .$(EXT), $(SENS_FIGS))

# geothermal heat flux figures
GHF_FIGS := ghf_cumu_bmelt ghf_cumu_bwat ghf_diff_bmelt ghf_diff_bwat \
             ghf_maps_bmelt ghf_maps_bwat ghf_maps_bwatvel ghf_maps_gflx
GHF_FIGS := $(addsuffix .$(EXT), $(GHF_FIGS))

# all python figures
PY_FIGS = $(BASE_FIGS) $(LR_FIGS) $(HR_FIGS) $(SENS_FIGS) $(GHF_FIGS) \
          map-cordillera.pdf map-northamerica.pdf \
          paleo-glaciation.pdf paleo-timeseries.pdf \
          plot-atm.pdf plot-cover.pdf plot-erosion.pdf plot-lastflow.pdf \
          plot-sdmap.pdf plot-snapshots.pdf  # broken: plot-sdeffect

# all tex figures
TEX_FIGS = model-pdd.pdf model-siassa.pdf model-variables.pdf \
           model-interfaces.pdf soft-workflow.pdf

# all python-latex figures
PYTEX_FIGS := tab_hr tab_lr tab_sens
PYTEX_FIGS := $(addsuffix .$(EXT), $(PYTEX_FIGS))

# all figures
ALL_FIGS = $(PY_FIGS) $(PYTEX_FIGS) $(TEX_FIGS) plot-lgm.jpg


# Rules
# -----

# default rule
all: $(ALL_FIGS)

# rules and dependencies for python figures
$(PY_FIGS): %.pdf : %.py matplotlibrc util/__init__.py util/io.py util/pl.py
	python2 $<

$(LR_FIGS): util/lr.py
$(HR_FIGS): util/hr.py
$(SENS_FIGS): util/sens.py

# rules and dependencies for python-latex figures
$(PYTEX_FIGS): %.pdf : %.py util
	python2 $<
	pdflatex $*.tex

tab_lr.$(EXT): util/lr.py
tab_sens.$(EXT): util/sens.py

# rules and dependencies for inkscape figures
$(INK_FIGS): %.pdf: %.svg
	inkscape $< --export-pdf=$@

# rules and dependencies for latex figures
$(TEX_FIGS): %.pdf : %.tex
	latexmk -pdf -dvi- -ps- $<

plot-lgm.jpg: plot-lgm.png
	convert -quality 85 $< $@

plot-lgm.png: plot-lgm.py
	python2 $<

# phony targets
.PHONY : data clean

# clean figures
clean:
	rm $(ALL_FIGS)
	rm -f *.{aux,log,fdb_latexmk,fls}
