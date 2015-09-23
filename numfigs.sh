#!/bin/bash

paper="cordillera-cycle"

i=1
grep includegraphics $paper.tex | while read l
do
    fig=${l:16:-1}
    ii=$(printf '%02d' $i)
    cp -n figures/$fig.pdf figures/fig$ii.pdf
    sed -i "s/\includegraphics{$fig}/\includegraphics{fig$ii}/" $paper.tex
    ((++i))
done
