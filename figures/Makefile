# Figures Makefile

PY_FIGS = atm.pdf deglac.pdf deglacseries.pdf deglacshots.pdf \
          duration.pdf icemaps-mis2.pdf icemaps-mis4.pdf \
          lastflow.pdf locmap.pdf \
          profiles-epica.pdf profiles-grip.pdf \
          snapshots.pdf timeseries.pdf warmbase.pdf warmfrac.pdf
ALL_FIGS = $(PY_FIGS)

all: data $(ALL_FIGS)

$(PY_FIGS): %.pdf : %.py
	python2 $<

.PHONY : data clean

data:
	cd data && $(MAKE)

clean:
	rm $(ALL_FIGS)
