# Figures Makefile

PY_FIGS = atm.pdf deglac.pdf deglacseries.pdf deglacshots.pdf \
          duration.pdf icemaps-mis2.pdf icemaps-mis4.pdf \
          lastflow.pdf locmap.pdf \
          profiles-epica.pdf profiles-grip.pdf \
          snapshots.pdf timeseries.pdf warmbase.pdf warmfrac.pdf
ALL_FIGS = $(PY_FIGS)

all: data $(ALL_FIGS)

figures.zip: $(ALL_FIGS)
	zip figures.zip $(ALL_FIGS)

$(PY_FIGS): %.pdf : %.py paperglobals.py
	python2 $<

icemaps-mis4.pdf: icemaps.py
icemaps-mis3.pdf: icemaps.py
icemaps-mis2.pdf: icemaps.py
profiles-grip.pdf: profiles.py
profiles-epica.pdf: profiles.py

.PHONY : data clean

data:
	cd data && $(MAKE)

clean:
	rm $(ALL_FIGS)
