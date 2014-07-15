# Figures Makefile

PY_FIGS = atm.png deglac.png deglacseries.png \
          deglacshots-grip.png deglacshots-epica.png \
          duration.png erosion.png lastflow.png locmap.png \
          profiles-epica.png profiles-grip.png \
          snapshots.png timeseries.png warmbase.png warmfrac.png
ALL_FIGS = $(PY_FIGS)

all: $(ALL_FIGS)

$(PY_FIGS): %.png : %.py
	python2 $<

.PHONY : clean

clean:
	rm $(ALL_FIGS)
	rm -f *.{aux,log,fdb_latexmk,fls}
