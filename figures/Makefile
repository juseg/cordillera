# Figures Makefile

PY_FIGS = atm.png deglac.png deglacseries.png \
          deglacshots-grip.png deglacshots-epica.png \
          duration.png icemaps-mis2.png icemaps-mis4.png \
          lastflow.png locmap.png \
          profiles-epica.png profiles-grip.png \
          snapshots.png timeseries.png warmbase.png warmfrac.png
ALL_FIGS = $(PY_FIGS)

all: data $(ALL_FIGS)

$(PY_FIGS): %.png : %.py
	python2 $<

.PHONY : data clean

data:
	cd data && $(MAKE)

clean:
	rm $(ALL_FIGS)
