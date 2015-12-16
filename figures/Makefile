# Figures Makefile

PY_FIGS = atm locmap \
          lr_maps lr_ts lr_ts_diff lr_ts_deglac lr_ts_scaling lr_violins \
          hr_geom_basedispl hr_geom_deglacage hr_geom_duration \
          hr_geom_lastflow hr_geom_warmbase hr_geom_warmfrac \
          hr_maps_deglac hr_maps_mis2 hr_maps_mis3 hr_maps_mis4 \
          hr_maps_puget \
          hr_pf_epica hr_pf_grip sens_ntil sens_rheo sens_tauc

PY_FIGS := $(addsuffix .pdf, ${PY_FIGS})
ALL_FIGS = $(PY_FIGS)

all: data $(ALL_FIGS)

figures.zip: $(ALL_FIGS)
	zip figures.zip $(ALL_FIGS)

${PY_FIGS}: %.pdf : %.py util matplotlibrc
	python2 $<

hr_maps_mis2.pdf: hr_maps_base.py
hr_maps_mis2.pdf: hr_maps_base.py
hr_maps_mis2.pdf: hr_maps_base.py

.PHONY : data clean

data:
	cd data && $(MAKE)

clean:
	rm $(ALL_FIGS)
