# Figures Makefile

# default figure extension
EXT = pdf

# figures without dependencies
BASE_FIGS := atm locmap
BASE_FIGS := $(addsuffix .$(EXT), $(BASE_FIGS))

# lo-res runs figures
LR_FIGS := lr_maps lr_ts lr_ts_diff lr_ts_scaling lr_violins
LR_FIGS := $(addsuffix .$(EXT), $(LR_FIGS))

# hi-res runs figures
HR_FIGS := hr_geom_basedispl hr_geom_deglacage hr_geom_duration \
           hr_geom_lastflow hr_geom_warmbase hr_geom_warmfrac \
           hr_maps_deglac hr_maps_mis2 hr_maps_mis3 hr_maps_mis4 \
           hr_maps_puget lr_ts_deglac \
           hr_pf_epica hr_pf_grip
HR_FIGS := $(addsuffix .$(EXT), $(HR_FIGS))

# sensitivity tests figures
SENS_FIGS := sens_plot_ntil sens_plot_rheo sens_plot_tauc \
             sens_dist_vel sens_maps sens_ts
SENS_FIGS := $(addsuffix .$(EXT), $(SENS_FIGS))

# all python figures
PY_FIGS = $(BASE_FIGS) $(LR_FIGS) $(HR_FIGS) $(SENS_FIGS)

# all figures
ALL_FIGS = $(PY_FIGS)

# to make all figures
all: data $(ALL_FIGS)

# rules and dependencies for python figures
$(PY_FIGS): %.pdf : %.py matplotlibrc util/__init__.py util/io.py util/pl.py
	python2 $<

$(LR_FIGS): util/lr.py
$(HR_FIGS): util/hr.py
$(SENS_FIGS): util/sens.py

# prepare figure.zip for the journal
figures.zip: $(ALL_FIGS)
	zip figures.zip $(ALL_FIGS)

# phony targets
.PHONY : data clean

data:
	cd data && $(MAKE)

clean:
	rm $(ALL_FIGS)
