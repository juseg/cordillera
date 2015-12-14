# Figures Makefile

PY_FIGS = atm deglac deglacseries deglacshots duration \
          icemaps-mis2 icemaps-mis3 icemaps-mis4 lastflow locmap \
          profiles-epica profiles-grip sens-ntil sens-rheo sens-tauc \
          snapshots timeseries warmbase warmfrac
PY_FIGS := $(addsuffix .pdf, ${PY_FIGS})
ALL_FIGS = $(PY_FIGS)

all: data $(ALL_FIGS)

figures.zip: $(ALL_FIGS)
	zip figures.zip $(ALL_FIGS)

${PY_FIGS}: %.pdf : %.py paperglobals.py matplotlibrc
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
