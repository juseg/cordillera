PAPER = cordillera-cycle

all: $(PAPER).tex figures
	latexmk -pdf -dvi- -ps- $(PAPER).tex

.PHONY : data figures clean

data: data/etopo1.nc data/ice18k.shp

data/etopo1.nc:
	cd data && bash get-etopo1.sh

data/ice18k.shp:
	cd data && bash get-dykeshp.sh

figures:
	cd figures && $(MAKE)

clean:
	rm -f data/ice*k.{dbf,shp,shx}
	cd figures && $(MAKE) clean
	latexmk -CA
